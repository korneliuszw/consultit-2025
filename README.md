# ConsultIT Etap 1

## Running
Tested python version: 3.12

Commands:
- createDatabase: Removes data from database and creates new database filled with tables
- loadData: load CSV files into the database

You can run multiple commands but they are chained so make sure they follow a logical order

Example:
```bash
python ./main.py createDatabase loadData
```


## Database
Diagram: https://dbdiagram.io/d/consultit-case-study-1-67d451b475d75cc8441eef71

For now, database is stored in hardcoded path ./network.db