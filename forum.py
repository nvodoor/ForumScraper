import threading
from classXen import Xen
from classVB import VB 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import time

Smash = Xen('http://www.smashboards.com/');
FoH = Xen('http://www.firesofheaven.org/');
Force = Xen('http://boards.theforce.net/');
Sherdog = Xen('http://forums.sherdog.com/');
DigitalPoint = Xen('http://forums.digitalpoint.com/');
DawgShed = Xen('http://www.dawgshed.com/');
Christian = Xen('http://www.christianforums.com/forums/');
Space = Xen('http://forums.spacebattles.com/')
BigFooty = Xen('http://www.bigfooty.com/forum');

Base = declarative_base();

engine = create_engine('sqlite:///Forum.sqlite')
Base.metadata.create_all(engine)
session = Session(bind=engine)

class Forum(Base):
	__tablename__ = 'ForumStats'

	id=Column(Integer, primary_key=True);
	name=Column(String)
	Messages=Column(Integer)
	Threads=Column(Integer)
	Members=Column(Integer)
	Date=Column(String)

	def __repr__(self):
		return self.name

class Hourly(Base):
	__tablename__ = 'HourlyStats'

	id=Column(Integer, primary_key=True);
	name=Column(String)
	Messages=Column(Integer)
	Threads=Column(Integer)
	Members=Column(Integer)
	Date=Column(String)

	def __repr__(self):
		return self.name

engine = create_engine('sqlite:///Forum.sqlite')
Base.metadata.create_all(engine)
session = Session(bind=engine)

forumarr = [Smash, FoH, Force, Sherdog, DigitalPoint, DawgShed, Christian, Space, BigFooty];
forumnames = ['SmashBoards', 'FoH', 'Force', 'Sherdog', 'DigitalPoint', 'DawgShed', 'Christian', 'Space', 'BigFooty'];


tables = engine.execute("SELECT * FROM sqlite_master WHERE TYPE='table'")
for index, table in enumerate(tables):
    table_name = table[1]
    print(f"The #{index} table in the database is called '{table_name}'.")

conn = engine.connect();

forumname = {};

def total():
	
	index = 0
	for name in forumarr:
		try:
			name.retrieve()
			# print(forumnames[index]);
			name.messageCount(forumname, forumnames[index]);
			name.discussionCount(forumname, forumnames[index]);
			name.memberCount(forumname, forumnames[index]);
			index += 1;
		except:
			print("Forum is down.")


	NeoGAF = VB('http://www.neogaf.com/forum')

	NeoGAF.retrieve()

	NeoGAF.totals(forumname, 'NeoGAF');

	# print(forumname);

	date = (time.strftime("%Y/%m/%d"))

	# print(date);
	# print(type(date));



	neo_gaf=Forum(name='NeoGAF', Messages=forumname['NeoGAFmessages'], Threads=forumname['NeoGAFdiscussions'], Members=forumname['NeoGAFmembers'], Date=date);

	session.add(neo_gaf);
	session.commit();

	for name in forumnames:
		try:
			forumadd = Forum(name=name, Messages=forumname[name+'message'], Threads=forumname[name+'discussions'], Members=forumname['NeoGAFmembers'], Date=date);
			session.add(forumadd);
			session.commit();
		except:
			print("Could not add to database.")

	print("total")
	threading.Timer(86400, total).start()

total();

forumtotalsaccumulate = {}
forumtotalsnew = {}

def accumulate():
	accindex = 0;
	# print(accindex);
	for name in forumarr:
		try:
			name.retrieve()
			# print(forumnames[accindex]);
			name.messageCount(forumtotalsnew, forumnames[accindex]);
			name.discussionCount(forumtotalsnew, forumnames[accindex]);
			name.memberCount(forumtotalsnew, forumnames[accindex]);
			accindex += 1;
		except:
			"Forum is down."

	NeoGAF = VB('http://www.neogaf.com/forum');
	
	NeoGAF.retrieve()
	NeoGAF.totals(forumtotalsnew, 'NeoGAF');

	date = (time.strftime("%Y/%m/%d"))

	for k,v in forumname.items():
		forumtotalsaccumulate[k] = forumtotalsnew[k] - v;

	# print (forumtotalsaccumulate)

	neo_gaf=Hourly(name='NeoGAF', Messages=forumtotalsaccumulate['NeoGAFmessages'], Threads=forumtotalsaccumulate['NeoGAFdiscussions'], Members=forumtotalsaccumulate['NeoGAFmembers'], Date=date);

	session.add(neo_gaf);
	session.commit();

	for name in forumnames:
		try:
			forumadd = Hourly(name=name, Messages=forumtotalsaccumulate[name+'message'], Threads=forumtotalsaccumulate[name+'discussions'], Members=forumtotalsaccumulate['NeoGAFmembers'], Date=date);
			session.add(forumadd);
			session.commit();
		except:
			print("could not add to database.")

	print("hourly")
	threading.Timer(3600, accumulate).start();



accumulate();

