# # Web-приложение Использовать бибилиотеку Flask
# # Вывод информации по десятизначному (без "8") сотовому номеру телефона РФ
# # (Оператор и Регион) по плану нумерации (файл Numbers-Plan-9.csv).
# # * В лучшем варианте дополнительно проверить был ли номер перенесён
# # он одного сотового оператора к другому (архивированный файл MNP.csv)
#
#


from flask import Flask, render_template, request
import csv
import zipfile

# Инициализация Flask приложения
app = Flask(__name__)

# Функция загрузки данных из архивированного файла MNP.csv
def load_mnp_data(filename):
    mnp_data = {}
    with zipfile.ZipFile(filename) as zfile:
        with zfile.open('MNP.csv', mode='r') as file:
            reader = csv.reader((line.decode('utf-8') for line in file))
            next(reader)  # Пропускаем заголовок
            # Обработка строк файла и добавление информации в словарь
            for row in reader:
                number = row[0]
                ported_to_operator = row[1]
                mnp_data[number] = ported_to_operator
    return mnp_data

# Загружаем данные из CSV-файла Numbers-Plan-9.csv
def load_number_plan(filename):
    number_plan = {}
    # Открытие CSV-файла и чтение данных
    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Пропускаем заголовок
        # Обработка строк файла и добавление информации в словарь
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
    # Загрузка данных о плане нумерации и данных о переносе номеров
    number_plan = load_number_plan('Numbers-Plan-9.csv')
    mnp_data = load_mnp_data('MNP.zip')  # Загружаем данные из архивированного файла MNP.zip
    # Получение номера из формы
    number = request.form['number']
    # Получение информации о номере из плана нумерации
    info = number_plan.get(number[:3], {'operator': 'Оператор не найден', 'region': ['Регион не найден']})
    operator = info['operator']
    regions = info['region']

    # Проверяем, был ли номер перенесен
    if number in mnp_data:
        ported_to_operator = mnp_data[number]
        return render_template('result.html', operator=operator, regions=regions, ported_to_operator=ported_to_operator)
    else:
        return render_template('result.html', operator=operator, regions=regions,
                               ported_to_operator="Номер не был перенесен")
# Запуск Flask приложения
if __name__ == '__main__':
    app.run(debug=True)
