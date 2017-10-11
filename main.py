from os import getpid

import multiprocessing

import GameModels as G
import Heuristics as H
import numpy
import logging
import time

num_workers = 1
doneStates = {}
heuristicType = 1
heuristic = H.FifteenPuzzleHeuristic
perturbation = 0


# return the state with minimum heuristic value from the horizon and
# add that state to the "done" set, so it will not be returned anymore
def argMin(setOfStates):
    localDicOfStates = {}
    for i in setOfStates:
        if i not in doneStates:
            localDicOfStates[i] = None
    pool = multiprocessing.Pool(processes=num_workers)
    returned = pool.starmap(task, localDicOfStates.items())
    pool.close()
    pool.join()
    for i in returned:
        localDicOfStates[i[0]] = i[1]
    if len(localDicOfStates) > 0:
        # return the minumum weighted state inside local set
        out = min(localDicOfStates, key=localDicOfStates.get)
        # flag the state as done
        doneStates[out] = localDicOfStates[out]
        logging.info("picked state value: {}".format(localDicOfStates[out]))
    else:
        out = None
    return out


# multiproc task
def task(i, v):
    logging.debug("async call processed by pid: {}".format(getpid()))
    logging.debug("state to be evaluated: \n {}".format(i.representation.table))
    if heuristicType == 1:
        value = heuristic.H1(i)
    elif heuristicType == 2:
        value = heuristic.H2(i)
    elif heuristicType == 3:
        value = heuristic.H3(i)
    else:
        value = heuristic.H4(i)
    # add very small random value to heuristic
    if perturbation == 1:
        value = float(value + numpy.random.uniform(0.00001, 10 ** (-20)))
    logging.debug("pid: {}, returned value {}".format(getpid(), value))
    return i, value


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
                return backpath(view)
            # add state to explored
            sExplored.add(view)
            logging.debug("added view to explored:\n {}".format(view.representation.table))
            # discover neighbors (inside GameModels)
            neighbors = game.neighbors(view)
            logging.debug("pre-expand horizon size: {}".format(len(sHorizon)))
            logging.debug("neighbors size: {}".format(len(neighbors)))
            # compute new horizon, avoiding already explored states
            sHorizon = sHorizon | (neighbors - sExplored)
            logging.debug("explored size: {}".format(len(sExplored)))
            logging.debug("new horizon size: {}".format(len(sHorizon)))

            logging.info("horizon size: {}".format(len(sHorizon)))
            logging.info("visited states: {}".format(len(doneStates)))
            logging.info("--------------------------------------------")

            logging.debug("---------------end of iteration--------------------")
        else:
            return None


# Main
# generate istance from user input and let the user choose which heuristic to use
def main():

    global heuristicType
    global perturbation
    global num_workers

    data = input("Insert the file name containing the input instance with a row per line, with each "
                 "element separated by a whitespace: ")
    try:
        finput = open(data, "r")
    except IOError:
        logging.error("Can't open file.")
        exit(1)

    starting_table = numpy.loadtxt(finput, delimiter=" ", dtype=int)
    size = starting_table.shape[0]

    choose = int(input("Choose the heuristic to use: \n"
                       "1 for Manhattan distance\n"
                       "2 for Misplaced Tiles\n"
                       "3 for \"improved\" Misplaced Tiles\n"
                       "4 for Manhattan with Linear Conflict\n"
                       "-> "))
    if choose not in range(0, 5):
        logging.error("Wrong input")
        exit(1)

    # set heuristic type
    heuristicType = choose

    perturbation = int(input("Do you want to perturbate the heuristic values (0 = no, 1 = yes): "))
    if perturbation not in range(0, 2):
        logging.error("Use only 0 or 1")
        exit(1)

    num_workers = int(input("Insert number of processes: "))
    logging_level = input("Insert logging level (DEBUG or INFO): ")

    logging.basicConfig(level=logging_level)

    logging.debug("Loaded matrix:\n {}".format(starting_table))

    # start counting time
    start_time = time.time()
    # initialize game
    G.final(size)
    game = G.FifteenPuzzleGame(starting_table)
    state0 = game.getState()
    # begin search
    path = search(game, state0)
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

    logging.info("Number of processes: {}".format(num_workers))
    logging.info("Number of moves to reach the final state: {}".format(i-1))
    logging.info("Solution reached going through {} states.".format(len(doneStates)))
    logging.info("Elapsed time: {} s".format(elapsed_time))


if __name__ == "__main__":
    main()
