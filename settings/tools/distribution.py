from django.db.models import Count
from collections import Counter
from django.db.models import Q

from django.contrib.auth.models import User

# from order.models import (
#     UserOrderHystory,
# )

# from settings.models import (
#     TelegaramBotForAdressMarket,
# )

# from order.tools.geo import (
#     find_nearest_addres,
# )

# from cart.models import (
#     CartUser,
# )

# from product.models import (
#     Products,
#     Combo,
# )

# from market.models import (
#     Adress,
#     Siti,
#     Shop,
# )

class Distribution:
    def __init__(self, user_id=2, client_long=0.0, client_lat=0.0):
        self.client_long = client_long
        self.client_lat = client_lat
        
        self.user = User.objects.get(pk=user_id)

        # Определяем, все ли товары из одной концепции
        # Гулякин фудхолл готовит всё
        # Гуленьги блинная/пельменная одно и тоже, заказ на фудхол не отправлять, если только они в корзине
        
        # Сначала определяем, из одной концепции ли товары, если да, то возвращаем адрес ближайшей точки этой концепции
        # Если не из одной концепции, то проверяем, только ли товары из гуленьки пельменная/блинная, если да, то вернуть адресс точки
        # В ином случае, ищем точку ближайшего фудхолла
            # Так же проверить есть ли фудхолл в городе заказа, если нету, то вернуть error: "null_foodholl"

    def check_multi_shop(self, city_id):
        cart = CartUser.objects.get(user=self.user)
        product_ids = list(cart.products.filter(is_combo=False).values_list('product__id', flat=True))

        # Все магазы в которых есть товары из корзины
        shops_with_products = set(Products.objects.filter(id__in=product_ids, shop__adress__siti__id=city_id).values_list('shop__id', flat=True))
        # Ищем магаз со всеми товарами корзины
        shops_id = []
        for shop_id in shops_with_products:
            products_in_shop = set(Products.objects.filter(id__in=product_ids, shop__id=shop_id).values_list('id', flat=True))
            if products_in_shop == set(product_ids):
                shops_id.append(shop_id)


        # Поиск комбо
        combo_ids = list(cart.products.filter(is_combo=True).values_list('combo__combo__id', flat=True))

        # Все магазы в которых есть комбо из корзины
        shops_with_combo = set(Combo.objects.filter(id__in=combo_ids).values_list('shop__id', flat=True))
        shops_with_combo = [i for i in shops_with_combo if Adress.objects.filter(shop=i, siti=city_id)]
        # print(shops_with_combo)


        # Ищем магаз со всеми товарами корзины
        combo_shops_id = []
        for shop_id in shops_with_combo:
            combo_in_shop = set(Combo.objects.filter(id__in=combo_ids, shop__id=shop_id).values_list('id', flat=True))
            # print(combo_in_shop)
            # print(combo_ids)
            if combo_in_shop == set(combo_ids):
                combo_shops_id.append(shop_id)
        


        common_shops = list(set(combo_shops_id).intersection(shops_id))
        if common_shops:
            return {"status": True, "shop_id": common_shops}
        
        return {"status": False, "message": "multi_shop", "shop_ids": list(list(shops_with_products) + list(shops_with_combo))}
    
    def check_foodholl_in_siti(self, siti_id):
        siti = Siti.objects.get(id=siti_id)
        shop = Shop.objects.get(link=1)
        adress = Adress.objects.filter(siti = siti, shop = shop)
        if adress:
            return {"status": True, "adress": adress}
        else:
            return {"status": False}
    
    def point_selection(self):
        resp = self.check_multi_shop()
        if resp["status"]:
            return {"shop_id": resp["shop_id"]}
        else:
            if len(resp["shop_ids"]) == 2:
                gul_b = Shop.objects.get(link=2)
                gul_p = Shop.objects.get(link=3)
                if gul_b.pk in resp["shop_ids"] and gul_p.pk in resp["shop_ids"]:
                    return {"shop_id": find_nearest_addres(self.client_long, self.client_lat, gul=True).pk}
                else:
                    return {"shop_id": 1}
            else:
                return {"shop_id": 1}
    
    def check_true_order(self, siti_id, get_adress=False):
        resp = self.check_multi_shop(siti_id)
        if resp["status"]:
            is_foodholl = False
        else:
            is_foodholl = True
            if len(resp["shop_ids"]) == 2:
                gul_b = Shop.objects.get(link=2)
                gul_p = Shop.objects.get(link=3)
                if gul_b.pk in resp["shop_ids"] and gul_p.pk in resp["shop_ids"]:
                    is_foodholl = False
                else:
                    is_foodholl = True
            else:
                is_foodholl = True
        
        if is_foodholl:
            if get_adress:
                foodholl = self.check_foodholl_in_siti(siti_id)
                if foodholl["status"]:
                    return {"status": True, "adress": [{
                        "id": i.pk, 
                        "siti": i.siti.name,
                        "market_id": i.shop.pk, 
                        "market": i.shop.name,
                        "adress": i.adress, 
                        "lat": i.long, 
                        "long": i.lat,
                        "is_around_clock": i.is_around_clock,

                        "time": [
                            [i.monday_with, i.monday_until],
                            [i.tuesday_with, i.tuesday_until],
                            [i.wednesday_with, i.wednesday_until],
                            [i.thursday_with, i.thursday_until],
                            [i.friday_with, i.friday_until],
                            [i.saturday_with, i.saturday_until],
                            [i.sunday_with, i.sunday_until],
                        ],
                        } for i in Adress.objects.filter(shop__in=[1], siti=siti_id)]}
                else:
                    return {"status": False}
            else:
                return {"status": self.check_foodholl_in_siti(siti_id)["status"]}
        else:
            if get_adress:
                return {"status": True, "adress": [{
                    "id": i.pk, 
                    "siti": i.siti.name,
                    "market_id": i.shop.pk, 
                    "market": i.shop.name,
                    "adress": i.adress, 
                    "lat": i.long, 
                    "long": i.lat,
                    "is_around_clock": i.is_around_clock,

                    "time": [
                            [i.monday_with, i.monday_until],
                            [i.tuesday_with, i.tuesday_until],
                            [i.wednesday_with, i.wednesday_until],
                            [i.thursday_with, i.thursday_until],
                            [i.friday_with, i.friday_until],
                            [i.saturday_with, i.saturday_until],
                            [i.sunday_with, i.sunday_until],
                        ],
                    } for i in Adress.objects.filter(shop__in=resp["shop_id"], siti=siti_id)]}
            else:
                return {"status": True}
    
    def nearest_adresses(self, city_id):
        resp = self.check_multi_shop(city_id)
        if resp["status"]:
            response = find_nearest_addres(self.client_long, self.client_lat, is_list_adress=True, siti_id=city_id, list_id=resp["shop_id"])
            return response
        
