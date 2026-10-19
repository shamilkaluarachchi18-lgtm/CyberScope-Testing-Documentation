# Week 9 Integration Changes

## Purpose

The Week 8 comparison script detected any listening-port difference as a device-state change. During testing, a temporary high-numbered UDP port changed naturally and caused a false-positive result.

Week 9 focused on improving this behaviour before final integration.

## Changes Made

### 1. Stable and Dynamic Port Separation

Listening ports are now separated into:

- **Stable listening ports**
- **Dynamic UDP ports**

Dynamic high-numbered UDP ports are recorded for visibility but do not automatically cause a compromise result.

### 2. CyberScope Internal Ports

The comparison logic includes support for ignoring CyberScope internal service ports:

- `5000` – Flask dashboard
- `8545` – Ganache blockchain

These ports should not be treated as external compromise indicators when they are required by the product itself.

### 3. More Meaningful Runtime Decision

The runtime comparison now treats changes differently:

- Stable attribute change → security-relevant
- New stable TCP listening service → security-relevant
- Temporary dynamic UDP change → informational
- CyberScope internal service port → ignored

## Result

This reduced the false-positive behaviour observed in Week 8 while keeping meaningful changes detectable.

A temporary UDP service on port `49000` remained **LEGITIMATE**, while a new TCP service on port `8080` produced **POTENTIAL COMPROMISE**.

## Product Relevance

This refinement supports the final CyberScope Device-DNA verification process by distinguishing normal network variation from more meaningful configuration changes.
