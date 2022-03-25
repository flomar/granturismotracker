from granturismotracker.database.database import database, Event, Driver, Track, Car, Record, Report
from granturismotracker.server.server import application


database.connect()
database.create_tables([Event, Driver, Track, Car, Record, Report])


if __name__ == "__main__":
    application.run(host="0.0.0.0", port=9999)
