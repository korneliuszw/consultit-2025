from sqlite3 import Connection

def create_network_infrastructure(conn: Connection):
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS NETWORK_INFRASTRUCTURE")
    cursor.execute('''
    CREATE TABLE NETWORK_INFRASTRUCTURE (
        ACCESS_POINT_ID VARCHAR(100) PRIMARY KEY,
        NAME TEXT NOT NULL,
        PARENT_ACCESS_POINT_ID VARCHAR(100),
        DEVICE_ORDER INTEGER NOT NULL,
        CONSTRAINT valid_parent CHECK (
            (NAME = 'IBAP' AND PARENT_ACCESS_POINT_ID IS NULL) OR
            (NAME != 'IBAP' AND PARENT_ACCESS_POINT_ID IS NOT NULL)
        ),
        FOREIGN KEY (PARENT_ACCESS_POINT_ID) REFERENCES NETWORK_INFRASTRUCTURE(ACCESS_POINT_ID)
    )
    ''')
    conn.commit()

def create_customers(conn: Connection):
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS Customers")
    cursor.execute('''
    CREATE TABLE CUSTOMERS (
        ID VARCHAR(50) PRIMARY KEY,
        NAME TEXT NOT NULL,
        ACCESS_POINT VARCHAR(100),
        MONTHLY_AMOUNT_DUE INTEGER DEFAULT 0,
        FOREIGN KEY (ACCESS_POINT) REFERENCES NETWORK_INFRASTRUCTURE(ACCESS_POINT_ID)
    )
    ''')

    conn.commit()

def create_downtime_log(conn: Connection):
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS TELEMETRY_DOWNTIME_LOG")
    cursor.execute('''
    CREATE TABLE TELEMETRY_DOWNTIME_LOG (
        DOWNTIME_ID INTEGER PRIMARY KEY,
        ACCESS_POINT_ID VARCHAR(100) NOT NULL,
        DOWNTIME_START_DATE TIMESTAMP NOT NULL,
        DOWNTIME_END_DATE TIMESTAMP NOT NULL,
        FOREIGN KEY (ACCESS_POINT_ID) REFERENCES NETWORK_INFRASTRUCTURE(ACCESS_POINT_ID)
    )
    ''')
    cursor.execute('''
        CREATE INDEX idx_downtime_start_date ON TELEMETRY_DOWNTIME_LOG(DOWNTIME_START_DATE)
    ''')
    conn.commit()

def create_invoices(conn: Connection):
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS INVOICES")
    cursor.execute('''
    CREATE TABLE INVOICES (
        INVOICE_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        CUSTOMER_ID VARCHAR(50) NOT NULL,
        CUSTOMER_NAME TEXT NOT NULL,
        MONTH VARCHAR(10) NOT NULL,
        FOREIGN KEY (CUSTOMER_ID) REFERENCES Customers(ID)
    )
    ''')
    conn.commit()

def create_invoices_lines(conn: Connection):
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS INVOICE_LINES")
    cursor.execute('''
    CREATE TABLE INVOICE_LINES (
        INVOICE_ID INTEGER,
        LINE_NUMBER INTEGER,
        TITLE TEXT NOT NULL CHECK (TITLE IN ('SUBSCRIPTION', 'REBATE')),
        LINE_AMOUNT INTEGER NOT NULL,
        PRIMARY KEY (INVOICE_ID, LINE_NUMBER),
        FOREIGN KEY (INVOICE_ID) REFERENCES INVOICES(INVOICE_ID)
    )
    ''')
    conn.commit()


def create_tables(conn: Connection):
    create_network_infrastructure(conn)
    create_customers(conn)
    create_downtime_log(conn)
    create_invoices(conn)
    create_invoices_lines(conn)