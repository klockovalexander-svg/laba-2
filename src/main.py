from matrix import calculate_diagonals

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

main_sum, sade_sum = calculate_diagonals(matrix)

if n <= 0:
    print("Матрицы не существует")
elif abs(main_sum - sade_sum) < 0.0000001:
    print("Диагонали равны")
elif main_sum > sade_sum:
    print("Главная диагональ больше")
else:
    print("Побочная диагональ больше")
