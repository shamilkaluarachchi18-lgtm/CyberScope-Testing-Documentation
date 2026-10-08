# Week 9 Testing Plan

## Objective

Validate the refined CyberScope network-attribute comparison logic and confirm that normal dynamic network changes do not automatically trigger false-positive compromise results.

## Environment

- Ubuntu VM in VMware
- Network interface: `ens33`
- Python 3
- Wireshark
- CyberScope V2 comparison script
- Trusted baseline stored in `cyberscope_baseline_v2.json`

## Test Strategy

Three main states are tested:

1. Normal trusted state
2. Legitimate dynamic UDP change
3. Controlled new TCP service

## Expected Behaviour

| Scenario | Expected Result |
|---|---|
| Normal baseline/runtime comparison | LEGITIMATE |
| Temporary UDP port 49000 | LEGITIMATE |
| New TCP service on port 8080 | POTENTIAL COMPROMISE |

## Wireshark Validation

Wireshark is used to compare:

- Legitimate DNS traffic using temporary UDP source ports
- Controlled HTTP traffic using TCP port 8080

The purpose is to provide packet-level context for the Python comparison results.

## Evidence Required

- Normal VM state
- V2 Python comparison script
- Trusted baseline output
- Normal runtime comparison
- UDP 49000 test
- TCP 8080 test
- DNS capture
- UDP Conversations
- TCP 8080 capture
- HTTP traffic
- TCP Conversations
- Protocol Hierarchy
