def calculate_diagonals(matrix):
    n = len(matrix)
    main_sum = 0
    side_sum = 0

    for i in range(n):
        main_sum += matrix[i][i]
        side_sum += matrix[i][n - 1 - i]

    return main_sum, side_sum
