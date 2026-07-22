# 🛡️ Cyber-Tools: Advanced Cybersecurity & Infrastructure Auditing Labs

Welcome to the **Cyber-Tools** repository. This project is a comprehensive portfolio demonstrating practical software engineering applied to offensive and defensive cybersecurity scenarios. It encompasses multi-threaded network scanners, automated vulnerability assessment engines, cryptographic file integrity monitors, and active directory defense simulations.

## 🚀 Repository Structure & Modules

This repository is split into distinct logical modules, each focusing on a specific tier of security engineering:

# 🛡️ Cyber-Tools: Advanced Cybersecurity & Infrastructure Auditing Labs

Welcome to the **Cyber-Tools** repository. This project is a comprehensive portfolio demonstrating practical software engineering applied to offensive and defensive cybersecurity scenarios. It encompasses multi-threaded network scanners, automated vulnerability assessment engines, cryptographic file integrity monitors, and active directory defense simulations.

## 🚀 Repository Structure & Modules

This repository is split into distinct logical modules, each focusing on a specific tier of security engineering:

### 📂 01-Foundations-Legacy

This module serves as the foundational core of the repository, demonstrating low-level network communications, multithreaded operations, basic cryptographic auditing, and automation wrappers using native Python ecosystems.

#### 🛰️ 1. Network Reconnaissance & Banner Grabbing Suite
* **`fast_port_scanner.py` & `full_port_scanner.py`:** Implements raw TCP/UDP port scanners leveraging the built-in `socket` library. It uses `socket.connect_ex()` to determine open states based on zero-return codes and dynamically tunes responsiveness via `soket.settimeout(0.5)` to optimize discovery speeds without causing massive network noise.
* **`service_checker.py`:** Focuses on tactical service interrogation by establishing direct network channels and actively sending payload greetings (`s.send(b'Hello\r\n')`) to extract service identities (banners) via `s.recv(1024)`, handling binary streams gracefully with standard decoding error filters.
* **`security_reporter.py`:** The centralized data ingestion agent that orchestrates multi-threaded banner acquisition using `ThreadPoolExecutor(max_workers=5)`. It models network structures into standardized JSON configurations (`scan_report.json`), complete with target tags, ISO timestamps, and nested array findings for downstream analysis.

#### 🎯 2. Vulnerability Assessment & Defensive Profiling
* **`vulnerability_scanner.py` & `advanced_vuln_scanner.py`:** Automated static analysis engines that evaluate active network profiles against local Vulnerability Databases (CVE catalog simulation). They utilize the Regular Expressions (`re`) module to extract software version strings (e.g., parsing `Apache/(\d+\.\d+\.?\d*)` and utilizing regex group matching) to flag critical vulnerabilities like Heartbleed, SSL validation bypasses, or Remote Code Execution (RCE) flaws.
* **`header_security_analyzer.py`:** A passive web assessment tool that inspects extracted HTTP headers on ports 80/443, auditing targets for vital defensive components such as `X-Frame-Options` (Clickjacking mitigation), `X-XSS-Protection` (Cross-Site Scripting control), `Content-Security-Policy` (CSP browser firewall), and `Strict-Transport-Security` (HSTS policy enforcement).
* **`security_scorer.py`:** An algorithmic risk-scoring matrix that computes a baseline security posture rating out of 100. It dynamically penalizes target servers based on exposed service footprints, critical software vulnerabilities, and missing security headers, triaging outcomes into LOW, MID, or HIGH risk matrices.

#### 🔑 3. Authentication Auditing & Brute-Force Simulations
* **`controlled_brute.py` & `brute_force_sim.py`:** Simulates dictionary attack vectors against internal systems. It utilizes high-velocity `threading` models to split wordlists, simulates network latency variables using `random.uniform()`, and tests user accounts simultaneously using custom thread pools to identify fragile credentials.
* **`brute_force_protection.py` (Inline Sim):** A behavioral control mechanism that models adaptive lockouts. It tracks failed authentication loops, enforces sequential chance reductions, and triggers immediate system state blocks when credential-stuffing limits are violated.

