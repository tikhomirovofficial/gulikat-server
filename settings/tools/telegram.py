import telebot
import threading

# from order.models import (
#     UserOrderHystory
# )

# from settings.models import (
#     TelegaramBotForAdressMarket,
# )

# from order.tools.geo import (
#     find_nearest_addres
# )

from settings.tools.distribution import Distribution

bot = telebot.TeleBot("6676328351:AAHmqaYn9EELamOCxU76UjVSPW8JV2w2vBM", parse_mode=None)

def send_message_auth(phone, code):
    message = f"Номер: {phone}\nВаш код авторизации: {code}"
    bot.send_message("-1002146195106", message)
    return True


# def send_message_order(order_id):
#     order = UserOrderHystory.objects.get(pk=order_id)
#     message = order.format_order_info()
#     bot.send_message("-1002112365906", message)
#     return True


# class TelegramBot(threading.Thread):
#     def __init__(self, order_id):
#         super().__init__()
#         self.order = UserOrderHystory.objects.get(pk=order_id)
#         self.token = "6676328351:AAHmqaYn9EELamOCxU76UjVSPW8JV2w2vBM"
#         # self.chanel = "-1002112365906"
    
#     def run(self):
#         self.set_chanel()
#         self.set_message()
#         self.send_message()

#     def set_chanel(self):
#         if self.order.delivery_type == 3:
#             tbfam = TelegaramBotForAdressMarket.objects.filter(adress=self.order.market_adress_id).first()
#         else:
#             distribution = Distribution(self.order.user.pk, self.order.adress.long, self.order.adress.lat)
#             # print(distribution)
#             adress = find_nearest_addres(self.order.adress.long, self.order.adress.long)
#             # print(adress.pk)
#             resp = distribution.nearest_adresses(adress.siti.pk)
#             # print(resp)

#             tbfam = TelegaramBotForAdressMarket.objects.filter(adress=self.order.market_adress_id).first()
        
#         if tbfam:
#             self.chanel = tbfam.chanel
#             if tbfam.token:
#                 self.token = tbfam.token
#         else:
#             self.chanel = "-1002020687207"

#     def send_message(self):
#         bot = telebot.TeleBot(self.token, parse_mode=None)
#         bot.send_message(self.chanel, self.message)
    
#     def set_message(self):
#         self.message = self.order.format_order_info()