global_dict = {}
# 1.游戏说明 2.简单模式 3.困难模式 4.双人游戏


def init():
    global global_dict
    global_dict = {
        'window_size': (900, 650),
        'fps': 30,
        'chess_size': (560, 560),
        'piece_size': (36, 36),
        'chessboard_x_y': (20, 20),
        'chessboard_size': (600, 600),
        'chess_line_color': (0, 0, 0),
        'game_state': 0,  # 游戏状态0.无 1.游戏规则 2.人机简单 3.人机困难 4. 双人游戏 5.游戏结束
        'menu_state': 1,
        'font': 'simsunnsimsun',
        'rule_font_size': 20,
        'rule_color': (0, 0, 0),
        'btn_font_size': 30,
        'btn_w_h': (140, 50),
        'btn_color': (132, 71, 34),
        'btn_activate_color': (0, 140, 0),
        'btn_space': 90,
        'btn_last_x_y': (670, 500),
        'btn_text_space': (10, 10),
        'title': '五子棋',
        'tips_text': '',
        'tips_font_size': 50,
        'tips_x_y': (650, 140),
        'tips_color': (0, 0, 0),
        'tips_continued_time': -1,
        'draw_tips': 0,
        'tips_other_event': 0,
        'white_chess_dict': r'img\chesswhite.png',
        'black_chess_dict': r'img\chessblack.png',
        'red_box_dict': r'img\redbox.png',
        'bg_dict': r'img\bg.png',
        'chessboard_dict': r'img\chessboard.png',
        'black': (0, 0, 0),
        'white': (255, 255, 255),
        'menu1': ['开始游戏', '游戏说明', '结束游戏'],
        'menu2': ['人机对战', '双人对战', '返回上级', '结束游戏'],
        'menu3': ['简单模式', '困难模式', '返回上级', '结束游戏'],
        'menu4': ['悔    棋', '重新开始', '结束游戏'],
        'now_chess_color': -1,  # 1为白棋，-1为黑棋，0为无
        'chess_follow': 0,  # fps低于40不建议开启
        'player_operation': 0,  # 1为玩家回合 0为机器回合
        'win_player': 0,  # -1为黑棋，1为白棋, 2为平局
        'win_text': '',
        'win_text_size': 80,
        'win_color': (0, 0, 0),
        'win_btn_color': (0, 0, 0),
        'win_btn_activate_color': (0, 140, 0),
        'win_btn_text_size': 30,
        'win_btn_text': '确　　定',


        'search_depth': 4,
        'Chess_score': {
            'EFive': 100000,
            'LFour': 10000,
            'LThree': 1000,
            'LTwo': 100,
            'LOne': 10,
            'DFour': 1000,
            'DThree': 100,
            'DTwo': 10,
            'None': 0,
        }
    }


def set_value(name, value):
    global_dict[name] = value


def get_value(name, defvalue=None):
    try:
        return global_dict[name]
    except KeyError:
        return defvalue
