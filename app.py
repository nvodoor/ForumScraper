from flask import Flask, jsonify
from flask_cors import CORS

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
import time
import string

engine = create_engine('sqlite:///Forum.sqlite');
# engine = create_engine('postgres://forum:forum@localhost/forum')

Base = automap_base()
Base.prepare(engine, reflect=True)

ForumStats = Base.classes.ForumStats;
HourlyStats = Base.classes.HourlyStats;
Users = Base.classes.Users;

session = Session(engine);

app = Flask(__name__);
#ALLOWS CORS Access
CORS(app);

#Create simple front page to describe routes
@app.route("/")
def guidance():
	return (
		f"<h1 style='text-align: center;'>Here are the available routes:</h1>"
		f"<ul style='text-align: center;'><li style='display: inline-block;'>/total</li></br>"
		f"<li style='display: inline-block;'>/daily/:date:</li></br><li style='display: inline-block;'>/hourly/:date:</li></br>"
		f"<li style='display: inline-block;'>specific/total/:forum name:</li></br><li style='display: inline-block;'>specific/daily/:date:/:forum name:</li></br>"
		f"<li style='display: inline-block;'>specific/hourly/:date:/:forum name:</li></br></ul>"
		f"<p style='text-align: center;'>Please enter dates formatted as YYYY-MM-DD</p>"
		f"<p style='text-align: center;'>Strings accepted for search queries.</p>"
	)

@app.route("/total+<string:username>+<string:password>")
def total(username,password):
	if session.query(Users).filter(Users.username == username).filter(Users.password == password).all():
		dates = (time.strftime("%Y/%m/%d"))

		totals = session.query(ForumStats).filter(ForumStats.Date == dates).all()

		#ttd is short for total to date
		ttd = [];

		for row in totals:
			totaldict = {};
			totaldict['name'] = row.name;
			totaldict['Messages'] = row.Messages;
			totaldict['Threads']= row.Threads;
			totaldict['Members'] = row.Members;
			ttd.append(totaldict);

		return jsonify(ttd);
	else:
		return (
			f"<p>Nothing to see here.</p>"
			)

@app.route("/daily/<string:date>")
def daily(date):

	properdate = date.replace('-', '/');

	daily = session.query(ForumStats).filter(ForumStats.Date == properdate).all()

	#dtd is short for daily to date
	dtd = [];

	for row in daily:
		totaldaily = {};
		totaldaily['name'] = row.name;
		totaldaily['Messages'] = row.Messages;
		totaldaily['Threads'] = row.Threads;
		totaldaily['Members'] = row.Members;
		dtd.append(totaldaily);

	return jsonify(dtd);

@app.route("/hourly/<string:date>")
def hourly(date):

	properdate = date.replace('-', '/');

	hourly = session.query(HourlyStats).filter(HourlyStats.Date == properdate).all()

	#hod is short for hourly on date
	hod = [];

	for row in hourly:
		totalhourly = {};
		totalhourly['name'] = row.name;
		totalhourly['Messages'] = row.Messages;
		totalhourly['Threads'] = row.Threads;
		totalhourly['Members'] = row.Members;
		hod.append(totalhourly);

	return jsonify(hod);

@app.route("/specific/total/<string:forum>")
def spectotal(forum):
	dates = (time.strftime("%Y/%m/%d"))

	totals = session.query(ForumStats).filter(ForumStats.Date == dates).filter(ForumStats.name == forum).all()

	#ttd is short for total to date
	ttd = [];

	for row in totals:
		totaldict = {};
		totaldict['name'] = row.name;
		totaldict['Messages'] = row.Messages;
		totaldict['Threads']= row.Threads;
		totaldict['Members'] = row.Members;
		ttd.append(totaldict);

	return jsonify(ttd);

@app.route("/specific/daily/<string:date>/<string:forum>")
def specdaily(date, forum):

	properdate = date.replace('-', '/');
	print(date);
	print(forum);

	daily = session.query(ForumStats).filter(ForumStats.Date == properdate).filter(ForumStats.name == forum).all()
	print(daily);

	#dtd is short for daily to date
	dtd = [];

	for row in daily:
		totaldaily = {};
		totaldaily['name'] = row.name;
		totaldaily['Messages'] = row.Messages;
		totaldaily['Threads'] = row.Threads;
		totaldaily['Members'] = row.Members;
		dtd.append(totaldaily);

	return jsonify(dtd);

@app.route("/specific/hourly/<string:date>/<string:forum>")
def spechourly(forum, date):

	properdate = date.replace('-', '/');
	print(date);
	print(forum);
	print(properdate);

	hourly = session.query(HourlyStats).filter(HourlyStats.Date == properdate).filter(HourlyStats.name == forum).all()
	print(daily);
	#hod is short for hourly on date
	hod = [];

	for row in hourly:
		totalhourly = {};
		totalhourly['name'] = row.name;
		totalhourly['Messages'] = row.Messages;
		totalhourly['Threads'] = row.Threads;
		totalhourly['Members'] = row.Members;
		hod.append(totalhourly);

	return jsonify(hod);

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=3134)