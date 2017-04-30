#!/usr/bin/python
#coding: latin-1

#A Game of Tag...

import socket, curses, time, os
from random import randint as ran

print '\x1b[8;24;80t'
print 'Please don\'t change the window size.'
time.sleep(0.5)

def Gameh(s):
	print '\x1b[8;24;80t'
	dims=(24, 80)
	world=[]
	for i in range(dims[0]-2):
		world.append([' ']*(dims[1]-2))
	clients=[]
	clientyxy={}
	yxylook={}
	q=-1
	while 1:
		window.border(0)
		try:
			data,addr=s.recvfrom(1024)
			window.erase()
			window.border(0)
			world=[]
			for i in range(dims[0]-2):
				world.append([' ']*(dims[1]-2))
			if addr not in clients:
				clients.append(addr)
				clientyxy[addr]=str(data).split('|')[0]
				yxylook[clientyxy[addr]]=str(data).split('|')[1]
				txt=str(data).split('|')[0]
				s.sendto('', addr)
			elif str(data) == 'q':
				clients.remove(addr)
				del	yxylook[clientyxy[addr]]
				del clientyxy[addr]
			elif len(str(data).split('|')[0].split(':')) == 2:
				clientyxy[addr]=str(data).split('|')[0]
				yxylook[str(data).split('|')[0]]=str(data).split('|')[1]
			objectz=[]
			xy=[]
			for i in clientyxy:
				xy.append(clientyxy[i]);i=clientyxy[i].split(':');i[0], i[1] = int(i[0]), int(i[1]);objectz.append([i[0]-1, i[1]-1])
			for i in objectz:
				try:
					world[i[0]][i[1]] = yxylook[str(i[0]+1)+':'+str(i[1]+1)]
				except Exception:
					pass
			for i in clients:
				txt=[]
				for l in clientyxy:
					if l != i:
						try:
							txt.append(clientyxy[l]+'|'+yxylook[clientyxy[l]])
						except Exception:
							pass
				s.sendto(';'.join(txt), i)
			try:
				for i in clientyxy:
					if i != addr and clientyxy[i] == clientyxy[addr]:
						s.sendto('$', addr)
						s.sendto('q', i)
						clients.remove(i)
						del	yxylook[clientyxy[addr]]
						del clientyxy[i]
						for f in clients:
							txt=[]
							for l in clientyxy:
								if l != f:
									txt.append(clientyxy[l]+'|'+yxylook[clientyxy[l]])
							s.sendto(';'.join(txt), i)
				clientyxy[('127.1.1.1', 7899)]='10:10'
				yxylook['10:10']=' '
				dims=(24, 80)
				objectz=[]
				xy=[]
				for i in clientyxy:
					xy.append(clientyxy[i]);i=clientyxy[i].split(':');i[0], i[1] = int(i[0]), int(i[1]);objectz.append([i[0]-1, i[1]-1])
				for i in objectz:
					try:
						world[i[0]][i[1]] = yxylook[str(i[0]+1)+':'+str(i[1]+1)]
					except Exception:
						pass
				for i in clients:
					txt=[]
					for l in clientyxy:
						if l != i and l != '127.1.1.1':
							txt.append(clientyxy[l]+'|'+yxylook[clientyxy[l]])
					s.sendto(';'.join(txt), i)
			except Exception as e:
				pass
			xs=1
			for i in world:
				window.addstr(xs, 1, ''.join(i), curses.color_pair(5))
				xs+=1
		except socket.error:
			pass
		q=window.getch()
		if q == ord('q'):
			for i in clients:
				s.sendto('r', i)
			return
