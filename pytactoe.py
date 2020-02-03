import curses
import sys
from curses import wrapper

def debugUi(stdscr):
    stdscr.clear()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    for x in range(0, 10):
        for y in range(0, 10):
            stdscr.addstr(10 + x, 10 + y, str(y), curses.color_pair(x))
        
    
    stdscr.refresh()
    stdscr.nodelay(True)
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
            elif mykey == 'KEY_RESIZE':
                #stdscr.addstr(31, 10, 'caught a resize')
                #rows, cols = stdscr.getmaxyx()
                #stdscr.resize(rows, cols)
                #stdscr.addstr(40, 10, "{} Rows {} Columns".format(str(rows), str(cols)))
                continue
                

            rows, cols = stdscr.getmaxyx()
            stdscr.addstr(rows, 10, "{} Rows {} Columns".format(str(rows), str(cols)))
            stdscr.addstr(rows, 0, mykey)


def main(stdscr):
    stdscr.clear()
    stdscr.nodelay(True)
    origrows, origcols = stdscr.getmaxyx()
    quit = False
    title = 'PyTacToe'
    curses.curs_set(False)
    stdscr.addstr(1, int((origcols - len(title)) / 2), title)
    stdscr.addstr(8, 10, '1) Play a game')
    stdscr.addstr(9, 10, '2) Debugging interface')
    stdscr.addstr(10,10, 'q) Quit' )

    while quit == False:
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
            elif mykey == '2':
                debugUi(stdscr)
            elif mykey == 'KEY_RESIZE':
                #stdscr.addstr(31, 10, 'caught a resize')
                #rows, cols = stdscr.getmaxyx()
                #stdscr.resize(rows, cols)
                #stdscr.addstr(40, 10, "{} Rows {} Columns".format(str(rows), str(cols)))
                continue
                

wrapper(main)

