import requests
from bs4 import BeautifulSoup


def fetch_cbr_rates():
    # загружает актуальные курсы валют с сайта ЦБ РФ и возвращает словарь {код: курс}

    url = "https://cbr.ru/currency_base/daily/"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        raise ConnectionError(f"Ошибка загрузки данных с ЦБ РФ: {e}")

    soup = BeautifulSoup(response.content, 'html.parser')  # создаём объект для парсинга HTML
    table = soup.find('table', {'class': 'data'})  # находим таблицу с курсами валют

    if not table:
        raise ValueError("Не удалось найти таблицу курсов на странице ЦБ РФ")

    rates = {}  # словарь для хранения курсов: {код валюты: курс за 1 единицу}

    for row in table.find_all('tr')[1:]:
        cols = row.find_all('td')  # получаем список ячеек в строке

        if len(cols) >= 5:
            try:
                char_code = cols[1].get_text(strip=True)  # код валюты (например, USD)
                nominal = float(cols[2].get_text(strip=True).replace(',', '.'))  # номинал
                value = float(cols[4].get_text(strip=True).replace(',', '.'))  # курс в рублях
                rate = value / nominal  # считаем курс за 1 единицу валюты
                rates[char_code] = rate  # сохраняем в словарь
            except (ValueError, IndexError):
                continue

    if not rates:
        raise ValueError("Не удалось извлечь курсы валют из таблицы")

    return rates  # возвращаем итоговый словарь с курсами


def get_supported_currencies():
    # возвращает список кодов валют (например, USD, EUR, CNY и т.д.)
    try:
        rates = fetch_cbr_rates()  # получаем курсы валют
        return sorted(rates.keys())
    except Exception as e:
        print(f"Предупреждение: не удалось загрузить курсы. Используем дефолтный набор: {e}")
        return ["USD", "EUR", "CNY", "GBP", "JPY"]
