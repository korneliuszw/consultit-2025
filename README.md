# ConsultIT Etap 1

## Running

Tested python version: 3.12
Use Linux or WSL for easier setup. PDF generation is very hard to setup on Windows because you have to
install (https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#windows)[MSYS2].

Install required system packages (Debian)

```bash
sudo apt install libsqlite3-dev python3-pip libpango-1.0-0 libharfbuzz0b libpangoft2-1.0-0 libharfbuzz-subset0 python3
```

If you are using pyenv and haven't installed libsqlite3 before, you need to reinstall your python version with pyenv
install

Install required libraries

```bash
pip install --user -r requirements.txt
```

To create a database with all the tables run

```bash
alembic upgrade head
```

Commands:

- loadData: load CSV files into the database (Task 2)
- generateInvoice (MM.YYYY): Generates invoices for a month and inserts them to database (Task 3)
- invoicesToCSV (MM.YYYY optional): Generates CSV for invoices. Omit a month to generate for all invoices in the
  database
- invoicesToPDF (MM.YYYY optional): Generates PDF for invoices. Omit a month to generate for all invoices in the
  database

You can run multiple commands but they are chained so make sure they follow a logical order

Example:

```bash
python ./main.py createDatabase loadData generateInvoice "01.2025" invoicesToCSV invoicesToPDF
```

## Database

Diagram: https://dbdiagram.io/d/consultit-case-study-1-67d451b475d75cc8441eef71

For now, database is stored in hardcoded path ./network.db

# ConsultIT Etap 2

## Users

For simplicity some assumptions were made for authentication and authorization.
Users can only have one role, either serviceman or consultant. There can be only one active session, so they can't be
logged in two places at once.
To add new users you send a POST requests with special token as Authorization header (so we don't have to implement
administator users as to not raise additional costs to development).