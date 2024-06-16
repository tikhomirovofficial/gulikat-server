from django.db import models
from django.contrib.auth.models import User
from cart.models import ProductsInCart
from lk.models import Adress

from settings.models import (
    AllProductsSettings,
)


from market.models import Adress as AdressMarket
from market.models import ProductsInAdress 

from settings.models import (
    OrderSettings,
)

from market.tools.geo import find_nearest_addres


class StatusDelivery(models.Model):
    title = models.CharField(max_length=50, blank=True, verbose_name="Название")

    def __str__(self) -> str:
        return f'{self.title}'
    
    class Meta:
        verbose_name_plural = 'Статусы доставки'


class UserOrderHystory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    products = models.ManyToManyField(ProductsInCart, blank=True, verbose_name="Продукты")
    datetime = models.DateTimeField(auto_now=True, verbose_name="Дата и время")
    price = models.FloatField(null=True, blank=True, verbose_name="Цена")
    user_adress = models.ForeignKey(Adress, on_delete=models.CASCADE, blank=True, verbose_name="Адрес доставки")
    is_call = models.BooleanField(default=True, verbose_name="Требуется звонок?")
    discount = models.IntegerField(default=0)
    market_adress = models.ForeignKey(AdressMarket, on_delete=models.CASCADE, blank=True, verbose_name="Адрес приготовления")
    pyment_id = models.CharField(max_length=700, blank=True, default="None", verbose_name="Номер оплаты")
    is_pyment = models.BooleanField(default=False, verbose_name="Оплачено?")
    status = models.ForeignKey(StatusDelivery, on_delete=models.CASCADE, blank=True, verbose_name="Статус")

    @classmethod
    def create_order_from_cart_user(cls, 
                                    cart_user, 
                                    adress_id=21, 
                                    is_call=True, 
                                    siti_id=1 
                                    ):
        
        order_settings = OrderSettings.objects.last()
        
        # Определяем ближайший адрес сборки заказа
        user_adress_id = adress_id
        siti_id = siti_id
        user_adress = Adress.objects.get(pk=user_adress_id)

        adress_market = find_nearest_addres(user_adress.long, user_adress.lat, siti_id)
        if isinstance(adress_market, Adress):
            print(adress_market)
            return {"status": False, "error": "nearest_adress_not_found"}
        
        user = User.objects.get(pk=cart_user.user.pk)
        cart_user = cart_user

        id_products_in_cart = [i.product.pk for i in cart_user.products.all()]

        products_in_adress = ProductsInAdress.objects.filter(adress = adress_market.pk, products__in=id_products_in_cart)

        not_activ_products = []
        for product_in_adress in products_in_adress:
            if product_in_adress.count == 0 or product_in_adress.products.is_activ == False:
                not_activ_products.append(product_in_adress.pk)
        if len(not_activ_products) > 0:
            return {"status": False, "error": "found_not_activ_products", "products_id": not_activ_products}
        

        order = cls(user=cart_user.user)
        # aps = AllProductsSettings.objects.last()
        # order.discount = aps.total_discount
        


        order.is_call = is_call
        order.market_adress = adress_market
        order.status = StatusDelivery.objects.get(id=1)
        order.user_adress = Adress.objects.get(id=adress_id)
        order.save()

        total_price = 0.0
        if len(cart_user.products.all()) < 1:
            return {"status": False, "error": "null_products_in_cart"}
        
        for product_in_cart in cart_user.products.all():
            product = product_in_cart.product
            order.products.add(product_in_cart)
            total_price += round(product.price * ((1 - (product.discount / 100) if product.discount != 0 else 1)), 2) * product_in_cart.count
        
        order.price = total_price    
        

        order.save()
        return order

    def format_order_info(self):
        order_info = f"Заказ #{self.id}\n"
        order_info += f"Пользователь: {self.user.username}\n"
        order_info += "Товары:\n"

        for product_in_cart in self.products.all():
            if not product_in_cart.is_combo:
                order_info += f"- {product_in_cart.product.title} ({product_in_cart.count} шт.)\n"
                
                for supplement_in_cart in product_in_cart.supplements.all():
                    order_info += f"  - {supplement_in_cart.supplements.title} ({supplement_in_cart.count} шт.)\n"
        
        for product_in_cart in self.products.all():
            if product_in_cart.is_combo:
                order_info += f"- {product_in_cart.combo.combo.title} ({product_in_cart.count} шт.)\n"
                order_info += f"  - {product_in_cart.combo.selected_product.title}\n"

        order_info += f"Сумма заказа: {self.price} рублей\n"
        order_info += f"Тип доставки: {self.delivery_type.title}\n"
        order_info += f"Количество приборов: {self.count_tools}\n"
        if self.delivery_type.pk != 3:
            order_info += f"Адрес доставки: {self.adress}\n"
            order_info += f"Адрес квартира: {self.adress.apartment}\n"  
            order_info += f"Адрес подъезд: {self.adress.entrance}\n"
            order_info += f"Адрес этаж: {self.adress.floor}\n"
            order_info += f"Адрес код двери: {self.adress.door_code}\n"
        else:
            order_info += f"Адрес самовывоза: {self.market_adress_id}\n"
        order_info += f"Тип оплаты: {self.pyment_type.title}\n"
        if self.delivery_type.pk != 3:
            order_info += f"Время доставки: {self.time_delivery}\n"
        else:
            order_info += f"Время получения: {self.time_delivery}\n"
        order_info += f"Способ оплаты: {self.pyment_type}\n"
        if self.change_with != 0:
            order_info += f"Нужна сдача с {self.change_with} рублей\n"
        order_info += f"Нужен звонок оператора: {('Да' if self.is_call else 'Нет')}\n"
        if self.pyment_type.pk == 1:
            order_info += f"Статус оплаты: {'Оплачено' if self.is_pyment else 'Ожидает оплаты'}\n"

        return order_info

    def __str__(self) -> str:
        return f'{self.user}'
    
    class Meta:
        verbose_name_plural = 'Заказы'
