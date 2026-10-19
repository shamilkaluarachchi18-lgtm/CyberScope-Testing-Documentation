# Final Week 10 Test Cases

## TC-10-01 – Legitimate Device Validation
**Purpose:** Confirm that a runtime dataset matching the trusted baseline is classified as legitimate.  
**Input:** `legitimate_runtime.json`  
**Expected Result:** `LEGITIMATE`  
**Observed Result:** `LEGITIMATE`  
**DNA Match:** YES  
**Changed Attributes:** None  
**Status:** PASS

---

## TC-10-02 – Controlled Network Tampering
**Purpose:** Confirm that a newly introduced stable TCP service changes the Device DNA and is detected.  
**Controlled Change:** Added `tcp 0.0.0.0:8080`  
**Input:** `tampered_network.json`  
**Expected Result:** `POTENTIAL COMPROMISE`  
**Observed Result:** `POTENTIAL COMPROMISE`  
**DNA Match:** NO  
**Changed Attribute:** `stable_listening_ports`  
**Status:** PASS

---

## TC-10-03 – Hostname Tampering
**Purpose:** Confirm that a system identity change affects the Device DNA.  
**Controlled Change:** Hostname changed from `crypto` to `cyberscope-tampered`  
**Input:** `tampered_hostname.json`  
**Expected Result:** `POTENTIAL COMPROMISE`  
**Observed Result:** `POTENTIAL COMPROMISE`  
**DNA Match:** NO  
**Changed Attribute:** `hostname`  
**Status:** PASS

---

## TC-10-04 – Restored Trusted State
**Purpose:** Confirm that the device returns to a legitimate state after the controlled changes are removed.  
**Input:** `restored_runtime.json`  
**Expected Result:** `LEGITIMATE`  
**Observed Result:** `LEGITIMATE`  
**DNA Match:** YES  
**Changed Attributes:** None  
**Status:** PASS

---

## TC-10-05 – Packet-Level Validation of Port 8080
**Purpose:** Confirm that the controlled TCP port 8080 change generated observable network activity.  
**Method:** Capture traffic in Wireshark while accessing the temporary HTTP service.  
**Observed Evidence:** TCP handshake, HTTP GET, HTTP 200 OK, TCP stream, TCP conversations, protocol hierarchy.  
**Status:** PASS

---

## TC-10-06 – Network Restoration
**Purpose:** Confirm that the temporary network service is removed after testing.  
**Method:** Stop the Python HTTP server and run `ss -tuln | grep 8080`.  
**Observed Result:** No output  
**Status:** PASS
