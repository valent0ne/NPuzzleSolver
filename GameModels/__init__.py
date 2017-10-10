import numpy
import logging
import Heuristics as H

# final state of fifteenpuzzle game, computed by final(state) function
finalTable = []


# define games
class Game:
    def __init__(self, initialState=None, heuristic=None):
        self.state = initialState
        self.heuristic = heuristic

    def neighbors(self, state):
        out = set([])
        return out

    def getState(self):
        return self.state

    def solution(self, state):
        return True


# class that model the puzzle
class FifteenPuzzleGame(Game):
    def __init__(self, table, heuristic):
        # the state of this puzzle is only composed by the table representing the state
        self.state = FifteenPuzzleState(None, table, heuristic)

    # computes the neighbors of a certain state
    # generating new states after making "moves"
    # in this case after moving the "empty tile" [0]
    def neighbors(self, state):
        logging.debug("--------------- neighbors ---------------")
        heuristic = H.FifteenPuzzleHeuristic()
        out = set([])
        rep = state.representation
        originalTable = numpy.copy(rep.table)
        shape = originalTable.shape
        size = shape[0]
        zeroXpos, zeroYpos = numpy.where(originalTable == 0)
        # logging.debug("zero tile is at position: {},{}".format(zeroXpos, zeroYpos))

        # one of these var. at True means that i can move the zero tile in that direction
        left = True
        right = True
        top = True
        bottom = True
        moves = 4

        # check where can i move
        if zeroXpos == (size - 1):
            bottom = False
            moves -= 1
            logging.debug("can't move zero at bottom")
        if zeroXpos == 0:
            top = False
            moves -= 1
            logging.debug("can't move zero at top")
        if zeroYpos == (size - 1):
            right = False
            moves -= 1
            logging.debug("can't move zero at right")
        if zeroYpos == 0:
            left = False
            moves -= 1
            logging.debug("can't move zero at left")

        logging.debug("i can do {} moves".format(moves))

        if top:
            newTable = numpy.copy(originalTable)
            temp = newTable[zeroXpos - 1, zeroYpos]
            logging.debug("moving {} - pos {},{} at bottom".format(temp, zeroXpos - 1, zeroYpos))
            # move zero at top and move temp tile at bottom
            newTable[zeroXpos, zeroYpos] = temp
            newTable[zeroXpos - 1, zeroYpos] = 0
            ns = FifteenPuzzleState(state, newTable, heuristic)
            logging.debug("new table after moving zero tile top:\n {}".format(ns.representation.table))
            out.add(ns)

        if bottom:
            newTable = numpy.copy(originalTable)
            temp = newTable[zeroXpos + 1, zeroYpos]
            logging.debug("moving {} - pos {},{} at top".format(temp, zeroXpos + 1, zeroYpos))
            # move zero at top and move temp tile at bottom
            newTable[zeroXpos, zeroYpos] = temp
            newTable[zeroXpos + 1, zeroYpos] = 0
            ns = FifteenPuzzleState(state, newTable, heuristic)
            logging.debug("new table after moving zero tile bottom:\n {}".format(ns.representation.table))
            out.add(ns)

        if left:
            newTable = numpy.copy(originalTable)
            temp = newTable[zeroXpos, zeroYpos - 1]
            logging.debug("moving {} - pos {},{} at right".format(temp, zeroXpos, zeroYpos - 1))
            # move zero at left and move temp tile at top
            newTable[zeroXpos, zeroYpos] = temp
            newTable[zeroXpos, zeroYpos - 1] = 0
            ns = FifteenPuzzleState(state, newTable, heuristic)
            logging.debug("new table after moving zero tile left:\n {}".format(ns.representation.table))
            out.add(ns)

        if right:
            newTable = numpy.copy(originalTable)
            temp = newTable[zeroXpos, zeroYpos + 1]
            logging.debug("moving {} - pos {},{} at left".format(temp, zeroXpos, zeroYpos + 1))
            # move zero at right and move temp tile at top
            newTable[zeroXpos, zeroYpos] = temp
            newTable[zeroXpos, zeroYpos + 1] = 0
            ns = FifteenPuzzleState(state, newTable, heuristic)
            logging.debug("new table after moving zero tile right:\n {}".format(ns.representation.table))
            out.add(ns)

        logging.debug("------------- end neighbors -------------\n")

        return out

    # return true if provided state is a final one
    def solution(self, state):
        out = numpy.array_equal(state.representation.table, finalTable)
        logging.debug("solution returned: {}".format(out))
        return out


# representation of a state
class FifteenPuzzleRepresentation:
    def __init__(self, table):
        self.table = numpy.copy(table)

    @staticmethod
    def isAdmissible():
        # every representation built by neighbour is admissible by construction
        return True


# a state has a parent state and a representation of the state
class FifteenPuzzleState:
    def __init__(self, parent, table, heuristic):
        self.parent = parent
        self.H = heuristic
        self.representation = FifteenPuzzleRepresentation(table)

    # redefined criteria on wich items of this class are
    # compared to be able to correctly use set operators
    # saying that 2 states are equal if the table that represent
    # the state is the same
    def __eq__(self, other):
        return numpy.array_equal(self.representation.table, other.representation.table)

    def __ne__(self, other):
        return not numpy.array_equal(self.representation.table, other.representation.table)

    def __hash__(self):
        return hash(self.representation.table.__hash__)


# computes the final table based on dimensions provided by the user
def final(size):
    # fill the matrix with values from 1 to len and add 0 to last tile
    global finalTable
    finalTable = numpy.arange(1, (size * size) + 1, 1)
    numpy.put(finalTable, [size * size], [0], mode="clip")
    finalTable = finalTable.reshape(size, size)
    logging.debug("finalTable:\n {}".format(finalTable))
    return
