"""
Agent-Based Graph Search
Manual Navigation, Depth-First Search (DFS), and Breadth-First Search (BFS)

This program demonstrates:
1. An Agent interacting with an Environment.
2. A graph represented using an adjacency list.
3. Manual navigation through the graph.
4. Depth-First Search (DFS) using a stack.
5. Breadth-First Search (BFS) using a queue.

Connection to tree lessons:
DFS and BFS can be used to traverse both trees and graphs.
Graphs require extra care because nodes can connect back to previously
visited nodes, which is why we maintain a "visited" set.
"""

from collections import deque


# ============================================================
# AGENT
# ============================================================

class Agent:
    """
    Represents an agent moving through an environment.

    The agent knows:
    - its environment
    - its current state

    The agent can:
    - perceive available actions
    - perform an action
    - check whether it reached the goal
    """

    def __init__(self, environment, start):
        self.environment = environment
        self.state = start

    def perceive(self):
        """
        Ask the environment which states can be reached
        from the agent's current state.
        """
        return self.environment.get_actions(self.state)

    def act(self, action):
        """
        Attempt to move to another state.

        The Environment decides whether the move is valid.
        """
        self.state = self.environment.transition(
            self.state,
            action
        )

    def goal_test(self):
        """
        Check whether the current state is the goal.
        """
        return self.environment.is_goal(self.state)


# ============================================================
# ENVIRONMENT
# ============================================================

class Environment:
    """
    Represents the world the agent moves through.

    graph:
        Describes which states are connected.

    goal:
        The state the agent is trying to reach.
    """

    def __init__(self, graph, goal):
        self.graph = graph
        self.goal = goal

    def get_actions(self, state):
        """
        Return all neighboring states that can be reached
        from the given state.

        If the state doesn't exist, return an empty list.
        """
        return self.graph.get(state, [])

    def transition(self, state, action):
        """
        Attempt to move from 'state' to 'action'.

        The move fails if:
        1. The requested state isn't a neighbor.
        2. The requested state is considered blocked.

        Otherwise, return the new state.
        """

        # Is the requested move actually connected
        # to our current position?
        if action not in self.graph.get(state, []):
            print("Invalid action. Staying in the same state.")
            return state

        # A node with no outgoing connections is treated
        # as blocked, unless that node is the goal.
        if self.graph.get(action, []) == [] and action != self.goal:
            print("Blocked cell. Staying in the same state.")
            return state

        # Valid move
        return action

    def is_goal(self, state):
        """
        Return True if the supplied state is the goal.
        """
        return state == self.goal


# ============================================================
# GRAPH
# ============================================================

"""
The graph is represented using an ADJACENCY LIST.

Example:

    (0,0): [(0,1), (1,0)]

means:

    From (0,0), you can move to:
        (0,1)
        (1,0)

Unlike a tree, a graph can contain connections that lead
back to nodes we've already visited.

For example:

    (0,0) -> (1,0)
    (1,0) -> (0,0)

This is why DFS and BFS need a "visited" set.
"""

graph = {
    (0, 0): [(0, 1), (1, 0)],
    (0, 1): [],

    (0, 2): [(0, 1), (1, 2)],

    (1, 0): [(0, 0), (2, 0)],
    (1, 2): [(0, 2), (2, 2)],

    (2, 0): [(1, 0), (2, 1)],
    (2, 1): [(2, 0), (2, 2)],

    (2, 2): []  # Goal
}


# ============================================================
# CREATE THE ENVIRONMENT AND AGENT
# ============================================================

# Create the environment.
# The goal is position (2,2).
env = Environment(
    graph=graph,
    goal=(2, 2)
)

# Create an agent starting at (0,0).
agent = Agent(
    environment=env,
    start=(0, 0)
)


# ============================================================
# MANUAL NAVIGATION
# ============================================================

def manual_navigation(agent):
    """
    Allow the USER to control the agent manually.

    This demonstrates the basic:

        PERCEIVE
            ↓
        CHOOSE ACTION
            ↓
        ACT
            ↓
        CHECK GOAL

    cycle.
    """

    print("\n--- Manual Navigation ---")
    print("Starting at:", agent.state)

    while not agent.goal_test():

        # PERCEIVE:
        # Ask the environment what moves are available.
        actions = agent.perceive()

        print("\nAvailable actions:", actions)

        # USER DECISION:
        # Ask the user where the agent should move.
        #
        # Example input:
        # (1, 0)
        choice = eval(input("Choose next state: "))

        # ACT:
        # Attempt the requested movement.
        agent.act(choice)

        print("Current state:", agent.state)

    print("\nGoal reached!")


# ============================================================
# DEPTH-FIRST SEARCH (DFS)
# ============================================================

def dfs(environment, start):
    """
    Depth-First Search

    DFS explores one path as deeply as possible
    before trying another path.

    DFS uses a STACK.

    Stack behavior:

        Last In, First Out
        LIFO

    Example:

        stack = [A, B, C]

        pop() removes C first.
    """

    # The stack contains states that still need
    # to be explored.
    stack = [start]

    # Keep track of states we've already explored.
    #
    # This is especially important with graphs because
    # graphs can contain cycles.
    visited = set()

    print("\n--- Depth-First Search ---")

    while stack:

        # Remove the LAST state added.
        #
        # This gives us LIFO behavior.
        state = stack.pop()

        # Ignore states we've already processed.
        if state in visited:
            continue

        print("Visiting:", state)

        # Mark this state as explored.
        visited.add(state)

        # Check if we've found the goal.
        if environment.is_goal(state):
            print("Goal found!")
            return True

        # Look at neighboring states.
        for neighbor in environment.get_actions(state):

            # Add unvisited neighbors to the stack.
            if neighbor not in visited:
                stack.append(neighbor)

    # If the stack becomes empty, there are no
    # remaining states to search.
    print("Goal not found.")
    return False


# ============================================================
# BREADTH-FIRST SEARCH (BFS)
# ============================================================

def bfs(environment, start):
    """
    Breadth-First Search

    BFS explores nodes level-by-level.

    It first explores everything one step away,
    then everything two steps away,
    then everything three steps away, etc.

    BFS uses a QUEUE.

    Queue behavior:

        First In, First Out
        FIFO

    We use deque because popleft() efficiently removes
    an item from the front of the queue.
    """

    # Create a queue containing the starting state.
    queue = deque([start])

    # Keep track of states we've already explored.
    visited = set()

    print("\n--- Breadth-First Search ---")

    while queue:

        # Remove the FIRST state added.
        #
        # This gives us FIFO behavior.
        state = queue.popleft()

        # Ignore states we've already processed.
        if state in visited:
            continue

        print("Visiting:", state)

        # Mark the state as explored.
        visited.add(state)

        # Check whether we've reached the goal.
        if environment.is_goal(state):
            print("Goal found!")
            return True

        # Examine neighboring states.
        for neighbor in environment.get_actions(state):

            # Add unvisited neighbors to the END
            # of the queue.
            if neighbor not in visited:
                queue.append(neighbor)

    print("Goal not found.")
    return False


# ============================================================
# RUN THE PROGRAM
# ============================================================

# OPTION 1:
# Let the user manually control the agent.
manual_navigation(agent)


# OPTION 2:
# Run Depth-First Search automatically.
#
# Uncomment this and comment out manual_navigation(agent)
# if you want to test DFS.
#
# dfs(env, (0, 0))


# OPTION 3:
# Run Breadth-First Search automatically.
#
# Uncomment this and comment out manual_navigation(agent)
# if you want to test BFS.
#
# bfs(env, (0, 0))
