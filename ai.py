from __future__ import absolute_import, division, print_function
import copy, random
from game import Game
import statistics


MOVES = {0: 'up', 1: 'left', 2: 'down', 3: 'right'}
MAX_PLAYER, CHANCE_PLAYER = 0, 1

# Tree node. To be used to construct a game tree.
class Node:
    # Recommended: do not modifying this __init__ function
    def __init__(self, state, current_depth, player_type):
        self.state = (copy.deepcopy(state[0]), state[1])

        # to store a list of (direction, node) tuples
        self.children = []

        self.depth = current_depth
        self.player_type = player_type
        self.move_action = 4

    # returns whether this is a terminal state (i.e., no children)
    def is_terminal(self):
        #TODO: complete this
        if len(self.children) == 0:
            return True
        else:
            return False


# AI agent. To be used do determine a promising next move.
class AI:
    # Recommended: do not modifying this __init__ function
    def __init__(self, root_state, depth):
        self.root = Node(root_state, 0, MAX_PLAYER)
        self.depth = depth
        self.simulator = Game()
        self.simulator.board_size = len(root_state[0])

    # recursive function to build a game tree
    def build_tree(self, node=None):
        if node == None:
            node = self.root

        if node.depth == self.depth:
            return

        if node.player_type == MAX_PLAYER:
            # TODO: find all children resulting from
            # all possible moves (ignore "no-op" moves)

            # NOTE: the following calls may be useful:
            # self.simulator.reset(*(node.state))
            # self.simulator.get_state()
            # self.simulator.move(direction)
            #pass
            for direct in range(0,4):
                state = (copy.deepcopy(node.state[0]), node.state[1])
                if self.simulator.get_state() == state:
                    if self.simulator.move(direct):
                        new_state = self.simulator.get_state()
                        n = Node(new_state, node.depth+1,CHANCE_PLAYER)
                        self.build_tree(n)
                        n.move_action = direct
                        node.children.append(n)
                else:
                   self.simulator.reset(copy.deepcopy(node.state[0]), node.state[1])
                   if self.simulator.move(direct):
                       new_state = self.simulator.get_state()
                       n = Node(new_state, node.depth+1,CHANCE_PLAYER)
                       self.build_tree(n)
                       n.move_action = direct
                       node.children.append(n)

        elif node.player_type == CHANCE_PLAYER:
            # TODO: find all children resulting from
            # all possible placements of '2's
            # NOTE: the following calls may be useful
            # (in addition to those mentioned above):
            # self.simulator.get_open_tiles():
            emptyspace = self.simulator.get_open_tiles()
            state = (copy.deepcopy(node.state[0]), node.state[1])
            for tile in emptyspace:
                if self.simulator.get_state() == state:
                    self.simulator.tile_matrix[tile[0]][tile[1]] = 2
                    new_state = self.simulator.get_state()
                    n = Node(new_state, node.depth+1,MAX_PLAYER)
                    self.build_tree(n)
                    node.children.append(n)
                else:
                    self.simulator.reset(copy.deepcopy(node.state[0]), node.state[1])
                    self.simulator.tile_matrix[tile[0]][tile[1]] = 2
                    new_state = self.simulator.get_state()
                    n = Node(new_state, node.depth+1,MAX_PLAYER)
                    self.build_tree(n)
                    node.children.append(n)
        # TODO: build a tree for each child of this node

    # expectimax implementation;
    # returns a (best direction, best value) tuple if node is a MAX_PLAYER
    # and a (None, expected best value) tuple if node is a CHANCE_PLAYER
    def expectimax(self, node = None):
        # TODO: delete this random choice but make sure the return type of the function is the same
        #return random.randint(0, 3), 0

        if node == None:
            node = self.root

        if node.is_terminal():
            # TO1DO: base case
            return node.move_action, node.state[1]

        elif node.player_type == MAX_PLAYER:
            # TODO: MAX_PLAYER logic
            #pass
            value = float('-inf')
            action = None
            for n in node.children:
                act, val = self.expectimax(n)
                if val > value:
                    action = n.move_action
                    value = val
            return action, value

        elif node.player_type == CHANCE_PLAYER:
            # TODO: CHANCE_PLAYER logic
            value = 0
            for n in node.children:
                act, val = self.expectimax(n)
                value = value + val/len(node.children)
            return None,value

    def Monte_Carlo(self, node= None):
        state = (copy.deepcopy(node.state[0]), node.state[1])
        avg =[]
        for direct in range(0,4):
            for i in range(0,10):
                if self.simulator.get_state() != state:
                    self.simulator.reset(copy.deepcopy(node.state[0]), node.state[1])
                if self.simulator.move(direct):
                    rand_direct = random.randint(0,4)
                    while self.simulator.move(rand_direct):
                        rand_direct = random.randint(0,4)
                        self.simulator.place_random_tile()
                    new_state = self.simulator.get_state()
                    avg.append(new_state[1])
                else:
                    avg.append(0)
        print(avg)
        return avg.index(max(avg))

    def build_tree_ec(self, node=None):
        if node == None:
            node = self.root

        if node.depth == self.depth:
            node.move_action = Monte_carlo(node)
            return

        if node.player_type == MAX_PLAYER:
            # TODO: find all children resulting from
            # all possible moves (ignore "no-op" moves)

            # NOTE: the following calls may be useful:
            # self.simulator.reset(*(node.state))
            # self.simulator.get_state()
            # self.simulator.move(direction)
            #pass
            for direct in range(0,4):
                state = (copy.deepcopy(node.state[0]), node.state[1])
                if self.simulator.get_state() == state:
                    if self.simulator.move(direct):
                        new_state = self.simulator.get_state()
                        n = Node(new_state, node.depth+1,CHANCE_PLAYER)
                        self.build_tree(n)
                        n.move_action = direct
                        node.children.append(n)
                else:
                   self.simulator.reset(copy.deepcopy(node.state[0]), node.state[1])
                   if self.simulator.move(direct):
                       new_state = self.simulator.get_state()
                       n = Node(new_state, node.depth+1,CHANCE_PLAYER)
                       self.build_tree(n)
                       n.move_action = direct
                       node.children.append(n)

        elif node.player_type == CHANCE_PLAYER:
            # TODO: find all children resulting from
            # all possible placements of '2's
            # NOTE: the following calls may be useful
            # (in addition to those mentioned above):
            # self.simulator.get_open_tiles():
            emptyspace = self.simulator.get_open_tiles()
            state = (copy.deepcopy(node.state[0]), node.state[1])
            for tile in emptyspace:
                if self.simulator.get_state() == state:
                    self.simulator.tile_matrix[tile[0]][tile[1]] = 2
                    new_state = self.simulator.get_state()
                    n = Node(new_state, node.depth+1,MAX_PLAYER)
                    self.build_tree(n)
                    node.children.append(n)
                else:
                    self.simulator.reset(copy.deepcopy(node.state[0]), node.state[1])
                    self.simulator.tile_matrix[tile[0]][tile[1]] = 2
                    new_state = self.simulator.get_state()
                    n = Node(new_state, node.depth+1,MAX_PLAYER)
                    self.build_tree(n)
                    node.children.append(n)



    # Do not modify this function
    def compute_decision(self):
        self.build_tree()
        direction, _ = self.expectimax(self.root)
        return direction

    # TODO (optional): implement method for extra credits
    def compute_decision_ec(self):
        # TODO delete this
        #return random.randint(0, 3)
        self.build_tree_ec()
        direction, _ = self.expectimax(self.root)
        return direction
