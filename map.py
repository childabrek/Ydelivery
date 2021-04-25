import requests
import math


class Maps:
    def __init__(self, city):
        self.city = city
        self.cafe_coord = (55.940563, 53.642714)

    def get_coord(self):
        response = requests.get(
            'https://geocode-maps.yandex.ru/1.x',
            params={
                'format': 'json',
                'apikey': "40d1649f-0493-4b70-98ba-98533de7710b",
                'geocode': self.city
            },
        )
        json_response = response.json()
        object1 = json_response['response']['GeoObjectCollection']
        address = object1['featureMember'][0]['GeoObject']['Point']['pos']
        return address

    def get_distance(self):
        # p1 и p2 - это кортежи из двух элементов - координаты точек
        radius = 6373.0
        p2 = self.get_coord().split()
        lon1 = math.radians(self.cafe_coord[0])
        lat1 = math.radians(self.cafe_coord[1])
        lon2 = math.radians(float(p2[0]))
        lat2 = math.radians(float(p2[1]))

        d_lon = lon2 - lon1
        d_lat = lat2 - lat1

        a = math.sin(d_lat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(d_lon / 2) ** 2
        c = 2 * math.atan2(a ** 0.5, (1 - a) ** 0.5)

        distance = radius * c
        return distance

    def get_image(self):
        coord = self.get_coord().split()
        link_img = f'https://static-maps.yandex.ru/1.x/?ll={coord[0]},' \
                   f'{coord[1]}&spn=0.016457,0.00619&l=map&pt={coord[0]},{coord[1]},pm2rdm'
        return link_img

