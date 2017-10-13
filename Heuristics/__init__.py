import numpy
import logging
import GameModels as G

default_differentiator = float(1.0e-10)
increaser = float(1.0e-10)
container = {}


class Heuristic:

    def __init__(self):
        pass

    @staticmethod
    def H1(state):
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
        table = state
        G.FifteenPuzzleGame.final(table.shape[0])
        finalState = G.finalTable
        logging.debug("analyzing state:\n {}".format(table))
        for i in numpy.nditer(table):
            if i == 0:
                continue
            logging.debug("item n. {}".format(i))
            # coordinates of i tile in this state
            xPos, yPos = numpy.where(table == i)
            logging.debug("coordinates of item {}: {},{}".format(i, xPos, yPos))
            # coordinates of i tile in final state
            finalXpos, finalYpos = numpy.where(finalState == i)
            logging.debug("coordinates of where item {} should be: {},{}".format(i, finalXpos, finalYpos))
            distance = manhattan_distance((xPos, yPos), (finalXpos, finalYpos))
            logging.debug("distance: {}".format(distance))
            out += distance

        logging.debug("heuristic weight: {}".format(out))
        logging.debug("----------------end H1----------------\n")
        return float(out)

    # count of misplaced tiles, skipping the 0 tile; higher H value
    # means higher distance from solution
    @staticmethod
    def H2(state):
        logging.debug("------------------H2------------------")
        out = 0
        table = state
        G.FifteenPuzzleGame.final(table.shape[0])
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
        return float(out)

    # Number of tiles out of row plus number of tiles out of column
    @staticmethod
    def H3(state):
        logging.debug("------------------H3------------------")
        out = 0
        table = state
        G.FifteenPuzzleGame.final(table.shape[0])
        finalState = G.finalTable
        logging.debug("analyzing state:\n {}".format(table))
        for i in numpy.nditer(table):
            if i == 0:
                continue
            # coordinates of i tile in this state
            xPos, yPos = numpy.where(table == i)
            # coordinates of i tile in final state
            finalXpos, finalYpos = numpy.where(finalState == i)
            if xPos != finalXpos:
                out += 1
            if yPos != finalYpos:
                out += 1
        logging.debug("heuristic weight: {}".format(out))
        logging.debug("----------------end H3----------------\n")
        return float(out)

    # Linear Conflict Tiles Definition: Two tiles tj and tk are in a linear conflict
    # if tj and tk are in the same line, the goal positions of tj and tk are both in that line,
    # tj is to the right of tk and goal position of tj is to the left of the goal position of tk.
    # The linear conflict adds at least two moves to the Manhattan Distance of the two conflicting tiles,
    # by forcing them to surround one another. Therefore the heuristic function will add a cost of 2 moves
    # for each pair of conflicting tiles.
    @staticmethod
    def H4(state):
        logging.debug("------------------H4------------------")
        out = 0
        table = state
        G.FifteenPuzzleGame.final(table.shape[0])
        finalState = G.finalTable
        logging.debug("analyzing state:\n {}".format(table))
        for i in numpy.nditer(table):
            if i == 0:
                continue
            logging.debug("item n. {}".format(i))
            # coordinates of i tile in this state
            xPos, yPos = numpy.where(table == i)
            logging.debug("coordinates of item {}: {},{}".format(i, xPos, yPos))
            # coordinates of i tile in final state
            finalXpos, finalYpos = numpy.where(finalState == i)
            logging.debug("coordinates of where item {} should be: {},{}".format(i, finalXpos, finalYpos))
            distance = manhattan_distance((xPos, yPos), (finalXpos, finalYpos))
            logging.debug("local distance: {}".format(distance))

            row = numpy.array(table[xPos])
            # tj and tk are in the same line
            for j in numpy.nditer(row):
                if i != j:
                    x2Pos, y2Pos = numpy.where(table == j)
                    finalX2pos, finalY2pos = numpy.where(finalState == j)
                    if xPos == finalXpos and x2Pos == finalX2pos:
                        # tj is to the right of tk and goal position of tj is to the left of the goal position of tk
                        if y2Pos > yPos and finalY2pos < finalYpos:
                            logging.debug("tile {} and {} are in linear conflict".format(i, j))
                            distance += 1

            out += distance
            logging.debug("updated local distance: {}".format(distance))

        logging.debug("heuristic weight: {}".format(out))
        logging.debug("----------------end H4----------------\n")
        return float(out)

    # hybtid
    @staticmethod
    def H5(i):
        h1 = FifteenPuzzleHeuristic.H1(i)*1.05
        h2 = FifteenPuzzleHeuristic.H2(i)*1.01
        h4 = FifteenPuzzleHeuristic.H4(i)*1.03

        #return min(h1, h2, h4)
        return (h1+h2+h4)/3

    @staticmethod
    def get_h(i):

        heuristic_type = i.configuration.heuristic_type
        perturbation = i.configuration.perturbation
        table = i.representation.table

        if heuristic_type == 1:
            value = FifteenPuzzleHeuristic.H1(table)
        elif heuristic_type == 2:
            value = FifteenPuzzleHeuristic.H2(table)
        elif heuristic_type == 3:
            value = FifteenPuzzleHeuristic.H3(table)
        elif heuristic_type == 4:
            value = FifteenPuzzleHeuristic.H4(table)
        else:
            value = FifteenPuzzleHeuristic.H5(table)

        logging.debug("value: {}".format(value))
        out = value + i.moves
        logging.debug("new value+moves: {}".format(out))

        if perturbation == 1:
            global container

            if value not in container:
                container[value] = default_differentiator

            out += container[value]
            logging.debug("value: {} container[value]: {} out: {}".format(value, container[value], out))

            container[value] += increaser
            logging.debug("increased container[value]: {}".format(container[value]))

        return out


# computes manhattan distance from 2 locations inside a matrix
def manhattan_distance(start, end):
    sx, sy = start
    ex, ey = end
    return abs(ex - sx) + abs(ey - sy)

