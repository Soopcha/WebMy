# # Web-приложение Использовать бибилиотеку Flask
# # Вывод информации по десятизначному (без "8") сотовому номеру телефона РФ
# # (Оператор и Регион) по плану нумерации (файл Numbers-Plan-9.csv).
# # * В лучшем варианте дополнительно проверить был ли номер перенесён
# # он одного сотового оператора к другому (архивированный файл MNP.csv)
#
#


from flask import Flask, render_template, request
import csv

app = Flask(__name__)

# Загружаем данные из CSV-файла
def load_number_plan(filename):
    number_plan = {}
    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Пропускаем заголовок
        for row in reader:
            number = row[0]
            operator = row[1]
            region = row[2]
            if number in number_plan:
                number_plan[number]['region'].append(region)
            else:
                number_plan[number] = {'operator': operator, 'region': [region]}
    return number_plan

# Главная страница с формой для ввода номера
@app.route('/')
def index():
    return render_template('index.html')

# Обработка запроса и вывод результата
@app.route('/search', methods=['POST'])
def search():
    number_plan = load_number_plan('Numbers-Plan-9.csv')
    number = request.form['number']
    info = number_plan.get(number[:3], {'operator': 'Оператор не найден', 'region': ['Регион не найден']})
    operator = info['operator']
    regions = info['region']
    return render_template('result.html', operator=operator, regions=regions)

if __name__ == '__main__':
    app.run(debug=True)
