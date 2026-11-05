import json
from urllib.request import Request, urlopen
from urllib.error import URLError

try:
    n = int(input("Введите размер матрицы: "))
except ValueError:
    print("Ошибка: размер матрицы должен быть целым числом")
    exit()

matrix = []

for i in range(n):
    row = []
    for j in range(n):
        try:
            x = float(input())
        except ValueError:
            print("Ошибка: элемент матрицы должен быть числом")
            exit()
        row.append(x)
    matrix.append(row)

data = json.dumps({"matrix": matrix}).encode("utf-8")

request = Request(
    "http://127.0.0.1:8000/compare",
    data=data,
    headers={"Content-Type": "application/json"},
    method="POST"
)

try:
    with urlopen(request) as response:
        result = json.loads(response.read())
except URLError:
    print("Ошибка: не удалось подключиться к серверу. Проверьте, запущен ли он.")
    exit()

main_sum = result["main_sum"]
sade_sum = result["side_sum"]

if n <= 0:
    print("Матрицы не существует")
elif abs(main_sum - sade_sum) < 0.0000001:
    print("Диагонали равны")
elif main_sum > sade_sum:
    print("Главная диагональ больше")
else:
    print("Побочная диагональ больше")
