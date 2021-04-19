
numDivision = 16

def nearBoardDot(currMovePos, step=2):
    left = currMovePos[0] - step if (currMovePos[0] - step) > 0 else 1
    right = currMovePos[0] + step if (currMovePos[0] + step) < numDivision else numDivision - 1
    top = currMovePos[1] - step if (currMovePos[1] - step) > 0 else 1
    bottom = currMovePos[1] + step if (currMovePos[1] + step) < numDivision else numDivision - 1
    return (left, right, top, bottom)

def numToBoardDotPos(num):
    return (1 + (num % (numDivision - 1)), (num // (numDivision - 1)) + 1)


def boardDotPosToNum(boardDot):
    return (boardDot[1] - 1) * (numDivision - 1) + boardDot[0] - 1