# 🛡️ Cyber Toolkit

A beginner-friendly Python CLI that brings together the most popular **open source cybersecurity tools** under one unified interface. Learn the industry-standard tools used by real penetration testers and security researchers.

> ⚠️ **Ethical Use Only**: Only use these tools on systems you own or have explicit written permission to test. Unauthorized scanning/testing is illegal.

---

## 🧰 Tools Included

| Module | Tool | What It Does |
|--------|------|--------------|
| `nmap` | [Nmap](https://nmap.org/) | Network discovery & port scanning |
| `nikto` | [Nikto](https://github.com/sullo/nikto) | Web server vulnerability scanner |
| `sqlmap` | [SQLMap](https://sqlmap.org/) | Automated SQL injection detection |
| `hashcat` | [Hashcat](https://hashcat.net/) | Password hash cracking |
| `gobuster` | [Gobuster](https://github.com/OJ/gobuster) | Directory & DNS brute-forcing |
| `whois` | Built-in | Domain WHOIS lookups |
| `sslcheck` | Built-in | SSL/TLS certificate analysis |

---

## 🚀 Quick Start

### 1. Clone the repo
```bash
git clone https://github.com/preethipakala/cyber-toolkit.git
cd cyber-toolkit
```

### 2. Install Python dependencies
```bash
pip install -r requirements.txt
```

### 3. Launch the interactive menu
```bash
python toolkit.py
```

### 4. Or run a specific tool directly
```bash
python toolkit.py nmap --target 127.0.0.1
python toolkit.py nikto --target http://localhost
python toolkit.py whois --domain example.com
python toolkit.py sslcheck --domain example.com
python toolkit.py sqlmap --url "http://testsite.com/page?id=1"
python toolkit.py gobuster --url http://localhost --wordlist data/wordlist.txt
python toolkit.py hashcat --hash 5f4dcc3b5aa765d61d8327deb882cf99 --mode 0
```

---

## 📁 Project Structure

```
cyber-toolkit/
├── toolkit.py              # Main CLI entry point & interactive menu
├── tools/
│   ├── __init__.py
│   ├── base.py             # Base class for all tool wrappers
│   ├── nmap_tool.py        # Nmap wrapper
│   ├── nikto_tool.py       # Nikto wrapper
│   ├── sqlmap_tool.py      # SQLMap wrapper
│   ├── hashcat_tool.py     # Hashcat wrapper
│   ├── gobuster_tool.py    # Gobuster wrapper
│   ├── whois_tool.py       # WHOIS lookup (built-in)
│   └── ssl_tool.py         # SSL/TLS checker (built-in)
├── utils/
│   ├── __init__.py
│   ├── checker.py          # Check if tools are installed
│   └── reporter.py         # Output formatting
├── data/
│   └── wordlist.txt        # Common directory wordlist for Gobuster
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 📚 What You'll Learn

- How real-world security tools work under the hood
- Web server vulnerability scanning with Nikto
- SQL injection discovery with SQLMap
- Network reconnaissance with Nmap
- Directory enumeration with Gobuster
- Password hash cracking concepts with Hashcat
- SSL/TLS certificate analysis
- How to wrap CLI tools in Python using `subprocess`

---

## 🔭 Tool Reference

### 🔍 Nmap — Network Scanner
```bash
python toolkit.py nmap --target 192.168.1.1
python toolkit.py nmap --target 192.168.1.1 --profile full
```
Profiles: `quick` (top 100 ports) | `standard` (top 1000) | `full` (all 65535) | `vuln` (vulnerability scripts)

### 🌐 Nikto — Web Scanner
```bash
python toolkit.py nikto --target http://localhost
```
Checks for outdated software, dangerous files, misconfigurations.

### 💉 SQLMap — SQL Injection
```bash
python toolkit.py sqlmap --url "http://testsite.com/page?id=1"
```
**Only use on your own apps or authorized targets.**

### 📂 Gobuster — Directory Brute-Force
```bash
python toolkit.py gobuster --url http://localhost --wordlist data/wordlist.txt
```

### 🔒 SSL Check — Certificate Analyzer
```bash
python toolkit.py sslcheck --domain example.com
```

### 🌍 WHOIS — Domain Lookup
```bash
python toolkit.py whois --domain example.com
```

### 🔑 Hashcat — Hash Cracker
```bash
python toolkit.py hashcat --hash 5f4dcc3b5aa765d61d8327deb882cf99 --mode 0
```
Mode 0 = MD5, Mode 100 = SHA1, Mode 1800 = SHA-512

---

## 🔭 Next Steps / Ideas

- [ ] Add Metasploit module launcher
- [ ] Add DNS enumeration (dnsenum/dnsrecon)
- [ ] Add output logging to JSON
- [ ] Add a `--safe` flag that blocks non-localhost targets
- [ ] Build a web dashboard to view scan results

---

## 📜 License

MIT — free to use, learn from, and extend.
