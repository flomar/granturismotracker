import os
import re
from datetime import datetime
from decimal import Decimal
from hashlib import sha256
from pathlib import Path
from peewee import *
import bottle


database = SqliteDatabase("granturismotracker.sqlite", pragmas={"foreign_keys": 1, "encoding": "UTF8"})


class Event(Model):
    id = AutoField()
    date_time = DateTimeField()
    class Meta:
        database = database


class Driver(Model):
    id = AutoField()
    name = TextField(unique=True)
    rank = IntegerField(default=0)
    sessions = IntegerField(default=0)
    points = DecimalField(max_digits=10, decimal_places=3, default=Decimal())
    class Meta:
        database = database


class Track(Model):
    id = AutoField()
    name = TextField(unique=True)
    sessions = IntegerField(default=0)
    class Meta:
        database = database


class Car(Model):
    id = AutoField()
    name = TextField(unique=True)
    sessions = IntegerField(default=0)
    class Meta:
        database = database


class Record(Model):
    id = AutoField()
    date_time = DateTimeField()
    driver = ForeignKeyField(Driver, field=Driver.id, on_delete="CASCADE")
    track = ForeignKeyField(Track, field=Track.id, on_delete="CASCADE")
    car = ForeignKeyField(Car, field=Car.id, on_delete="CASCADE")
    sessions = IntegerField(default=0)
    time = IntegerField()
    gold = BooleanField(default=False)
    silver = BooleanField(default=False)
    bronze = BooleanField(default=False)
    class Meta:
        database = database


def events_create_event(date_time):
    try:
        print(date_time)
        event = Event(date_time=datetime.fromisoformat(date_time))
        event.save()
        return True
    except:
        return False


def events_delete_event(date_time):
    try:
        event = Event().select().where(datetime.fromisoformat(date_time) == datetime.fromisoformat(date_time)).get()
        event.delete_instance()
        return True
    except:
        return False


def drivers_create_driver(name):
    try:
        if str(name) == "":
            return False
        driver = Driver(name=name)
        driver.save()
        update_driver_statistics()
        return True
    except:
        return False


def drivers_delete_driver(name):
    try:
        driver = Driver.select().where(Driver.name == name).get()
        driver.delete_instance()
        update_driver_statistics()
        return True
    except:
        return False


def tracks_create_track(name):
    try:
        if str(name) == "":
            return False
        track = Track(name=name)
        track.save()
        update_driver_statistics()
        return True
    except:
        return False


def tracks_delete_track(name):
    try:
        track = Track.select().where(Track.name == name).get()
        track.delete_instance()
        update_driver_statistics()
        return True
    except:
        return False


def cars_create_car(name):
    try:
        if str(name) == "":
            return False
        car = Car(name=name)
        car.save()
        update_driver_statistics()
        return True
    except:
        return False


def cars_delete_car(name):
    try:
        car = Car.select().where(Car.name == name).get()
        car.delete_instance()
        update_driver_statistics()
        return True
    except:
        return False


def records_create_record(driver, track, car, time):
    try:
        driver = Driver.select().where(Driver.name == driver).get()
        track = Track.select().where(Track.name == track).get()
        car = Car.select().where(Car.name == car).get()
        if str(time) == "":
            driver.sessions += 1
            driver.save()
            track.sessions += 1
            track.save()
            car.sessions += 1
            car.save()
            return True
        else:
            time = re.search("^([0-9]+):([0-9]{2})\.([0-9]{3})$", time)
            if not time:
                return False
            time_minutes = int(time.group(1))
            time_seconds = int(time.group(2))
            time_milliseconds = int(time.group(3))
            time = time_minutes * 60 * 1000 + time_seconds * 1000 + time_milliseconds
        try:
            record = Record.select().where(Record.driver == driver, Record.track == track, Record.car == car).get()
        except:
            record = None
        driver.sessions += 1
        driver.save()
        track.sessions += 1
        track.save()
        car.sessions += 1
        car.save()
        if not record:
            record = Record(date_time=datetime.now(), driver=driver, track=track, car=car, sessions=1, time=time)
            record.save()
        elif record.time >= time:
            record.date_time = datetime.now()
            record.sessions += 1
            record.time = time
            record.save()
        update_driver_statistics()
        return True
    except:
        return False


def records_delete_record(record):
    try:
        record = Record.select().where(Record.id == record).get()
        record.delete_instance()
        update_driver_statistics()
        return True
    except:
        return False


