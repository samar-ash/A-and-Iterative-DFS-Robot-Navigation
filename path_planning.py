class Path:
    def __init__(self, file_name):
        self.file_name = file_name
        self.read_file()
        self.close_list = set()

    def read_file(self):
        file = open('worlds/' + self.file_name, 'r')
        state = {"robot_location": [], "samples_location": []}
        lines = file.readlines()
        gridsize = [int(lines[0]), int(lines[1])]

        count = -2
        blocks_location = []
        for line in lines:
            count += 1
            robot_index = line.rfind('@')
            if robot_index != -1:
                state['robot_location'].append([count, robot_index])
            for char_idx in range(len(line)):
                if line[char_idx] == '*':
                    sample_index = line.rfind('*')
                    state['samples_location'].append([count, sample_index])
                elif line[char_idx] == '#':
                    block_index = char_idx
                    blocks_location.append([count, block_index])

        return state, blocks_location, gridsize

    def solve(self, state, algorithm, max_param=1):
        iteration = 0

        node = Node(state, None, None)
        if algorithm == "dfs":
            open_list = OpenList()
        else:
            open_list = Queue()
            if algorithm == "A*":
                heuristic_approach=int(input("What heuristic approach you would like to try?0,1,2=>\n"
                                "0 means heuristic=0\n"
                                "1 means load the first heuristic approach\n"
                                "2 means second heauritsic approach\n"
                                 "and 3 means second heauritsic approach\n"))
            else:
                heuristic_approach=0
        close_list = OpenList()
        open_list.add(node)

        i = 0
        count = 1
        while True:
            i += 1
            iteration += 1
            if open_list.empty():
                raise Exception("no solution")
            node = open_list.remove()
            if node.goal(node.state):
                final_actions = []
                while node.parent is not None:
                    final_actions.append(node.actions)
                    node = node.parent
                final_actions.reverse()
                print("The expanded nodes are:", (close_list.show()), "and The generated nodes are", count)
                return final_actions
            if algorithm == "dfs" and (iteration > max_param):
                raise Exception("You Reached the maximum depth")

            neighbor_action = ["U", "D", "L", "R", "S"]
            for move in neighbor_action:
                g_commulative = node.g_cost
                result=node.update_state(algorithm,node.state, move, gridsize,blocks_location,g_commulative,heuristic_approach)
                g_commulative=result[0]
                heuristic=result[1]
                new_state = result[2]
                if new_state != 0 and not open_list.contain_state(new_state) and not close_list.contain_state(
                        new_state):
                    child = Node(new_state, node, move,g_commulative,heuristic)
                    open_list.add(child)

                    count += 1

            print(move, open_list.show())
            close_list.add(node)


class Node:
    def __init__(self, state, parent, actions, g_cost=0,heuristic=0):
        self.state = state
        self.parent = parent
        self.actions = actions
        self.g_cost = g_cost
        self.heuristic = heuristic

    def goal(self, state):
        if len(state["samples_location"]) == 0:
            return True

    def update_state(self, algorithm,state, action, gridsize,blocks_location, g_cost=0,heuristic=0):
        flag = 0
        g_cost += 1
        robot_x_cordinate = int(state['robot_location'][0][0])
        robot_y_cordinate = int(state['robot_location'][0][1])
        if algorithm == "A*" and heuristic!=0:
            if heuristic == 1:
                heuristic = abs(robot_x_cordinate - state['samples_location'][0][0]) + (
                    abs(robot_y_cordinate - state['samples_location'][0][1]))
            elif heuristic == 2 or heuristic == 3:
                from scipy.spatial import distance
                coords = state['samples_location']
                if heuristic==2:
                    robot_agent=state['robot_location']
                    dists = distance.cdist(coords, robot_agent, 'cityblock')
                if heuristic == 3:
                    dists = distance.cdist(coords, coords, 'cityblock')
                import numpy as np
                heuristic=np.max(dists)

        if action == "U":
            if ((robot_x_cordinate - 1) >= 1) and (
                    [robot_x_cordinate - 1, robot_y_cordinate] not in blocks_location):
                robot_x_cordinate -= 1
                action = "U"
                flag = 1
        elif action == "D":
            if (robot_x_cordinate + 1) <= gridsize[0] and (
                    [robot_x_cordinate + 1, robot_y_cordinate] not in blocks_location):
                robot_x_cordinate += 1
                action = "D"
                flag = 1

        elif action == "L":
            if (robot_y_cordinate - 1) >= 1 and ([robot_x_cordinate, robot_y_cordinate - 1] not in blocks_location):
                robot_y_cordinate -= 1
                action = "L"
                flag = 1
        elif action == "R":
            if (robot_y_cordinate + 1) <= gridsize[1] and (
                    [robot_x_cordinate, robot_y_cordinate + 1] not in blocks_location):
                robot_y_cordinate += 1
                action = "R"
                flag = 1
        elif action == "S":
            if state['robot_location'][0] in state['samples_location']:
                flag = 1
                action = "S"
        if flag == 1:
            new_state = {"robot_location": [[robot_x_cordinate, robot_y_cordinate]],
                         "samples_location": state['samples_location']}
            if action == "S" and state['robot_location'][0] in state['samples_location']:
                new_state['samples_location'] = [x for x in new_state['samples_location'] if
                                                 x != state['robot_location'][0]]
                return [g_cost,heuristic,new_state]

            return [g_cost,heuristic,new_state]

        else:
            return [g_cost,heuristic,0]


class OpenList:
    def __init__(self):
        self.open_list = []

    def add(self, node):
        self.open_list.append(node)

    def contain_state(self, state):
        for node in self.open_list:
            if node.state == state:
                return True
        return False

    def empty(self):
        return len(self.open_list) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty open_list")
        else:

            node = self.open_list[-1]
            self.open_list = self.open_list[:-1]
            return node

    def show(self):
        j = 0
        for node in self.open_list:
            j += 1
            print(j,node.actions, node, node.parent,node.g_cost,node.heuristic,node.g_cost+node.heuristic)
        return j


class Queue(OpenList):
    def __init__(self):
        super().__init__()

    def remove(self):
        if self.empty():
            raise Exception("empty open_list")

        min = self.open_list[0].heuristic+self.open_list[0].g_cost
        node_min=self.open_list[0]
        for node in self.open_list:
            if node.heuristic + node.g_cost < min:
                min = node.heuristic + node.g_cost
                node_min = node
        self.open_list.remove(node_min)
        return node_min


path_planning = Path("small1.txt")
state, blocks_location, gridsize = path_planning.read_file()
print("blocks locations:", blocks_location)
print("size of a world:", gridsize)
print(path_planning.solve(state, algorithm="A*", max_param=1000
                          ))
