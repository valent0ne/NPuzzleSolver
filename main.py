from operator import attrgetter
import GameModels as G
import numpy
import logging
import time

heuristicType = 1
perturbation = 0


# return the state with minimum heuristic value from the horizon and
# add that state to the "done" set, so it will not be returned anymore
def argMin(setOfStates):
    if len(setOfStates) > 0:
        # return the minumum weighted state inside local set
        out = min(setOfStates, key=attrgetter('heuristic'))
        # flag the state as done
        logging.info("picked state value: {}".format(out.heuristic))
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
def search(game, state0):
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
            logging.debug("added view to explored:\n {}".format(view.representation.table))
            # discover neighbors (inside GameModels)
            neighbors = game.neighbors(view)
            logging.debug("pre-expand horizon size: {}".format(len(sHorizon)))
            logging.debug("neighbors size: {}".format(len(neighbors)))
            # compute new horizon, avoiding already explored states
            sHorizon = (sHorizon | neighbors) - sExplored
            # logging.debug("explored size: {}".format(len(sExplored)))
            logging.debug("new horizon size: {}".format(len(sHorizon)))
            logging.info("horizon size: {}".format(len(sHorizon)))
            logging.info("visited states: {}".format(len(sExplored)))
            logging.info("--------------------------------------------")

            logging.debug("---------------end of iteration--------------------")
        else:
            return None


# Main
# generate istance from user input and let the user choose which heuristic to use
def main():

    global heuristicType
    global perturbation
    global logging_level

    data = input("Insert the file name containing the input instance with a row per line, with each "
                 "element separated by a whitespace, default \"data\": ")
    try:
        finput = open(data, "r")
    except IOError:
        finput = open("data", "r")

    starting_table = numpy.loadtxt(finput, delimiter=" ", dtype=int)
    size = starting_table.shape[0]

    try:
        choose = int(input("Choose the heuristic to use: \n"
                           "1 for Manhattan distance\n"
                           "2 for Misplaced Tiles\n"
                           "3 for \"improved\" Misplaced Tiles\n"
                           "4 for Manhattan with Linear Conflict\n"
                           "5 hybrid\n"
                           "default is 1:  "))
    except Exception:
        choose = 1

    # set heuristic type
    heuristicType = choose

    try:
        perturbation = int(input("Do you want to perturbate the heuristic values (0 = no, 1 = yes, default = no): "))
    except:
        perturbation = 0

    logging_level = input("Insert logging level (DEBUG or INFO, default = INFO): ")
    if logging_level != "INFO" and logging_level != "DEBUG":
        logging.basicConfig(level='INFO')
    else:
        logging.basicConfig(level=logging_level)


    logging.debug("Loaded matrix:\n {}".format(starting_table))

    # start counting time
    start_time = time.time()
    # initialize game
    G.final(size)
    game = G.FifteenPuzzleGame(starting_table)
    state0 = game.getState()
    # begin search
    path, num_visited_states = search(game, state0)
    if path is None:
        logging.error("Solution not found.")
        exit(1)

    # calculate elapsed time
    elapsed_time = time.time() - start_time

    logging.info("\nComputed moves to solution: \n")
    # print solution
    i = 0
    for x in path:
        logging.info("move #{} \n {}\n".format(i, x.representation.table))
        i += 1

    logging.info("Number of moves to reach the final state: {}".format(i-1))
    logging.info("Solution reached analyzing {} states".format(num_visited_states))
    logging.info("Elapsed time: {} s".format(elapsed_time))


if __name__ == "__main__":
    main()
