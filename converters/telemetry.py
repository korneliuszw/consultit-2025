from datetime import datetime, timedelta
from os import environ

from converters.base import DataConverter

DATETIME_FORMAT = "%d.%m.%Y %H:%M:%S"

class TelemetryConverter(DataConverter):
    def __init__(self):
        super().__init__(environ.get("TELEMETRY_DOWNTIME_LOG_DATA", "./data/telemetry.csv"))

    def get_query(self):
        return """
            INSERT INTO TELEMETRY_DOWNTIME_LOG
                (ACCESS_POINT_ID, DOWNTIME_START_DATE, DOWNTIME_END_DATE)
                VALUES (?, ?, ?)
        """
    
    def str_to_time(str_date, str_time):
        if len(str_date) < 9:
            raise Exception("Date too short!")
        elif len(str_time) != 8:
            raise Exception("Invalid time format")
        elif str_date[1] == ".":
            # Days of months are not padded so we must do it ourselfs
            str_date = "0" + str_date
        
        return datetime.strptime(f"{str_date} {str_time}", DATETIME_FORMAT)
    
    def minutes_to_timedelta(minutes):
        return timedelta(minutes=int(minutes))
        

    def get_dates(row):
        date = TelemetryConverter.str_to_time(row["DOWNTIME_START_DATE"], row["DOWNTIME_START_TIME"])
        duration = TelemetryConverter.minutes_to_timedelta(row["DOWNTIME_DURATION_MINUTES"])
        return (date, date+duration)


    def to_tuple(self, row):
        dates = TelemetryConverter.get_dates(row)
        return (row["ACCESS_POINT_ID"], dates[0], dates[1])

    