import imp
from app import Meter, MeterData, db

import random
import time
import datetime


def random_date(no_dates=1):
    dates = []
    for i in range(no_dates):
        d = random.randint(1, int(time.time()))
        dates.append(datetime.fromtimestamp(d).strftime('%Y-%m-%d'))
    return dates

def populate_meter():
    new_meters = []
    for i in range(10):
       new_meter = Meter(label=f"test label {i}")
       new_meters.append(new_meter)
    db.session.add_all(new_meters)
    db.session.commit()
    

def create_meter_data():
    new_meter_data = []
    dates = random_date(10)
    for meter in Meter.query.all():
        meter_data = MeterData(
            meter_id=meter.id, 
            timestamp=random.choice(dates), 
            value=random.randint(1,100))
        new_meter_data.append(meter_data)
    db.session.add_all(new_meter_data)
    db.session.commit()
