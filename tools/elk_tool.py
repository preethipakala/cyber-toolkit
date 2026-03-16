#!/usr/bin/env python3
"""
elk_tool.py — ELK Stack (Elasticsearch + Logstash + Kibana) SIEM helper.

The ELK Stack is the most widely deployed open source SIEM backend:
  Elasticsearch — stores and indexes security events at massive scale
  Logstash      — ingests, parses, and enriches log data from any source
  Kibana        — dashboards and visualizations for threat hunting
  Filebeat      — lightweight log shipper (runs on endpoints)

In a SIEM context, the pipeline looks like:

  [Endpoints/Firewalls/IDS]
         |
    Filebeat / Logstash
         |
    Elasticsearch  <-- stores all events
         |
       Kibana      <-- analyst dashboards, SIEM rules, alerts

Install: https://www.elastic.co/guide/en/elastic-stack/current/installing-elastic-stack.html
  Or use Docker: docker-compose up (see docs/elk-docker-compose.yml)
"""

import json
import urllib.request
import urllib.error
from tools.base import BaseTool
from utils.reporter import print_section, print_error, print_success, print_warning

DEFAULT_ES_URL = "http://localhost:9200"
DEFAULT_KB_URL = "http://localhost:5601"


class ELKTool(BaseTool):
    name         = "elk"
    display_name = "ELK Stack — Elasticsearch / Logstash / Kibana SIEM"
    binary       = "elasticsearch"
    install_hint = "https://www.elastic.co/guide/en/elastic-stack/current/installing-elastic-stack.html"

    def run(self, action: str = "health",
            es_url: str = DEFAULT_ES_URL,
            kb_url: str = DEFAULT_KB_URL,
            index: str = "") -> str:
        if action == "health":
            return self._es_health(es_url)
        if action == "indices":
            return self._list_indices(es_url)
        if action == "kibana":
            return self._kibana_status(kb_url)
        if action == "ingest":
            return self._show_ingest_guide()
        if action == "search" and index:
            return self._search_index(es_url, index)
        print_warning("Actions: health | indices | kibana | ingest | search")
        return ""

    def _http_get(self, url: str) -> dict | None:
        """Make a simple GET request and return parsed JSON."""
        try:
            with urllib.request.urlopen(url, timeout=5) as resp:
                return json.loads(resp.read().decode())
        except urllib.error.URLError as e:
            print_error(f"Cannot connect to {url}: {e.reason}")
            return None
        except Exception as e:
            print_error(f"Request failed: {e}")
            return None

    def _es_health(self, es_url: str) -> str:
        """Check Elasticsearch cluster health."""
        print_section("Elasticsearch Cluster Health")
        data = self._http_get(f"{es_url}/_cluster/health?pretty")
        if data:
            status = data.get("status", "unknown")
            color = {"green": "\033[92m", "yellow": "\033[93m", "red": "\033[91m"}.get(status, "")
            reset = "\033[0m"
            print(f"  Cluster : {data.get('cluster_name')}")
            print(f"  Status  : {color}{status.upper()}{reset}")
            print(f"  Nodes   : {data.get('number_of_nodes')}")
            print(f"  Shards  : {data.get('active_shards')} active")
            return str(data)
        return ""

    def _list_indices(self, es_url: str) -> str:
        """List all Elasticsearch indices (log sources)."""
        print_section("Elasticsearch Indices")
        data = self._http_get(f"{es_url}/_cat/indices?format=json&s=index")
        if data:
            print(f"  {'Index':<40} {'Docs':>10} {'Size':>10}")
            print(f"  {'-'*40} {'-'*10} {'-'*10}")
            for idx in data:
                print(f"  {idx.get('index',''):<40} {idx.get('docs.count',''):>10} {idx.get('store.size',''):>10}")
        return str(data)

    def _kibana_status(self, kb_url: str) -> str:
        """Check Kibana API status."""
        print_section("Kibana Status")
        data = self._http_get(f"{kb_url}/api/status")
        if data:
            overall = data.get("status", {}).get("overall", {})
            print(f"  Kibana version : {data.get('version', {}).get('number', 'N/A')}")
            print(f"  Overall status : {overall.get('level', 'N/A')}")
            print(f"  Summary        : {overall.get('summary', 'N/A')}")
        return str(data)

    def _search_index(self, es_url: str, index: str) -> str:
        """Show the 5 most recent documents in an index."""
        print_section(f"Latest Events in Index: {index}")
        data = self._http_get(
            f"{es_url}/{index}/_search?size=5&sort=@timestamp:desc&pretty"
        )
        if data:
            hits = data.get("hits", {}).get("hits", [])
            for i, hit in enumerate(hits, 1):
                print(f"  [{i}] {json.dumps(hit.get('_source', {}), indent=6)[:300]}")
        return str(data)

    def _show_ingest_guide(self) -> str:
        """Print a guide for shipping logs into ELK."""
        print_section("ELK Log Ingestion Guide")
        guide = """
  Option 1 — Filebeat (most common, lightweight agent)
  ─────────────────────────────────────────────────────
  Install:  sudo apt install filebeat
  Config:   /etc/filebeat/filebeat.yml
  Enable:   sudo filebeat modules enable system suricata zeek
  Start:    sudo systemctl start filebeat

  Option 2 — Logstash pipeline (for parsing/enrichment)
  ─────────────────────────────────────────────────────
  Input  → reads from file, syslog, Beats, Kafka, etc.
  Filter → grok, mutate, geoip, useragent, kv
  Output → ships to Elasticsearch

  Option 3 — Wazuh → Elasticsearch
  ─────────────────────────────────────────────────────
  Wazuh natively supports Elasticsearch/OpenSearch as output.
  Set output.elasticsearch in /var/ossec/etc/ossec.conf

  Tip: Use Elastic's pre-built SIEM rules in Kibana → Security
        """
        print(guide)
        return guide

    def interactive(self):
        print("\n  [ELK] Elasticsearch / Logstash / Kibana SIEM")
        print("  Actions: health | indices | kibana | ingest | search")
        action   = input("  Action [health]: ").strip() or "health"
        es_url   = input(f"  Elasticsearch URL [{DEFAULT_ES_URL}]: ").strip() or DEFAULT_ES_URL
        kb_url   = input(f"  Kibana URL [{DEFAULT_KB_URL}]: ").strip() or DEFAULT_KB_URL
        index    = ""
        if action == "search":
            index = input("  Index name (e.g. filebeat-*): ").strip()
        self.run(action=action, es_url=es_url, kb_url=kb_url, index=index)

    def run_from_args(self, args):
        self.run(
            action=getattr(args, "action", "health"),
            es_url=getattr(args, "es_url", DEFAULT_ES_URL),
            kb_url=getattr(args, "kb_url", DEFAULT_KB_URL),
            index=getattr(args, "index", "")
        )
