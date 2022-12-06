import sqlite3
import time


class DbConnect:

    query = """ INSERT INTO ads_details("date", "urlid", "ad_id", "ad_title",
    "category", "region", "subregion", "city", "ad_price", "private_business",
    "user_id", "make", "model", "generation", "version", "vin", "registration",
    "year", "mileage", "fuel_type", "engine_capacity", "battery_capacity",
    "engine_power", "gearbox", "transmission", "accident_free", "damaged",
    "condition", "body_type", "door_count", "nr_seats", "color", "colour_type",
    "alloy_wheels_type", "headlight_lamp_type", "country_origin",
    "air_conditioning_type", "cruisecontrol_type", "sunblind_type",
    "tyre_type", "sunroof", "convertible_top_type","upholstery_type") VALUES
    (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """

    def __init__(self, database):
        try:
            self.con = sqlite3.connect(database)
            self.cursor = self.con.cursor()
            print("Database connected successfully.")
        except:
            print(f"DB connection error has occurred: {e}")

    def insert_data(self, values):
        try:
            self.cursor.execute(self.query, values)
            self.con.commit()
        except sqlite3.Error as e:
            sqlstate = e.args[0]
            if sqlstate == '23000':
                pass
            else:
                print(f" Query Failed……{e}")

    def get_data(self, query):
        """pulls data out of database"""
        records = []
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            rows = cursor.fetchall()
        except sqlite3.Error as e:
            print(f" Query Failed……{e}")
        for row in rows:
            records.append(row)
        return records