# False-Positive Findings

## Issue Identified

During Week 8, the original Python comparison logic treated every listening-port difference as a device-state change.

A temporary high-numbered UDP port disappeared between the trusted baseline and runtime collection. This caused the script to report a changed device state even though no deliberate tampering had occurred.

## Why This Matters

Dynamic network values can change during legitimate system operation. If CyberScope treats all of these values as fixed Device-DNA attributes, the system may generate unnecessary false-positive alerts.

## Week 9 Improvement

The comparison logic was refined to:

- Separate stable listening ports from dynamic UDP ports.
- Keep dynamic UDP changes as informational.
- Ignore CyberScope internal service ports where appropriate.
- Continue treating new stable TCP services as security-relevant.

## Validation

### Temporary UDP Port 49000

The UDP port appeared in the dynamic section but the final result remained:

`LEGITIMATE`

### TCP Port 8080

The new stable TCP listener was detected and the final result became:

`POTENTIAL COMPROMISE`

## Conclusion

The Week 9 refinement reduced false-positive behaviour without removing the ability to detect meaningful network-state changes.

This finding should be considered when refining the final Device-DNA integrity logic and evaluation process.
