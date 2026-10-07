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

# Core Idea

The program separates the **Agent** from the **Environment**.

```text
Agent
  │
  │ perceive()
  ▼
Environment
  │
  │ available actions
  ▼
Agent chooses an action
  │
  │ act()
  ▼
Environment performs transition
  │
  ▼
New State
```

The agent does not directly control the graph.

Instead, it asks the environment what actions are available and asks the environment to perform movements.

---

# The Graph

The environment is represented using an **adjacency list**:

```python
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
```

Each key represents a **state/node**.

Its value contains the states that can be reached from that node.

For example:

```python
(0, 0): [(0, 1), (1, 0)]
```

means:

```text
          (0,1)
            ↑
            |
          (0,0)
            |
            ↓
          (1,0)
```

From `(0,0)`, the agent can attempt to move to `(0,1)` or `(1,0)`.

---

# Agent

The `Agent` represents something that can move through the environment.

```python
class Agent:
    def __init__(self, environment, start):
        self.environment = environment
        self.state = start
```

The agent remembers two things:

```text
environment → the world it is interacting with
state       → its current position
```

It has three main operations.

### Perceive

```python
agent.perceive()
```

Asks:

> What actions can I perform from my current state?

Internally:

```python
return self.environment.get_actions(self.state)
```

### Act

```python
agent.act(action)
```

Attempts to move somewhere.

The environment decides whether that movement is valid.

### Goal Test

```python
agent.goal_test()
```

Checks whether the agent has reached the goal.

---

# Environment

The `Environment` contains the rules of the world.

```python
class Environment:
    def __init__(self, graph, goal):
        self.graph = graph
        self.goal = goal
```

It knows:

```text
graph → where movement is possible
goal  → where the agent is trying to go
```

The environment handles movement through:

```python
transition(state, action)
```

A movement can be rejected if the requested destination is not connected to the current state.

The program also treats a node with no outgoing connections as blocked unless that node is the goal.

---

# Manual Navigation

The first version lets the human perform the search.

```python
manual_navigation(agent)
```

The loop follows:

```text
PERCEIVE
   ↓
SEE AVAILABLE ACTIONS
   ↓
CHOOSE ACTION
   ↓
ACT
   ↓
NEW STATE
   ↓
GOAL?
   │
   └── No → Repeat
```

Example:

```text
Starting at: (0, 0)

Available actions: [(0, 1), (1, 0)]
Choose next state: (1, 0)

Current state: (1, 0)
```

In this mode, **the human is effectively the search algorithm**.

DFS and BFS replace that human decision-making with an algorithm.

---

# Connection to Binary Trees

DFS and BFS are often introduced using **binary trees**.

For example:

```text
        A
       / \
      B   C
     / \ / \
    D  E F  G
```

A binary tree is useful for learning traversal because every node has at most two children.

However, DFS and BFS are not limited to binary trees.

They can also search **graphs**.

```text
Tree Traversal
      ↓
 DFS / BFS
      ↓
Graph Traversal
      ↓
Path Finding
      ↓
Agent Search
```

The major difference is that graphs can contain cycles.

For example:

```text
A → B
↑   ↓
└── C
```

Without remembering visited nodes, an algorithm could repeatedly visit:

```text
A → B → C → A → B → C → ...
```

This is why both search functions use:

```python
visited = set()
```

---

# Depth-First Search (DFS)

DFS searches **deep into one path before trying another**.

It uses a:

```text
STACK
```

A stack follows:

```text
LIFO
Last In, First Out
```

Example:

```text
Stack:

[A]
[A, B]
[A, B, C]

pop()

C ← removed first
```

In Python:

```python
stack = [start]

state = stack.pop()
```

For a tree such as:

```text
        A
       / \
      B   C
     / \
    D   E
```

DFS might visit:

```text
A → B → D → E → C
```

It goes deep into a branch before returning to explore another branch.

Conceptually:

```text
DFS
 ↓
Stack
 ↓
LIFO
 ↓
Go deep first
```

---

# Breadth-First Search (BFS)

BFS searches **level by level**.

It uses a:

```text
QUEUE
```

A queue follows:

```text
FIFO
First In, First Out
```

For example:

```text
Queue:

[A, B, C]

remove first

A ← removed

[B, C]
```

The project uses Python's `deque`:

```python
from collections import deque
```

The queue starts with:

```python
queue = deque([start])
```

The first element is removed using:

```python
state = queue.popleft()
```

For:

```text
            A
          /   \
         B     C
        / \   / \
       D   E F   G
```

BFS visits:

```text
A
B C
D E F G
```

Conceptually:

```text
BFS
 ↓
Queue
 ↓
FIFO
 ↓
Search level-by-level
```

---

# DFS vs BFS

The easiest way to remember the difference is:

```text
             GRAPH SEARCH
                  │
          ┌───────┴───────┐
          │               │
         DFS             BFS
          │               │
        Stack           Queue
          │               │
        LIFO             FIFO
          │               │
     Deep first      Level-by-level
```

DFS asks:

> What happens if I keep following this path?

BFS asks:

> What can I reach in one step? Then two steps? Then three?

---

# Running the Program

Run the Python file:

```bash
python main.py
```

By default:

```python
manual_navigation(agent)
```

runs the interactive version.

Enter coordinates such as:

```text
(1, 0)
```

A possible route to the goal is:

```text
(0,0)
  ↓
(1,0)
  ↓
(2,0)
  ↓
(2,1)
  ↓
(2,2)
```

---

# Running DFS

Comment out:

```python
manual_navigation(agent)
```

and enable:

```python
dfs(env, (0, 0))
```

The algorithm will automatically traverse the graph looking for `(2,2)`.

---

# Running BFS

Comment out manual navigation and enable:

```python
bfs(env, (0, 0))
```

BFS will automatically explore the graph level-by-level until it finds the goal.

---

# Key Concepts

The important concepts demonstrated by this project are:

| Concept | Purpose |
|---|---|
| Node / State | A location in the graph |
| Edge | Connection between states |
| Adjacency List | Stores which nodes are connected |
| Agent | Entity navigating the environment |
| Environment | Contains the graph and movement rules |
| Goal Test | Determines whether the destination was reached |
| Stack | Data structure used by DFS |
| Queue | Data structure used by BFS |
| `visited` | Prevents repeatedly exploring nodes |
| DFS | Searches deeply through paths |
| BFS | Searches outward level-by-level |

---

# Learning Progression

This example connects several data-structure and AI concepts:

```text
Binary Trees
     ↓
Tree Traversal
     ↓
Stacks and Queues
     ↓
DFS and BFS
     ↓
Graphs
     ↓
Graph Search
     ↓
State-Space Search
     ↓
Agent + Environment
```

The important realization is that **DFS and BFS are not just binary-tree exercises**.

They are general search techniques.

A tree gives you a simple structure for learning them. A graph makes the problem more realistic. An agent then uses those search concepts to determine how to navigate through an environment.

---

## Summary

Remember these two rules:

```text
DFS = Stack = LIFO = Deep First

BFS = Queue = FIFO = Level First
```

And for graphs:

```text
Always consider visited nodes.
```

That prevents the search algorithm from getting trapped repeatedly traversing cycles in the graph.
