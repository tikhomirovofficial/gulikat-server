import uuid

from yookassa import Configuration, Payment

Configuration.account_id = 218300
Configuration.secret_key = "live_70bzQuA5pYjIBVmCXdRF3Y7LhDJtSdthm04Q18ZkD_w"


def yoo_payment(price, order_id, user_phone):
    print(f"{price:.2f}")
    receipt_items = [
        {
            "description": "Доставка заказа",
            "quantity": "1.00",
            "amount": {
                "value": f"{price:.2f}",
                "currency": "RUB"
            },
            "vat_code": 2,
            "payment_subject": "commodity",
            "payment_mode": "full_prepayment"
        }
    ]
    payment = Payment.create({
        "amount": {
            "value": f"{price:.2f}",
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": f"http://dev.advafert.ru/{order_id}"
        },
        "capture": True,
        "description": "Тестовый заказ",
        "receipt": {
            "items": receipt_items,
            "phone": f"{user_phone}"
        }
    }, uuid.uuid4())
    return payment


def is_payment(payment_id):
    payment = Payment.find_one(payment_id)
    print(payment.status)
    if payment.status == "succeeded":
        return True
    else:
        return False