import re

from datetime import datetime
from decimal import Decimal
from peewee import *


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
    time = IntegerField(default=0)
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


def records_create_record(driver, track, car, time):
    try:
        driver = Driver.select().where(Driver.name == driver).get()
        track = Track.select().where(Track.name == track).get()
        car = Car.select().where(Car.name == car).get()
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
            record = Record(date_time=datetime.now(), driver=driver, track=track, car=car, time=time)
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


def update_statistics(record=None):
    try:
        points_past_gold = Decimal(1.0)
        points_past_silver = Decimal(0.25)
        points_past_bronze = Decimal(0.125)
        points_current = Decimal(100.0)
        if record:
            if record.driver:
                record.driver.sessions += 1
                record.driver.save()
            if record.track:
                record.track.sessions += 1
                record.track.save()
            if record.car:
                record.car.sessions += 1
                record.car.save()
        if record:
            records = Record.select().order_by(Record.time.asc()).where((Record.time > 0) & (Record.driver != record.driver) & (Record.track == record.track) & (Record.car == record.car)).limit(3)
            record_gold = records[0] if len(records) >= 1 else None
            record_silver = records[1] if len(records) >= 2 else None
            record_bronze = records[2] if len(records) >= 3 else None
            if record_gold and (record.time == 0 or record.time > record_gold.time):
                record_gold.driver.points_past += points_past_gold
                record_gold.driver.save()
            if record_silver and (record.time == 0 or record.time > record_silver.time):
                record_silver.driver.points_past += points_past_silver
                record_silver.driver.save()
            if record_bronze and (record.time == 0 or record.time > record_bronze.time):
                record_bronze.driver.points_past += points_past_bronze
                record_bronze.driver.save()
        for track in Track.select():
            for car in Car.select():
                rank = 1
                for record in Record.select().order_by(Record.time.asc()).where((Record.time > 0) & (Record.track == track) & (Record.car == car)):
                    record.gold = rank == 1
                    record.silver = rank == 2
                    record.bronze = rank == 3
                    record.save()
                    rank += 1

        for driver in Driver.select():
            driver_points_current = Decimal(0.0)
            for track in Track.select():
                for car in Car.select():
                    records_driver = Record.select().order_by(Record.time.asc()).where((Record.time > 0) & (Record.driver == driver) & (Record.track == track) & (Record.car == car)).limit(1)
                    record_driver_best = records_driver[0] if len(records_driver) > 0 else None
                    if not record_driver_best:
                        continue
                    records_opponents = Record.select().order_by(Record.time.asc()).where((Record.time > 0) & (Record.track == track) & (Record.car == car)).limit(1)
                    record_opponent_best = records_opponents[0] if len(records_opponents) > 0 else None
                    if not record_opponent_best:
                        continue
                    driver_points_current += Decimal(record_opponent_best.time) / Decimal(record_driver_best.time) * Decimal(points_current)
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
        return True
    except:
        return False
