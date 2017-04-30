#!/usr/bin/python
#coding: latin-1

import curses, time, random, os, os.path
if not os.path.isfile('Highscore.txt'):
	file = open('Highscore.txt', 'w')
	file.write('0')
	file.close()
from random import randint as ran
s = curses.initscr()
curses.initscr()
curses.start_color()
curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_GREEN)
curses.init_pair(3, curses.COLOR_CYAN,curses.COLOR_BLACK)
curses.init_pair(4, curses.COLOR_WHITE,curses.COLOR_BLACK)
curses.init_pair(5, 9, curses.COLOR_BLACK)
curses.init_pair(6, 227, curses.COLOR_BLACK)
dims = s.getmaxyx()
window = curses.newwin(dims[0], dims[1], 0, 0)
window.timeout(100)
window.keypad(1)
curses.noecho()
curses.curs_set(0)
window.border(0)
print "\x1b[8;50;70t"
dims = window.getmaxyx()

def game():
	txt = ''
	dims=window.getmaxyx()
	health = 3
	pause = False
	ls = []
	for i in range(dims[0]-2):
		ls.append([' ']*(dims[1]-2))
	x = dims[0]-dims[0]/12
	y = dims[1]/2
	score=1
	pos = 5
	txt1=''
	txt2='@-@-@'
	file = open('Highscore.txt', 'r')
	high = file.read()
	high=int(high)
	count=10
	count1=0
	bb=0
	g5=1
	while 1:
		window.erase()
		window.border(0)
		xs=1
		if health == 2:
			txt2=['#','-@-@']
		elif health == 1:
			txt2=['#-#', '-@']
		if score > high:
			txt1=' +HighScore!!!'
		for i in ls:
			rmp = ''.join(i)
			window.addstr(xs, 1, rmp, curses.color_pair(5))
			xs+=1
		window.addstr(0, dims[1]/2-15, 'BB: '+str(bb)+' BPL: '+str(pos)+' Score: '+str(score)+txt1, curses.color_pair(1))
		if health == 3:
			window.addstr(dims[0]-1, dims[1]/2-7, 'Health |'+txt2+'|', curses.color_pair(g5))
		elif health == 2:
			window.addstr(dims[0]-1, dims[1]/2-7, 'Health | '+txt2[1]+'|', curses.color_pair(g5))
			window.addstr(dims[0]-1, dims[1]/2+1, txt2[0], curses.color_pair(5))
		elif health == 1:
			window.addstr(dims[0]-1, dims[1]/2-7, 'Health |   '+txt2[1]+'|', curses.color_pair(g5))
			window.addstr(dims[0]-1, dims[1]/2+1, txt2[0], curses.color_pair(5))
		window.addstr(x-1, y, '|', curses.color_pair(3))
		window.addstr(x, y-2, '_(+)_', curses.color_pair(3))
		window.addstr(dims[0]/2, dims[1]/2-20, txt, curses.color_pair(1))
		ls78=list(' Star Corridor ')
		for i in range(len(ls78)):
			window.addstr(i+19, 0, ls78[i], curses.color_pair(6))
			window.addstr(i+19, dims[1]-1, ls78[i], curses.color_pair(6))
		q=window.getch()
		if g5==4:
			curses.flash()
			curses.beep()
			g5=1
		if q == 10:
			if pause == False:
				pause = True
			elif pause == True:
				pause = False
				txt = ''
		if pause == False:
			if q == curses.KEY_LEFT and y > 3:
				y-=1
			elif q == curses.KEY_RIGHT and y < dims[1]-4:
				y+=1
			ls[x-2][y-1]=':'
			for ii, i in enumerate(ls):
				for oo, o in enumerate(i):
					if o == ':':
						try:
							ls[ii+1][oo]=' '
							ls[ii][oo]=' '
							ls[ii-2][oo] = ':'
							if ls[ii-1][oo] == '#':
								ls[ii-1][oo]=' '
								ls[ii-2][oo]=' '
								bb+=1
						except Exception:
							ls[ii-2][oo]=' '
					elif o == '#':
						try:
							if (x-1 == ii and y-3 == oo) | (x-1 == ii and y-2 == oo) | (x-1 == ii and y-1 == oo) | (x-1 == ii and y == oo) | (x-1 == ii and y+1 == oo) | (x-2 == ii and y-1 == oo):
								g5=4
								curses.flash()
								curses.beep()
								if health > 1:
									health-=1
								else:
									window.clear()
									window.border(0)
									file = open('Highscore.txt', 'r')
									high = file.read()
									if int(high) < score:
										file = open('Highscore.txt', 'w')
										score=str(score)
										file.write(score)
										txt = '+Highscore!!!'
										file.close()
									while 1:
										window.clear()
										print "\x1b[8;50;70t"
										window.addstr(dims[0]/2, dims[1]/2-5, 'GAME OVER!', curses.color_pair(1))
										window.addstr(dims[0]/2+1, dims[1]/2-7, 'Your Score is '+str(score)+'!', curses.color_pair(1))
										window.addstr(dims[0]/2+2, dims[1]/2-5, txt, curses.color_pair(1))
										window.addstr(dims[0]/2+4, dims[1]/2-5, 'Press Enter', curses.color_pair(1))
										q = window.getch()
										if q == ord('\n'):
											return
						except Exception:
							pass
			if score % 2 == 0:
				if pos > 50:
					window.timeout(90)
				if pos > 100:
					pos += 0.005
					window.timeout(80)
				elif pos > 130:
					pos += 0.001
					window.timeout(70)
				elif pos > 145:
					pos+=0.0005
					window.timeout(60)
				else:
					pos += 0.01
			ls.pop()
			ls3 = []
			for i in range(len(ls[1])):
				altot = ran(0, 150)
				if altot <= pos:
					ls3.append('#')
				elif altot > pos:
					ls3.append(' ')
			ls = [ls3] + ls
			score+=1
		elif pause == True:
			txt = 'Press Enter to UnPause or Press "q" to Quit.'
			if q == ord('q'):
				file = open('Highscore.txt', 'r')
				high = file.read()
				txt = ''
				if int(high) < score:
					file = open('Highscore.txt', 'w')
					score=str(score)
					file.write(score)
					txt = '+Highscore!!!'
					file.close()
				while 1:
					window.clear()
					window.border(0)
					print "\x1b[8;50;70t"
					window.addstr(dims[0]/2, dims[1]/2-5, 'Why End?', curses.color_pair(1))
					window.addstr(dims[0]/2+1, dims[1]/2-8, 'Your Score is '+str(score)+'!', curses.color_pair(1))
					window.addstr(dims[0]/2+2, dims[1]/2-3, txt, curses.color_pair(1))
					window.addstr(dims[0]/2+4, dims[1]/2-6, 'Press Enter', curses.color_pair(1))
					q = window.getch()
					if q == ord('\n'):
						return
		



