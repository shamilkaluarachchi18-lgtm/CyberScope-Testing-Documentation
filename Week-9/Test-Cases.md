# Week 9 Test Cases

## TC-09-01 – Normal Runtime Comparison

**Purpose:** Confirm that the trusted Ubuntu VM remains legitimate when stable attributes match the baseline.

**Method:** Run the V2 comparison script with no deliberate modification.

**Expected Result:** `LEGITIMATE`

**Observed Result:** `LEGITIMATE`

**Status:** PASS

---

## TC-09-02 – Dynamic UDP False-Positive Test

**Purpose:** Confirm that a temporary high-numbered UDP port is treated as dynamic information and does not automatically cause a compromise result.

**Controlled Change:** Temporary UDP listener on port `49000`.

**Expected Result:** `LEGITIMATE`

**Observed Result:** `LEGITIMATE`

**Status:** PASS

**Observation:** The new UDP port was displayed in the dynamic UDP section but did not affect the final security decision.

---

## TC-09-03 – New TCP Service Detection

**Purpose:** Confirm that a newly introduced stable TCP listening service is treated as a meaningful network-state change.

**Controlled Change:** Python HTTP server started on TCP port `8080`.

**Expected Result:** `POTENTIAL COMPROMISE`

**Observed Result:** `POTENTIAL COMPROMISE`

**Status:** PASS

**Observation:** The script identified `tcp 0.0.0.0:8080` as a new stable listening port.

---

## TC-09-04 – Legitimate DNS Behaviour Analysis

**Purpose:** Confirm through Wireshark that normal DNS activity can use changing high-numbered UDP source ports.

**Method:** Generate DNS queries and analyse traffic using the `dns` display filter and UDP Conversations.

**Observed Behaviour:** DNS queries used temporary high-numbered UDP source ports while communicating with destination port 53.

**Conclusion:** Dynamic UDP source ports can be part of normal network behaviour.

---

## TC-09-05 – Controlled TCP/HTTP Behaviour Analysis

**Purpose:** Confirm through Wireshark that the new TCP port 8080 service is actively accepting connections and transferring application-layer traffic.

**Method:** Filter traffic using `tcp.port == 8080` and `http`, then review TCP Conversations and Protocol Hierarchy.

**Observed Behaviour:** TCP handshakes, HTTP GET requests, HTTP 200 responses and multiple conversations involving port 8080 were observed.

**Conclusion:** A new listening TCP service with active communication is more security-relevant than short-lived dynamic UDP activity.