def update_driver_statistics():
    try:
        base_points = 100.0
        for driver in Driver.select():
            driver.points = Decimal(0.0)
            driver.save()
            records = Record.select().where(Record.driver == driver)
            for record in records:
                records_all = Record.select().order_by(Record.time.asc()).where(Record.track == record.track and Record.car == record.car)
                record_best = records_all[0] if len(records_all) > 0 else None
                if not record_best:
                    continue
                driver.points += Decimal(record_best.time / record.time * base_points)
                driver.save()
        for track in Track.select():
            for car in Car.select():
                index = 0
                for record in Record.select().order_by(Record.time.asc()).where(Record.track == track and Record.car == record.car):
                    record.gold = index == 0
                    record.silver = index == 1
                    record.bronze = index == 2
                    record.save()
                    index += 1
        index = 0
        for driver in Driver.select().order_by(Driver.points.desc(), Driver.name):
            driver.rank = index + 1
            driver.save()
            index += 1
    except:
        pass


database.connect()
database.create_tables([Event, Driver, Track, Car, Record])
bottle.TEMPLATE_PATH.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), "views"))
application = bottle.Bottle()


@application.route("/static/<filepath:path>")
def server_static(filepath):
    return bottle.static_file(filepath, root=os.path.join(os.path.dirname(os.path.realpath(__file__)), "static"))


def is_administrator(username, password):
    try:
        if username == "root" and sha256(password.encode("utf-8")).hexdigest() == "816347ae09cc90cc51e42fd7405f0d51869179eb6c9fd615fda360e06abbe546":
            return True
        return False
    except:
        return False

@application.route("/administrator", method="GET")
@bottle.auth_basic(is_administrator)
def route_get_administrator():
    try:
        data = {
            "events": Event.select().order_by(Event.date_time.desc()),
            "drivers": Driver.select().order_by(Driver.name),
            "tracks": Track.select().order_by(Track.name),
            "cars": Car.select().order_by(Car.name),
            "records": Record.select().order_by(Record.date_time.desc())
        }
    except:
        pass
    return bottle.template("pageadministrator", data)


@application.route("/administrator", method="POST")
@bottle.auth_basic(is_administrator)
def route_post_administrator_drivers_create():
    try:
        action = bottle.request.forms.action
        if action == "form_events_create_action":
            events_create_event(bottle.request.forms.form_events_create_input_date_time_event_date_time)
        if action == "form_events_delete_action":
            events_delete_event(bottle.request.forms.form_events_delete_select_event_date_time)
        if action == "form_drivers_create_action":
            drivers_create_driver(bottle.request.forms.form_drivers_create_input_text_driver_name)
        if action == "form_drivers_delete_action":
            drivers_delete_driver(bottle.request.forms.form_drivers_delete_select_driver_name)
        if action == "form_tracks_create_action":
            tracks_create_track(bottle.request.forms.form_tracks_create_input_text_track_name)
        if action == "form_tracks_delete_action":
            tracks_delete_track(bottle.request.forms.form_tracks_delete_select_track_name)
        if action == "form_cars_create_action":
            cars_create_car(bottle.request.forms.form_cars_create_input_text_car_name)
        if action == "form_cars_delete_action":
            cars_delete_car(bottle.request.forms.form_cars_delete_select_car_name)
        if action == "form_records_create_action":
            records_create_record(bottle.request.forms.form_records_create_select_driver_name, bottle.request.forms.form_records_create_select_track_name, bottle.request.forms.form_records_create_select_car_name, bottle.request.forms.form_records_create_input_text_record_time)
        if action == "form_records_delete_action":
            records_delete_record(bottle.request.forms.form_records_delete_select_record)
        data = {
            "events": Event.select().order_by(Event.date_time.desc()),
            "drivers": Driver.select().order_by(Driver.name),
            "tracks": Track.select().order_by(Track.name),
            "cars": Car.select().order_by(Car.name),
            "records": Record.select().order_by(Record.date_time.desc())
        }
    except:
        pass
    return bottle.template("pageadministrator", data)


@application.route("/")
@application.route("/home")
def route_home():
    try:
        data = {
            "now": datetime.now(),
            "events": Event.select().order_by(Event.date_time.desc())
        }
    except:
        pass
    return bottle.template("pagehome", data)


@application.route("/drivers")
def route_drivers():
    try:
        data = {
            "drivers": Driver.select().order_by(Driver.points.desc(), Driver.name)
        }
    except:
        pass
    return bottle.template("pagedrivers", data)


@application.route("/tracks")
def route_tracks():
    try:
        data = {
            "tracks": Track.select().order_by(Track.sessions.desc(), Track.name)
        }
    except:
        pass
    return bottle.template("pagetracks", data)


@application.route("/cars")
def route_cars():
    try:
        data = {
            "cars": Car.select().order_by(Car.sessions.desc(), Car.name)
        }
    except:
        pass
    return bottle.template("pagecars", data)


@application.route("/records")
def route_records():
    try:
        data = {
            "records": Record.select().order_by(Record.date_time.desc())
        }
    except:
        pass
    return bottle.template("pagerecords", data)
