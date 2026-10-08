# CyberScope Week 9 – Technical Documentation

## Overview

Week 9 focused on refining the CyberScope network-security testing process and reducing false-positive detections before final Week 10 integration and testing.

My work this week focused on two technical areas:

1. Refining the Python baseline-versus-runtime comparison logic.
2. Using Wireshark to compare legitimate dynamic network behaviour with a controlled suspicious TCP service.

The main improvement was separating stable network attributes from dynamic network activity so that harmless temporary UDP changes would not automatically trigger a compromise result.

## Week 9 Objectives

- Refine the CyberScope attribute comparison logic.
- Separate stable listening ports from dynamic UDP ports.
- Ignore CyberScope internal service ports where appropriate.
- Test whether a legitimate temporary UDP change remains classified as legitimate.
- Confirm that a meaningful new TCP service is still detected.
- Use Wireshark to explain why some network changes are more security-relevant than others.
- Record the testing process clearly for team review and Week 10 final testing.

## Key Results

- Normal baseline comparison returned **LEGITIMATE**.
- Temporary UDP port `49000` was treated as dynamic information and still returned **LEGITIMATE**.
- New TCP service on port `8080` was treated as a meaningful stable change and returned **POTENTIAL COMPROMISE**.
- Wireshark showed that DNS traffic used changing temporary UDP source ports during normal activity.
- Wireshark confirmed active TCP and HTTP communication on port `8080`.

## Repository Structure

- `Integration-Changes.md` – summary of the Week 9 logic improvements.
- `Testing-Plan.md` – purpose, method, expected results and evidence requirements.
- `Test-Cases.md` – structured Week 9 test cases.
- `False-Positive-Findings.md` – false-positive issue identified in Week 8 and the Week 9 improvement.
- `Evidence-Index.md` – list of screenshots/evidence to upload.
- `scripts/cyberscope_compare_v2.py` – improved Python comparison script.
- `results/week9_test_results.csv` – summary of Week 9 test results.

## Week 10 Readiness

The Week 9 refinements prepare CyberScope for final Week 10 compromised-device/network testing. The next stage is to validate the integrated product using legitimate and tampered scenarios and confirm final detection results.