#### ⚙️ 4. Enterprise Automation & Monitoring Frameworks
* **`orchestrator.py`:** A command-line automation harness that uses `os.system()` to map out the entire defensive pipeline—sequentially firing up data collection, passing artifacts to vulnerability scanners, and calling the risk scoring matrix to build a cohesive workflow loop.
* **`bulk_orchestrator.py` & `fast_bulk_orchestrator.py`:** Advanced mass-auditing scripts designed to ingest lists of target assets (`targets.txt`). The standard version processes targets sequentially, while the fast version spawns asynchronous workers (`threading.Thread`) to process multiple targets concurrently, automatically backing up individual JSON reports to prevent race conditions and state overwrites.
* **`file_integrity_check.py`:** A lightweight Host Intrusion Detection System (HIDS) simulation. It chunk-reads data buffers via `hashlib.sha256()` to process heavy system files safely, validating current cryptographic file fingerprints against baseline hashes to instantly flag unauthorized persistence or malicious file modifications.
* **`logger_tool.py` & `logger.py`:** Enterprise logging facades configured via `logging.basicConfig()`. They systematically map out execution streams into `cyber_tool.log`, standardizing audit logs into strict `TIMESTAMP - LEVEL - MESSAGE` schemas for SIEM ingestion simulation.
* **`security_dashboard.py`:** A centralized terminal-based security operation center (SOC) console. It searches the directory tree for JSON reports, dynamically casts metrics, handles type conversion errors, and renders system status tables complete with conditional status indicators (🔴 Critical / 🟡 Warning / 🟢 Secure) alongside the latest log feeds.



### 📂 02-Professional-OOP

This module focuses on applying object-oriented programming (OOP) principles to construct reusable, modular, and maintainable networking frameworks. It heavily relies on the `Scapy` library for advanced packet crafting, protocol analysis, and active network defense simulation.

#### 🛡️ 1. Layer-2 and Layer-3 Protocol Auditing & Defense
* **`arp_mitm_defender.py`:** A host-based intrusion prevention system (HIPS) simulation. It places the interface into continuous sniffing mode using `scapy.sniff(store=False)`, parsing inbound ARP Reply messages (`op=2`). It validates the hardware source address (`hwsrc`) of the gateway against a pre-configured static cryptographic binding, raising immediate high-severity alerts upon detecting ARP cache poisoning (Man-in-the-Middle mitigation).
* **`dns_analyser_pro.py`:** A deep packet inspection (DPI) tool designed to monitor application-layer anomalies. It hooks into UDP port 53 traffic, intercepts DNS query definitions (`DNSQR`), and cross-references requested domain names against an enterprise blacklist while simultaneously logging server responses (`DNSRR`) to monitor outbound command-and-control (C2) vectors.

#### ⚔️ 2. Offensive Automation & Traffic Generation
* **`mac_flooder_pro.py`:** An offensive stress-testing engine that simulates a MAC Table Overflow attack against a Layer-2 network switch. It uses loop cycles to craft malicious Ethernet envelopes containing randomized hardware addresses (`scapy.RandMAC()`) bundled inside broadcast ARP headers, rapidly flooding the switch to force fail-open states.
* **`network_security_tool.py`:** A dual-purpose script combining targeted ARP impersonation and real-time query interception. It uses low-level Layer-2 address resolution loops (`scapy.srp`) to dynamically bind arbitrary IP ranges to the attacker interface, creating an automated data routing choke point.
* **`stealth_port_scanner.py`:** A stealthy TCP reconnaissance agent implementing half-open (SYN) port auditing. It injects synchronized probe request headers (`flags="S"`) via Layer-3 sockets (`scapy.sr1`) and analyzes response flags, safely mapping open entry points while evading application-layer system logs.

#### 🧪 3. Custom Packet Crafting & Software Architecture
* **`packet_crafter.py` & `packet_crafter_v2.py`:** Demonstrates core network stack layering by manually chaining standard protocol envelopes (IP/ICMP) and embedding hidden diagnostic string signatures inside arbitrary data transport layers (`Raw(load=...)`).
* **`packet_wizard_pro.py`:** An advanced packet manipulation matrix capable of generating custom diagnostic probes alongside Christmas Tree packets (`flags="FPU"`). It lights up FIN, PSH, and URG flags simultaneously to audit legacy firewall behaviors and stateless filter parameters.
* **`security_scanner_v2.py`:** A structural demonstration of structural OOP code design. It models enterprise vulnerability management systems by encapsulating multi-tier asset tracking data parameters and structured scanning methods into cohesive, reusable software objects.


