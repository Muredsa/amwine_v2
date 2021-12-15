from scrapy.spiders import Spider
from scrapy_splash import SplashRequest

import json

from ..splash_scripts import script_count_pages, script_url_poducts
from ..help_functions import find_number_of_pages


class AmwineSpider(Spider):
    name = 'amwineparse'
    splash_headers = {
        'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36',
        'cookie':'PHPSESSID=8XXWLR1ydXflmegWct9ExxbgIE0bvNxk; AMWINE__CITY_NAME=Москва; AMWINE__CITY_SALE_LOCATION_ID=19; AMWINE__REGION_ELEMENT_ID=342; AMWINE__REGION_ELEMENT_XML_ID=77; AMWINE__REGION_CODE=moscow; AMWINE__AUTO_GEOSERVICE=1; AMWINE__GUEST_ID=97793073; AMWINE__SALE_UID=ed62e3e74ad23fcd8afee8e67d837a73; popmechanic_sbjs_migrations=popmechanic_1418474375998=1|||1471519752600=1|||1471519752605=1; _userGUID=0:kx4nr008:QLCKkwGn7ZgZ~MsNlgDlWRf6h0Z7wkI9; AMWINE__IS_ADULT=Y; AMWINE__AB_HASH=1_8; TEST_AMWINE__AB_HASH=1_8; BX_USER_ID=4fed2f7bcc10700e1cbf2bcf59126176; _ga=GA1.2.1142451021.1639398858; _gid=GA1.2.1669348580.1639398858; _ym_uid=1639398858601693246; _ym_d=1639398858; _fbp=fb.1.1639398858174.2081343788; _hjSessionUser_2478301=eyJpZCI6IjhiN2ZlYmUyLTlhZmEtNTIzMi04OTNjLTc2OWIyOTY0YTYzMiIsImNyZWF0ZWQiOjE2MzkzOTg4NTgxMDQsImV4aXN0aW5nIjp0cnVlfQ==; AMWINE__shop_id=963; dSesn=6a6ef471-77dd-253c-16c0-2b52e2c713f9; _dvs=0:kx79pyio:ns3OyMWFdkEhoXTDP0pSZmAnbWWIRkv6; _ym_isad=1; _ym_visorc=w; _hjSession_2478301=eyJpZCI6ImE5MTA2ODNhLTAzZTctNDU3Yy04OWJmLTc1YTNhYWNjYTUyMSIsImNyZWF0ZWQiOjE2Mzk1NTc2NTM5NjJ9; _hjAbsoluteSessionInProgress=0; AMWINE__LAST_VISIT=15.12.2021 12:53:53; mindboxDeviceUUID=2bded7a3-a150-4976-bc77-6a3bac2fa6a7; directCrm-session={"deviceGuid":"2bded7a3-a150-4976-bc77-6a3bac2fa6a7"}'
    }

    start_urls = [
        #'https://amwine.ru/catalog/krepkie_napitki/viski/',
        'https://amwine.ru/catalog/krepkie_napitki/konyak/',]

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(
                url=url,
                callback=self.parse_pages,
                endpoint='execute',
                splash_headers=self.splash_headers,
                args={
                    'json': 1,
                    'url': url,
                    'lua_source': script_count_pages,
                    'wait': 0
                }
            )

    def parse_pages(self, response):
        url = response.url
        pages_count = find_number_of_pages(response)
        page_prefix = "?page="
        for page_count in range(pages_count-41):
            url_page = f'{url}{page_prefix}{page_count+1}'
            yield SplashRequest(
                url=url_page,
                callback=self.parse_url_item_in_page,
                endpoint='execute',
                splash_headers=self.splash_headers,
                args={
                    'json': 1,
                    'url': url_page,
                    'lua_source': script_url_poducts,
                    'wait': 0
                })

    def parse_url_item_in_page(self, response):
        product_items = json.loads(response.text)
        site_prefix = "https://amwine.ru"
        for item in product_items:
            url_item = site_prefix+item['link']
            yield SplashRequest(
                url=url_item,
                callback=self.parse_item,
                args={
                    'wait': 0
                }
            )


    def parse_item(self,response):
        print("-------------------------------------------------------------------")
        print(response.url)
        print("-------------------------------------------------------------------")
