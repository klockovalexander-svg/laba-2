n = int(input("Введите размер матрицы: "))
matrix = []

main_sum = 0 
sade_sum = 0 

for i in range(n):
    row = []
    for j in range(n):
        x = float(input())
        row.append(x)
    matrix.append(row)

for i in range(n):
    main_sum += matrix[i][i]
    sade_sum += matrix[i][n - 1 - i]

if main_sum > sade_sum:
    print("Главная диагональ больше")
elif main_sum < sade_sum:
    print("Побочная диагональ больше")
else:
    print("Диагонали равны")