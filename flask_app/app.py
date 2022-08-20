
"""Simple app to list and retrieve data a related to a meter check."""

from flask import Flask, jsonify
from flask import render_template

from flask_sqlalchemy import SQLAlchemy
import random
import time
from datetime import datetime

# intial setup

app = Flask(__name__)
db = SQLAlchemy(app)

# We can move these types confidential informations into .env or .ini files.
app.config['SECRET_KEY']='secret'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///meter.db'


# Models

class Meter(db.Model):
	"""
	Model to store meters.

	Attributes:
		id(int)			: Id of the object.
		label(string)	: Label name of the meter.
	"""

	id = db.Column(db.Integer, primary_key=True, index=True)
	label = db.Column(db.String(50), unique=True)

	def __repr__(self):
		"""Object representation as string."""
		return f'{self.label} : {self.id}'


class MeterData(db.Model):
	"""
	Model to store meter  related information.

	Attributes:
		id(int)				: Id of the object.
		meter_id(fk)		: Id of the meter object.
		timestamp(datetime)	:Meter data added date.
		value(int)			: Reading in value in the meter.
	"""

	id = db.Column(db.Integer, primary_key=True, index=True)
	meter_id = db.Column(db.Integer, db.ForeignKey('meter.id'))
	timestamp = db.Column(db.DateTime, default=datetime.utcnow)
	value = db.Column(db.Integer)
	
	def __repr__(self):
		"""Object representation as string."""
		return f'Meter - {self.meter_id} : {self.timestamp}'\
			f': {self.value} : {self.id}'


# Urls and attached functions

@app.route('/add/fake-data/')
def populate_models():
	"""Function populates meter and meter_data models."""
	try:
		populate_meter()
		populate_meter_data()
	except:
		return {"message": "Fake data population failed"}, 400
	return {"message": "Fake data populated successfully"}

@app.route('/meters/list/')
def get_meters():
	"""Function lists all meters used in this app as json response."""
	return jsonify([
		{
			'id': meter.id, 
            'label': meter.label
			} for meter in Meter.query.all()
	])

@app.route('/meters/')
def get_meters_clickable():
	"""Function redirects to meters list html."""
	meters = Meter.query.all()
	return render_template('meters.html', meters=meters)
		
@app.route('/meters/<id>/')
def get_meter(id):
	"""
	Function returns all meter_data under a specific meter.
	(meter id is passed as parameter.)
	"""
	meter_datas = MeterData.query.filter_by(
		meter_id=id).order_by(MeterData.timestamp.desc())
	data =  jsonify([
		{
			'id': meter_data.id, 
            'timestamp': meter_data.timestamp, 
			'value': meter_data.value
			} for meter_data in meter_datas
	])
	return data


# Utility functions.

def random_date(no_dates=1):
	"""Function generates random dates."""
	dates = []
	for i in range(no_dates):
		d = random.randint(1, int(time.time()))
		dates.append(datetime.fromtimestamp(d))
	return dates

def populate_meter():
	"""Function populates meter model."""
	new_meters = []
	for i in range(1,11):
		new_meter = Meter(label=f"test label {i}")
		new_meters.append(new_meter)
	db.session.add_all(new_meters)
	db.session.commit()
    

def populate_meter_data():
	"""Function populates meter_data model."""
	new_meter_data = []
	dates = random_date(100)
	print(dates)
	for meter in Meter.query.all():
		for i in range(5):
			meter_data = MeterData(
				meter_id=meter.id, 
				timestamp=random.choice(dates), 
				value=random.randint(1,100))
			new_meter_data.append(meter_data)
	db.session.add_all(new_meter_data)
	db.session.commit()

if __name__ == '__main__':
	app.run()
