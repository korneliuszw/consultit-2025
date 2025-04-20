from datetime import datetime
from enum import Enum
from typing import Optional, List

from sqlalchemy import ForeignKey, String, UUID, LargeBinary, MetaData
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase


class ModelBase(DeclarativeBase):
    uppercase_naming_convention = {
        "ix": "IX_%(table_name)s_%(column_0_N_name)s",  # Indexes
        "uq": "UQ_%(table_name)s_%(column_0_N_name)s",  # Unique constraints
        "ck": "CK_%(table_name)s_%(constraint_name)s",  # Check constraints
        "fk": "FK_%(table_name)s_%(column_0_N_name)s_%(referred_table_name)s",  # Foreign keys
        "pk": "PK_%(table_name)s",  # Primary keys
    }
    metadata = MetaData(naming_convention=uppercase_naming_convention)
    pass


class AccessPointModel(ModelBase):
    __tablename__ = "NETWORK_INFRASTRUCTURE"
    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    parent_access_point_id: Mapped[Optional[str]] = mapped_column(
        ForeignKey(f"{__tablename__}.id", ondelete="CASCADE"),
    )
    device_order: Mapped[int] = mapped_column()

    parent: Mapped["AccessPointModel"] = relationship(remote_side="AccessPointModel.id")

    telemetry_logs: Mapped[List["TelemetryLogModel"]] = relationship(
        back_populates="access_point"
    )
    customer: Mapped["CustomerModel"] = relationship(back_populates="device")

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


class SubscriptionModel(ModelBase):
    __tablename__ = "SUBSCRIPTION_PLAN"
    plan_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column()
    base_price: Mapped[int] = mapped_column()
    final_price_formula: Mapped[str] = mapped_column()
    subscribers: Mapped[List["CustomerModel"]] = relationship(
        back_populates="subscription"
    )


class CustomerModel(ModelBase):
    __tablename__ = "CUSTOMER"
    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    name: Mapped[str] = mapped_column()
    access_point: Mapped[str] = mapped_column(ForeignKey(AccessPointModel.id))
    owned_ip_addresses: Mapped[int] = mapped_column(default=0)
    marketing_bonus: Mapped[bool] = mapped_column(default=False)
    einvoice_bonus: Mapped[bool] = mapped_column(default=False)
    subscription_plan_id: Mapped[int] = mapped_column(
        ForeignKey(SubscriptionModel.plan_id), default=0
    )
    device: Mapped["AccessPointModel"] = relationship(back_populates="customer")
    subscription: Mapped["SubscriptionModel"] = relationship(
        back_populates="subscribers"
    )

    def __repr__(self):
        return f"CustomerModel(id={self.id}, name={self.name}, access_point={self.access_point}, monthly_amount_due={self.monthly_amount_due})"


class InvoiceModel(ModelBase):
    __tablename__ = "INVOICES"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    customer_id: Mapped[str] = mapped_column(ForeignKey(CustomerModel.id))
    customer_name: Mapped[str] = mapped_column()
    month: Mapped[str] = mapped_column(String(10))
    subscription_plan_name: Mapped[str] = mapped_column()
    subscription_used_formula: Mapped[str] = mapped_column()
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
