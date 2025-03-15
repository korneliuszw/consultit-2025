from datetime import datetime
from sqlite3 import Connection


class TelemetryLogModel:
    access_point_id: str
    start_date: datetime
    end_date: datetime

    def __init__(self, access_point_id, start_date, end_date):
        self.access_point_id = access_point_id
        self.start_date = start_date
        self.end_date = end_date

class TelemetryLogDAO:
    def get_in_month(conn: Connection, month: str) -> list[TelemetryLogModel]:
        """Month must be of format %m.%Y so 01.2025 => january of 2025"""
        result = conn.cursor().execute("""
            SELECT ACCESS_POINT_ID, DOWNTIME_START_DATE, DOWNTIME_END_DATE
            FROM TELEMETRY_DOWNTIME_LOG
            WHERE strftime("%m.%Y", DOWNTIME_START_DATE) = ?
        """, (month,)).fetchall()
        return list(map(lambda value: TelemetryLogModel(value[0], value[1], value[2]), result))
