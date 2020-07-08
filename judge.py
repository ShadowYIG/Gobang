import gobal


def is_vector(x, y):
    chess_arr = gobal.get_value('chess_arr')
    # 横
    count = 1
    for i in range(1, 5):
        if 0 <= x + i < 19:
            if chess_arr[x + i][y] == chess_arr[x][y]:
                count += 1
            else:
                break
        else:
            break
    for i in range(1, 5):
        if 0 <= x - i < 19:
            if chess_arr[x - i][y] == chess_arr[x][y]:
                count += 1
            else:
                break
        else:
            break
    if count >= 5:
        return chess_arr[x][y]  # 返回chess_arr当前位置的值，从而得知棋子颜色

    # 竖
    count = 1
    for i in range(1, 5):
        if 0 <= y + i < 19:
            if chess_arr[x][y + i] == chess_arr[x][y]:
                count += 1
            else:
                break
        else:
            break
    for i in range(1, 5):
        if 0 <= y - i < 19:
            if chess_arr[x][y - i] == chess_arr[x][y]:
                count += 1
            else:
                break
        else:
            break
    if count >= 5:
        return chess_arr[x][y]  # 返回chess_arr当前位置的值，从而得知棋子颜色

    # \
    count = 1
    for i in range(1, 5):
        if 0 <= x + i < 19 and 0 <= y + i < 19:
            if chess_arr[x + i][y + i] == chess_arr[x][y]:
                count += 1
            else:
                break
        else:
            break
    for i in range(1, 5):
        if 0 <= x - i < 19 and 0 <= y - i < 19:
            if chess_arr[x - i][y - i] == chess_arr[x][y]:
                count += 1
            else:
                break
        else:
            break
    if count >= 5:
        return chess_arr[x][y]  # 返回chess_arr当前位置的值，从而得知棋子颜色

    # /
    count = 1
    for i in range(1, 5):
        if 0 <= x + i < 19 and 0 <= y - i < 19:
            if chess_arr[x + i][y - i] == chess_arr[x][y]:
                count += 1
            else:
                break
        else:
            break
    for i in range(1, 5):
        if 0 <= x - i < 19 and 0 <= y + i < 19:
            if chess_arr[x - i][y + i] == chess_arr[x][y]:
                count += 1
            else:
                break
        else:
            break
    if count >= 5:
        return chess_arr[x][y]  # 返回chess_arr当前位置的值，从而得知棋子颜色
    draw = 0
    # for i in range(19):
    #     for j in range(19):
    #         if chess_arr[x][y] == 0:
    #             draw = 0
    #             break
    return draw
