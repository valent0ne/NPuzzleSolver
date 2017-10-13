from operator import attrgetter
import GameModels as G
import Configuration as conf
import numpy
import logging
import time
import os

# return the state with minimum heuristic value from the horizon and
# add that state to the "done" set, so it will not be returned anymore
def argMin(setOfStates):
    if len(setOfStates) > 0:
        # return the minumum weighted state inside local set
        out = min(setOfStates, key=attrgetter('heuristic'))
        # flag the state as done
        logging.debug("picked state value: {}".format(out.heuristic))
    else:
        out = None
    return out


# pick a state from horizon
def pick(setOfStates):
    return argMin(setOfStates)


# return reverse path to root
def backpath(state):
    father = state.parent
    lStates = [state]
    while father is not None:
        lStates.append(father)
        father = father.parent
    return reversed(lStates)


# search function, it analyzes the horizon, pick the best state and iterate on the new state
def search(game, state0, update, start_time):
    i=0
    sHorizon = set([])
    sExplored = set([])
    # add initial state
    sHorizon.add(state0)
    while len(sHorizon) > 0:
        logging.debug("initial horizon size: {}".format(len(sHorizon)))

        # pick the best state from horizon
        view = pick(sHorizon)
        # if view contains something
        if view is not None:
            if game.solution(view):
                # logging.debug("solution found")
                return backpath(view), len(sExplored)
            # add state to explored
            sExplored.add(view)
            distance_from_goal = view.heuristic - view.moves
            logging.debug("added view to explored:\n {}".format(view.representation.table))
            # discover neighbors (inside GameModels)
            neighbors = game.neighbors(view)
            logging.debug("pre-expand horizon size: {}".format(len(sHorizon)))
            logging.debug("neighbors size: {}".format(len(neighbors)))
            # compute new horizon, avoiding already explored states
            sHorizon = (sHorizon | neighbors) - sExplored
            
            if i == update:
                i = 0
                print("\nelapsed time: {0:.3f} s".format(time.time()-start_time))
                print("horizon size: {}".format(len(sHorizon)))
                print("visited states: {}".format(len(sExplored)))
                print("approximated distance from solution: {}".format(distance_from_goal))
                print("current picked state representation:\n {}".format(view.representation.table))
            i += 1
            
            # logging.debug("explored size: {}".format(len(sExplored)))
            # logging.debug("new horizon size: {}".format(len(sHorizon)))
            # logging.debug("horizon size: {}".format(len(sHorizon)))
            # logging.debug("visited states: {}".format(len(sExplored)))
            # logging.debug("--------------------------------------------")

            # logging.debug("---------------end of iteration--------------------")
            
        else:
            return None

def cls():
    os.system('cls' if os.name=='nt' else 'clear')



# Main
# generate istance from user input and let the user choose which heuristic to use
def main():

    cls()

    data = input("Insert the file name containing the input instance with a row per line, \n"
                 "with each element separated by a whitespace, default \"intputs/data\": ")
    try:
        finput = open(data, "r")
    except IOError:
        finput = open("data", "r")

    starting_table = numpy.loadtxt(finput, delimiter=" ", dtype=int)
    size = starting_table.shape[0]

    try:
        choose = int(input("Choose the heuristic to use: \n"
                           "\t[1] for Manhattan distance\n"
                           "\t[2] for Misplaced Tiles\n"
                           "\t[3] for \"improved\" Misplaced Tiles\n"
                           "\t[4] for Manhattan with Linear Conflict\n"
                           "\t[5] hybrid\n"
                           "default is [1]:  "))
        if choose not in range(6):
            raise Exception
    except:
        choose = 1


    try:
        perturbation = int(input("Do you want to perturbate the heuristic values? (0 = no, 1 = yes, default = no): "))
        if perturbation not in range(2):
            raise Exception
    except:
        perturbation = 0

    try:
        update = int(input("You will get updates every X iterations, insert X (default = 1000): "))
    except:
        update = 1000

    logging_level = input("Insert logging level (DEBUG or INFO, default = INFO): ")
    if logging_level != "INFO" and logging_level != "DEBUG":
        logging.basicConfig(level='INFO')
    else:
        logging.basicConfig(level=logging_level)

    print("\nLoaded matrix:\n {}".format(starting_table))

    c = conf.Configuration(choose, perturbation)

    print("\ncomputing...")

    # start counting time
    start_time = time.time()
    # initialize game
    game = G.FifteenPuzzleGame(starting_table, c)
    G.FifteenPuzzleGame.final(size)
    state0 = game.getState()
    # begin search
    path, num_visited_states = search(game, state0, update, start_time)
    if path is None:
        logging.error("Solution not found.")
        exit(1)

    # calculate elapsed time
    elapsed_time = time.time() - start_time

    print("\nComputed moves to solution: \n")
    # print solution
    i = 0
    for x in path:
        print("move #{} \n {}\n".format(i, x.representation.table))
        i += 1

    print("\nInitial state: \n{}".format(starting_table))
    print("Used heuristic: [{}]".format(c.heuristic_type))
    print("Number of moves to reach the final state: {}".format(i-1))
    print("Solution reached analyzing {} states".format(num_visited_states))
    print("Elapsed time: {0:.3f} s".format(elapsed_time))


if __name__ == "__main__":
    main()
