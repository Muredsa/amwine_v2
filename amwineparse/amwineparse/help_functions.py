from scrapy_splash.response import Response
import math

def find_number_of_pages(response: Response):
    data = response.text.replace('[', '').replace(']', '').split(',')
    data_list = list(map(lambda item: int(item), list(data)))
    count_products_in_page = data_list[1]
    all_count_products = data_list[0]
    return math.ceil(all_count_products / count_products_in_page)