### 📂 03-Network-Analysis

This module serves as a post-incident investigation and proactive threat hunting engine. It leverages the `Scapy` ecosystem to ingest raw packet capture artifacts (`.pcap`), executing deep packet analysis, forensic parsing, and stateful algorithmic anomaly detection to identify multi-vector network intrusions.

#### 🦅 1. Threat Hunting & Intrusion Detection Engines
* **`arp_spoof_detector.py`:** A forensic analysis agent designed to uncover Man-in-the-Middle (MITM) operations. It reads historical network streams via `scapy.rdpcap()`, dynamically mapping Layer-3 IP structures against Layer-2 physical hardware addresses inside a stateful ledger. It triggers high-severity alerts whenever a single protocol source maps to conflicting hardware fingerprints, identifying historical cache poisoning vectors.
* **`ddos_flood_detector.py`:** A stateful network telemetry analysis script engineered to identify distributed denial-of-service (DDoS) and SYN flood signatures. It parses structural TCP header flags (`flags = "S"`) and maintains an active dictionary counter per source address, isolating high-velocity traffic spikes that cross established volumetric security thresholds.
* **`dns_tunneling_detector.py`:** An application-layer anomaly detection utility tailored to stop stealthy data exfiltration and command-and-control (C2) channeling. By examining DNS Request packets (`qr == 0`), it systematically calculates the character length configurations of incoming query names (`qname`), flagging queries that violate anomalous length boundaries.

#### 🔍 2. Forensic Auditing & Reconnaissance Mapping
* **`pcap_credential_harvester.py`:** A passive data leakage inspector that scans unencrypted application transport layers for exposure profiles. It acts as a cleartext credential auditor by extracting the `Raw` payload message layer of historical sessions and running multi-condition substring checks against a definitive dictionary of sensitive keywords.
* **`pcap_hacker_detector.py`:** A digital forensics dashboard that aggregates total network traffic configurations. It maps out overall package distribution ratios across the entire capture timeline, computing standard volume distributions to rapidly distinguish baseline infrastructure hosts from high-frequency anomaly vectors.
* **`port_scanner.detector.py`:** An adversarial reconnaissance profiling tool that tracks coordinated vertical and horizontal host sweeps. It structures incoming target hits into distinct, non-duplicate port sets (`set()`) for each discovered source address, flagging adversarial scanning entities whose distinct destination port hits exceed threshold limits.


### 📂 04-Code-Security

This module bridges the gap between software engineering and application security (AppSec) by introducing automated DevSecOps and Secure Software Development Life Cycle (SSDLC) practices. It contains custom-built engines for Static Application Security Testing (SAST), Software Supply Chain Auditing, and Data Leakage Prevention (DLP).

#### 🛡️ 1. Static Application Security Testing (SAST) & Supply Chain Security
* **`static_code_analyzer.py`:** A pattern-matching Static Application Security Testing (SAST) engine. It uses deterministic regular expressions (`re.search`) to audit source code files line-by-line for high-risk code smells, automatically isolating hardcoded secrets, dangerous execution wrappers (`eval`/`exec`), and legacy cryptographic modules.
* **`dependency_vulnerability_scanner.py`:** A software supply chain security scanner that audits explicit package manifests (`requirements.txt`). It implements custom version-parsing array logic to compare installed component releases against a local CVE/Vulnerability Advisory intelligence database, mitigating downstream components risk.
* **`hash_integrity_verifier.py`:** A file integrity monitoring (FIM) daemon designed to intercept host-based tampering. It baselines a clean file state using chunked binary streaming (`4096 bytes`) into a unique SHA-256 digest, keeping persistent file loops to trigger alarms if unauthorized manipulation or arbitrary file destruction occurs.

#### 🔐 2. Data Privacy & Anti-Reverse Engineering
* **`regex_pii_detector.py`:** A stateful Data Leakage Prevention (DLP) routine mapped out to discover Personally Identifiable Information (PII) inside production server logs. It employs specialized character boundary expressions to track credit card components, email strings, and local national ID formats, alerting security operation centers to log-poisoning leaks.
* **`source_code_obfuscator.py` & `protected_analyzer.py`:** An automated intellectual property protection pipeline. It ingests plain-text scripts, transforms standard components into low-level binary matrices, and applies full Base64 obfuscation wrapper algorithms. The resulting capsule shields human readability while preserving execution structures via secure runtime interpretation (`exec(base64.b64decode(...))`).


