# WEEK 10 – Quantum-Inspired Networking

**Teaching Intent**: This lab explores networking concepts inspired by quantum principles such as no-cloning and state collapse. Messages behave like tokens that can only be read once.

## Overview

This lab introduces **quantum-inspired messaging** where:
- Messages are tokens
- Tokens can only be read once
- Reading changes the state (state collapse)
- Expired tokens become invalid

The system simulates secure, ephemeral communication.

## Learning Outcomes

- Implement one-time-read tokens
- Understand state collapse behavior
- Simulate secure message passing
- Explore conceptual quantum networking

## Key Concepts

| Concept | Description |
|--------|-------------|
| One-Time Read | Token can only be accessed once |
| State Collapse | Reading changes availability |
| No-Cloning | Tokens cannot be duplicated |
| Expiry | Tokens become invalid after time |

## Repository Structure

week10-quantum-network-basic/
├── README.md
├── node.py
├── token.py
├── config.py
└── docs/
└── run_instructions.md


## Quick Start

Run 3 nodes:

Terminal 1:

python node.py 11000 11001 11002


Terminal 2:

python node.py 11001 11000 11002


Terminal 3:

python node.py 11002 11000 11001


## How It Works


Create token
↓
Send to peer
↓
Peer reads token
↓
Token becomes invalid


## Week Comparison

| Week | Concept |
|------|--------|
| Week 7 | Store |
| Week 8 | Opportunistic |
| Week 9 | Learning |
| Week 10 | State-based |

## Key Takeaway

> Messages can be treated as ephemeral tokens that disappear after use, enabling secure and m