import gobal
import pygame
import chessboard
import event as ev
import simpleai


def main():
    pygame.init()
    gobal.init()
    screen = pygame.display.set_mode(gobal.get_value('window_size'))
    pygame.display.set_caption(gobal.get_value('title'))
    cb = chessboard.ChessBoard(screen)
    clock = pygame.time.Clock()
    fps = gobal.get_value('fps')
    chess_arr = [[0 for _ in range(19)] for _ in range(19)]
    chess_stack = []
    gobal.set_value('chess_arr', chess_arr)
    gobal.set_value('chess_stack', chess_stack)
    sp_ai = simpleai.SimpleAi()
    while True:
        clock.tick(fps)
        ev.handle_event()
        ev.chess_event()
        ev.vector_event()
        cb.draw_bg()
        cb.draw_chessboard()
        cb.draw_chess()
        cb.draw_box()
        cb.draw_menu()
        cb.draw_game_rule()
        cb.draw_tips()
        cb.draw_mouse()
        cb.draw_vector()
        pygame.display.flip()
        ev.robot_event(sp_ai)


if __name__ == '__main__':
    main()

