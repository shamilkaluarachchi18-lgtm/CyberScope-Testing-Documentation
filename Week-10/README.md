# CyberScope Week 10 – Final Technical Documentation

## Overview
Week 10 focused on final validation, final testing evidence, sprint closure, and technical documentation for the CyberScope project.

My individual contribution focused on **network security and testing**. The final Week 10 work validated whether CyberScope-related detection logic could distinguish trusted and modified device/network states and whether packet-level evidence supported those results.

## Final Week 10 Activities
1. **Python-based final validation**
   - Created a trusted device baseline.
   - Generated SHA-256 Device-DNA values.
   - Tested legitimate, network-tampered, hostname-tampered, and restored states.
   - Recorded test outcomes in CSV format.
2. **Final Wireshark validation**
   - Confirmed normal network state before testing.
   - Introduced a controlled TCP service on port 8080.
   - Captured TCP and HTTP traffic.
   - Analysed TCP stream, conversations, and protocol hierarchy.
   - Confirmed that port 8080 was removed after testing.
3. **Agile sprint closure**
   - Updated the final team tracker.
   - Confirmed all planned tasks were complete.
   - Recorded 31 completed tasks and 100% project completion.
4. **Final documentation**
   - Organised test cases, results, evidence, observations, limitations, and final reflection in GitHub.

## Final Result
The Week 10 standalone validation produced four successful test outcomes:
- Legitimate runtime → **LEGITIMATE**
- New TCP port 8080 → **POTENTIAL COMPROMISE**
- Hostname tampering → **POTENTIAL COMPROMISE**
- Restored runtime → **LEGITIMATE**

All four tests matched the expected outcomes.

## Repository Structure
- `Final-Testing-Summary.md`
- `Final-Test-Cases.md`
- `Final-Integration-Outcome.md`
- `Technical-Reflection.md`
- `Known-Limitations-and-Future-Work.md`
- `Evidence-Index.md`
- `results/week10_results_summary.csv`
- `evidence/README.md`

## Note
This Week 10 evidence validates the final security-testing logic using standalone Python test datasets and Wireshark packet captures. It should not be described as proof that the complete Flask/Ganache application was running during these specific tests unless separate evidence shows that full integrated system execution.
