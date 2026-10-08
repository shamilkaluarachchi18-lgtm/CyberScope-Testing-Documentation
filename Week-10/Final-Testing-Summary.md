# Final Testing Summary

## Objective
Validate whether the final CyberScope security-testing logic could distinguish trusted and modified states using Device-DNA comparison and packet-level network evidence.

## Test Environment
- Ubuntu VM in VMware
- Hostname: `crypto`
- Interface: `ens33`
- IP address: `192.168.137.145`
- MAC address: `00:0c:29:70:9b:b5`
- Python 3
- Wireshark
- JSON trusted/runtime datasets
- SHA-256 hashing
- CSV result logging

## Python Validation Summary

| Test | Expected Result | Actual Result | Status |
|---|---|---|---|
| Legitimate runtime | LEGITIMATE | LEGITIMATE | PASS |
| New TCP service on port 8080 | POTENTIAL COMPROMISE | POTENTIAL COMPROMISE | PASS |
| Hostname changed | POTENTIAL COMPROMISE | POTENTIAL COMPROMISE | PASS |
| Restored runtime | LEGITIMATE | LEGITIMATE | PASS |

## Wireshark Validation Summary
The controlled network scenario used a temporary Python HTTP server on TCP port 8080.

Wireshark confirmed:
- TCP connection establishment to port 8080
- HTTP `GET / HTTP/1.1`
- HTTP `200 OK`
- Multiple TCP conversations involving port 8080
- Ethernet → IPv4 → TCP → HTTP protocol hierarchy
- Removal of port 8080 after the controlled test

## Final Interpretation
The Python validator showed that meaningful device/network changes altered the Device DNA and produced a compromise result. Wireshark independently confirmed that the controlled TCP service was active and generating real application-layer traffic.

The restored runtime produced the original trusted Device DNA again, showing that the validation process could distinguish trusted, modified, and restored states.
