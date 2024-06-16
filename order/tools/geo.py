import math
from geopy.distance import geodesic

from market.models import (
    Adress,
)

def distance_between_coordinates(lat1, lon1, lat2, lon2):
    earth_radius_m = 6371000

    # Преобразование координат в радианы
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # Разница между координатами
    delta_lat = lat2_rad - lat1_rad
    delta_lon = lon2_rad - lon1_rad

    # Формула Гаверсинуса
    a = math.sin(delta_lat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Расстояние в метрах
    distance_m = earth_radius_m * c

    return distance_m



def find_nearest_addres(longitude, latitude, foodholl=False, gul=False, list_id=[], siti_id=0, is_list_adress=False):
    target_point = (longitude, latitude)
    if foodholl:
        shop = Shop.objects.get(link=1)
        addresses = Adress.objects.filter(shop = shop)
    elif gul:
        shop = [i for i in Shop.objects.get(id__in=[Shop.objects.get(link=2).pk, Shop.objects.get(link=3).pk])]
        addresses = Adress.objects.filter(shop = shop)
    elif is_list_adress:
        addresses = Adress.objects.filter(shop__in=list_id, siti=siti_id)
        print(addresses.count())
    else:
        addresses = Adress.objects.all()

    distances = {}
    for address in addresses:
        address_point = (address.long, address.lat)
        distance = geodesic(target_point, address_point).km
        distances[address] = distance
    
    nearest_address = min(distances, key=distances.get)
    return nearest_address