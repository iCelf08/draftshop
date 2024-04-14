from enum import Enum

class PaymentMethodEnum(str, Enum):
    STRIPE = "stripe"
    CARD = "card"