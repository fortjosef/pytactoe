import curses
import sys
import math
from curses import wrapper

def translatePlayer(playerAsInt):
    if playerAsInt == -1:
        return "X"
    elif playerAsInt == 1:
        return "Y"

    return ""

def checkForWin(playField):
    #amount of possible solutions amtRows + amountCols + 2
    rowTotals = [0 for x in range(3)]
    colTotals = [0 for x in range(3)]
    diagTotals = [0, 0]

    for y in range(3):
        for x in range(3):
            rowTotals[y] += playField[y][x]
            colTotals[x] += playField[y][x]
            if x == y:
                diagTotals[0] += playField[y][x]
            
            if x + y == 2:
                diagTotals[1] += playField[y][x]

    #not doing early returns because when i add shifting there will be the posibility of having both an X and Y win or even more
    winsForX = 0
    winsForY = 0

    for x in range(3):
        if rowTotals[x] == -3:
            winsForX += 1
        if colTotals[x] == -3:
            winsForX += 1
        if rowTotals[x] == 3:
            winsForY += 1
        if colTotals[x] == 3:
            winsForY += 1
        if x < 2:
            if diagTotals[x] == -3:
                winsForX += 1
            if diagTotals[x] == 3:
                winsForY += 1
    
    if winsForX == winsForY:
        if winsForX > 0:
            return 2 #draw
        else:
            return 0 #no win
    
    if winsForX > winsForY:
        return -1
    else:
        return 1

def game(stdscr):
    stdscr.clear()
    quit = False
    drawScreen = True
    computerOpponent = False
    curses.curs_set(True)
    playField = [
        [0,0,0],
        [0,0,0],
        [0,0,0]
    ]
    cursorX = 0
    cursorY = 0
    currentPlayer = -1
    stdscr.addstr(0, 0, "Arrow Keys to move, Return to place piece")
    stdscr.addstr(1, 0, "Q to quit")

#KEY_LEFT, KEY_UP, KEY_RIGHT, KEY_DOWN
    while quit == False:
        rows, cols = stdscr.getmaxyx()
        playFieldXOrigin = math.floor((cols - 5) / 2)
        playFieldYOrigin = 5
        stdscr.addstr(2, 0, translatePlayer(currentPlayer) + " to move")
        stdscr.move(playFieldYOrigin + (cursorY * 2), playFieldXOrigin + (cursorX * 2))

        if drawScreen == True:
            for y in range(0,5):
                if y == 1 or y == 3:
                    stdscr.addstr(playFieldYOrigin + y, playFieldXOrigin, "-----")
                else:
                    for x in range(0,5):
                        if x == 1 or x == 3:
                            stdscr.addstr(playFieldYOrigin + y, playFieldXOrigin + x, "|")
                        else:
                            stdscr.addstr(playFieldYOrigin + y, playFieldXOrigin + x, translatePlayer(playField[int(y / 2)][int(x / 2)]))

            stdscr.move(playFieldYOrigin + (cursorY * 2), playFieldXOrigin + (cursorX * 2))
            drawScreen = False


        
        try:
            mykey = stdscr.getkey()
        except curses.error:
            #combine this with below, would wan other curses errors coming thorugh
            pass
        except:
            type, value, traceback = sys.exc_info()
            stdscr.addstr(30, 10, "{} {}".format(str(type), str(value)))
        else:
            if mykey == 'q':
                quit = True
                continue
            elif mykey == 'KEY_UP':
                if cursorY > 0:
                    cursorY -= 1
                    stdscr.move(playFieldYOrigin + (cursorY * 2), playFieldXOrigin + (cursorX * 2))
            elif mykey == 'KEY_DOWN':
                if cursorY < 2:
                    cursorY += 1
                    stdscr.move(playFieldYOrigin + (cursorY * 2), playFieldXOrigin + (cursorX * 2))
            elif mykey == 'KEY_RIGHT':
                if cursorX < 2:
                    cursorX += 1
                    stdscr.move(playFieldYOrigin + (cursorY * 2), playFieldXOrigin + (cursorX * 2))
            elif mykey == 'KEY_LEFT':
                if cursorX > 0:
                    cursorX -= 1
                    stdscr.move(playFieldYOrigin + (cursorY * 2), playFieldXOrigin + (cursorX * 2))
            elif mykey == '\n':
                if playField[cursorY][cursorX] == 0:
                    playField[cursorY][cursorX] = currentPlayer
                    drawScreen = True
                    winResult = checkForWin(playField)
                    stdscr.addstr(10, 0, str(winResult))

                    if winResult != 0:
                        #will need to add handling for a draw
                        #will also need to add handling for a cat
                        stdscr.addstr(0, 0, translatePlayer(winResult) + " WINS!!!")
                    else:   
                        if currentPlayer == -1:
                            currentPlayer = 1
                        else:
                            currentPlayer = -1
                else:
                    curses.beep()
            elif mykey == 'KEY_RESIZE':
                #stdscr.addstr(31, 10, 'caught a resize')
                #rows, cols = stdscr.getmaxyx()
                #stdscr.resize(rows, cols)
                #stdscr.addstr(40, 10, "{} Rows {} Columns".format(str(rows), str(cols)))
                continue

