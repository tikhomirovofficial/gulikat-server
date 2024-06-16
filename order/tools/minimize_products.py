from order.models import (
    UserOrderHystory,
)

from market.models import (
    Adress,
    ProductsInAdress,
)

def minimize(order: UserOrderHystory) -> bool:
    product_in_adress = ProductsInAdress.objects.filter(adress=order.market_adress)
    for product in order.products.all():
            pia = product_in_adress.filter(products=product.product.pk).first()
            if pia:
                    pia.count -= product.count
                    pia.save()
    return True