def menu():
	dims = window.getmaxyx()
	ls2 = ['>', '<']
	ls3 = ['', '']
	g2 = 2
	g3 = 1
	n = 2
	wt = ''
	file=open('Highscore.txt', 'r')
	xsw = file.read()
	while 1:
		print "\x1b[8;50;70t"
		q = 'f'
		dims = window.getmaxyx()
		window.clear()
		window.border(0)
		window.addstr((dims[0]/2)-6, (dims[1]/2)-len('Star Corridor')/2+1, 'Star Corridor', curses.color_pair(6))
		window.addstr((dims[0]/2)-3, (dims[1]/2)-len('Highscore: '+xsw)/2+1, 'Highscore: '+xsw, curses.color_pair(3))
		window.addstr((dims[0]/2)-1, (dims[1]/2)-len(ls2[0]+'Play Game'+ls2[1])/2, ls2[0]+'Play Game'+ls2[1], curses.color_pair(g2))
		window.addstr((dims[0]/2)+1, (dims[1]/2)-len(ls3[0]+'Quit'+ls3[1])/2, ls3[0]+'Quit'+ls3[1], curses.color_pair(g3))
		q = window.getch()
		if q == curses.KEY_UP:
			if n > 2:
				n -= 1
		elif q == curses.KEY_DOWN:
			if n < 3:
				n += 1
		if n == 2:
			wt = 'g'
			g2 = 2
			g1 = 1
			g3 = 1
			ls2[0], ls2[1] = '>', '<'
			ls3[0], ls3[1] = '', ''
		elif n == 3:
			wt = 'q'
			g3 = 2
			g1 = 1
			g2 = 1
			ls3[0], ls3[1] = '>', '<'
			ls2[0], ls2[1] = '', ''
		if q == 10:
			if wt == 's':
				pass
			elif wt == 'g':
				game()
				file=open('Highscore.txt', 'r')
				xsw = file.read()
			elif wt == 'q':
				c = 0
				while 1:
					print "\x1b[8;50;70t"
					window.getch()
					window.clear()
					window.border(0)
					window.addstr((dims[0]/2), (dims[1]/2)-5, 'Thanks for playing!', curses.color_pair(1))
					c+=1
					if c == 5:
						curses.endwin()
						file.close()
						os.system('clear')
						os.system('bash')

menu()

curses.endwin()