def debugUi(stdscr):
    stdscr.clear()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    for x in range(0, 10):
        for y in range(0, 10):
            stdscr.addstr(10 + x, 10 + y, str(y), curses.color_pair(x))
        
    oldlen = 0
    stdscr.refresh()
    stdscr.nodelay(True)
    curses.curs_set(True)
    origrows, origcols = stdscr.getmaxyx()
    quit = False

    while quit == False:
        rows, cols = stdscr.getmaxyx()

        if rows != origrows or cols != origrows:
            stdscr.addstr(rows - 1, 10, 'caught a resize')
            stdscr.resize(rows, cols)
            stdscr.addstr(rows - 1, 10, "{} Rows {} Columns".format(str(rows), str(cols)))

        try:
            mykey = stdscr.getkey()
        except curses.error:
            #combine this with below, would wan other curses errors coming thorugh
            pass
        except:
            type, value, traceback = sys.exc_info()
            stdscr.addstr(30, 10, "{} {}".format(str(type), str(value)))
        else:
            if mykey == 'q':
                quit = True
                continue
            #elif mykey == 'KEY_RESIZE':
                #stdscr.addstr(31, 10, 'caught a resize')
                #rows, cols = stdscr.getmaxyx()
                #stdscr.resize(rows, cols)
                #stdscr.addstr(40, 10, "{} Rows {} Columns".format(str(rows), str(cols)))
                #continue
                
            #try:
            rows, cols = stdscr.getmaxyx()
            #try:
            stdscr.addstr(rows - 1, 10, "{} Rows {} Columns".format(str(rows), str(cols)))
            #except:
                #type, value, traceback = sys.exc_info()
                #stdscr.addstr(30, 10, "{} {}".format(str(type), str(value)))
            addin = ''
            if len(mykey) < oldlen:
                addin = ' ' * (oldlen - len(mykey))

            stdscr.addstr(rows - 2, 10, mykey + addin)
            oldlen = len(mykey)
            #except curses.error:
                #pass



def main(stdscr):
    
    stdscr.nodelay(True)
    origrows, origcols = stdscr.getmaxyx()
    quit = False
    drawScreen =  True
    title = 'PyTacToe'
    curses.curs_set(False)
    

    while quit == False:
        if drawScreen == True:
            stdscr.clear()
            stdscr.addstr(1, int((origcols - len(title)) / 2), title)
            stdscr.addstr(8, 10, '1) Play a game')
            stdscr.addstr(9, 10, '2) Debugging interface')
            stdscr.addstr(10,10, 'q) Quit' )
            drawScreen = False

        try:
            mykey = stdscr.getkey()
        except curses.error:
            #combine this with below, would wan other curses errors coming thorugh
            pass
        except:
            type, value, traceback = sys.exc_info()
            stdscr.addstr(30, 10, "{} {}".format(str(type), str(value)))
        else:
            if mykey == 'q':
                quit = True
                continue
            elif mykey == '1':
                game(stdscr)
                drawScreen = True
            elif mykey == '2':
                debugUi(stdscr)
                drawScreen = True
            elif mykey == 'KEY_RESIZE':
                #stdscr.addstr(31, 10, 'caught a resize')
                #rows, cols = stdscr.getmaxyx()
                #stdscr.resize(rows, cols)
                #stdscr.addstr(40, 10, "{} Rows {} Columns".format(str(rows), str(cols)))
                continue
            
            #stdscr.addstr(30, 10, "f00")

wrapper(main)

