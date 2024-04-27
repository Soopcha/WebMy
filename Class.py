# # Web-приложение Использовать бибилиотеку Flask
# # Вывод информации по десятизначному (без "8") сотовому номеру телефона РФ
# # (Оператор и Регион) по плану нумерации (файл Numbers-Plan-9.csv).
# # * В лучшем варианте дополнительно проверить был ли номер перенесён
# # он одного сотового оператора к другому (архивированный файл MNP.csv)
#
#
# from flask import Flask, render_template, request
# import csv
#
# app = Flask(__name__)
#
#
# # Функция для загрузки данных из CSV-файла
# def load_data(file_name):
#     data = {}
#     with open(file_name, mode='r', encoding='utf-8') as file:
#         reader = csv.reader(file)
#         next(reader)  # Пропускаем заголовок
#         for row in reader:
#             data[row[0]] = {'Operator': row[1], 'Region': row[2]}
#     return data
#
#
# # Загрузка данных о плане нумерации
# number_plan_data = load_data('Numbers-Plan-9.csv')
#
# # Загрузка данных о переносе номеров
# mnp_data = load_data('MNP.csv')
#
#
# # Главная страница
# @app.route('/')
# def index():
#     return render_template('index.html')
#
#
# # Обработчик формы
# @app.route('/result', methods=['POST'])
# def result():
#     number = request.form['number']
#     if len(number) != 10:
#         return render_template('index.html', error='Номер должен быть десятизначным')
#
#     if '8' in number:
#         return render_template('index.html', error='Номер не должен содержать "8"')
#
#     operator = number_plan_data.get(number[:3])
#     region = "Не найдено"
#     if operator:
#         region = operator['Region']
#         operator = operator['Operator']
#
#     mnp_info = mnp_data.get(number)
#     if mnp_info:
#         operator = mnp_info['Operator']
#         region = mnp_info['Region']
#
#     return render_template('result.html', number=number, operator=operator, region=region)
#
#
# if __name__ == '__main__':
#     app.run(debug=True)
