# README.md (Week 8 – Opportunistic Routing)

```markdown
# WEEK 8 – Opportunistic Routing

**Teaching Intent**: Not all networks have stable paths. In opportunistic networks, nodes forward messages when a good opportunity appears — not when a fixed route exists. Nodes decide forwarding based on delivery probability rather than certainty.

## Overview

This lab introduces **opportunistic routing**. Nodes maintain delivery probabilities for peers and forward messages opportunistically when they encounter a node with a higher probability of delivering the message.

Instead of retrying blindly like store-and-forward, nodes **make probabilistic forwarding decisions**.

Probability becomes the routing table.

## Learning Outcomes

By completing this week, you will:
- ✅ Maintain delivery probability tables
- ✅ Forward packets opportunistically
- ✅ Store messages when delivery not possible
- ✅ Forward only to good candidates
- ✅ Train traits: probabilistic reasoning, adaptive decision-making, opportunistic networking

## Key Concepts

| Concept | Description |
|---------|-------------|
| **Delivery Probability** | Likelihood a peer can deliver a message |
| **Opportunistic Forwarding** | Forward only when a good opportunity appears |
| **Encounter-Based Routing** | Nodes forward when they meet useful peers |
| **Message Queue** | Store messages until forwarding opportunity |
| **Forward Threshold** | Minimum probability required to forward |
| **Adaptive Routing** | Routing decisions change over time |

## Repository Structure

```

week08-opportunistic-routing-basic/
├── README.md
├── node.py
├── delivery_table.py
├── config.py
└── docs/
└── run_instructions.md

```

## Quick Start

### 1. Open Project in VS Code

Open folder:
```

week08-opportunistic-routing-basic

```

### 2. Open Multiple Terminals

In VS Code:
```

Terminal → New Terminal

````

Create **3 terminals** (for 3 nodes).

### 3. Run Multiple Nodes (Same Machine)

Terminal 1:
```bash
python node.py 9000 9001 9002
````

Terminal 2:

```bash
python node.py 9001 9000 9002
```

Terminal 3:

```bash
python node.py 9002 9000 9001
```

Format:

```
python node.py <my_port> <peer1> <peer2>
```

### Expected Output

Terminal 1:

```
[NODE 9000] Listening...
[NODE 9000] Store message for 9001
[NODE 9000] Store message for 9002
```

Terminal 2:

```
[NODE 9001] Listening...
[NODE 9001] Received: Hello from node 9000
```

Terminal 3:

```
[NODE 9002] Listening...
[NODE 9002] Received: Hello from node 9001
```

Messages are forwarded **opportunistically based on probability**.

## Implementation Deep Dive

### Delivery Probability Table (delivery_table.py)

Each node keeps a table:

```
Peer Port → Delivery Probability
```

Example:

```
9001 → 0.7
9002 → 0.3
```

Node will only forward messages to peers with probability above threshold.

```python
class DeliveryTable:
    def __init__(self):
        self.table = {}

    def update_probability(self, peer, prob):
        self.table[peer] = prob

    def get_probability(self, peer):
        return self.table.get(peer, 0.0)

    def get_best_candidates(self, threshold):
        return [peer for peer, prob in self.table.items() if prob >= threshold]
```

### Opportunistic Forwarding Logic

Flow:

```
Message created
    ↓
Try direct send
    ↓
Fail?
    ↓
Store in queue
    ↓
Check probability table
    ↓
Find best candidate
    ↓
Forward to candidate
    ↓
Candidate forwards again later
```

This is **multi-hop probabilistic routing**.

## Opportunistic Routing Flow Diagram

```
Node A has message
    ↓
Cannot reach destination
    ↓
Stores message
    ↓
Encounters Node B
    ↓
Is P(B) > threshold?
        ↓ YES
Forward message to B
        ↓
B repeats process
```

## Contrast with Previous Weeks

| Week   | Routing Type    | Decision               |
| ------ | --------------- | ---------------------- |
| Week 5 | P2P             | Direct                 |
| Week 6 | MANET Flooding  | Broadcast              |
| Week 7 | Store & Forward | Retry later            |
| Week 8 | Opportunistic   | Forward by probability |

## Difference: Store-Forward vs Opportunistic

| Feature      | Store-Forward   | Opportunistic    |
| ------------ | --------------- | ---------------- |
| Retry        | Yes             | Sometimes        |
| Queue        | Yes             | Yes              |
| Decision     | Retry same peer | Choose best peer |
| Routing      | Fixed           | Adaptive         |
| Intelligence | Low             | Higher           |

**Summary**:

* Store-forward = retry later
* Opportunistic = forward smarter

## Testing Scenarios

### Test 1: All Nodes Running

Start all nodes → messages forwarded immediately.

### Test 2: One Node Offline

Stop node 9001 → messages stored in queue.

### Test 3: Node Comes Back Online

Restart node 9001 → queued messages forwarded.

### Test 4: Change Probability

Change probability values:

```
delivery_table.update_probability(peer, 0.2)
delivery_table.update_probability(peer, 0.8)
```

Observe forwarding behavior changes.

## Common Mistakes

| Mistake                  | Problem               |
| ------------------------ | --------------------- |
| Forward to all peers     | Not opportunistic     |
| Ignore probability table | Wrong routing logic   |
| No message queue         | Messages lost         |
| Blocking send            | Node cannot receive   |
| Threshold too high       | No forwarding happens |

## Real-World Applications

| System                 | Use Case                                  |
| ---------------------- | ----------------------------------------- |
| Wildlife Tracking      | Animals exchange sensor data when near    |
| Disaster Networks      | Phones exchange messages without internet |
| Space Networks         | Satellites forward data when in range     |
| Mobile Ad-Hoc Networks | Military communication                    |
| Opportunistic IoT      | Devices sync when nearby                  |

## Extensions

### Extension A: Dynamic Probability Updates

Increase probability when messages successfully delivered.

### Extension B: Message TTL

Messages expire after some time.

### Extension C: Logging

Track:

* Delivery attempts
* Success rate
* Forward count

### Extension D: Encounter Simulation

Nodes randomly meet each other and update probabilities.

## Opportunistic Routing Model Summary

```
No route → Store
Meet good node → Forward
Bad node → Keep
Repeat until delivered
```

## Key Takeaway

> Opportunistic routing does not wait for a perfect path.
> It forwards messages when opportunity appears.

This is how networks work when:

* Nodes move
* Links unstable
* Paths unknown
* Connectivity intermittent

**Probability replaces routing tables.**

---

**Status**: Implemented
**Previous**: Week 7 – Store-and-Forward
**Next**: Week 9 – Bio-Inspired Routing

```

---

## สรุป Week 7 → Week 8 (เข้าใจภาพรวม)
อันนี้สำคัญมาก ถ้าเรียนต่อเนื่อง

| Week | แนวคิด |
|------|--------|
| Week 6 | Flooding |
| Week 7 | Store & Forward |
| Week 8 | Opportunistic Routing |
| Week 9 | Bio-inspired Routing |
| Week 10 | Reinforcement Routing |

Flow ของทั้งวิชา:
```

Direct Send
→ Flooding
→ Store & Forward
→ Opportunistic
→ Adaptive
→ Intelligent Routing

```

---

ถ้าจะทำ **run_instructions.md** ด้วย เดี๋ยวเขียนให้ต่อได้เลย.
```
