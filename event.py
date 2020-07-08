import gobal
import pygame
import sys
import main
import pubfun
import judge
import simpleai


def handle_event():
    for event in pygame.event.get():  # 遍历所有事件
        if event.type == pygame.QUIT:  # 如果单击关闭窗口，则退出
            sys.exit()
        if event.type == pygame.BUTTON_WHEELDOWN:
            btn_w, btn_h = gobal.get_value('btn_w_h')
            btn_space = gobal.get_value('btn_space')
            btn_x, btn_y = gobal.get_value('btn_last_x_y')
            game_state = gobal.get_value('game_state')
            mouse_x = pygame.mouse.get_pos()[0]
            mouse_y = pygame.mouse.get_pos()[1]
            if game_state != 5 and btn_x < mouse_x < btn_x + btn_w and (btn_y - 3 * btn_space) < mouse_y < btn_y + btn_h:  # 处于菜单范围内
                menu_event(mouse_y, btn_y, btn_h, btn_space)
                continue
            chessboard_x, chessboard_y = gobal.get_value('chessboard_x_y')
            chessboard_size = gobal.get_value('chessboard_size')
            chess_w, chess_h = gobal.get_value('chess_size')
            chess_space = (chessboard_size[0] - chess_w) // 2
            chess_x = chessboard_x + chess_space
            chess_y = chessboard_y + chess_space
            # 这里预留10个像素，增强边角点击成功率
            if chess_x - 10 < mouse_x < chess_x + chess_w + 10 and chess_y - 10 < mouse_y < chess_y + chess_h + 10:  # 处于棋盘范围内
                if game_state in [2, 3, 4]:
                    if game_state == 4:
                        gobal.set_value('player_operation', 1)
                        player_chess_event(mouse_x, mouse_y)
                    else:
                        player_chess_event(mouse_x, mouse_y)
            if game_state == 5:
                vector_btn_event(mouse_x, mouse_y)


def menu_event(mouse_y, btn_y, btn_h, btn_space):  # 上一个过程已经缩小范围，这里仅需要判断y
    menu_state = gobal.get_value('menu_state')
    # menu_state:
    # 1.           ['开始游戏', '游戏说明', '结束游戏']
    # 2.['人机对战', '双人对战', '返回上级', '结束游戏']
    # 3.['简单模式', '困难模式', '返回上级', '结束游戏']
    # 4.           ['悔    棋', '重新开始', '结束游戏']
    # game_state:1.游戏说明 2.简单模式 3.困难模式 4.双人游戏
    if btn_y - 3 * btn_space < mouse_y < btn_y - 3 * btn_space + btn_h:  # 点击位置在第一个按钮，只有menu2，3有
        if menu_state == 2:  # 人机对战
            gobal.set_value('menu_state', 3)
        elif menu_state == 3:
            gobal.set_value('game_state', 2)
            gobal.set_value('menu_state', 4)
    elif btn_y - 2 * btn_space < mouse_y < btn_y - 2 * btn_space + btn_h:  # 点击位置在第二个按钮，有menu1，2，3，4
        if menu_state == 1:
            gobal.set_value('menu_state', 2)
            gobal.set_value('game_state', 0)
        elif menu_state == 2:
            gobal.set_value('game_state', 4)
            gobal.set_value('menu_state', 4)
        elif menu_state == 3:
            gobal.set_value('game_state', 3)
            gobal.set_value('menu_state', 4)
        elif menu_state == 4:  # 悔棋
            regret_chess_event()
    elif btn_y - btn_space < mouse_y < btn_y - btn_space + btn_h:  # 点击第三个按钮
        if menu_state == 1:
            game_state = gobal.get_value('game_state')
            if game_state == 1:
                gobal.set_value('game_state', 0)
            else:
                gobal.set_value('game_state', 1)
        elif menu_state == 2:
            gobal.set_value('menu_state', 1)
        elif menu_state == 3:
            gobal.set_value('menu_state', 2)
        elif menu_state == 4:
            main.main()  # 直接初始化
    elif btn_y < mouse_y < btn_y + btn_h:  # 点击第四个按钮
        pygame.quit()
        sys.exit()


def chess_event():
    other_event = gobal.get_value('tips_other_event')
    game_state = gobal.get_value('game_state')
    if other_event <= 1 and game_state in [2, 3, 4]:  # 该事件优先级为1，如果存在优先级比这个高则不画事件
        chess_color = gobal.get_value('now_chess_color')
        if chess_color == 1:
            gobal.set_value('tips_color', (255, 255, 255))
            gobal.set_value('tips_text', "白方出棋")
        else:
            gobal.set_value('tips_color', (0, 0, 0))
            gobal.set_value('tips_text', "黑方出棋")
        gobal.set_value('draw_tips', 1)
        gobal.set_value('tips_font_size', 50)
        gobal.set_value('tips_continued_time', -1)


