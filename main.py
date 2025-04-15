import sys
from datetime import datetime

from converters.convert import convert_data
from database import engine, DbSession
from invoices.creator import generate_invoices
from invoices.csv import generate_invoices_for_all
from invoices.pdf import generate_pdf_invoices_for_all
from models import UserModel, UserRole
from repository import UserRepository
from utils import password_hash


def get_month_from_cli(cur_idx, optional=False):
    try:
        if len(sys.argv) <= cur_idx + 1:
            raise Exception("Missing month argument")
        str_arg = sys.argv[cur_idx + 1]
        datetime.strptime(str_arg, "%m.%Y")
        return str_arg
    except Exception as e:
        if optional:
            return None
        raise e


with engine.connect() as conn:

    for idx, x in enumerate(sys.argv):
        if x == "loadData":
            convert_data()
        elif x == "generateInvoice":
            generate_invoices(get_month_from_cli(idx))
        elif x == "invoicesToCSV":
            generate_invoices_for_all(get_month_from_cli(idx, True))
        elif x == "invoicesToPdf":
            generate_pdf_invoices_for_all(get_month_from_cli(idx, True))
        elif x == "createAdmin":
            login = sys.argv[idx + 1]
            password = sys.argv[idx + 2]
            if len(login) < 2 or len(password) < 2:
                raise Exception("Login and password must be at least 2 characters")
            with DbSession() as session:
                UserRepository.create_user(
                    session,
                    UserModel(
                        login=login,
                        password_hash=password_hash(password),
                        role=UserRole.ADMIN,
                    ),
                )
                session.commit()
