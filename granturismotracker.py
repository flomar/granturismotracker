from granturismotracker.database.database import database, Event, Driver, Track, Car, Record
from granturismotracker.server.server import application


database.connect()
database.create_tables([Event, Driver, Track, Car, Record])


if __name__ == "__main__":
    application.run(host="0.0.0.0", port=9999)
