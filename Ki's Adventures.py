#!/usr/bin/python
#coding: latin-1
#KAd or Ki's Adventures is a mario like game...
#Made By Mrpyfisher199
import curses, time, random
from random import randint as ran
s = curses.initscr() # line 7 to line 26 is curses initiation.
curses.initscr()
curses.start_color()
curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_GREEN)
curses.init_pair(3, curses.COLOR_CYAN,curses.COLOR_BLACK)
curses.init_pair(4, curses.COLOR_WHITE,curses.COLOR_BLACK)
curses.init_pair(5, 9, curses.COLOR_BLACK)
curses.init_pair(6, 227, curses.COLOR_BLACK)
curses.init_pair(7, 209, curses.COLOR_BLACK)
curses.init_pair(8, 130, curses.COLOR_BLACK)
print '\x1b[8;24;80t' #Changes size of screen.
window = curses.newwin(24, 80, 0, 0)
window.timeout(50)
window.keypad(1)
curses.noecho()
curses.curs_set(0)
window.border(0)
print '\x1b[8;24;80t'
dims = window.getmaxyx()
def game(): #game
	dims=[24,80] #size of world
	ls=[] #This is used for the bullets...
	fly=1 #line 30 to line 31 are the jumping variables.
	flys=1
	c=0
	cs=0 # count
	x=21;y=2 # location
	for i in range(20): # Generating the base for the variable ls (line 29)
		ls.append(([' ']*78))
	lev=20 # Level Variables
	levs={1:11, 2:7, 3:6, 4:6, 5:6, 6:5, 7:5, 8:5, 9:4, 10:4, 11:4, 12:3, 13:3, 14:3, 15:2, 16:2, 17:2, 18:1, 19:1, 20:1}
	pause=False # pause variable
	al=ran(4, 66) #location of hill 1
	als=ran(4, 66)	#location fo hill 2
	health=5
	while 1:
		window.erase() # Clearing of the screen
		window.border(0) # The border
		window.addstr(1,1,''.join(['-']*78));window.addstr(22,1,''.join(['#']*78)) # Decoration...
		xs=2 
		for i in ls: # adding ls to the screen
			window.addstr(xs, 1, ''.join(i))
			xs+=1
		window.addstr(0, 35, 'Health: '+str(health)) #health
		window.addstr(21, al,'#############');window.addstr(20,al+3,'#######');window.addstr(19,al+6,'#') # hills
		window.addstr(21, als,'#############');window.addstr(20,als+3,'#######');window.addstr(19,als+6,'#')
		if pause == True:
			window.addstr(12, 23, 'Press Enter to Unpause or Press "q" to exit.') # Display of option in this mode
		window.addstr(x-1, y-1, '\\', curses.color_pair(1));window.addstr(x-1, y, '|', curses.color_pair(3));window.addstr(x-1, y+1, '/', curses.color_pair(8)) #display of character
		window.addstr(x, y-1, '|#|', curses.color_pair(7)) # dicplay of character
		q=window.getch() # checking for input from the user
		if q == ord('\n'): #Pause
			if pause == False:
				pause=True
			elif pause==True:
				pause=False
		if pause == False:
			if y == 77: # If new level
				x=21;y=2
				al=ran(4, 66)
				als=random.randint(4, 66)
				ls=[]
				for i in range(20):
					ls.append(([' ']*78))
				fly=1
				flys=1
				if lev > 1: # if level <= 20
					lev-=1
				else: # else display the screen with the sword.
					while 1: # practically the same while loop like the one before us (line 43) 
						window.erase()
						window.border(0)
						if pause == True:
							window.addstr(12, 23, 'Press Enter to Unpause or Press "q" to exit.')
						window.addstr(1,1,''.join(['-']*78));window.addstr(22,1,''.join(['#']*78))
						window.addstr(x-1, y-1, '\\', curses.color_pair(1));window.addstr(x-1, y, '|', curses.color_pair(3));window.addstr(x-1, y+1, '/', curses.color_pair(8))
						window.addstr(x, y-1, '|#|', curses.color_pair(7))
						window.addstr(21, 40, 'A', curses.color_pair(2))
						window.addstr(20, 40, '!', curses.color_pair(6)) # the sword
						q=window.getch()
						if (x==21 or x==20 or x==19) and (y==39 or y== 40 or y==41):
							window.erase()
							window.border(0)
							window.addstr(12, 35, 'YOU WON!!!', curses.color_pair(6))
							q=window.getch()
							time.sleep(1)
							return
						if q == ord('\n'):
							if pause == False:
								pause=True
							elif pause==True:
								pause=False
						if pause == False:
							if q == curses.KEY_RIGHT and y<77:
								y+=1
							elif q == curses.KEY_LEFT and y > 2:
								y-=1
							elif q == curses.KEY_UP and fly<2:
								fly=2
							if fly>1:
								if flys==1 and c < 5:
									x-=1
									c+=1
								if c == 5:
									flys=2
								if flys==2 and c > 0:
									x+=1
									c-=1
								if c==0:
									fly=1
									flys=1
						else:
							if ord('q') == q:
								return
			if q == curses.KEY_RIGHT and y<77 and (window.instr(x,y+2,1)!='#'): # checking if q is the Right key and there isn't a object in the way.
				y+=1
			elif q == curses.KEY_LEFT and y > 2 and (window.instr(x,y-2,1)!='#'): # checking if q is the Left key and there isn't a object in the way.
				y-=1
			elif q == curses.KEY_UP and fly<2: # Checking whether the user wants to jump or not.
				fly=2
			#The Bug is somewhere here (line 128 to line 147)
			if fly>1: # if the user wants to jump:
				if flys==1 and c < 5: #going up
					x-=1
					c+=1
				if c == 5:
					flys=2
				if flys==2 and c > 0: # going down
					x+=1
					c-=1
					if (window.instr(x+1,y, 1)=='#' or window.instr(x+1,y-1, 1)=='#' or window.instr(x+1,y+1, 1)=='#') and fly>1 and flys==2: # checking wether there is a block under us	
						fly=1
						flys=1
						c=0
				if c==0:
					fly=1
					flys=1
			elif (window.instr(x+1,y, 1)==' ' and window.instr(x+1,y-1, 1)==' ' and window.instr(x+1,y+1, 1)==' ') and fly<2: #checking in wether we need to go down or not.
				c=0
				x+=1
			if ls[x-2][y-1]=='|' or ls[x-2][y-2]=='|' or ls[x-2][y] == '|': #checking for bullets that are hitting us
				if health > 1:
					health-=1
					curses.flash()
					ls[x-2][y-1]=' ';ls[x-2][y-2]=' ';ls[x-2][y]=' '
				else: #Game Over!!!
					curses.beep()
					window.erase()
					window.border(0)
					window.addstr(12, 33, 'Game Over!!!', curses.color_pair(5)) # Game Over!!!
					q=window.getch()
					time.sleep(1)
					return
			if cs == 4: # Making new bullets
				cs=0
				ls.pop()
				ls=[([' ']*78)]+ls
				for i in range(levs[lev]):
					ls[0][ran(0, 77)]='|'
			cs+=1
		else: # if paused
			if ord('q') == q: #if the user want's to quit
				return
