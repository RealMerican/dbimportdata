import os
import re
import sqlite3
import urllib

#READ ME:
# ecoding: iso-latin-1 | iso 8859 - 1
# files inputs may need to be updated
# update relevant file paths below
# program may run slow if overwriting whole (movies.sqlite) database
# cut file:$ head -1000 actors.list > actors_short.list

#TO DO:
#***import file directly from imdb
#create shell file
#pull numerals out of names
#create user input option for diversity type 

###UPDATE THE BELOW TO DATA STORAGE PATH
dbpath = os.getcwd() + "/db/"
datapath = os.getcwd() + "/data/"

#dbpath = "/Users/eomalle1/Desktop/Database/db/"
#datapath = "/Users/eomalle1/Desktop/Database/data/"

### UPDATE DATABASE NAME BELOW
os.chdir(dbpath)
conn = sqlite3.connect('movies_test.sqlite')
conn.text_factory = str
cur = conn.cursor()

### UPDATE FILE INPUTS BELOW
os.chdir(datapath)
actors = list()
actors.append('actresses_short.list')
actors.append('actors_short.list')
directors = list()
directors.append('directors_short.list')
producers = list()
producers.append('producers_short.list')
writers = list()
writers.append('writers_short.list')
genres = list()
genres.append('genres_short.list')
ratings = list()
ratings.append('mpaa_short.list')
plots = list()
plots.append('plot_short.list')

### CREATING SQL DATABASE ###
cur.executescript('''
DROP TABLE IF EXISTS Actors;
DROP TABLE IF EXISTS Directors;
DROP TABLE IF EXISTS Producers;
DROP TABLE IF EXISTS Writers;
DROP TABLE IF EXISTS Diversity;
DROP TABLE IF EXISTS Genres;
DROP TABLE IF EXISTS Ratings;
DROP TABLE IF EXISTS Plots;

CREATE TABLE Actors (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    year TEXT,
    title TEXT, 
    name TEXT,
    role TEXT);
	
CREATE TABLE Directors (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	name TEXT,
	title TEXT);
	
CREATE TABLE Producers (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	name TEXT,
	title TEXT);
	
CREATE TABLE Writers (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	name TEXT,
	title TEXT);

CREATE TABLE Genres (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	genre TEXT,
	title TEXT);

CREATE TABLE Ratings (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	rating TEXT,
	for TEXT,
	title TEXT);

CREATE TABLE Plots (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	plot TEXT,
	title TEXT);
	
CREATE TABLE Diversity (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	title_id TEXT,
	actor TEXT,
	diversity TEXT);''')


### PULLING IN ACTOR AND ROLE DATA ####
for fname in actors:

	fhand = open(fname)

	for line in fhand:
		#print type(line)
		#pull out records with film data only
		if re.match('^[\t]+', line):
			l = re.findall('^[\t]+(.+)', line.rstrip())
			if len(l) < 1: continue
			else:
				#find title data
				t = re.findall('(^\S.+?)[(]', l[0])
				try:
					t = t.pop(0)
					#t = t.encode('utf-8')
				except:
					t = 'NA'
				#find year 
				y = re.findall('^\S.*?[(]([0-9].+?)[)]', l[0])
				try:
					y = y.pop(0)
					y = y[0:4]
				except:
					y = 'NA'
				#find role data
				r = re.findall('^\S.*[[](.+?)[]]', l[0])
				try: 
					r = r.pop(0)
				except:
					r = 'NA'
				t = t.decode('iso-8859-1')
				r = r.decode('iso-8859-1')

		
		#pull out records with actor and film data
		elif re.findall('^.+', line):
			l = line.strip()
			if len(l) < 1 : continue 
			else:
				#find actor data...need to update to include single names
				a = re.findall('(^.+,.+?)[\t]', l)	
				try:
					a = a.pop(0)	
				except: continue
				#find title data
				t = re.findall('^.*[\t]+(.+?)[(]', l)
				try:
					t = t.pop(0)
				except:
					t = 'NA'

				#find year data
				y = re.findall('^.*?[(]([0-9].+?)[)]', l)
				try:
					y = y.pop(0)
					y = y[0:4]
				except:
					y = 'NA'
				#find role data
				r = re.findall('^.*[[](.+?)[]]', l)
				try:
					r = r.pop(0)
				except:
					r = 'NA'
				try:
					s = a.split(', ')
					s = s.pop(0)
				except:
					s = 'NA'
				try:
					g = a.split(', ')
					g = g.pop(1)
				except:
					g = 'NA'
				#decoding
				a = a.decode('iso-8859-1')	
				s = s.decode('iso-8859-1')
				g = g.decode('iso-8859-1')
				t = t.decode('iso-8859-1')
				r = r.decode('iso-8859-1')
				#generating first/last name structure
				name = g + ' ' + s


		#skip blank lines
		else: continue
	

		cur.execute('''INSERT OR IGNORE INTO Actors (title, year, name, role) 
			  VALUES(?, ?, ?, ?)''', (t, y, name, r ) )
		print name, y, t	
	conn.commit()

