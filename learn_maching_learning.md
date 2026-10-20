# Agent-Based Graph Search

A simple Python project demonstrating how an **agent navigates an environment represented as a graph**.

The project connects basic lessons about **trees, graphs, stacks, queues, DFS, and BFS** to a simple AI-style **Agent + Environment** model.

## What This Demonstrates

The program contains three ways of navigating the graph:

1. **Manual Navigation** — the user decides where the agent moves.
2. **Depth-First Search (DFS)** — automatically searches using a stack.
3. **Breadth-First Search (BFS)** — automatically searches using a queue.

The goal is to move from:

```text
Start: (0, 0)
```

to:

```text
Goal: (2, 2)
```

---
Practical Example: Hugging Face Embeddings for State Representation
Below is how you can use Hugging Face transformers to convert state descriptions into embeddings and measure similarity between different positions or goals.

1. Generating Encodings & Embeddings
Python
import torch
from transformers import AutoTokenizer, AutoModel

# Load a pretrained model and tokenizer from Hugging Face Hub
model_name = "sentence-transformers/all-MiniLM-L6-v2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

# Define environmental state descriptions
state_a = "Agent is at grid position (0, 0) near the start"
state_b = "Agent is at grid position (0, 1) adjacent to start"
state_goal = "Agent is at goal position (2, 2)"

# Step 1: Tokenization (Encoding)
inputs = tokenizer([state_a, state_b, state_goal], padding=True, truncation=True, return_tensors="pt")

# Step 2: Forward Pass to extract Embeddings (Latent Space)
with torch.no_grad():
    outputs = model(**inputs)
    # Mean pooling over token embeddings to get state-level embeddings
    embeddings = outputs.last_hidden_state.mean(dim=1)

print("Embedding Shape:", embeddings.shape)  # e.g., torch.Size([3, 384])
2. Semantic/Spatial Vector Search
Once states are represented as dense embeddings, an agent can evaluate similarity to a target goal or find adjacent nodes in vector space using cosine similarity:

Python
import torch.nn.functional as F

# Compute pairwise cosine similarity between states
sim_a_b = F.cosine_similarity(embeddings[0], embeddings[1], dim=0)
sim_a_goal = F.cosine_similarity(embeddings[0], embeddings[2], dim=0)

print(f"Similarity (Start -> Adjacent): {sim_a_b.item():.4f}")
print(f"Similarity (Start -> Goal):     {sim_a_goal.item():.4f}")
The Graph & Classical Search
In the underlying environment, states can still be represented as an adjacency list or mapped directly into vector space:

Python
graph = {
    (0, 0): [(0, 1), (1, 0)],
    (0, 1): [],
    (0, 2): [(0, 1), (1, 2)],
    (1, 0): [(0, 0), (2, 0)],
    (1, 2): [(0, 2), (2, 2)],
    (2, 0): [(1, 0), (2, 1)],
    (2, 1): [(2, 0), (2, 2)],
    (2, 2): []
}
Agent-Environment Loop
Python
class Agent:
    def __init__(self, environment, start):
        self.environment = environment
        self.state = start

    def perceive(self):
        """Asks environment for valid actions from current state."""
        return self.environment.get_actions(self.state)

    def act(self, action):
        """Attempts transition to a new state."""
        self.state = self.environment.transition(self.state, action)

    def goal_test(self):
        """Checks if current state matches target goal."""
        return self.environment.is_goal(self.state)
Search Algorithms: Depth-First Search vs. Breadth-First Search

Classical graph search strategies traverse discrete state spaces using fundamental data structures:


## DFS (Depth-First Search)

Uses a Stack (LIFO) to explore as deep as possible along each path before backtracking.

```python
def dfs(environment, start):
    stack = [start]
    visited = set()

    while stack:
        state = stack.pop()
        if state in visited:
            continue
        visited.add(state)

        if environment.is_goal(state):
            return True

        for next_state in environment.get_actions(state):
            if next_state not in visited:
                stack.append(next_state)
    return False

```

### BFS (Breadth-First Search)

Uses a **Queue (FIFO)** to explore nodes level-by-level, ensuring the shortest path in unweighted graphs.

```python
from collections import deque

def bfs(environment, start):
    queue = deque([start])
    visited = set()

    while queue:
        state = queue.popleft()
        if state in visited:
            continue
        visited.add(state)

        if environment.is_goal(state):
            return True

        for next_state in environment.get_actions(state):
            if next_state not in visited:
                queue.append(next_state)
    return False

```

---

# Key Concepts

| Concept | Purpose |
| --- | --- |
| Node / State | A discrete location or continuous representation in the state space |
| Edge | Connection or valid transition between states |
| Adjacency List | Structural definition of connected graph nodes |
| Agent | Autonomous entity making actions based on perception |
| Environment | Defines transitions, validation, and goal criteria |
| Tokenization / Encoding | Mapping categorical inputs or symbols to numeric IDs |
| Embeddings | Dense vector representations capturing semantic/spatial relationships |
| Hugging Face `transformers` | Library for converting unstructured state observations into latent embeddings |
| Stack (LIFO) | Data structure powering Depth-First Search (DFS) |
| Queue (FIFO) | Data structure powering Breadth-First Search (BFS) |
| `visited` Set | Prevents infinite loops caused by cycles in graph structures |

---

# Learning Progression

```text
Binary Trees & Graphs
          ↓
DFS & BFS (Stacks & Queues)
          ↓
Agent + Environment Architecture
          ↓
Tokenization & Discrete Encodings
          ↓
Dense Latent Embeddings (Hugging Face)
          ↓
Vector-Based Graph Search & Neural Planning

```

---

## Summary

* **DFS** uses a **Stack (LIFO)** to navigate deeply down a single path.
* **BFS** uses a **Queue (FIFO)** to explore outward level-by-level.
* **Encodings** turn raw environmental states into discrete numerical tokens.
* **Embeddings** (via Hugging Face) project states into a continuous vector space where distance corresponds to semantic or spatial similarity, enabling intelligent search and neural agents.
