# 🛡️ SIEM Tools — Overview & Learning Guide

This document explains the SIEM (Security Information and Event Management) tools integrated into the Cyber Toolkit and how they work together in a real-world Security Operations Center (SOC).

---

## 📌 What is a SIEM?

A **SIEM (Security Information and Event Management)** system collects, normalizes, correlates, and analyzes security events across your infrastructure:

- 🖥️ Servers and endpoints
- 🌐 Network devices (firewalls, routers, switches)
- 🗄️ Applications and databases
- ☁️ Cloud services

### 🎯 Goal:

Detect threats faster by correlating logs from multiple sources.

---

## 🧱 SIEM Stack Architecture

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

## 🔧 Tool Roles

### 🔵 Zeek — Network Visibility

- Generates structured logs for all network activity
- Logs include: `conn.log`, `dns.log`, `http.log`, `ssl.log`, `files.log`
- Best for:

  - Detecting command-and-control (C2)
  - DNS tunneling
  - Suspicious traffic patterns

👉 Zeek is **not alert-based** — it logs everything for analysis.

---

### 🔴 Suricata — Threat Detection (IDS/IPS)

- Signature-based intrusion detection system

- Uses rulesets like:

  - ET Open
  - Snort rules

- Outputs:

  - `eve.json` (perfect for ELK ingestion)

Best for:

- Detecting exploits
- Malware traffic
- Port scans

---

### 🟠 Wazuh — Host-Based SIEM / XDR

- Endpoint monitoring and correlation engine

Monitors:

- System logs (Linux, Windows, macOS)
- File integrity (FIM)
- Rootkits and anomalies
- Vulnerabilities

Features:

- Centralized manager
- Rule-based alerting
- Active response

---

### 🟢 ELK Stack — Storage & Visualization

| Component         | Role                        |
| ----------------- | --------------------------- |
| **Elasticsearch** | Stores and indexes logs     |
| **Logstash**      | Parses and enriches logs    |
| **Kibana**        | Dashboards & threat hunting |
| **Filebeat**      | Ships logs from sources     |

---

## 🔄 Typical Alert Flow

```
1. Attacker scans your network
2. Suricata detects scan → generates alert
3. Log written to /var/log/suricata/eve.json
4. Filebeat ships log → Logstash → Elasticsearch
5. Wazuh correlates related events
6. Alert appears in Kibana dashboard
7. Analyst investigates using Zeek logs
```

---

## 🚀 Running the SIEM Lab (Docker)

### Start everything:

```bash
docker-compose -f docs/elk-docker-compose.yml up -d
```

---

### 🌐 Access Services

| Service       | URL                    |
| ------------- | ---------------------- |
| Kibana        | http://localhost:5601  |
| Elasticsearch | http://localhost:9200  |
| Wazuh API     | http://localhost:55000 |

---

### ⚡ Health Check

```bash
python toolkit.py elk --action health
```

---

### 🧪 Test Log Ingestion

```bash
sudo mkdir -p /var/log/suricata
echo "test log" | sudo tee /var/log/suricata/test.log
```

Then check logs in **Kibana → Discover**

---

## 📚 Learning Resources

| Resource           | Link                                  |
| ------------------ | ------------------------------------- |
| Wazuh Docs         | https://documentation.wazuh.com       |
| Suricata Docs      | https://docs.suricata.io              |
| Zeek Docs          | https://docs.zeek.org                 |
| Elastic Security   | https://www.elastic.co/security       |
| TryHackMe SIEM Lab | https://tryhackme.com                 |
| Splunk Training    | https://www.splunk.com/en_us/training |

---
