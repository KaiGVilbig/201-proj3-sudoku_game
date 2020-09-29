# File:          proj3.py
# Author:        Kai Vilbig
# Date:          11/30/2018
# Section:       28
# E-mail:        sw92057@umbc.edu
# Description:   Sudoku game


QUIT = "q"
#------------------------------------------------------------------------------

# prettyPrint() prints the board with row and column labels,
#               and spaces the board out so that it looks nice
# Input:        board;   the square 2d game board (of integers) to print
# Output:       None;    prints the board in a pretty way
def prettyPrint(board):
    # print column headings and top border
    print("\n    1 2 3 | 4 5 6 | 7 8 9 ")
    print("  +-------+-------+-------+")

    for i in range(len(board)):
        # convert "0" cells to underscores  (DEEP COPY!!!)
        boardRow = list(board[i])
        for j in range(len(boardRow)):
            if boardRow[j] == 0:
                boardRow[j] = "_"

        # fill in the row with the numbers from the board
        print( "{} | {} {} {} | {} {} {} | {} {} {} |".format(i + 1,
                boardRow[0], boardRow[1], boardRow[2],
                boardRow[3], boardRow[4], boardRow[5],
                boardRow[6], boardRow[7], boardRow[8]) )

        # the middle and last borders of the board
        if (i + 1) % 3 == 0:
            print("  +-------+-------+-------+")

#------------------------------------------------------------------------------
            
# savePuzzle() writes the contents a sudoku puzzle out
#              to a file in comma separated format
# Input:       board;    the square 2d puzzle (of integers) to write to a file
#              fileName; the name of the file to use for writing to
def savePuzzle(board, fileName):
    ofp = open(fileName, "w")
    for i in range(len(board)):
        rowStr = ""
        for j in range(len(board[i])):
            rowStr += str(board[i][j]) + ","
        # don't write the last comma to the file
        ofp.write(rowStr[ : len(rowStr)-1] + "\n")
    ofp.close()

#------------------------------------------------------------------------------

# finds all the possible numbers and returns them back to the solve function
def possibleNums(board, x, y):

    # by creating a dictionary, the code is first able to check row, column and
    # 3x3 grid if a certain number (the key) works. If it doesn's we set the value
    # of that key to 1. If the number works, the value remains 0.
    # Once we find which numbers we can use, we set the vaule equal to the key
    possible = {}
    
    for i in range(1, 10):

        possible[i] = 0
    
    # check horizontal
    for i in range(0, 9):

        if board[x][i] != 0:

            possible[board[x][i]] = 1

    # check vertical
    for i in range(0, 9):

        if board[i][y] != 0:

            possible[board[i][y]] = 1

    # check each 3x3 grid
    k = 0
    l = 0

    # checks to see where the index is and sets it to the top left of the 3x3 grid
    # it is in
    if x >= 0 and x <=2:

        k = 0

    elif x >= 3 and x <= 5:

        k = 3

    else:

        k = 6

    if y >= 0 and y <= 2:

        l = 0

    elif y >= 3 and y <= 5:

        l = 3

    else:

        l = 6

    # checks the 3x3 grid
    for i in range(k, k + 3):

        for j in range(l, l + 3):

            if board[i][j] != 0:

                possible[board[i][j]] = 1

    # now that the dictionary values are 1 and 0, we know that the
    # keys with value 0 are numbers that can go in the cell.
    # we assign the value equal to the key
    for i in range(1, 10):

        if possible[i] == 0:

            possible[i] = i
            
        else:

            possible[i] = 0
    
    return possible

#------------------------------------------------------------------------------

# check to see if the board is full
def isBoardFull(board):

    anyZeroInBoard = []
    for i in range(len(board)):

        if 0 not in board[i]:
            
            anyZeroInBoard.append(True)

        else:

            anyZeroInBoard.append(False)
            
    if False not in anyZeroInBoard:

        return True
        
#------------------------------------------------------------------------------

# compares the user's input to the number in the same index of the solved board
def compare(board, row, column):

    compareFile = getFile("solved.txt")

    if compareFile[row][column] == board[row][column]:

        return True

    else:

        return False
    
#------------------------------------------------------------------------------

