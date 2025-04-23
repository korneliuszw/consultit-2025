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
            name="Klient indywidualny 600Mbps",
            base_price=5000,
            final_price_formula="BASE_PRICE - 500 * EINVOICE_BONUS - 500 * MARKETING_BONUS",
        ),
        SubscriptionModel(
            name="Klient indywidualny 1Gbps",
            base_price=6000,
            final_price_formula="BASE_PRICE - 500 * EINVOICE_BONUS - 500 * MARKETING_BONUS",
        ),
        SubscriptionModel(
            name="Klient SME Światłowód symetryczny 500Mbps",
            base_price=10000,
            final_price_formula="BASE_PRICE + 500 * max(IP_COUNT - 1, 0) - 2 * DOWNTIME_DAYS * DAILY_RATE",
        ),
        SubscriptionModel(
            name="Klient SME Światłowód symetryczny 1Gbps",
            base_price=15000,
            final_price_formula="BASE_PRICE + 500 * max(IP_COUNT - 1, 0) - 2 * DOWNTIME_DAYS * DAILY_RATE",
        ),
        SubscriptionModel(
            name="Klient SME Światłowód symetryczny 2Gbps",
            base_price=20000,
            final_price_formula="BASE_PRICE + 500 * max(IP_COUNT - 1, 0) - 2 * DOWNTIMES_DAYS * DAILY_RATE",
        ),
        SubscriptionModel(
            name="Klient SME Światłowód symetryczny 4Gbps",
            base_price=30000,
            final_price_formula="BASE_PRICE + 500 * max(IP_COUNT - 1, 0) - 2 * DOWNTIME_DAYS *  DAILY_RATE",
        ),
    ]
    session.add_all(plans)
    session.commit()
