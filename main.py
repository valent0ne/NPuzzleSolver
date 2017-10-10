import GameModels as G
import Heuristics as H
import numpy
import logging
import time
import math

logging.basicConfig(level=logging.INFO)

doneStates = {}
heuristicType = 0
heuristic = H.FifteenPuzzleHeuristic


# return the state with minimum heuristic value from the horizon and
# add that state to the "done" set, so it will not be returned anymore
def argMin(setOfStates):
    localDicOfStates = {}
    for i in setOfStates:
        # avoid states already returned
        if i not in doneStates:
            # calculate heuristic based on user choice
            if heuristicType == 1:
                value = heuristic.H1(i)
            else:
                value = heuristic.H2(i)
            # add couple key value (state, weight) to local set
            localDicOfStates[i] = value
    if len(localDicOfStates) > 0:
        # return the minumim weighted state inside local set
        out = min(localDicOfStates, key=localDicOfStates.get)
        # flag the state as done
        doneStates[out] = localDicOfStates[out]
        logging.info("picked a state with value {} from the neighborhood".format(localDicOfStates[out]))
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
    i = 1
    sHorizon = set([])
    sExplored = set([])
    # add initial state
    sHorizon.add(state0)
    while len(sHorizon) > 0:
        logging.debug("while iteration n. {}".format(i))
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
            logging.info("visited states: {}".format(len(doneStates)))
            logging.debug("---------------end of iteration--------------------")
        else:
            return None
        i += 1


# Main
# generate istance from user input and let the user choose wich heuristic to use
def main():

    # data = input("Insert input using this syntax x, y, z, ... : ")
    # choose = int(input("Choose the heuristic to use (1 for manhattan distance, 2 for misplaced tiles): "))
    # if choose != 1 and choose != 2:
    #     logging.error("Use only 1 or 2")
    #     exit(1)
    # splitted = data.split(",")
    # # converting string items to integer
    # splitted = [int(i) for i in splitted]
    # logging.debug("Inserted data: {}".format(splitted))
    # logging.debug("Number of items: {}".format(len(splitted)))
    # size = int(math.sqrt(len(splitted)))
    #
    # if not math.sqrt(len(splitted)).is_integer():
    #     logging.error("You have inserted {} items, you should have inserted a number of items resulting in a NxN matrix (4, 9, 16 ...) ".format(len(splitted)))
    #     exit(1)
    # logging.debug("Size of matrix: {}x{}".format(size,size))
    # # generate instance from user input (user inputs 1,3,0,2 and the matrix [[1,3],[0,2]] is generated
    # # numpy is a package useful to handle matrices
    # startingTable = numpy.array(splitted).reshape((size, size))

    data = input("Insert the file name containing the input instance with a row per line, with each "
                 "element separated by a whitespace: ")
    finput = open(data, "r")
    startingTable = numpy.loadtxt(finput, delimiter=" ", dtype=int)
    size = startingTable.shape[0]

    logging.debug("Loaded matrix:\n {}".format(startingTable))

    choose = int(input("Choose the heuristic to use (1 for manhattan distance, 2 for misplaced tiles): "))
    if choose != 1 and choose != 2:
        logging.error("Use only 1 or 2")
        exit(1)

    # set heuristic type
    global heuristicType
    heuristicType = choose

    # start counting time
    start_time = time.time()
    # initialize game
    G.final(size)
    game = G.FifteenPuzzleGame(startingTable, heuristic=heuristic)
    state0 = game.getState()
    # begin search
    path = search(game, state0)
    # calculate elapsed time
    elapsed_time = time.time() - start_time

    logging.info("Solution reached visiting {} states: ".format(len(doneStates)))

    # print solution
    i = 0
    for x in path:
        logging.info("move {} \n {}\n".format(i, x.representation.table))
        i += 1
    logging.info("Elapsed time: {} s".format(elapsed_time))


if __name__ == "__main__":
    main()