def menu(): # menu
	dims = window.getmaxyx() # get size of screen
	ls2 = ['>', '<'] # the one that is selected has a value of ['>', '<']
	ls3 = ['', '']
	g2 = 2 #for color
	g3 = 1
	n = 2
	wt = '' # which option
	while 1: # menu loop
		q = 'f'
		window.erase()
		dims = window.getmaxyx()
		window.border(0)
		#Decoration:
		window.addstr((dims[0]/2)-6, (dims[1]/2)-len('Ki\'s Adventures')/2+1, 'Ki\'s Adventures', curses.color_pair(6))
		window.addstr((dims[0]/2)-1, (dims[1]/2)-len(ls2[0]+'Play Game'+ls2[1])/2, ls2[0]+'Play Game'+ls2[1], curses.color_pair(g2))
		window.addstr((dims[0]/2)+1, (dims[1]/2)-len(ls3[0]+'Quit'+ls3[1])/2, ls3[0]+'Quit'+ls3[1], curses.color_pair(g3))
		q = window.getch()
		if q == curses.KEY_UP: # changing the selected one
			if n > 2:
				n -= 1
		elif q == curses.KEY_DOWN: # changing the selected one
			if n < 3:
				n += 1
		if n == 2: # changing the selected one
			wt = 'g'
			g2 = 2
			g1 = 1
			g3 = 1
			ls2[0], ls2[1] = '>', '<'
			ls3[0], ls3[1] = '', ''
		elif n == 3: # changing the selected one
			wt = 'q'
			g3 = 2
			g1 = 1
			g2 = 1
			ls3[0], ls3[1] = '>', '<'
			ls2[0], ls2[1] = '', ''
		if q == 10: # User pressed "Return"
			if wt == 'g': # game
				game()
			elif wt == 'q': # Exit of game
				c = 0
				while 1:
					curses.endwin()
					return
menu()
