import json
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

try:
    n = int(input("Введите размер матрицы: "))
except ValueError:
    print("Ошибка: размер матрицы должен быть целым числом")
    exit()

if n <= 0:
    print("Матрицы не существует")
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

data = json.dumps({
    "version": 1,
    "matrix": matrix
}).encode("utf-8")

request = Request(
    "http://127.0.0.1:8000/compare",
    data=data,
    headers={"Content-Type": "application/json"},
    method="POST"
)

try:
    with urlopen(request, timeout=5) as response:
        result = json.loads(response.read())
except TimeoutError:
    print("Ошибка: сервер не ответил за 5 секунд.")
    exit()
except HTTPError as error:
    if error.code == 409:
        print("Ошибка: версия клиента не поддерживается сервером.")
    else:
        print(f"Ошибка сервера: HTTP {error.code}.")
    error.close()
    exit()
except URLError as error:
    if isinstance(error.reason, TimeoutError):
        print("Ошибка: сервер не ответил за 5 секунд.")
    else:
        print("Ошибка: не удалось подключиться к серверу. "
              "Проверьте, запущен ли он.")
    exit()

main_sum = result["main_sum"]
sade_sum = result["side_sum"]

print("Введённая матрица:")
for row in matrix:
    print(" ".join(f"{value:.3f}" for value in row))

print("Сумма главной диагонали:", main_sum)
print("Сумма побочной диагонали:", sade_sum)

if abs(main_sum - sade_sum) < 0.0000001:
    print("Диагонали равны")
elif main_sum > sade_sum:
    print("Главная диагональ больше")
else:
    print("Побочная диагональ больше")
