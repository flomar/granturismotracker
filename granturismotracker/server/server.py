import os
from textwrap import wrap
import bottle

from datetime import datetime
from decimal import Decimal
from hashlib import sha256


bottle.TEMPLATE_PATH.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), "../views"))
application = bottle.Bottle()


from granturismotracker.database.database import Event, Driver, Track, Car, Record, Report
from granturismotracker.database.database import events_create_event, events_delete_event
from granturismotracker.database.database import drivers_create_driver, drivers_delete_driver
from granturismotracker.database.database import tracks_create_track, tracks_delete_track
from granturismotracker.database.database import cars_create_car, cars_delete_car
from granturismotracker.database.database import records_create_record, records_delete_record


def create_request_data():
    data = {
        "now": datetime.now(),
        "now_string": datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    }
    return data


@application.route("/static/<filepath:path>")
def server_static(filepath):
    return bottle.static_file(filepath, root=os.path.join(os.path.dirname(os.path.realpath(__file__)), "../static"))


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
    data = create_request_data()
    try:
        data["events"] = Event.select().order_by(Event.date_time.desc())
        data["drivers"] = Driver.select().order_by(Driver.name)
        data["tracks"] = Track.select().order_by(Track.name)
        data["cars"] = Car.select().order_by(Car.name)
        data["records"] = Record.select().where(Record.time > 0).order_by(Record.date_time.desc())
    except:
        data["events"] = []
        data["drivers"] = []
        data["tracks"] = []
        data["cars"] = []
        data["records"] = []
    return bottle.template("pageadministrator", data)


@application.route("/administrator", method="POST")
@bottle.auth_basic(is_administrator)
def route_post_administrator_drivers_create():
    data = create_request_data()
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
            records_create_record(bottle.request.forms.form_records_create_select_driver_name, bottle.request.forms.form_records_create_select_track_name, bottle.request.forms.form_records_create_select_car_name, bottle.request.forms.form_records_create_input_text_record_pps, bottle.request.forms.form_records_create_input_text_record_time)
        if action == "form_records_delete_action":
            records_delete_record(bottle.request.forms.form_records_delete_select_record)
        data["events"] = Event.select().order_by(Event.date_time.desc())
        data["drivers"] = Driver.select().order_by(Driver.name)
        data["tracks"] = Track.select().order_by(Track.name)
        data["cars"] = Car.select().order_by(Car.name)
        data["records"] = Record.select().where(Record.time > 0).order_by(Record.date_time.desc())
    except:
        data["events"] = []
        data["drivers"] = []
        data["tracks"] = []
        data["cars"] = []
        data["records"] = []
    return bottle.template("pageadministrator", data)


@application.route("/")
@application.route("/home")
def route_home():
    data = create_request_data()
    try:
        data["reports"] = Report.select().where(Report.date_time_expiration > datetime.now()).order_by(Report.date_time.desc())
        data["events"] = Event.select().order_by(Event.date_time.desc())
    except:
        data["reports"] = []
        data["events"] = []
    return bottle.template("pagehome", data)


@application.route("/drivers")
def route_drivers():
    data = create_request_data()
    try:
        data["drivers"] = Driver.select().where(Driver.points > Decimal(0.0)).order_by(Driver.rank.asc(), Driver.name)
    except:
        data["drivers"] = []
    return bottle.template("pagedrivers", data)


@application.route("/drivers/details/<id:int>")
def route_drivers_details(id):
    data = create_request_data()
    try:
        driver = Driver.select().where(Driver.id == id).get()
        data["driver"] = driver
        data["gold"] = Record.select().where((Record.driver == driver) & (Record.gold)).count()
        data["silver"] = Record.select().where((Record.driver == driver) & (Record.silver)).count()
        data["bronze"] = Record.select().where((Record.driver == driver) & (Record.bronze)).count()
        data["records"] = Record.select().where((Record.time > 0) & (Record.driver == driver)).order_by(Record.date_time.desc())
    except:
        driver = None
        data["driver"] = driver
        data["gold"] = 0
        data["silver"] = 0
        data["bronze"] = 0
        data["records"] = []
    return bottle.template("pagedriversdetails", data)


@application.route("/tracks")
def route_tracks():
    data = create_request_data()
    try:
        data["tracks"] = Track.select().order_by(Track.sessions.desc(), Track.name)
    except:
        data["tracks"] = []
    return bottle.template("pagetracks", data)


@application.route("/cars")
def route_cars():
    data = create_request_data()
    try:
        data["cars"] = Car.select().order_by(Car.sessions.desc(), Car.name)
    except:
        data["cars"] = []
    return bottle.template("pagecars", data)


@application.route("/records")
def route_records():
    data = create_request_data()
    try:
        data["records"] = Record.select().where((Record.time > 0) & ((Record.gold) | (Record.silver) | (Record.bronze))).order_by(Record.date_time.desc())
    except:
        data["records"] = []
    return bottle.template("pagerecords", data)


@application.route("/reports")
def route_records():
    data = create_request_data()
    try:
        data["reports"] = Report.select().order_by(Report.date_time.desc())
    except:
        data["reports"] = []
    return bottle.template("pagereports", data)


@application.route("/rules")
def route_rules():
    data = create_request_data()
    try:
        pass
    except:
        pass
    return bottle.template("pagerules", data)
