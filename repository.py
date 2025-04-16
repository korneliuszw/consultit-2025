from typing import Type, Optional, List

from sqlalchemy import func
from sqlalchemy.orm import Session

from models import (
    AccessPointModel,
    UserModel,
    CustomerModel,
    InvoiceModel,
    InvoiceLineModel,
    TelemetryLogModel,
)


class AccessPointRepository:
    @staticmethod
    def get_all(session: Session) -> list[Type[AccessPointModel]]:
        return (
            session.query(AccessPointModel)
            .order_by(AccessPointModel.device_order)
            .all()
        )


class UserRepository:
    @staticmethod
    def get_by_login(session: Session, login: str) -> Optional[UserModel]:
        """Returns a user by login"""
        return session.query(UserModel).filter(UserModel.login == login).first()

    @staticmethod
    def create_user(session: Session, user: UserModel):
        """Creates a user from model"""
        return session.add(user)

    @staticmethod
    def get_by_id(session: Session, user_id: int) -> Optional[UserModel]:
        """Returns a user by id"""
        return session.get(UserModel, user_id)


class InvoiceRepository:
    @staticmethod
    def create(session: Session, data: InvoiceModel):
        session.add(data)

    @staticmethod
    def insert_lines(session: Session, line: List[InvoiceLineModel]):
        session.add_all(line)

    @staticmethod
    def get_all(session: Session) -> List[Type[InvoiceModel]]:
        return session.query(InvoiceModel).all()

    @staticmethod
    def get_for_month(session: Session, month: str) -> List[Type[InvoiceModel]]:
        return session.query(InvoiceModel).filter(InvoiceModel.month == month).all()

    @staticmethod
    def get_lines(invoice: InvoiceModel) -> List[InvoiceLineModel]:
        return invoice.lines


class CustomerRepository:
    @staticmethod
    def get_all(session: Session) -> List[Type[CustomerModel]]:
        return session.query(CustomerModel).all()


class TelemetryLogRepository:
    @staticmethod
    def get_in_month(
        session: Session, month: str, device_ids: List[str] = None
    ) -> List[Type[TelemetryLogModel]]:
        """Month must be of format %m.%Y so 01.2025 => january of 2025"""
        query = session.query(TelemetryLogModel).filter(
            func.strftime("%m.%Y", TelemetryLogModel.start_date) == month
        )
        if device_ids != None:
            query = query.filter(TelemetryLogModel.access_point_id.in_(device_ids))
        return query.all()