### 📂 05-Network-Pentesting

This module focuses on network security analysis, penetration testing methodologies, and defensive boundary mechanisms. It demonstrates how network protocols function under load, how systems intercept unauthorized authentication attempts, and how boundary firewalls analyze streaming traffic packets.

#### 🌐 1. Network Analysis & Perimeter Defense Simulators
* **`cyber_firewall_mitigator.py`:** An inline packet-filtering simulation engine powered by Scapy. It hooks into live network interfaces (`sniff`) to parse Layer 3 IP headers, matching source signatures against an active threat intelligence blacklist to simulate traffic dropping and host isolation.
* **`icmp_flood_analyzer.py`:** A network latency and quality-of-service stress testing utility. It constructs custom ICMP echo-request structures using raw packet generation to determine high-latency thresholds and measure infrastructure resilience under high packet frequencies.
* **`ssh_bruteforce_mitigator.py`:** An authentication security simulator that models Intrusion Prevention System (IPS) behavior. It manages automated brute-force thresholds using Paramiko authentication routines, dynamically blacklisting simulated source points when failure limits are breached.
* **`ssh_honeypot_simulator.py`:** A low-interaction SSH deception mechanism designed for threat intelligence gathering. It spins up a decoy socket listener on port 2222, logging incoming credential patterns and authentication sequences while intentionally denying access to track intruder dictionary assets.

#### 🔍 2. Vulnerability Scanning & Infrastructure Auditing
* **`sqli_vulnerability_scanner.py`:** A vulnerability validation utility built to identify SQL Injection entry points. It tests target parameters against web database fuzzing arrays and parses HTTP response structures for exposed backend syntax errors (MySQL, SQL Server, etc.).
* **`subdomain_takeover_scanner.py`:** A DNS infrastructure audit daemon. It tracks subdomain CNAME redirections to verify pointers against missing cloud platform fingerprints (e.g., GitHub Pages, Heroku, Netlify), mitigating supply-chain domain highjacking vectors.
* **`recon_vulnerability_scanner.py`:** An automated HTTP reconnaissance module mapping out active web perimeters. It performs subdomain discovery via targeted status-code validation (200, 301, 403), flagging misconfigured development portals or unauthenticated admin surfaces.
* **`malware_threat_analyzer.py`:** A static malware triage tool that computes digital file fingerprints via chunked SHA-256 binary streaming. It scans local binaries for embedded indicators of compromise (IoCs), generating unified risk scores for threat assessment.
* **`crypto_ransom_simulator.py`:** A cryptographic lab exercise demonstrating the impact of symmetric algorithms on file systems. It uses standard Fernet blueprints to showcase secure file lock-states and disaster recovery/decryption restoration phases.
* **`wifi_deauth_simulator.py`:** A wireless audit simulation modeling 802.11 Layer 2 frame manipulation. It crafts synthetic Deauthentication management frames using Scapy syntax to demonstrate wireless architecture limitations in controlled, authorized test environments.


### 📂 06-Exploit-Development-Automation

This module establishes a comprehensive Purple Team simulation environment, pairing automated exploitation vectors (`hacker_*.py`) with production-grade defense controls, detection engines, and mitigation shields (`security_*.py`). It maps out web vulnerabilities, infrastructure compromises, and continuous integration risks alongside real-time corporate logging telemetry.

