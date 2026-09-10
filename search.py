import heapq
import sys
from maze import Node, StackFrontier, QueueFrontier, Maze


class SearchNode:
    def __init__(self, state, parent=None, action=None, cost=0, depth=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.cost = cost
        self.depth = depth

    def __lt__(self, other):
        return self.cost < other.cost


class PriorityQueueFrontier:
    def __init__(self):
        self.frontier = []
        self.counter = 0

    def add(self, node):
        entry = (node.cost, self.counter, node)
        self.counter += 1
        heapq.heappush(self.frontier, entry)

    def contains_state(self, state):
        return any(node.state == state for _, _, node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            _, _, node = heapq.heappop(self.frontier)
            return node


class SearchMaze(Maze):

    def solve_uniform_cost(self):
        """Finds optimal cost solution using Uniform Cost Search."""
        self.num_explored = 0
        start = SearchNode(state=self.start, parent=None, action=None, cost=0, depth=0)
        frontier = PriorityQueueFrontier()
        frontier.add(start)
        self.explored = set()

        while True:
            if frontier.empty():
                raise Exception("no solution")

            node = frontier.remove()

            if node.state in self.explored:
                continue

            self.num_explored += 1
            self.explored.add(node.state)

            if node.state == self.goal:
                actions = []
                cells = []
                curr = node
                while curr.parent is not None:
                    actions.append(curr.action)
                    cells.append(curr.state)
                    curr = curr.parent
                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                self.total_cost = node.cost
                return

            for action, state in self.neighbors(node.state):
                if state not in self.explored:
                    step_cost = self.get_cost(state)
                    child = SearchNode(
                        state=state,
                        parent=node,
                        action=action,
                        cost=node.cost + step_cost,
                        depth=node.depth + 1
                    )
                    frontier.add(child)

    solve_ucs = solve_uniform_cost

    def solve_limited_depth(self, limit):
        """Finds a solution using Depth-Limited Search up to the given limit."""
        self.num_explored = 0
        start = SearchNode(state=self.start, parent=None, action=None, cost=0, depth=0)
        frontier = StackFrontier()
        frontier.add(start)

        explored_depths = {self.start: 0}
        self.explored = set()
        cutoff_occurred = False

        while True:
            if frontier.empty():
                if cutoff_occurred:
                    raise Exception("cutoff")
                else:
                    raise Exception("no solution")

            node = frontier.remove()
            self.num_explored += 1
            self.explored.add(node.state)

            if node.state == self.goal:
                actions = []
                cells = []
                curr = node
                while curr.parent is not None:
                    actions.append(curr.action)
                    cells.append(curr.state)
                    curr = curr.parent
                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                self.total_cost = node.cost
                return

            if node.depth < limit:
                for action, state in self.neighbors(node.state):
                    next_depth = node.depth + 1
                    if state not in explored_depths or next_depth < explored_depths[state]:
                        explored_depths[state] = next_depth
                        step_cost = self.get_cost(state)
                        child = SearchNode(
                            state=state,
                            parent=node,
                            action=action,
                            cost=node.cost + step_cost,
                            depth=next_depth
                        )
                        frontier.add(child)
            else:
                cutoff_occurred = True

    solve_dls = solve_limited_depth

    def solve_iterative_deepening(self, max_limit=None):
        """Finds a solution using Iterative Deepening Search."""
        total_explored = 0
        limit = 0
        all_explored = set()

        if max_limit is None:
            max_limit = self.height * self.width

        while limit <= max_limit:
            try:
                self.solve_limited_depth(limit)
                total_explored += self.num_explored
                all_explored.update(self.explored)
                self.num_explored = total_explored
                self.explored = all_explored
                return
            except Exception as e:
                if str(e) == "cutoff":
                    total_explored += self.num_explored
                    all_explored.update(self.explored)
                    limit += 1
                elif str(e) == "no solution":
                    total_explored += self.num_explored
                    all_explored.update(self.explored)
                    self.num_explored = total_explored
                    self.explored = all_explored
                    raise Exception("no solution")
                else:
                    raise e

        raise Exception("no solution")

    solve_ids = solve_iterative_deepening

    def solve(self, algorithm="ucs", limit=10):
        """Generic solve method accepting algorithm name."""
        algo = algorithm.lower()
        if algo in ("ucs", "uniform_cost", "uniform cost"):
            return self.solve_uniform_cost()
        elif algo in ("dls", "limited_depth", "limited depth"):
            return self.solve_limited_depth(limit)
        elif algo in ("ids", "iterative_deepening", "iterative deepening"):
            return self.solve_iterative_deepening()
        else:
            raise ValueError(f"Unknown search algorithm: {algorithm}")


def uniform_cost_search(maze_file):
    m = SearchMaze(maze_file)
    m.solve_uniform_cost()
    return m


def limited_depth_search(maze_file, limit):
    m = SearchMaze(maze_file)
    m.solve_limited_depth(limit)
    return m


def iterative_deepening_search(maze_file, max_limit=None):
    m = SearchMaze(maze_file)
    m.solve_iterative_deepening(max_limit)
    return m


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage: python search.py maze.txt [algorithm] [limit]")

    maze_file = sys.argv[1]
    algo = sys.argv[2].lower() if len(sys.argv) > 2 else "all"
    limit_arg = int(sys.argv[3]) if len(sys.argv) > 3 else 20

    m = SearchMaze(maze_file)
    print("Maze:")
    m.print()

    algorithms = []
    if algo == "all":
        algorithms = [("Uniform Cost Search", "ucs"), ("Limited Depth Search (limit=" + str(limit_arg) + ")", "dls"), ("Iterative Deepening Search", "ids")]
    elif algo in ("ucs", "uniform_cost", "uniform cost"):
        algorithms = [("Uniform Cost Search", "ucs")]
    elif algo in ("dls", "limited_depth", "limited depth"):
        algorithms = [(f"Limited Depth Search (limit={limit_arg})", "dls")]
    elif algo in ("ids", "iterative_deepening", "iterative deepening"):
        algorithms = [("Iterative Deepening Search", "ids")]
    else:
        sys.exit(f"Unknown algorithm: {algo}")

    for name, key in algorithms:
        print(f"=== Solving with {name} ===")
        search_maze = SearchMaze(maze_file)
        try:
            if key == "ucs":
                search_maze.solve_uniform_cost()
            elif key == "dls":
                search_maze.solve_limited_depth(limit_arg)
            elif key == "ids":
                search_maze.solve_iterative_deepening()

            print("States Explored:", search_maze.num_explored)
            print("Total Path Cost:", getattr(search_maze, "total_cost", "N/A"))
            print("Solution Path Length:", len(search_maze.solution[1]))
            print("Solution:")
            search_maze.print()
            img_filename = f"maze_{key}.png"
            search_maze.output_image(img_filename, show_explored=True)
            print(f"Saved visualization to {img_filename}\n")
        except Exception as e:
            print(f"Failed to solve: {e}\n")
