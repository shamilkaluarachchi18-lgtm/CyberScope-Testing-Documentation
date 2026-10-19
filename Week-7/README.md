
# CyberScope Week 7 Testing Documentation

## Week 7 Overview

During Week 7, I focused on applying my Python programming and network analysis learning directly to the CyberScope project.

The main activities completed were:

- Automated network attribute collection using Python
- Collection of network and system information from the Ubuntu VM
- Baseline network traffic capture using Wireshark
- ICMP traffic analysis
- DNS traffic analysis
- HTTP traffic analysis
- Protocol hierarchy analysis

---

## 1. Python Network Attribute Automation

I developed a Python script to automatically collect network-related information from the CyberScope Ubuntu VM.

The script collects:

- Hostname
- Active network interface
- IPv4 address
- MAC address
- Default gateway
- DNS configuration
- Routing information
- Listening ports

The results are also saved to a text file so that the same collection process can be repeated during future testing.

### Purpose

The purpose of this script is to reduce the need to manually run separate Linux commands and provide a consistent method of collecting network attributes.

This can support the CyberScope device-DNA process by providing attribute values that can later be compared with a trusted baseline.

---

## 2. Wireshark Baseline Traffic Analysis

I also captured normal network traffic from the Ubuntu VM using Wireshark on the ens33 interface.

The following network traffic was analysed:

### ICMP

ICMP Echo Requests and Echo Replies were captured between the Ubuntu VM and 8.8.8.8.

### DNS

DNS queries and responses for google.com were captured and analysed.

### HTTP

HTTP communication was captured to observe normal application-layer network activity.

### Protocol Hierarchy

Wireshark Protocol Hierarchy Statistics were used to identify the different protocols present in the capture.

Protocols observed included:

- TCP
- UDP
- DNS
- ICMP
- HTTP
- TLS
- ARP
- NTP

---

## Key Learning

This activity helped me understand that network monitoring should consider both device configuration and network behaviour.

Stable attributes such as MAC address and hostname may be useful for device integrity verification, while network traffic characteristics such as protocols, destinations and DNS activity may provide additional behavioural information.

However, normal network traffic can change depending on device activity. Therefore, network behaviour should be interpreted together with other security-relevant attributes rather than automatically treating every change as a compromise.

---

## Current Status

Week 7 Python automation and baseline Wireshark analysis completed.

The next stage will focus on using the collected baseline information to support structured CyberScope security testing.
