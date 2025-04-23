from typing import List

from sqlalchemy.orm import Session

from models import SubscriptionModel


def create_subscription_plans(session: Session):
    plans: List[SubscriptionModel] = [
        SubscriptionModel(
            name="Klient indywidualny 300Mbps",
            base_price=4000,
            final_price_formula="BASE_PRICE - 500 * EINVOICE_BONUS - 500 * MARKETING_BONUS",
        ),
        SubscriptionModel(
            name="Klient SME Światłowód symetryczny 500Mbps",
            base_price=10000,
            final_price_formula="BASE_PRICE + 500 * max(IP_COUNT - 1, 0) - 2 * DOWNTIME_DAYS * DAILY_RATE",
        ),
        SubscriptionModel(
            name="Klient SME Światłowód symetryczny 500Mbps All inclusive",
            base_price=10000,
            final_price_formula="BASE_PRICE + 500 * max(IP_COUNT - 1, 0) - 2 * DOWNTIME_DAYS * DAILY_RATE - 500 * EINVOICE_BONUS - 500 * MARKETING_BONUS",
        ),
    ]
    session.add_all(plans)
    session.commit()
