import gradio as gr
from cbr_rates import fetch_cbr_rates, get_supported_currencies


def convert_currency(amount, from_currency, to_currency):
    if amount <= 0:
        return None, "Сумма должна быть больше нуля."
    try:
        rates = fetch_cbr_rates()
    except Exception as e:
        return None, (
            f"Ошибка получения курсов: {e}.<br>"
            "Проверьте подключение или перейдите на сайт ЦБ РФ: "
            "<a href='https://cbr.ru/currency_base/daily/' target='_blank'>Курсы валют ЦБ РФ</a>"
        )
    if from_currency not in rates:
        return None, f"Валюта {from_currency} не поддерживается."
    if to_currency not in rates:
        return None, f"Валюта {to_currency} не поддерживается."
    amount_in_rub = amount * rates[from_currency]
    result = amount_in_rub / rates[to_currency]
    return round(result, 4), f"Конверсия выполнена успешно!<br>"


def create_interface():
    with gr.Blocks() as demo:
        gr.HTML("""
            <h1>Конвертер валют (курсы ЦБ РФ)</h1>
            <p style="font-size: 16px;">
                Актуальные курсы загружаются с официального сайта
                <a href="https://cbr.ru/currency_base/daily/" target="_blank">
                    Центрального банка РФ
                </a>
            </p>
        """)
        with gr.Row():
            amount_input = gr.Number(
                label="Сумма",
                precision=4,
                placeholder="Введите сумму (≥ 0.01)"
            )
            from_currency = gr.Dropdown(
                label="Из валюты",
                choices=get_supported_currencies(),
            )
            to_currency = gr.Dropdown(
                label="В валюту",
                choices=get_supported_currencies(),
            )
        convert_btn = gr.Button("Конвертировать", variant="primary")
        result_output = gr.Number(label="Результат", precision=4)
        with gr.Group():
            error_output = gr.HTML()

        def on_convert(amount, from_curr, to_curr):  # обработчик нажатия кнопки
            result, message = convert_currency(amount, from_curr, to_curr)
            return result, message

        # связывание кнопки с обработчиком
        convert_btn.click(
            on_convert,
            inputs=[amount_input, from_currency, to_currency],
            outputs=[result_output, error_output]
        )
    return demo


if __name__ == "__main__":
    demo = create_interface()
    demo.launch(share=True)