l = None
a = None
s = None
g = None
t = None
r = None
y = None
n = None
name = None
h = None
f = None

### PULLING DIRECTOR DATA ####
for fname in directors:

	fhand = open(fname)

	for line in fhand:
		#print type(line)
		#pull out records with film data only
		if re.match('^[\t]+', line):
			l = re.findall('^[\t]+(.+)', line.rstrip())
			if len(l) < 1: continue
			else:
				#find title data
				t = re.findall('(^\S.+?)[(]', l[0])
				try:
					t = t.pop(0)
				except:
					t = 'NA'
				#set role data
				t = t.decode('iso-8859-1')

		
		#pull out records with name and film data
		elif re.findall('^.+', line):
			l = line.strip()
			if len(l) < 1 : continue 
			else:
				#find name data...need to update to include single names
				n = re.findall('(^.+,.+?)[\t]', l)	
				try:
					n = n.pop(0)	
				except: continue
				#find title data
				t = re.findall('^.*[\t]+(.+?)[(]', l)
				try:
					t = t.pop(0)
				except:
					t = 'NA'
				#getting surname
				try:
					s = n.split(', ')
					s = s.pop(0)
				except:
					s = 'NA'
				#getting given name
				try:
					g = n.split(', ')
					g = g.pop(1)
				except:
					g = 'NA'
				#decoding
				n = n.decode('iso-8859-1')	
				s = s.decode('iso-8859-1')
				g = g.decode('iso-8859-1')
				t = t.decode('iso-8859-1')
				#generating first/last name structure
				name = g + ' ' + s


		#skip blank lines
		else: continue
	

		cur.execute('''INSERT OR IGNORE INTO Directors (title, name) 
			  VALUES(?, ?)''', (t, name) )
		print name, t	
	conn.commit()

l = None
a = None
s = None
g = None
t = None
r = None
y = None
n = None
name = None
h = None
f = None

### PULLING PRODUCER DATA ####
for fname in producers:

	fhand = open(fname)

	for line in fhand:
		#print type(line)
		#pull out records with film data only
		if re.match('^[\t]+', line):
			l = re.findall('^[\t]+(.+)', line.rstrip())
			if len(l) < 1: continue
			else:
				#find title data
				t = re.findall('(^\S.+?)[(]', l[0])
				try:
					t = t.pop(0)
				except:
					t = 'NA'
				#set role data
				t = t.decode('iso-8859-1')

		
		#pull out records with name and film data
		elif re.findall('^.+', line):
			l = line.strip()
			if len(l) < 1 : continue 
			else:
				#find name data...need to update to include single names
				n = re.findall('(^.+,.+?)[\t]', l)	
				try:
					n = n.pop(0)	
				except: continue
				#find title data
				t = re.findall('^.*[\t]+(.+?)[(]', l)
				try:
					t = t.pop(0)
				except:
					t = 'NA'
				#getting surname
				try:
					s = n.split(', ')
					s = s.pop(0)
				except:
					s = 'NA'
				#getting given name
				try:
					g = n.split(', ')
					g = g.pop(1)
				except:
					g = 'NA'
				#decoding
				n = n.decode('iso-8859-1')	
				s = s.decode('iso-8859-1')
				g = g.decode('iso-8859-1')
				t = t.decode('iso-8859-1')
				#generating first/last name structure
				name = g + ' ' + s


		#skip blank lines
		else: continue
	

		cur.execute('''INSERT OR IGNORE INTO Producers (title, name) 
			  VALUES(?, ?)''', (t, name) )
		print name, t	
	conn.commit()

l = None
a = None
s = None
g = None
t = None
r = None
y = None
n = None
name = None
h = None
f = None

