from sqlite3 import Connection


class AccessPointModel:
    id: str
    name: str
    parent: str
    def __init__(self, id, name, parent):
        self.id = id
        self.name = name
        self.parent = parent
        pass

class AccessPointDAO:
    def get_all(conn: Connection) -> list[AccessPointModel]:
        result = conn.cursor().execute("""
                SELECT ACCESS_POINT_ID, PARENT_ACCESS_POINT_ID
                FROM NETWORK_INFRASTRUCTURE
                ORDER BY DEVICE_ORDER ASC
            """).fetchall()
        return list(map(lambda value: AccessPointModel(value[0], None, value[1]), result))