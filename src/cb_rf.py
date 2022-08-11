import requests
from xml.etree import ElementTree


def get_rate(my_time):
    response = requests.get(f"https://www.cbr.ru/scripts/XML_daily.asp?date_req={my_time}", stream=True)

    response.raw.decode_content = True

    root = ElementTree.parse(response.raw)

    usd = root.find("./Valute[@ID='R01235']")
    usd_value = usd.find("Value")
    return usd_value.text

if __name__ == "__main__":
    print(get_rate('20.05.2022'))
