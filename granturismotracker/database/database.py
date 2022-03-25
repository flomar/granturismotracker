import re

from datetime import datetime, timedelta
from decimal import Decimal
from peewee import *


database = SqliteDatabase("granturismotracker.sqlite", pragmas={"foreign_keys": 1, "encoding": "UTF8"})


class Event(Model):
    id = AutoField()
    date_time = DateTimeField()
    date_time_expiration = DateTimeField()
    class Meta:
        database = database


class Driver(Model):
    id = AutoField()
    name = TextField(unique=True)
    rank = IntegerField(default=0)
    sessions = IntegerField(default=0)
    points = DecimalField(max_digits=10, decimal_places=3, default=Decimal())
    points_past = DecimalField(max_digits=10, decimal_places=3, default=Decimal())
    points_current = DecimalField(max_digits=10, decimal_places=3, default=Decimal())
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
    pps = DecimalField(max_digits=10, decimal_places=3, default=Decimal())
    time = IntegerField(default=0)
    gold = BooleanField(default=False)
    silver = BooleanField(default=False)
    bronze = BooleanField(default=False)
    class Meta:
        database = database


class Report(Model):
    id = AutoField()
    date_time = DateTimeField()
    date_time_expiration = DateTimeField()
    driver = ForeignKeyField(Driver, field=Driver.id, on_delete="CASCADE")
    track = ForeignKeyField(Track, field=Track.id, on_delete="CASCADE")
    car = ForeignKeyField(Car, field=Car.id, on_delete="CASCADE")
    pps = DecimalField(max_digits=10, decimal_places=3, default=Decimal())
    time = IntegerField(default=0)
    gold = BooleanField(default=False)
    silver = BooleanField(default=False)
    bronze = BooleanField(default=False)
    performance = DecimalField(max_digits=10, decimal_places=3, default=Decimal())
    class Meta:
        database = database


def events_create_event(date_time):
    try:
        date_time = datetime.fromisoformat(date_time)
        date_time_expiration = date_time + timedelta(hours=12)
        event = Event(date_time=date_time, date_time_expiration=date_time_expiration)
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
        return update_statistics()
    except:
        return False


def drivers_delete_driver(name):
    try:
        driver = Driver.select().where(Driver.name == name).get()
        driver.delete_instance()
        return update_statistics()
    except:
        return False


def tracks_create_track(name):
    try:
        if str(name) == "":
            return False
        track = Track(name=name)
        track.save()
        return update_statistics()
    except:
        return False


def tracks_delete_track(name):
    try:
        track = Track.select().where(Track.name == name).get()
        track.delete_instance()
        return update_statistics()
    except:
        return False


def cars_create_car(name):
    try:
        if str(name) == "":
            return False
        car = Car(name=name)
        car.save()
        return update_statistics()
    except:
        return False


def cars_delete_car(name):
    try:
        car = Car.select().where(Car.name == name).get()
        car.delete_instance()
        return update_statistics()
    except:
        return False


def records_create_record(driver, track, car, pps, time):
    try:
        driver = Driver.select().where(Driver.name == driver).get()
        track = Track.select().where(Track.name == track).get()
        car = Car.select().where(Car.name == car).get()
        if str(pps) == "":
            return False
        else:
            pps = re.search("^([0-9]+)\.([0-9]+)$", pps)
            if not pps:
                return False
            pps = Decimal("{0}.{1}".format(pps.group(1), pps.group(2)))
        if str(time) == "":
            time = 0
        else:
            time = re.search("^([0-9]+):([0-9]{2})\.([0-9]{3})$", time)
            if not time:
                return False
            time_minutes = int(time.group(1))
            time_seconds = int(time.group(2))
            time_milliseconds = int(time.group(3))
            time = time_minutes * 60 * 1000 + time_seconds * 1000 + time_milliseconds
        try:
            record = Record(date_time=datetime.now(), driver=driver, track=track, car=car, pps=pps, time=time)
            record.save()
        except:
            return False
        return update_statistics(record)
    except:
        return False


def records_delete_record(record):
    try:
        record = Record.select().where(Record.id == record).get()
        record.delete_instance()
        return update_statistics()
    except:
        return False


