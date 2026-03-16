# 🛡️ SIEM Tools — Overview & Learning Guide

This document explains the SIEM (Security Information and Event Management) tools
integrated into the Cyber Toolkit and how they fit together in a real security operations center (SOC).

---

## What is a SIEM?

A **SIEM** collects, normalizes, correlates, and alerts on security events from across your entire environment:
- Servers and endpoints
- Network devices (firewalls, switches, routers)
- Applications and databases
- Cloud services

The goal: detect threats faster by connecting the dots across many log sources.

---

## The SIEM Stack in This Toolkit

```
┌─────────────────────────────────────────────────────────────┐
│                        VISIBILITY LAYER                     │
│   Kibana Dashboard  ◄──  Wazuh Dashboard                   │
├─────────────────────────────────────────────────────────────┤
│                        STORAGE LAYER                        │
│         Elasticsearch / Wazuh Indexer (OpenSearch)          │
├─────────────────────────────────────────────────────────────┤
│                      CORRELATION LAYER                      │
│        Wazuh Manager (rules, decoders, active response)     │
├──────────────────────┬──────────────────────────────────────┤
│   DETECTION LAYER    │        COLLECTION LAYER              │
│   Suricata (IDS/IPS) │  Zeek (NSM) + Filebeat + Logstash   │
├──────────────────────┴──────────────────────────────────────┤
│                      NETWORK / ENDPOINTS                    │
│         Servers · Firewalls · Workstations · Cloud          │
└─────────────────────────────────────────────────────────────┘
```

---

## Tool Roles

### 🔵 Zeek — Network Visibility
- Sits on the network and generates structured logs for every connection
- Logs: `conn.log`, `dns.log`, `http.log`, `ssl.log`, `files.log`
- Great for: detecting C2 beacons, DNS tunneling, unusual data transfers
- NOT alert-based — Zeek logs everything and lets your SIEM find patterns

### 🔴 Suricata — Threat Detection
- Signature-based IDS/IPS — fires alerts when traffic matches known attack patterns
- Uses community rulesets: ET Open, Snort rules, custom rules
- Output: EVE JSON (ships perfectly into ELK or Wazuh)
- Great for: detecting exploits, port scans, malware C2 traffic in real-time

### 🟠 Wazuh — Host-Based SIEM / XDR
- Runs agents on endpoints to monitor:
  - System logs (syslog, Windows Event Log, macOS logs)
  - File integrity (FIM) — alerts when critical files change
  - Rootkit and anomaly detection
  - Vulnerability scanning
- Correlates events across all agents on a central manager
- Integrates natively with Suricata, Zeek, and ELK

### 🟢 ELK Stack — Storage, Search & Visualization
- **Elasticsearch**: stores billions of events, full-text search, aggregations
- **Logstash**: parse and enrich logs (grok filters, GeoIP, user-agent)
- **Kibana**: build dashboards, run threat hunting queries, set up SIEM detection rules
- **Filebeat**: lightweight agent to ship logs from endpoints to Elasticsearch

---

## Typical Alert Flow

```
1. Attacker scans your network
2. Suricata fires an alert: ET SCAN Nmap Scripting Engine
3. EVE JSON log written to /var/log/suricata/eve.json
4. Filebeat ships the log to Elasticsearch
5. Wazuh agent also notices the scan in system logs
6. Wazuh Manager correlates the two events → high severity alert
7. Kibana SIEM dashboard shows the alert to the analyst
8. Analyst investigates using Zeek conn.log and dns.log
```

---

## Getting Started (Local Lab)

The easiest way to run a full SIEM lab locally:

```bash
# Option 1: Wazuh all-in-one installer (VM or bare metal)
curl -sO https://packages.wazuh.com/4.7/wazuh-install.sh
sudo bash wazuh-install.sh -a

# Option 2: ELK via Docker Compose
git clone https://github.com/deviantony/docker-elk.git
cd docker-elk
docker-compose up

# Option 3: Elastic Security (built-in SIEM in Kibana)
# After ELK is running, go to Kibana → Security
```

---

## Learning Resources

| Resource | Link |
|----------|------|
| Wazuh docs | https://documentation.wazuh.com |
| Suricata docs | https://docs.suricata.io |
| Zeek docs | https://docs.zeek.org |
| Elastic SIEM | https://www.elastic.co/security |
| TryHackMe SIEM room | https://tryhackme.com/room/introductoryroomdfirmodule |
| Splunk Free Training | https://www.splunk.com/en_us/training/free-courses.html |