# user plays
def play(board, correctness, puzzleFile):

    keepPlaying = True

    # keep track of the indexes of the moves so that the user can undo
    moves = []

    while keepPlaying:

        prettyPrint(board)
        
        # makes sure user inputs corect menu options
        nextMove = input("Play number (p), save (s), undo (u), quit (q): ")
        while nextMove != "s" and nextMove != "u" and nextMove != QUIT and \
              nextMove != "p":

            print("Please enter a valid option")
            print()
            nextMove = input("Play number (p), save (s), undo (u), quit (q): ")

        # saves the function
        if nextMove == "s":

            savePuzzle(board, "userPuzzle.txt")
            print("Progress saved")

        # undo last move
        elif nextMove == "u":

            origionalBoard = getFile(puzzleFile)
            if len(moves) == 0:

                print("You can't undo anymore!")

            else:

                # gets where the last move was placed
                lastMoveIndex = len(moves) - 1

                # splits the last move into its row and column
                lastMoveRow = moves[lastMoveIndex][0]
                lastMoveColumn = moves[lastMoveIndex][1]

                print("Removed the", num, "you played at position (" + \
                      str(lastMoveRow) + ", " + str(lastMoveColumn) + ").")

                # removes the last move
                board[lastMoveRow][lastMoveColumn] = 0
                moves.remove(moves[lastMoveIndex])
                
        # quit and show final board
        # in my game, quitting means you lose because winners never quit
        elif nextMove == QUIT:

            print("Good bye! Here is the final board:")
            prettyPrint(board)
            print()
            keepPlaying = False

        # user choses to play
        else:

            prettyPrint(board)

            # make sure user inputs num between 1 and 9
            row = int(input("Enter a row number (1-9): ")) - 1
            while row > 8 or row < 0:

                print("Please enter a valid row (1-9)")
                print()
                row = int(input("Enter a row number (1-9): ")) - 1

            # make sure user inputs num between 1 and 9
            column = int(input("Enter a column number (1-9): ")) - 1
            while column > 8 or column < 0:

                print("Please enter a valid column (1-9)")
                print()
                column = int(input("Enter a column number (1-9): ")) - 1

            # make sure user inputs num between 1 and 9
            num = int(input("Enter a number to put in cell (1-9): "))
            while num > 9 or num < 1:

                print("Please enter a valid number (1-9)")
                print()
                num = int(input("Enter a number to put in cell(1-9): "))
                
            numsGoodToPlace = {}
            numsGoodToPlace = possibleNums(board, row, column)

            listOfGoodNums = list(numsGoodToPlace.values())

            # check to make sure the user does not place a number
            # in an already full cell
            cellNotTaken = True
            if board[row][column] != 0:

                print("That cell is already full!")
                cellNotTaken = False

            if cellNotTaken:
                
                while num not in listOfGoodNums:

                    print("You can't put that number in there")
                    print()
                    num = int(input("Enter a number to put in cell(1-9): "))
                    print()

                    while num > 9 or num < 1:

                        print("Please enter a valid number (1-9)")
                        print()
                        num = int(input("Enter a number to put in cell(1-9): "))

                # the number will only be placed and checked for correctness
                # if the cell is empty
            
                # add current move to the list of moves
                currentMove = [row, column]
                moves.append(currentMove)
                
                board[row][column] = num
            
                if correctness == "y":

                    correct = compare(board, row, column)

                    if correct == False:

                        print(num, "is not the right number for position (" + \
                              str(column) + ", " + str(column) + ")!")

                        board[row][column] = 0

            # stop playing if the board is full
            if isBoardFull(board):

                keepPlaying = False

#------------------------------------------------------------------------------

# solve the puzzle
def solve(solveBoard):
    
    x = 0
    y = 0

    # when the code finds the possible numbers, it will store them in a dictionary
    # therefor we store the possibilities in a dictionary here as well since it will
    # be returned as a dictionary
    possibilities = {}

    # check to see if board is full
    if isBoardFull(solveBoard):

        # put this in because puzzleD takes a while to find the solution
        print("one sec...")
        savePuzzle(solveBoard, "solved.txt")
        print()
        
    else:

        # find the index of the last blank space because in order to find the first
        # I would have had to use break and we have not learned that
        for i in range(len(solveBoard)):

            for j in range(len(solveBoard[i])):
                
                if solveBoard[i][j] == 0:
                    
                    x = i
                    y = j
     
        possibilities = possibleNums(solveBoard, x, y)
        
        # go through all the possibilities and call the function
        # again wiht the updated board
        for i in range(1, 10):

            if possibilities[i] != 0:

                solveBoard[x][y] = possibilities[i]
                
                solve(solveBoard)
    
            # backtrack if the number didn't work
            solveBoard[x][y] = 0
        
#------------------------------------------------------------------------------

# gets a text file and puts it into a list
def getFile(fileToOpen):

    puzzleBoard = open(fileToOpen)
    board = puzzleBoard.readlines()
    
    # get rid of the commas
    for i in range(len(board)):

        board[i] = board[i].strip()
        board[i] = board[i].split(",")

        # make all of the items in the board integers instead of
        # strings so that the prettyPrint function can replace them
        # with _
        for j in range(len(board[i])):

            board[i][j] = int(board[i][j])

    return board
            
#------------------------------------------------------------------------------

# checks to see if the player has won
def winCheck(board):

    compareBoard = getFile("solved.txt")

    if board == compareBoard:

        return True
    
#------------------------------------------------------------------------------
    
def main():

    print()
    puzzleFile = input("Enter the filename of the Sudoku Puzzle: ")
    board = getFile(puzzleFile)
    
    prettyPrint(board)

    # deep copy
    solveBoard = []
    for i in range(len(board)):

        solveBoardRow = list(board[i])
        solveBoard.append(solveBoardRow)

    # put this print statement in because puzzleD takes a while to find the solution
    # so it won't look like the program just crashed.
    print()
    print("Please hold on while the computer solves the "\
          "puzzle...")
    solve(solveBoard)
    
    playOrSolve = input("play (p) or solve (s)? ")

    while playOrSolve != "p" and playOrSolve != "s":

        print("Please enter a valid answer")
        print()
        playOrSolve = input("play (p) or solve (s)? ")
    
    if playOrSolve == "p":

        # get user input on whether user wants to play with correctness
        correctness = input("Play with correctness checking?: ")
        while correctness != "y" and correctness != "n":

            # makes sure user inputs correct
            print("Please enter a valid answer")
            print()
            correctness = input("Play with correctness checking?: ")
            
        play(board, correctness, puzzleFile)

    # if the user choses solve, the program will print the solved board
    elif playOrSolve == "s":

        print("Here is the completed board")
        solvedPuzzle = getFile("solved.txt")
        prettyPrint(solvedPuzzle)
        print()

    if playOrSolve != "s":
        
        # prints out message based on if the user has won or not
        if winCheck(board):

            print()
            print("Congradulations, you won!")
            print()
        
        else:

            print()
            print("oof")
            print("Ya lost my dude")
            print()
        
main()
