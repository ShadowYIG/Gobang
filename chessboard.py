import gobal
import pygame
import pubfun


class ChessBoard:
    def __init__(self, screen):
        self.screen = screen
        self.bg_img = pygame.image.load(gobal.get_value('bg_dict'))
        self.chess_size = gobal.get_value('chess_size')
        self.bg_size = gobal.get_value('window_size')
        self.chessboard_size = gobal.get_value('chessboard_size')
        self.piece_size = gobal.get_value('piece_size')

        self.chessboard_img = pygame.image.load(gobal.get_value('chessboard_dict'))
        self.chessboard_img = pygame.transform.scale(self.chessboard_img, self.chessboard_size)
        self.write_img = pygame.image.load(gobal.get_value('white_chess_dict'))
        self.write_img = pygame.transform.scale(self.write_img, self.piece_size)
        self.black_img = pygame.image.load(gobal.get_value('black_chess_dict'))
        self.black_img = pygame.transform.scale(self.black_img, self.piece_size)
        self.red_img = pygame.image.load(gobal.get_value('red_box_dict'))
        self.red_img = pygame.transform.scale(self.red_img, (self.piece_size[0], self.piece_size[1]))
        self.chess_space = (self.chessboard_size[0] - self.chess_size[0]) // 2
        self.grid_width = self.chess_size[0] // 14
        self.chessboard_x_y = gobal.get_value('chessboard_x_y')
        self.chess_line_color = gobal.get_value('chess_line_color')
        self.pf = pubfun.PubFun()
        self.tips_time = pygame.time.get_ticks()
        self.tips_start = 0

    def draw_bg(self):
        self.screen.blit(self.bg_img, (0, 0))

    def draw_chessboard(self):
        # 加载背景图片
        self.screen.blit(self.chessboard_img, self.chessboard_x_y)
        # 画网格线，棋盘为 15行 15列的
        grid_width = self.grid_width
        # print(grid_width)
        chess_size = self.chess_size
        chessboard_size = self.chessboard_size
        chessboard_x_y = self.chessboard_x_y
        chess_space = (chessboard_size[0] - chess_size[0]) // 2
        first_dot = (chessboard_x_y[0] + chess_space, chessboard_x_y[1] + chess_space)
        end_dot = (first_dot[0] + chess_size[0], first_dot[1] + chess_size[1])
        rect_lines = [
            (first_dot, (first_dot[0], end_dot[1])),
            (first_dot, (end_dot[0], first_dot[1])),
            ((first_dot[0], end_dot[1]), end_dot),
            ((end_dot[0], first_dot[1]), end_dot),
        ]
        for line in rect_lines:
            pygame.draw.line(self.screen, self.chess_line_color, line[0], line[1], 3)

        # 画出中间的网格线
        for i in range(13):
            pygame.draw.line(self.screen, self.chess_line_color, (first_dot[0], first_dot[1] + grid_width * (i + 1)),
                             (end_dot[0], first_dot[1] + grid_width * (i + 1)))
            pygame.draw.line(self.screen, self.chess_line_color,
                             (first_dot[0] + grid_width * (i + 1), first_dot[1]),
                             (first_dot[0] + grid_width * (i + 1), end_dot[1]))

        # 画出棋盘中的9个点
        chess_dot = [(3, 3), (3, 7), (3, 11), (7, 3), (7, 7), (7, 11), (11, 3), (11, 7), (11, 11)]
        for i, j in chess_dot:
            pygame.draw.circle(self.screen, self.chess_line_color,
                               (first_dot[0] + grid_width * i, first_dot[1] + grid_width * j), 5)

    def draw_chess(self):
        chess_arr = gobal.get_value('chess_arr')
        for i in range(19):
            for j in range(19):
                if chess_arr[i][j] == 1:  # 1为白棋，-1为黑棋，0为无
                    self.screen.blit(self.write_img, self.pf.arr2pos((i, j)))
                elif chess_arr[i][j] == -1:
                    self.screen.blit(self.black_img, self.pf.arr2pos((i, j)))

    def draw_menu(self):
        menu_state = gobal.get_value('menu_state')
        game_state = gobal.get_value('game_state')
        menu = gobal.get_value('menu1')
        btn_color = gobal.get_value('btn_color')
        btn_activate_color = gobal.get_value('btn_activate_color')
        btn_last_x_y = gobal.get_value('btn_last_x_y')
        btn_text_space = gobal.get_value('btn_text_space')
        btn_font_size = gobal.get_value('btn_font_size')
        btn_w_h = gobal.get_value('btn_w_h')
        btn_space = gobal.get_value('btn_space')
        font = gobal.get_value('font')
        mouse_x = pygame.mouse.get_pos()[0]
        mouse_y = pygame.mouse.get_pos()[1]
        if menu_state == 2:
            menu = gobal.get_value('menu2')
        elif menu_state == 3:
            menu = gobal.get_value('menu3')
        elif menu_state == 4:
            menu = gobal.get_value('menu4')
        re_menu = menu[::-1]
        for i in range(len(menu)):
            x, y, w, h = btn_last_x_y[0], btn_last_x_y[1] - i * btn_space, btn_w_h[0], btn_w_h[1]
            color = btn_color
            if x < mouse_x < x + w and y < mouse_y < y + h and game_state != 5:  # 游戏状态不能为游戏结束
                color = btn_activate_color
            pygame.draw.rect(self.screen, color, [x, y, w, h], 5)
            my_font = pygame.font.SysFont(font, btn_font_size)
            text = my_font.render(re_menu[i], True, color)
            self.screen.blit(text, (x + btn_text_space[0], y + btn_text_space[1]))

    def draw_game_rule(self):
        game_state = gobal.get_value('game_state')
        if game_state == 1:
            font = gobal.get_value('font')
            font_size = gobal.get_value('rule_font_size')
            color = gobal.get_value('rule_color')
            my_font = pygame.font.SysFont(font, font_size)
            pygame.draw.rect(self.screen, color, [640, 120, 220, 140], 3)
            text1 = my_font.render("双方分别用黑白棋子", True, color)
            text2 = my_font.render("下在棋盘的交叉点上", True, color)
            text3 = my_font.render("先形成五子连线者获胜", True, color)
            text4 = my_font.render("连线为横竖斜均可", True, color)
            self.screen.blit(text1, (650, 130))
            self.screen.blit(text2, (650, 160))
            self.screen.blit(text3, (650, 190))
            self.screen.blit(text4, (650, 220))

    def draw_tips(self):
        draw = gobal.get_value('draw_tips')
        tips_text = gobal.get_value('tips_text')
        if draw == 1:
            font = gobal.get_value('font')
            font_size = gobal.get_value('tips_font_size')
            color = gobal.get_value('tips_color')
            tips_x_y = gobal.get_value('tips_x_y')
            tips_continued_time = gobal.get_value('tips_continued_time')
            my_font = pygame.font.SysFont(font, font_size)
            text = my_font.render(tips_text, True, color)
            self.screen.blit(text, tips_x_y)
            if tips_continued_time != -1 and self.tips_start:
                if (pygame.time.get_ticks() - self.tips_time)/1000 >= tips_continued_time:
                    gobal.set_value('draw_tips', 0)
                    gobal.set_value('tips_text', '')
                    gobal.set_value('tips_other_event', 0)  # 将优先级值为最低，以便其他tips显示
                    self.tips_start = 0
            else:
                self.tips_start = 1
                self.tips_time = pygame.time.get_ticks()

    def draw_mouse(self):
        mouse_x = pygame.mouse.get_pos()[0]
        mouse_y = pygame.mouse.get_pos()[1]
        btn_space = gobal.get_value('btn_space')
        btn_x, btn_y = gobal.get_value('btn_last_x_y')
        btn_w, btn_h = gobal.get_value('btn_w_h')
        menu_state = gobal.get_value('menu_state')
        game_state = gobal.get_value('game_state')
        chess_follow = gobal.get_value('chess_follow')
        if menu_state in [2, 3]:
            if btn_y - 3 * btn_space < mouse_y < btn_y - 3 * btn_space + btn_h:  # 点击位置在第一个按钮，只有menu2，3有
                pass
        else:
            if btn_y - 2 * btn_space < mouse_y < btn_y - 2 * btn_space + btn_h:  # 点击位置在第一个按钮，只有menu2，3有
                pass
            elif btn_y - 1 * btn_space < mouse_y < btn_y - 1 * btn_space + btn_h:  # 点击位置在第一个按钮，只有menu2，3有
                pass
            elif btn_y * btn_space < mouse_y < btn_y * btn_space + btn_h:  # 点击位置在第一个按钮，只有menu2，3有
                pass
        if game_state in [2, 3, 4] and chess_follow:  # 经测试低于40fps会大程度影响游戏体验因此自动不开启跟随
            chess_w, chess_h = self.chess_size
            chess_x = self.chessboard_x_y[0] + self.chess_space - 5  # 这里预留5个像素
            chess_y = self.chessboard_x_y[1] + self.chess_space - 5  # 这里预留5个像素
            chess_color = gobal.get_value('now_chess_color')
            if chess_x < mouse_x < chess_w - chess_x + 5 and chess_y < mouse_y < chess_h - chess_y + 5:
                if chess_color == 1:
                    self.screen.blit(self.write_img, (mouse_x - 16, mouse_y - 16))
                elif chess_color == -1:
                    self.screen.blit(self.black_img, (mouse_x - 16, mouse_y - 16))
                pygame.mouse.set_visible(False)
            else:
                pygame.mouse.set_visible(True)

    def draw_vector(self):
        game_state = gobal.get_value('game_state')
        if game_state == 5:  # 游戏结束
            font = gobal.get_value('font')
            font_size = gobal.get_value('win_text_size')
            win_color = gobal.get_value('win_color')
            btn_color = gobal.get_value('win_btn_color')
            win_text = gobal.get_value('win_text')
            btn_text_size = gobal.get_value('win_btn_text_size')
            win_btn_text = gobal.get_value('win_btn_text')
            win_x = self.bg_size[0] // 2 - len(win_text) * font_size // 2
            win_y = self.bg_size[1] // 2 - font_size - 10  # 按钮与字体之间预留20px
            btn_x = self.bg_size[0] // 2 - len(win_btn_text) * btn_text_size // 2
            btn_y = self.bg_size[1] // 2 + 10
            my_font = pygame.font.SysFont(font, font_size)
            text = my_font.render(win_text, True, win_color)
            self.screen.blit(text, (win_x, win_y))
            mouse_x = pygame.mouse.get_pos()[0]
            mouse_y = pygame.mouse.get_pos()[1]
            if btn_x < mouse_x < btn_x + len(win_btn_text) * btn_text_size + 20 and btn_y < mouse_y < btn_y + btn_text_size + 20:
                btn_color = gobal.get_value('win_btn_activate_color')
            my_font = pygame.font.SysFont(font, btn_text_size)
            text1 = my_font.render(win_btn_text, True, btn_color)
            self.screen.blit(text1, (btn_x + 10, btn_y + 10))
            pygame.draw.rect(self.screen, btn_color, [btn_x, btn_y, len(win_btn_text) * btn_text_size + 20, btn_text_size + 20], 3)

    def draw_box(self):
        chess_stack = gobal.get_value('chess_stack')
        if len(chess_stack) > 0:
            self.screen.blit(self.red_img, self.pf.arr2pos((chess_stack[-1][0], chess_stack[-1][1])))