def Gamec(server,s,look):
	print '\x1b[8;24;80t'
	dims=(24, 80)
	x,y=ran(1, 22),ran(1,78)
	s.sendto(str(x)+':'+str(y)+'|'+look[1], server)
	world=[]
	objectz=[]
	yxylook={}
	for i in range(dims[0]-2):
		world.append([' ']*(dims[1]-2))
	txt=''
	kills=0
	while 1:
		window.erase()
		window.border(0)
		window.addstr(12, 33, 'Connecting...')
		q=window.getch()
		if q == ord('q'):
			return
		try:
			data, addr = s.recvfrom(1024)
			if str(data) != '':
				objects=str(data).split(';')
				objectz=[]
				for i in objects:
					il=i.split('|')[0];yxylook[il]=i.split('|')[1];i=i.split('|')[0].split(':');i[0], i[1] = int(i[0]), int(i[1]);objectz.append([i[0]-1, i[1]-1])
			txt='Players Online: '+str(len(objectz)+1)
			break
		except Exception:
			s.sendto(str(x)+':'+str(y)+'|'+look[1], server)
	latest=-1
	while 1:
		txt='Players Online: '+str(len(objectz))+' Kills: '+str(kills)
		for i in objectz:
			world[i[0]][i[1]] = yxylook[str(i[0]+1)+':'+str(i[1]+1)]
		window.erase()
		window.border(0)
		window.addstr(0, 27, txt)
		xs=1
		for i in world:
			window.addstr(xs, 1, ''.join(i), curses.color_pair(5))
			xs+=1
		window.addstr(x, y, look[1], curses.color_pair(look[0]))
		q=window.getch()
		if q == curses.KEY_UP and x>1 and latest==-1:
			x-=1
			s.sendto(str(x)+':'+str(y)+'|'+look[1], server)
		elif q == curses.KEY_DOWN and x<dims[0]-2 and latest==-1:
			x+=1
			s.sendto(str(x)+':'+str(y)+'|'+look[1], server)
		elif q == curses.KEY_LEFT and y>1 and latest==-1:
			y-=1
			s.sendto(str(x)+':'+str(y)+'|'+look[1], server)
		elif q == curses.KEY_RIGHT and dims[1]-2>y and latest==-1:
			y+=1
			s.sendto(str(x)+':'+str(y)+'|'+look[1], server)
		elif q == ord('q'):
			s.sendto('q', server)
			return
		latest=q
		try:
			data, addr = s.recvfrom(1024)
			if str(data) == 'q':
				tl=1
				while tl==1:
					window.erase()
					window.border(0)
					window.addstr(12, 36, 'Game Over!!!')
					window.addstr(13, 21, 'Enter "q" to Quit Or Press Enter to Play Again.')
					q=window.getch()
					if q == ord('\n'):
						x,y=ran(1, 22),ran(1,78)
						s.sendto(str(x)+':'+str(y)+'|'+look[1], server)
						world=[]
						objectz=[]
						for i in range(dims[0]-2):
							world.append([' ']*(dims[1]-2))
						txt=''
						kills=0
						while 1:
							window.erase()
							window.border(0)
							window.addstr(12, 33, 'Connecting...')
							q=window.getch()
							if q == ord('q'):
								return
							try:
								data, addr = s.recvfrom(1024)
								if str(data) != '':
									objects=str(data).split(';')
									objectz=[]
									for i in objects:
										il=i.split('|')[0];yxylook[il]=i.split('|')[1];i=i.split('|')[0].split(':');i[0], i[1] = int(i[0]), int(i[1]);objectz.append([i[0]-1, i[1]-1])
									txt='Players Online: '+str(len(objectz)+1)
									tl=5
									break
							except socket.error:
								s.sendto(str(x)+':'+str(y)+'|'+look[1], server)
					elif q == ord('q'):
						return
				tl=1
				while tl==1:
					if 1+1>1:
						x,y=ran(1, 22),ran(1,78)
						s.sendto(str(x)+':'+str(y)+'|'+look[1], server)
						world=[]
						objectz=[]
						for i in range(dims[0]-2):
							world.append([' ']*(dims[1]-2))
						txt=''
						kills=0
						while 1:
							window.erase()
							window.border(0)
							window.addstr(12, 33, 'Connecting...')
							q=window.getch()
							if q == ord('q'):
								return
							try:
								data, addr = s.recvfrom(1024)
								if str(data) != '':
									objects=str(data).split(';')
									objectz=[]
									for i in objects:
										il=i.split('|')[0];yxylook[il]=i.split('|')[1];i=i.split('|')[0].split(':');i[0], i[1] = int(i[0]), int(i[1]);objectz.append([i[0]-1, i[1]-1])
									txt='Players Online: '+str(len(objectz)+1)
									tl=5
									break
							except socket.error:
								s.sendto(str(x)+':'+str(y)+'|'+look[1], server)
					elif q == ord('q'):
						return
			if str(data) == 'r':
				window.erase()
				window.border(0)
				window.addstr(12, 33, 'Connecting...')
				q=window.getch()
				while 1:
					window.erase()
					window.border(0)
					window.addstr(12, 33, 'Connecting...')
					q=window.getch()
					if q == ord('q'):
						return
					s.sendto(str(x)+':'+str(y)+'|'+look[1], server)
					try:
						data, addr = s.recvfrom(1024)
						if str(data) != '':
							objects=str(data).split(';')
							objectz=[]
							for i in objects:
								il=i.split('|')[0];yxylook[il]=i.split('|')[1];i=i.split('|')[0].split(':');i[0], i[1] = int(i[0]), int(i[1]);objectz.append([i[0]-1, i[1]-1])
							break
					except Exception as e:
						s.sendto(str(x)+':'+str(y)+'|'+look[1], server)
			elif str(data) != '':
				if '$' == str(data):
					kills+=1
				else:
					objects=str(data).split(';')
					objectz=[]
					for i in objects:
						il=i.split('|')[0];yxylook[il]=i.split('|')[1];i=i.split('|')[0].split(':');i[0], i[1] = int(i[0]), int(i[1]);objectz.append([i[0]-1, i[1]-1])
				world=[]
				for i in range(dims[0]-2):
					world.append([' ']*(dims[1]-2))
			else:
				world=[]
				for i in range(dims[0]-2):
					world.append([' ']*(dims[1]-2))
		except socket.error as e:
			if str(e) == 'timed out':
				pass
			else:
				raise e
