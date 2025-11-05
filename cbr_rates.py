import requests
from bs4 import BeautifulSoup


def fetch_cbr_rates():
    url = "https://cbr.ru/currency_base/daily/"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        raise ConnectionError(f"Ошибка загрузки данных с ЦБ РФ: {e}")
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table', {'class': 'data'})
    if not table:
        raise ValueError("Не удалось найти таблицу курсов на странице ЦБ РФ")
    rates = {}
    for row in table.find_all('tr')[1:]:
        cols = row.find_all('td')
        if len(cols) >= 5:
            try:
                char_code = cols[1].get_text(strip=True)  # Код валюты
                nominal = float(cols[2].get_text(strip=True).replace(',', '.'))
                value = float(cols[4].get_text(strip=True).replace(',', '.'))
                rate = value / nominal
                rates[char_code] = rate
            except (ValueError, IndexError):
                continue
    if not rates:
        raise ValueError("Не удалось извлечь курсы валют из таблицы")
    return rates


def get_supported_currencies():
    try:
        rates = fetch_cbr_rates()
        return sorted(rates.keys())
    except Exception as e:
        print(f"Предупреждение: не удалось загрузить курсы. Используем дефолтный набор: {e}")
        return ["USD", "EUR", "CNY", "GBP", "JPY"]
