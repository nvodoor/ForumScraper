from flask import Flask, jsonify

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
import time
import string

engine = create_engine('sqlite:///Forum.sqlite');

Base = automap_base()
Base.prepare(engine, reflect=True)

ForumStats = Base.classes.ForumStats;
HourlyStats = Base.classes.HourlyStats;

session = Session(engine);

app = Flask(__name__);

#Create simple front page to describe routes
@app.route("/")
def guidance():
	return (
		f"<h1 style='text-align: center;'>Here are the available routes:</h1>"
		f"<ul style='text-align: center;'><li style='display: inline-block;'>/total</li></br>"
		f"<li style='display: inline-block;'>/daily/:date:</li></br><li style='display: inline-block;'>/hourly/:date:</li></br>"
		f"<li style='display: inline-block;'>specific/total/:forum name:</li></br><li style='display: inline-block;'>specific/daily/:forum name:/:date:</li></br>"
		f"<li style='display: inline-block;'>specific/hourly/:forum name:/:date:</li></br></ul>"
		f"<p style='text-align: center;'>Please enter dates formatted as YYYY-MM-DD</p>"
		f"<p style='text-align: center;'>Strings accepted for search queries.</p>"
	)

@app.route("/total")
def total():
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

	daily = session.query(ForumStats).filter(ForumStats.Date == properdate).filter(ForumStats.name == forum).all()

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
def spechourly(date, forum):

	properdate = date.replace('-', '/');

	hourly = session.query(HourlyStats).filter(HourlyStats.Date == properdate).filter(HourlyStats.name == forum).all()

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
    app.run(debug=True)