#### 🥷 1. Automated Exploitation Frameworks (Red Team Simulators)
* **`hacker_api_fuzzer.py`:** An offensive utility designed to exploit Broken Object Level Authorization (BOLA/IDOR) vulnerabilities[cite: 7]. It automates token-backed iterations over localized API parameters to uncover data exposure risks[cite: 7].
* **`hacker_api_mass_assigner.py` & `hacker_mass_assigner.py`:** Injection tools built to simulate Overposting attacks[cite: 7]. They inject hidden database attributes (`is_admin`, `balance`) into poorly validated API endpoints to attempt privilege escalation[cite: 7].
* **`hacker_command_weaponizer.py`:** A Remote Code Execution (RCE) scanner that embeds shell-breaking command strings into application query strings to execute operating system operations[cite: 7].
* **`hacker_deserialization_bomber.py`:** A weaponized object serializer engineering toxic payloads via Python standard library unpickling structures to force shell command executions on system extraction[cite: 7].
* **`hacker_dns_rebinder.py`:** A stateful DNS manipulation pipeline that alters resolve values dynamically to bypass browser origin security mechanisms and funnel traffic into protected local spaces[cite: 7].
* **`hacker_jwt_manipulator.py`:** A cryptographic token forgery generator that breaks weak token structures, unpacking payload JSON arrays to elevate access permissions artificially[cite: 7].
* **`hacker_pipeline_poisoner.py`:** A supply-chain compromise utility that modifies target YAML deployment scripts to drop continuous delivery backdoors during compilation tasks[cite: 7].
* **`hacker_ransomware_simulator.py`:** An education-focused file locking system that mimics cryptographic threat traits by traversing target folder spaces, scrambling document contents, and altering file extensions[cite: 7].
* **`hacker_reverse_shell_agent.py`:** A stealth shell connection broker utilizing internal sub-processes to provide active runtime command control panels back to external Command and Control (C2) interfaces[cite: 7].
* **`hacker_ssrf_fuzzer.py`:** A proxy manipulation fuzzer designed to exploit Server-Side Request Forgery flaws, forcing public interfaces to query cloud metadata backends and private infrastructure targets[cite: 7].
* **`hacker_ssti_fuzzer.py`:** A template manipulation array that designs abstract code skeletons to query server templating frameworks for structural weaknesses and code execution pathways[cite: 7].
* **`hacker_xxe_injector.py`:** An XML parsing attack payload that injects External Entity references and custom DTD definitions to target arbitrary local flag parameters[cite: 7].

#### 🛡️ 2. Production Security Shields & Mitigations (Blue Team Countermeasures)
* **`security_api_gatekeeper.py` & `security_mass_assignment_shield.py`:** Rigid API boundary components enforcing structural whitelist filtering via Data Transfer Objects (DTOs) to block IDOR vectors and strip out unrecognized payload modifications[cite: 7].
* **`security_api_gateway.py`:** An institutional token broker verifying authentication context bindings directly against backend user parameters to neutralize BOLA intrusion activities[cite: 7].
* **`security_deserialization_shield.py`:** A secure class extraction wrapper restricting unpickling capabilities to white-listed system templates, blocking remote system execution overrides[cite: 7].
* **`security_dns_protector.py`:** A core DNS security parsing engine auditing name resolutions for anomalous private local IP addresses to deflect DNS Rebinding attempts[cite: 7].
* **`security_edr_hunter.py`:** An Endpoint Detection and Response simulation agent monitoring process hierarchies for malicious network traffic and killing unauthorized shells at the kernel boundary[cite: 7].
* **`security_fim_monitor.py`:** A high-frequency File Integrity Monitoring system tracing system extensions to recognize encryption threats and respond with rapid endpoint isolation[cite: 7].
* **`security_jwt_validator.py`:** A strict cryptographic validation mechanism enforcing robust signature authentication steps to defend user scopes from manipulation[cite: 7].
* **`security_pipeline_shield.py`:** A DevSecOps continuous deployment guard utilizing static regular expressions to identify and block injected commands within continuous integration pipelines[cite: 7].
* **`security_ssrf_validator.py`:** An application-layer proxy control mechanism checking structural hostname URLs to completely block target resolution inside private routing boundaries[cite: 7].
* **`security_ssti_sandbox.py`:** An Abstract Syntax Tree (AST) inspection component checking input formatting blocks for restricted keywords prior to rendering routines[cite: 7].
* **`security_waf_mitigator.py`:** A Web Application Firewall simulating traffic parsing routines to alert on character sequences common to command injection[cite: 7].
* **`security_xxe_defuser.py`:** A robust XML parser built on secure parsing abstractions, blocking unexpected external entities and stopping data exfiltration vectors[cite: 7].


### 📂 07-Advanced-Purple-Team-Scenarios

