import numpy
import logging
import GameModels as G

logging.basicConfig(level=logging.INFO)


class Heuristic:

    def __init__(self):
        pass

    @staticmethod
    def H1(state):
        return 1

    @staticmethod
    def H2(state):
        return 1


class FifteenPuzzleHeuristic(Heuristic):
    # manhattan distance
    # sum of all the manhattan distances from the current tile position
    # to where it should be in the final state
    # higher H value means higher distance from solution
    @staticmethod
    def H1(state):
        logging.debug("------------------H1------------------")
        out = 0
        table = numpy.copy(state.representation.table)
        finalState = G.finalTable
        logging.debug("analyzing state:\n {}".format(table))
        for i in numpy.nditer(table):
            # logging.debug("item n. {}".format(i))
            # coordinates of i tile in this state
            xPos, yPos = numpy.where(table == i)
            # logging.debug("coordinates of item {}: {},{}".format(i, xPos, yPos))
            # coordinates of i tile in final state
            finalXpos, finalYpos = numpy.where(finalState == i)
            # logging.debug("coordinates of where item {} should be: {},{}".format(i, finalXpos, finalYpos))
            distance = manhattan_distance((xPos, yPos), (finalXpos, finalYpos))
            # logging.debug("distance: {}".format(distance))
            out += distance
        logging.debug("heuristic weight: {}".format(out))
        logging.debug("----------------end H1----------------\n")
        return out

    # count of misplaced tiles, skipping the 0 tile; higher H value
    # means higher distance from solution
    @staticmethod
    def H2(state):
        logging.debug("------------------H2------------------")
        out = 0
        table = numpy.copy(state.representation.table)
        finalState = G.finalTable
        logging.debug("analyzing state:\n {}".format(table))
        for i in numpy.nditer(table):
            if i == 0:
                continue
            # coordinates of i tile in this state
            xPos, yPos = numpy.where(table == i)
            # coordinates of i tile in final state
            finalXpos, finalYpos = numpy.where(finalState == i)
            if not (xPos == finalXpos and yPos == finalYpos):
                out += 1
        logging.debug("heuristic weight: {}".format(out))
        logging.debug("----------------end H2----------------\n")
        return out


# computes manhattan distance from 2 locations inside a matrix
def manhattan_distance(start, end):
    sx, sy = start
    ex, ey = end
    return abs(ex - sx) + abs(ey - sy)