def update_statistics(record_new=None):
    try:
        points_past_gold = Decimal(1.0)
        points_past_silver = Decimal(0.25)
        points_past_bronze = Decimal(0.125)
        points_current = Decimal(100.0)
        if record_new:
            if record_new.driver:
                record_new.driver.sessions += 1
                record_new.driver.save()
            if record_new.track:
                record_new.track.sessions += 1
                record_new.track.save()
            if record_new.car:
                record_new.car.sessions += 1
                record_new.car.save()
        if record_new:
            records = Record.select().where((Record.time > 0) & (Record.driver != record_new.driver) & (Record.track == record_new.track) & (Record.car == record_new.car)).order_by(Record.time.asc()).limit(3)
            record_gold = records[0] if len(records) >= 1 else None
            record_silver = records[1] if len(records) >= 2 else None
            record_bronze = records[2] if len(records) >= 3 else None
            if record_gold and (record_new.time == 0 or record_new.time > record_gold.time):
                record_gold.driver.points_past += points_past_gold
                record_gold.driver.save()
            if record_silver and (record_new.time == 0 or record_new.time > record_silver.time):
                record_silver.driver.points_past += points_past_silver
                record_silver.driver.save()
            if record_bronze and (record_new.time == 0 or record_new.time > record_bronze.time):
                record_bronze.driver.points_past += points_past_bronze
                record_bronze.driver.save()
        for track in Track.select():
            for car in Car.select():
                rank = 1
                for record in Record.select().where((Record.time > 0) & (Record.track == track) & (Record.car == car)).order_by(Record.time.asc(), Record.pps.asc()):
                    record.gold = rank == 1
                    record.silver = rank == 2
                    record.bronze = rank == 3
                    record.save()
                    rank += 1
        record_new = Record.select().where(Record.id==record_new.id).get() if record_new else None
        if record_new:
            performance = Decimal(0.0)
            if record_new.time != 0:
                records_opponents = Record.select().where((Record.time > 0) & (Record.track == track) & (Record.car == car)).order_by(Record.time.asc()).limit(1)
                record_opponent_best = records_opponents[0] if len(records_opponents) > 0 else None
                performance = Decimal(points_current) if not record_opponent_best else Decimal(record_opponent_best.pps) / Decimal(record_new.pps) * Decimal(record_opponent_best.time) / Decimal(record_new.time) * Decimal(points_current)
            report = Report(date_time=record_new.date_time, date_time_expiration=record_new.date_time + timedelta(hours=12), driver=record_new.driver, track=record_new.track, car=record_new.car, pps=record_new.pps, time=record_new.time, gold=record_new.gold, silver=record_new.silver, bronze=record_new.bronze, performance=performance)
            report.save()
        for driver in Driver.select():
            driver_points_current = Decimal(0.0)
            for track in Track.select():
                for car in Car.select():
                    records_driver = Record.select().where((Record.time > 0) & (Record.driver == driver) & (Record.track == track) & (Record.car == car)).order_by(Record.time.asc()).limit(1)
                    record_driver_best = records_driver[0] if len(records_driver) > 0 else None
                    if not record_driver_best:
                        continue
                    records_opponents = Record.select().where((Record.time > 0) & (Record.track == track) & (Record.car == car)).order_by(Record.time.asc()).limit(1)
                    record_opponent_best = records_opponents[0] if len(records_opponents) > 0 else None
                    if not record_opponent_best:
                        continue
                    driver_points_current += Decimal(record_opponent_best.pps) / Decimal(record_driver_best.pps) * Decimal(record_opponent_best.time) / Decimal(record_driver_best.time) * Decimal(points_current)
            driver.points_current = driver_points_current
            driver.save()
        for driver in Driver.select():
            driver.points = driver.points_past + driver.points_current
            driver.save()
        rank = 1
        for driver in Driver.select().order_by(Driver.points.desc(), Driver.name):
            driver.rank = rank
            driver.save()
            rank += 1
        for record in Record.select():
            if record.time == 0:
                record.delete_instance()
        for driver in Driver.select():
            for track in Track.select():
                for car in Car.select():
                    entry = 1
                    for record in Record.select().where((Record.time > 0) & (Record.driver == driver) & (Record.track == track) & (Record.car == car)).order_by(Record.time.asc()):
                        if entry > 3:
                            record.delete_instance()
                        entry += 1
        return True
    except:
        return False