This module culminates the training suite by simulating advanced infrastructure attack primitives and OS-level memory defenses. It models Active Directory post-exploitation activities alongside modern host protection architectures designed to neutralize credential theft and unauthorized access validation.

#### 🥷 1. Lateral Movement & Hash Operations (Red Team)
* **`hacker_pth_exploit.py` / `PassTheHashSimulatedExploit`:** An offensive simulation tracing NTLM authentication protocol abuse[cite: 7]. It automates the generation of synthetic SMB challenge-response transactions using pre-stolen credential hashes, mapping out horizontal privilege escalation pathways across remote hosts without requiring raw text passwords[cite: 7].

#### 🛡️ 2. Memory Isolation & Evasion Blockers (Blue Team)
* **`security_credential_guard.py` / `Credential Guard Monitor`:** A defensive daemon simulating OS-level kernel memory protections[cite: 7]. It intercepts unauthorized read operations aimed at sensitive authentication subsystems (`lsass.exe`), flagging the abusive configuration of debugging privileges (`SeDebugPrivilege`) and systematically restricting access to safeguard cryptographic assets[cite: 7].

#### 🥷 3. Kerberos Exploitation & Service Ticket Extraction (Red Team)
* **`hacker_kerberoasting.py` / `AdvancedKerberoastingSimulator`:** An offensive automation framework designed to simulate targeted Kerberoasting attacks within Active Directory environments.
  * **Target Discovery:** Queries LDAP/AD records to identify SPN-bound service accounts (e.g., MSSQL, HTTP, Backup services).
  * **Protocol Interaction:** Formulates and transmits non-administrative `TGS-REQ` (Ticket Granting Service Request) messages to Domain Controllers.
  * **Cryptographic Extraction:** Parses returned `TGS-REP` ticket structures and isolates the encrypted ticket payload, supporting both legacy (`RC4-HMAC`, enctype 23) and modern (`AES256-CTS-HMAC-SHA1-96`, enctype 18) standards.
  * **Hashcat/John Compatibility:** Exports extracted cryptographic hashes directly into standard offline cracking formats (`$krb5tgs$23$` and `$krb5tgs$18$`) for post-exploitation password recovery workflows.

#### 🛡️ 4. Active Directory SIEM & Behavioral Monitoring (Blue Team)
* **`security_kerberoasting_monitor.py` / `EnterpriseKerberosAuditor`:** A real-time behavioral detection engine modeling Windows Event Log telemetry analysis for Active Directory domain protection.
  * **Telemetry Ingestion:** Monitored ingestion pipeline for Windows Event ID 4769 (`A Kerberos service ticket was requested`).
  * **Sliding-Window Anomaly Detection:** Utilizes a stateful, time-pendered algorithm to compute `TGS-REQ` volume per source IP within configurable time windows, effectively identifying automated bulk-roasting scripts.
  * **Cipher Downgrade Inspection:** Flags suspicious requests explicitly specifying legacy `RC4-HMAC` encryption types against accounts configured for AES.
  * **Automated Mitigation:** Executes dynamic incident response procedures by adding offending host addresses to an active isolation registry, automatically rejecting subsequent authentication attempts (`DROP`).

  #### 🥷 5. Pre-Authentication Abuse & AS-REP Roasting (Red Team)
* **`hacker_asrep_roasting.py` / `ASREPRoastingSimulator`:** An offensive security auditing module that identifies Active Directory user accounts with Kerberos Pre-Authentication disabled (`DONT_REQ_PREAUTH` / UAC flag `0x10000`). It simulates `AS-REQ` requests without timestamp verification, extracts encrypted `AS-REP` response structures, and formats them into Hashcat-compatible signatures (`$krb5asrep$23$`) for offline credential recovery.

#### 🛡️ 6. Event ID 4768 SIEM Audit & Dynamic Mitigation (Blue Team)
* **`security_asrep_monitor.py` / `ASREPMonitoringEngine`:** A real-time behavioral detection module analyzing Windows Event ID 4768 (`A Kerberos authentication ticket was requested`) log streams. It monitors requests bypassing Pre-Authentication, detects weak cipher downgrades (`RC4-HMAC` / `0x17`), tracks request frequencies via a sliding-window algorithm, and triggers automated incident response workflows to enforce security policies and restrict malicious IPs.