sc = raw_input('Enter "s" if you wan\'t to be the host of the game,\nOr enter "c" if you wan\'t to be a client.\n> ')
while sc != 's' and sc != 'c':
	sc = raw_input('Enter "s" if you wan\'t to be the host of the game,\nOr enter "c" if you wan\'t to be a client.\n> ')
if sc == 'c':
	ylook=raw_input('Do you want to customize your character?(y/n)\n> ')
	look=[]
	if ylook=='y':
		ycolor=raw_input('What Color? [Default (Gold) = 1, Blue = 2, Green = 3, White = 4]\n> ')
		if ycolor == '1' or ycolor not in ('2', '3', '4'):
			look.append(6)
		elif ycolor == '2':
			look.append(3)
		elif ycolor == '3':
			look.append(1)
		elif ycolor == '4':
			look.append(4)
		ybody=raw_input('What should your body look like (One Character Long)\n> ')
		while len(ybody) > 1:
			ybody=raw_input('What should your body look like (One Character Long)\n> ')
		if len(ybody)<1 or ybody == '|' or ybody == ';' or ybody == ':':
			look.append('+')
		else:
			look.append(ybody)
	else:
		look=[6, '+']
	server = raw_input('Enter server ip:port (Example: 127.0.0.1:5000)\n> ').split(':');server[1]=int(server[1]);server=tuple(server)
	host = '0.0.0.0'
	port = 0
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.bind((host, port))
	curses.initscr()
	curses.start_color()
	curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
	curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_GREEN)
	curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)
	curses.init_pair(4, curses.COLOR_WHITE,curses.COLOR_BLACK)
	curses.init_pair(5, 9, curses.COLOR_BLACK)
	curses.init_pair(6, 227, curses.COLOR_BLACK)
	window = curses.newwin(24, 80, 0, 0)
	window.timeout(24)
	window.keypad(1)
	curses.noecho()
	curses.curs_set(0)
	window.border(0)
	s.settimeout(0.01)
	Gamec(server,s,look)
	curses.endwin()
	print 'Ending...'
	s.close()
else:
	port = 5000
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("8.8.8.8", 80))
	host=s.getsockname()[0]
	s.close()
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.bind((host,port))
	print 'Hosting On: '+host+':'+str(port)
	jhg=raw_input('Enter Any Key to Continue\n> ')
	curses.initscr()
	curses.start_color()
	curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
	curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_GREEN)
	curses.init_pair(3, curses.COLOR_CYAN,curses.COLOR_BLACK)
	curses.init_pair(4, curses.COLOR_WHITE,curses.COLOR_BLACK)
	curses.init_pair(5, 9, curses.COLOR_BLACK)
	curses.init_pair(6, 227, curses.COLOR_BLACK)
	window = curses.newwin(24, 80, 0, 0)
	window.timeout(6)
	window.keypad(1)
	curses.noecho()
	curses.curs_set(0)
	window.border(0)
	s.settimeout(0.01)
	Gameh(s)
	curses.endwin()
	print 'Ending...'
	s.close()