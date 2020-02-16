import curses
import sys
import math
from curses import wrapper

def game(stdscr):
    stdscr.clear()
    quit = False
    drawScreen = True
    playField = [
        ['','','X'],
        ['O','',''],
        ['','','']
    ]

    while quit == False:
        rows, cols = stdscr.getmaxyx()
        playFieldXOrigin = math.floor((cols - 5) / 2)
        playFieldYOrigin = 0

        if drawScreen == True:
            for y in range(0,5):
                if y == 1 or y == 3:
                    stdscr.addstr(playFieldYOrigin + y, playFieldXOrigin, "-----")
                else:
                    for x in range(0,5):
                        if x == 1 or x == 3:
                            stdscr.addstr(playFieldYOrigin + y, playFieldXOrigin + x, "|")
                        else:
                            stdscr.addstr(playFieldYOrigin + y, playFieldXOrigin + x, playField[int(y / 2)][int(x / 2)])

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

