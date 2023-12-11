"""
Snekoban Game
"""

import json
import typing

# NO ADDITIONAL IMPORTS!


direction_vector = {
    "up": (-1, 0),
    "down": (+1, 0),
    "left": (0, -1),
    "right": (0, +1),
}


def new_game(level_description):
    """
    Given a description of a game state, create and return a game
    representation of your choice.

    The given description is a list of lists of lists of strs, representing the
    locations of the objects on the board (as described in the lab writeup).

    For example, a valid level_description is:

    [
        [[], ['wall'], ['computer']],
        [['target', 'player'], ['computer'], ['target']],
    ]

    The exact choice of representation is up to you; but note that what you
    return will be used as input to the other functions.
    """

    boardgame = {
        "target": set(),
        "player": set(),
        "computer": frozenset(),
        "wall": set(),
        "height": len(level_description),
        "width": len(level_description[0]),
    }
    for row in range(len(level_description)):
        for col in range(len(level_description[row])):
            for obj in level_description[row][col]:
                if obj == "player":
                    boardgame[obj] = (row, col)
                elif obj == "computer":
                    x_temp = set(boardgame[obj])
                    x_temp.add((row, col))
                    boardgame[obj] = frozenset(x_temp)
                else:
                    boardgame[obj].add((row, col))

    return boardgame


def victory_check(game):
    """
    Given a game representation (of the form returned from new_game), return
    a Boolean: True if the given game satisfies the victory condition, and
    False otherwise.
    """

    if game["target"] != set():
        return game["computer"] == game["target"]

    return False


def step_game(game, direction):
    """
    Given a game representation (of the form returned from new_game), return a
    new game representation (of that same form), representing the updated game
    after running one step of the game.  The user's input is given by
    direction, which is one of the following: {'up', 'down', 'left', 'right'}.

    This function should not mutate its input.
    """
    new_bgame = {
        "target": game["target"],
        "wall": game["wall"],
        "player": game["player"],
        "computer": set(game["computer"]),
        "height": game["height"],
        "width": game["width"],
    }
    new_board = new_bgame
    location = (
        new_bgame["player"][0] + direction_vector[direction][0],
        new_bgame["player"][1] + direction_vector[direction][1],
    )
    new_location = (
        location[0] + direction_vector[direction][0],
        location[1] + direction_vector[direction][1],
    )
    if location in new_bgame["wall"]:
        return new_board
    if location in new_bgame["computer"]:
        if new_location in new_bgame["wall"] or new_location in new_bgame["computer"]:
            new_board["player"] = new_bgame["player"]

            return new_board
        else:
            new_board["player"] = location
            new_board["computer"].remove(location)
            new_board["computer"].add(new_location)

    else:
        new_board["player"] = location

    return new_board


def dump_game(game):
    """
    Given a game representation (of the form returned from new_game), convert
    it back into a level description that would be a suitable input to new_game
    (a list of lists of lists of strings).

    This function is used by the GUI and the tests to see what your game
    implementation has done, and it can also serve as a rudimentary way to
    print out the current state of your game for testing and debugging on your
    own.
    """

    new_bgame = []
    for row in range(game["height"]):
        row_list = []
        for col in range(game["width"]):
            column = []
            loc = (row, col)
            if loc in game["wall"]:
                column.append("wall")
            if loc in game["target"]:
                column.append("target")
            if loc in game["computer"]:
                column.append("computer")
            row_list.append(column)
        new_bgame.append(row_list)
    new_bgame[game["player"][0]][game["player"][1]].append("player")
    return new_bgame

def can_move_to(state, direction):
    """"given the location of player
    returns possible steps player can take"""
    new_state = step_game(state, direction)
    if state["player"] != new_state["player"]:
        return True


def get_next_directions(game,):  
    """given the location of player
        returns possible steps player can take 
        returns a list of possible directions the player can take"""
    directions = []
    for key in direction_vector.keys():
        if can_move_to(game, key):
            directions.append(key)

    return directions


def freeze_board(board):
    """Creates an immutable board with unique elements"""
    return (board["player"], frozenset(board["computer"]))


def solve_puzzle(game):
    """
    Given a game representation (of the form returned from new game), find a
    solution.

    Return a list of strings representing the shortest sequence of moves ("up",
    "down", "left", and "right") needed to reach the victory condition.

    If the given level cannot be solved, return None"""
    queue = [(game, [])]
    visited = set()

    while queue:
        curr_game = queue.pop(0)
        path = curr_game[1]
        curr_board = curr_game[0]
        if freeze_board(curr_board) not in visited:  # only check board if not seen
            if victory_check(curr_board):
                return path
            visited.add(freeze_board(curr_board))
            for direction in get_next_directions(curr_board):
                next_state = step_game(curr_board, direction)
                next_path = path + [direction]
                queue.append((next_state, next_path))
    return None 
   
 

if __name__ == "__main__":
    pass