def player_chess_event(mouse_x, mouse_y):
    pf = pubfun.PubFun()
    chess_arr = gobal.get_value('chess_arr')
    chess_color = gobal.get_value('now_chess_color')
    tips_event = gobal.get_value('tips_other_event')
    chess_stack = gobal.get_value('chess_stack')
    x, y = pf.getpos(mouse_x, mouse_y)
    play_opr = gobal.get_value('player_operation')
    # print(x, y)
    if chess_arr[x][y] == 0:
        if play_opr == 1:
            chess_arr[x][y] = chess_color
            chess_stack.append((x, y))
            gobal.set_value('chess_arr', chess_arr)
            gobal.set_value('now_chess_color', -chess_color)
            gobal.set_value('chess_stack', chess_stack)
            is_win = judge.is_vector(x, y)
            if is_win != 0:
                gobal.set_value('game_state', 5)  # 游戏状态为5则为胜利, 6为失败
                gobal.set_value('win_player', is_win)
            for i in chess_arr:
                print(i)
            gobal.set_value('player_operation', 0)
        else:
            pass
    elif tips_event <= 2:
        gobal.set_value('tips_text', "此处已经有棋子")
        gobal.set_value('draw_tips', 1)
        gobal.set_value('tips_color', (180, 0, 0))
        gobal.set_value('tips_font_size', 30)
        gobal.set_value('tips_continued_time', 1)
        gobal.set_value('tips_other_event', 2)  # 该事件优先级为2


def vector_event():
    game_state = gobal.get_value('game_state')
    win_player = gobal.get_value('win_player')
    if game_state == 5:
        if win_player == -1:
            gobal.set_value('win_text', '黑方胜利')
        elif win_player == 1:
            gobal.set_value('win_text', '白方胜利')
        elif win_player == 2:
            gobal.set_value('win_text', '双方平局')


def vector_btn_event(mouse_x, mouse_y):
    bg_size = gobal.get_value('window_size')
    win_btn_text = gobal.get_value('win_btn_text')
    btn_text_size = gobal.get_value('win_btn_text_size')
    btn_x = bg_size[0] // 2 - len(win_btn_text) * btn_text_size // 2
    btn_y = bg_size[1] // 2 + 10
    if btn_x < mouse_x < btn_x + len(win_btn_text) * btn_text_size + 20 and btn_y < mouse_y < btn_y + btn_text_size + 20:
        main.main()


def robot_event(sp_ai):
    game_state = gobal.get_value('game_state')
    player_operation = gobal.get_value('player_operation')
    # print(game_state, player_operation)
    if game_state == 2 and player_operation == 0:
        robot_simple_chess_event(sp_ai)
    elif game_state == 3 and player_operation == 0:
        robot_hard_chess_event()


def robot_simple_chess_event(sp_ai):
    chess_arr = gobal.get_value('chess_arr')
    chess_color = gobal.get_value('now_chess_color')
    chess_stack = gobal.get_value('chess_stack')
    s, x, y = sp_ai.get_best_chess(chess_arr, -1)
    print(s, x, y)
    chess_arr[x][y] = -1
    gobal.set_value('chess_arr', chess_arr)
    chess_stack.append((x, y))
    gobal.set_value('now_chess_color', -chess_color)
    gobal.set_value('chess_stack', chess_stack)
    is_win = judge.is_vector(x, y)
    if is_win != 0:
        gobal.set_value('game_state', 5)  # 游戏状态为5则为胜利, 6为失败
        gobal.set_value('win_player', is_win)
    gobal.set_value('player_operation', 1)



def robot_hard_chess_event():
    pass


def regret_chess_event():
    chess_stack = gobal.get_value('chess_stack')
    chess_arr = gobal.get_value('chess_arr')
    game_state = gobal.get_value('game_state')
    chess_color = gobal.get_value('now_chess_color')
    player_operation = gobal.get_value('player_operation')
    if len(chess_stack) != 0:
        if game_state in [2, 3 and len(chess_stack) >= 2] and player_operation:  # 人机模式，退2颗棋
            for _ in range(2):
                x, y = chess_stack.pop(-1)
                chess_arr[x][y] = 0
            gobal.set_value('chess_arr', chess_arr)
        elif game_state == 4:  #双人模式,退1颗棋,换执子手
            x, y = chess_stack.pop(-1)
            chess_arr[x][y] = 0
            gobal.set_value('now_chess_color', -chess_color)
            gobal.set_value('chess_arr', chess_arr)
        else:
            gobal.set_value('tips_text', "非玩家操作阶段")
            gobal.set_value('draw_tips', 1)
            gobal.set_value('tips_color', (180, 0, 0))
            gobal.set_value('tips_font_size', 30)
            gobal.set_value('tips_continued_time', 1)
            gobal.set_value('tips_other_event', 2)  # 该事件优先级为2
    else:
        gobal.set_value('tips_text', "当前棋盘无棋子")
        gobal.set_value('draw_tips', 1)
        gobal.set_value('tips_color', (180, 0, 0))
        gobal.set_value('tips_font_size', 30)
        gobal.set_value('tips_continued_time', 1)
        gobal.set_value('tips_other_event', 2)  # 该事件优先级为2