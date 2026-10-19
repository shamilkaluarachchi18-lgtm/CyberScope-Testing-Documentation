# Known Limitations and Future Work

## Current Limitations

### 1. Standalone Validation
The Week 10 Python evidence uses structured JSON datasets and a standalone validator. It demonstrates the detection logic but does not by itself prove that the full Flask/Ganache application was running during those specific tests.

### 2. Limited Test Scenarios
The final Week 10 validation used a small number of controlled scenarios:
- legitimate runtime
- new TCP service
- hostname change
- restored runtime

More scenarios would be needed for broader evaluation.

### 3. Attribute Stability
Some network attributes are dynamic by nature. Temporary UDP ports and similar runtime values may change without malicious activity.

### 4. Thresholding and Weighting
The current testing approach treats selected stable changes as meaningful. A more advanced system could assign different weights or confidence levels to different attribute changes.

## Future Improvements
- Collect multiple trusted baselines over time.
- Classify attributes by stability.
- Add more controlled tampering scenarios.
- Automate test execution and result aggregation.
- Add severity scoring for changed attributes.
- Compare multiple packet-level indicators with Device-DNA results.
- Validate the full integrated application end-to-end under repeated test conditions.
