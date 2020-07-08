import gobal


class PubFun:
    def __init__(self):
        self.chess_size = gobal.get_value('chess_size')
        self.chessboard_size = gobal.get_value('chessboard_size')
        self.chessboard_x_y = gobal.get_value('chessboard_x_y')
        self.grid_width = self.chess_size[0] // 14
        self.piece_size = gobal.get_value('piece_size')

    def arr2pos(self, arr):

        chess_space = (self.chessboard_size[0] - self.chess_size[0]) // 2
        first_dot = (self.chessboard_x_y[0] + chess_space, self.chessboard_x_y[1] + chess_space)
        # end_dot = (self.chess_size[0] - first_dot[0], self.chess_size[1] - first_dot[1])
        pos_x = first_dot[0] + self.grid_width * arr[0] - self.piece_size[0] // 2
        pos_y = first_dot[1] + self.grid_width * arr[1] - self.piece_size[0] // 2
        return pos_x, pos_y

    def getpos(self, mouse_x, mouse_y):
        chess_space = (self.chessboard_size[0] - self.chess_size[0]) // 2
        first_dot = (self.chessboard_x_y[0] + chess_space, self.chessboard_x_y[1] + chess_space)
        x_tmp = round((mouse_x - first_dot[0]) / self.grid_width)  # 计算鼠标最接近的格点
        y_tmp = round((mouse_y - first_dot[1]) / self.grid_width)
        if x_tmp in range(0, 15) and y_tmp in range(0, 15):  # 1到15判断标号是否有效
            pos_x = x_tmp
            pos_y = y_tmp
            return pos_x, pos_y
