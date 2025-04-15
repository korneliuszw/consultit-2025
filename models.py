from datetime import datetime
from enum import Enum
from typing import Optional, List

from sqlalchemy import ForeignKey, String, UUID, LargeBinary
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase


class ModelBase(DeclarativeBase):
    pass


class AccessPointModel(ModelBase):
    __tablename__ = "NETWORK_INFRASTRUCTURE"
    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    parent_access_point_id: Mapped[Optional[str]] = mapped_column(
        ForeignKey(f"{__tablename__}.id", ondelete="CASCADE"),
    )
    device_order: Mapped[int] = mapped_column()

    parent: Mapped["AccessPointModel"] = relationship("AccessPointModel")
    telemetry_logs: Mapped[List["TelemetryLogModel"]] = relationship(
        back_populates="access_point"
    )

    def __repr__(self):
        return f"AccessPointModel(id={self.id}, name={self.name}, parentAccessPointId={self.parent_access_point_id}), deviceOrder={self.device_order})"


class TelemetryLogModel(ModelBase):
    __tablename__ = "TELEMETRY_DOWNTIME_LOG"
    downtime_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    access_point_id: Mapped[str] = mapped_column(ForeignKey(AccessPointModel.id))
    start_date: Mapped[datetime] = mapped_column()
    end_date: Mapped[datetime] = mapped_column()
    access_point: Mapped["AccessPointModel"] = relationship(
        back_populates="telemetry_logs"
    )

    def __repr__(self):
        return f"TelemetryLogModel(downtime_id={self.downtime_id}, access_point_id={self.access_point_id}, start_date={self.start_date}, end_date={self.end_date})"


class InvoiceLineTitle(Enum):
    SUBSCRIPTION = "SUBSCRIPTION"
    REBATE = "REBATE"


class CustomerModel(ModelBase):
    __tablename__ = "CUSTOMER"
    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    name: Mapped[str] = mapped_column()
    access_point: Mapped[str] = mapped_column(ForeignKey(AccessPointModel.id))
    monthly_amount_due: Mapped[int] = mapped_column(default=0)

    def __repr__(self):
        return f"CustomerModel(id={self.id}, name={self.name}, access_point={self.access_point}, monthly_amount_due={self.monthly_amount_due})"


class InvoiceModel(ModelBase):
    __tablename__ = "INVOICES"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    customer_id: Mapped[str] = mapped_column(ForeignKey(CustomerModel.id))
    customer_name: Mapped[str] = mapped_column()
    month: Mapped[str] = mapped_column(String(10))
    lines: Mapped[List["InvoiceLineModel"]] = relationship(back_populates="invoice")

    def __repr__(self):
        return f"InvoiceModel(id={self.id}, customer_id={self.customer_id}, customer_name={self.customer_name}, month={self.month})"


class InvoiceLineModel(ModelBase):
    __tablename__ = "INVOICE_LINES"
    invoice_id: Mapped[int] = mapped_column(
        ForeignKey(InvoiceModel.id), primary_key=True
    )
    line_number: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[InvoiceLineTitle] = mapped_column()
    amount: Mapped[int] = mapped_column()
    invoice: Mapped["InvoiceModel"] = relationship(back_populates="lines")

    def __repr__(self):
        return f"InvoiceLineModel(invoice_id={self.invoice_id}, line_number={self.line_number}, title={self.title}, amount={self.amount})"


class UserRole(Enum):
    CONSULTANT = "CONSULTANT"
    SERVICEMAN = "SERVICEMAN"
    ADMIN = "ADMIN"


class UserModel(ModelBase):
    __tablename__ = "USERS"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    login: Mapped[str] = mapped_column(String(50))
    password_hash: Mapped[bytes] = mapped_column(LargeBinary)
    role: Mapped[UserRole] = mapped_column()
    current_session_id: Mapped[Optional[UUID]] = mapped_column(
        UUID(as_uuid=True), nullable=True
    )

    def __repr__(self):
        return f"UserModel(id={self.id}, login={self.login}, role={self.role}, current_session_id={self.current_session_id})"
