# Week 9 Evidence Index

Upload your actual screenshots into this folder and rename them clearly.

Recommended filenames:

1. `01-normal-vm-state.png`
   - hostname, ens33 IP/MAC and listening ports

2. `02-python-v2-script.png`
   - improved `cyberscope_compare_v2.py` logic

3. `03-refined-baseline.png`
   - V2 trusted baseline and JSON structure

4. `04-normal-comparison-legitimate.png`
   - stable attributes match and result is LEGITIMATE

5. `05-dynamic-udp-49000-legitimate.png`
   - temporary UDP port appears but result remains LEGITIMATE

6. `06-tcp-8080-potential-compromise.png`
   - new stable TCP port 8080 detected as POTENTIAL COMPROMISE

7. `07-wireshark-dns.png`
   - legitimate DNS queries using UDP source ports

8. `08-wireshark-udp-conversations.png`
   - UDP conversations showing changing temporary ports

9. `09-wireshark-tcp-8080.png`
   - traffic filtered with `tcp.port == 8080`

10. `10-wireshark-http.png`
    - HTTP GET / 200 OK / 404 traffic

11. `11-wireshark-tcp-conversations.png`
    - TCP conversations involving port 8080

12. `12-wireshark-protocol-hierarchy.png`
    - IPv4 → TCP → HTTP hierarchy for the controlled service

## Evidence Use

These screenshots support the Week 9 PDJ claims about:

- false-positive reduction
- stable versus dynamic network attributes
- legitimate DNS behaviour
- controlled TCP service detection
- packet-level validation using Wireshark
