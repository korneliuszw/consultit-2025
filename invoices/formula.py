from functools import cached_property
from math import floor

from simpleeval import SimpleEval

from database import DbSession
from invoices.downtime_calculator import calculate_customer_downtime
from models import CustomerModel, SubscriptionModel


class FormulaVariables:
    def __init__(
        self, customer: CustomerModel, subscription: SubscriptionModel, month: str
    ):
        self.customer = customer
        self.subscription = subscription
        self.month = month
        self.used_variables = set()

    @cached_property
    def BASE_PRICE(self):
        self.used_variables.add(("BASE_PRICE", self.subscription.base_price))
        return self.subscription.base_price

    @cached_property
    def MARKETING_BONUS(self):
        self.used_variables.add(("MARKETING_BONUS", self.customer.marketing_bonus))
        return self.customer.marketing_bonus

    @cached_property
    def EINVOICE_BONUS(self):
        self.used_variables.add(("EINVOICE_BONUS", self.customer.einvoice_bonus))
        return self.customer.einvoice_bonus

    @cached_property
    def IP_COUNT(self):
        self.used_variables.add(("IP_COUNT", self.customer.owned_ip_addresses))
        return self.customer.owned_ip_addresses

    @cached_property
    def DOWNTIME_DAYS(self):
        with DbSession() as session:
            downtimes = calculate_customer_downtime(session, self.customer, self.month)
            self.used_variables.add(("DOWNTIME_DAYS", downtimes))
            return downtimes

    @cached_property
    def DAILY_RATE(self):
        rate = floor(self.subscription.base_price / 30)
        self.used_variables.add(("DAILY_RATE", rate))
        return rate

    def __getitem__(self, item):
        return getattr(self, item)


class FormulaEval(SimpleEval):
    def __init__(
        self, customer: CustomerModel, subscription: SubscriptionModel, month: str
    ):
        super().__init__()
        self.functions.update(
            max=max,
            min=min,
            floor=floor,
        )
        self.names = FormulaVariables(
            customer=customer, subscription=subscription, month=month
        )

    def get_used_variables(self):
        variables = list(self.names.used_variables)
        variables.sort(key=lambda var: var[0])
        return variables