### PULLING WRITER DATA ####
for fname in writers:

	fhand = open(fname)

	for line in fhand:
		#print type(line)
		#pull out records with film data only
		if re.match('^[\t]+', line):
			l = re.findall('^[\t]+(.+)', line.rstrip())
			if len(l) < 1: continue
			else:
				#find title data
				t = re.findall('(^\S.+?)[(]', l[0])
				try:
					t = t.pop(0)
				except:
					t = 'NA'
				#set role data
				t = t.decode('iso-8859-1')

		
		#pull out records with name and film data
		elif re.findall('^.+', line):
			l = line.strip()
			if len(l) < 1 : continue 
			else:
				#find name data...need to update to include single names
				n = re.findall('(^.+,.+?)[\t]', l)	
				try:
					n = n.pop(0)	
				except: continue
				#find title data
				t = re.findall('^.*[\t]+(.+?)[(]', l)
				try:
					t = t.pop(0)
				except:
					t = 'NA'
				#getting surname
				try:
					s = n.split(', ')
					s = s.pop(0)
				except:
					s = 'NA'
				#getting given name
				try:
					g = n.split(', ')
					g = g.pop(1)
				except:
					g = 'NA'
				#decoding
				n = n.decode('iso-8859-1')	
				s = s.decode('iso-8859-1')
				g = g.decode('iso-8859-1')
				t = t.decode('iso-8859-1')
				#generating first/last name structure
				name = g + ' ' + s


		#skip blank lines
		else: continue
	

		cur.execute('''INSERT OR IGNORE INTO Writers (title, name) 
			  VALUES(?, ?)''', (t, name) )
		print name, t	
	conn.commit()

l = None
a = None
s = None
g = None
t = None
r = None
y = None
n = None
name = None
h = None
f = None
		
### PULLING GENRE DATA ####
for fname in genres:

	fhand = open(fname)

	for line in fhand:
		#print type(line)
		#pull out records with film data only
		if re.findall('^.+', line):
			l = line.strip()
			if len(l) < 1 : continue 
			else:
				#find title data
				t = re.findall('(^.*)[(]', l)	
				try:
					t = t.pop(0)	
				except: continue
				#find genre data
				g = re.findall('^.*[\t]+(.+)', l)
				try:
					g = g.pop(0)
				except:
					g = 'NA'
				#decoding
				t = t.decode('iso-8859-1')	
				g = g.decode('iso-8859-1')

		#skip blank lines
		else: continue
	

		cur.execute('''INSERT OR IGNORE INTO Genres (genre, title) 
			  VALUES(?, ?)''', (g, t) )
		print g, t
	conn.commit()
print 'done'

l = None
a = None
s = None
g = None
t = None
r = None
y = None
n = None
name = None
h = None
f = None

### PULLING RATINGS DATA ####
for fname in ratings:

	fhand = open(fname)
	t = None
	f = None
	
	for line in fhand:
		
		try: 
			line.split(":")
		except: 
			continue
		if line.split(":")[0] == 'MV':
			print 'title: ',t, 'rating: ', r, 'for: ', f
			cur.execute('''INSERT OR IGNORE INTO Ratings (rating, for, title) 
 			  VALUES(?, ?, ?)''', (r, f, t) )
			f = None
			f = str()
			h = None
			t = re.findall('MV:\s(.+?)\s+[(]', line)
			t = t.pop(0)
			t = t.decode('iso-8859-1')
		elif line.split(":")[0] == 'RE':
			h = re.findall('RE:\s(.*)', line)
			h = h.pop(0)
			f = f + h
			r = re.findall('Rated\s(.+?)\s', f)
			r = r.pop(0)
			r = r.decode('iso-8859-1')
		else: continue

	

	
	conn.commit()

l = None
a = None
s = None
g = None
t = None
r = None
y = None
n = None
name = None
h = None
f = None

### PULLING PLOT DATA ###
for fname in plots:

	fhand = open(fname)
	t = None
	p = None
	
	for line in fhand:
		
		try: 
			line.split(":")
		except: 
			continue
		if line.split(":")[0] == 'MV':
			print 'TITLE: ',t, 'PLOT: ', p 
			cur.execute('''INSERT OR IGNORE INTO Plots (plot, title) 
 			  VALUES(?, ?)''', (p, t) )
			p = None
			p = str()
			h = None
			t = re.findall('MV:\s(.+?)\s+[(]', line)
			t = t.pop(0)
			t = t.decode('iso-8859-1')
		elif line.split(":")[0] == 'PL':
			h = re.findall('PL:\s(.*)', line)
			h = h.pop(0)
			p = p + h
		else: continue

	

	
	conn.commit()

l = None
a = None
s = None
g = None
t = None
r = None
y = None
n = None
name = None
h = None
f = None
p = None



#### TO DO: ########
#IMPORT RELEASE DATE DATA
# UNDERSTAND DUPS
# use plot/ratings ex?
#view for the titles table
#create a sql example that will pull from the title table
# & associated persons table (and other relevant)



#GOALS:
	#IMPROT MOVIES, SUMMARY, YEAR, ETC.
	#SET RAW_INPUT FUNCTION FOR ENTERING ACTOR/FILM DIVERSITY
	#Group maintained db?

