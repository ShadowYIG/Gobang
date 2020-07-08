import gobal
from random import randint
import re

# class ZobristHash:
#     def __init__(self):
#         self.max = 2**32
#         self.len = 15
#         self.player1 = [[self.get_random() for x in range(self.len)] for y in range(self.len)]
#         self.player2 = [[self.get_random() for x in range(self.len)] for y in range(self.len)]
#         self.data = [self.player1, self.player2]
#         self.code = self.get_random()
#         self.cache = {}
#
#     def get_random(self):
#         return randint(1, self.max)
#
#     def generate(self, index, x, y):
#         self.code = self.code ^ self.data[index][y][x]
#
#     def reset_cache(self):
#         self.cache = {}
#
#     def get_cache(self):
#         if self.code in self.cache:
#             return self.cache[self.code]
#         else:
#             return None
#
#     def set_cache(self, depth, score):
#         self.cache[self.code] = (depth, score)


class SimpleAi:
    def __init__(self):
        self.score = gobal.get_value('Chess_score')
        self.s_alpha = gobal.get_value('alpha')
        self.s_beta = gobal.get_value('beta')
        self.belta = 0
        self.alpha = 0
        self.best_move = (7, 7)
        self.depth = gobal.get_value('search_depth')

    @staticmethod
    def get_line(board, x, y, role, direction):
        line = [0 for _ in range(9)]
        temp_x = x + (-5 * direction[0])  # 从当前点向前偏移5位，下面有+1位实际上是4位
        temp_y = y + (-5 * direction[1])
        for i in range(9):
            temp_x = temp_x + direction[0]
            temp_y = temp_y + direction[1]
            # print(temp_x, temp_y)
            if temp_x < 0 or temp_x >= 15 or temp_y < 0 or temp_y >= 15:
                line[i] = -role  # 将边界值为对方棋
            else:
                line[i] = board[temp_x][temp_y]
        return line

    # 报废
    def get_score_count(self, board, x, y, role, direction):
        line = self.get_line(board, x, y, role, direction)
        m_range_left, m_range_right = 4, 4
        count = {'EFive': 0, 'LFour': 0, 'LThree': 0, 'LTwo': 0, 'LOne': 0,
                 'DFour': 0, 'DThree': 0, 'DTwo': 0, 'DOne': 0}
        while m_range_left >= 0:  # 获取自己棋子的范围
            if line[m_range_left] != role:
                break
            m_range_left -= 1

        while m_range_right < 9:
            if line[m_range_right] != role:
                break
            m_range_right += 1

        # 获取对方棋子首次出现位置
        o_range_left, o_range_right = m_range_left, m_range_right
        while o_range_left >= 0:
            if line[o_range_left] == -role:
                break
            o_range_left -= 1

        while o_range_right < 9:
            if line[o_range_right] == -role:
                break
            o_range_right += 1

        m_count = m_range_right - m_range_left - 1
        o_count = o_range_right - o_range_left - 1  # 可为自己棋数量
        # print(line, o_range_right, o_range_left, m_range_right, m_range_left, m_count, o_count)
        # print(m_count, o_count)
        if m_count == 5:
            count['EFive'] += 1
            return count
        block = 0
        if m_range_right == o_range_right:  # 右边被封
            block += 1
        if m_range_left == o_range_left:  # 左边被封
            block += 1

        # 011110, 21111, 11112, 211112
        if m_count == 4:
            if block == 0:
                count['LFour'] += 1
            elif block == 1:
                count['DFour'] += 1
            else:
                pass

        # 001110, 011100, 11100, 00111, 10111, 11101, 211100, 001112, 21112
        if m_count == 3:
            if block == 2:
                pass
            elif block == 1 and o_count >= 5:
                if (m_range_left - 1 >= 0 and line[m_range_left - 1] == role and line[m_range_left] != -role) or \
                        (m_range_right + 1 < 9 and line[m_range_right + 1] == role and line[m_range_right] != -role):
                    count['DFour'] += 1
                else:
                    count['DThree'] += 1
            elif block == 0:
                count['LThree'] += 1

        # 00110, 01100, 21100, 20110, 2112, 10110,
        if m_count == 2:
            if block == 2:
                pass
            elif block == 1:
                count['DTwo'] += 1
            elif block == 0:
                if (line[m_range_left] == 0 and m_range_left - 1 >= 0 and line[m_range_left - 1] == role and
                    m_range_left - 2 >= 0 and line[m_range_left] != -role) or \
                    (line[m_range_right] == 0 and m_range_right + 1 < 9 and line[m_range_right + 1] == role and
                        m_range_right + 2 < 9 and line[m_range_right] != -role):
                    count['LThree'] += 1
                else:
                    count['LTwo'] += 1
            else:
                pass

        return count

    # 获得某点的得匹配数量
    def get_count(self, board, x, y, role, direction):
        line = self.get_line(board, x, y, role, direction)
        str_line = self.line_to_string(line)
        count = {'EFive': 0, 'LFour': 0, 'LThree': 0, 'LTwo': 0, 'LOne': 0,
                 'DFour': 0, 'DThree': 0, 'DTwo': 0, 'DOne': 0}
        EFive = [['11111'], ['-1-1-1-1-1']]
        LFour = [['011110'], ['0-1-1-1-10']]
        DFour = [['01111-1', '0101110', '0110110'], ['0-1-1-1-11', '0-10-1-1-10',  '0-1-10-1-10']]
        LThree = [['01110', '010110'], ['0-1-1-10', '0-10-1-10']]
        DThree = [['00111-1', '01011-1', '01101-1', '10011', '10101', '-101110-1'], ['00-1-1-11',
                  '0-10-1-11', '0-1-10-11', '-100-1-1', '10-1-1-101']]
        LTwo = [['00110', '01010', '010010'], ['00-1-10', '0-10-10', '0-100-10']]
        DTwo = [['00011-1', '00101-1', '01001-1', '10001', '-101010-1', '-101100-1'],
                ['000-1-11', '00-10-11', '0-100-11', '-1000-1', '10-10-101', '10-1-1001']]
        index = 0
        if role == 1:
            index = 0
        else:
            index = 1
        for costr in EFive[index]:
            if costr in str_line:
                count['EFive'] += 1
        for costr in LFour[index]:
            if costr in str_line:
                count['LFour'] += 1
        for costr in DFour[index]:
            if costr in str_line:
                count['DFour'] += 1
        for costr in LThree[index]:
            if costr in str_line:
                count['LThree'] += 1
        for costr in DThree[index]:
            if costr in str_line:
                count['DThree'] += 1
        for costr in LTwo[index]:
            if costr in str_line:
                count['LTwo'] += 1
        for costr in DTwo[index]:
            if costr in str_line:
                count['DTwo'] += 1
        return count

    @staticmethod
    def line_to_string(line):
        str_line = ""
        for i in range(len(line)):
            str_line += str(line[i])
        return str_line

    def count_to_score(self, count, role):
        score = 0
        weight = 1
        if role != -1:
            weight = 0.9
        if count['EFive'] > 0:
            score += self.score['EFive']
        if count['LFour'] > 0:
            score += self.score['LFour']
        if count['DFour'] > 0:
            score += self.score['DFour']
        # if count['LThree'] == 2:
        #     score += self.score['LThree']
        if count['LThree'] > 0:
            score += self.score['LThree']
        if count['DThree'] > 0:
            score += self.score['DThree']
        if count['LTwo'] > 0:
            score += self.score['LTwo']
        if count['DTwo'] > 0:
            score += self.score['DTwo']
        return score * weight

    # 获得某点的总分
    def get_score(self, board, x, y, role):
        direction = [(1, 0), (0, 1), (1, 1), (1, -1)]  # 4个方向
        score = 0
        position = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 0],
            [0, 1, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 1, 0],
            [0, 1, 2, 3, 4, 4, 4, 4, 4, 4, 4, 3, 2, 1, 0],
            [0, 1, 2, 3, 4, 5, 5, 5, 5, 5, 4, 3, 2, 1, 0],
            [0, 1, 2, 3, 4, 5, 6, 6, 6, 5, 4, 3, 2, 1, 0],
            [0, 1, 2, 3, 4, 5, 6, 7, 6, 5, 4, 3, 2, 1, 0],
            [0, 1, 2, 3, 4, 5, 6, 6, 6, 5, 4, 3, 2, 1, 0],
            [0, 1, 2, 3, 4, 5, 5, 5, 5, 5, 4, 3, 2, 1, 0],
            [0, 1, 2, 3, 4, 4, 4, 4, 4, 4, 4, 3, 2, 1, 0],
            [0, 1, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 1, 0],
            [0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        for dire in direction:
            count = self.get_count(board, x, y, role, dire)
            score = score + self.count_to_score(count, role)
        score = score + position[x][y]
        return score

    @staticmethod
    def has_neighbor(board, x, y, distance=1, count=1):
        start_x, end_x = x - distance, x + distance
        start_y, end_y = y - distance, y + distance
        for i in range(start_x, end_x + 1):
            for j in range(start_y, end_y + 1):
                if 0 <= i < 15 and 0 <= j < 15:
                    if board[i][j] != 0:
                        count -= 1
                    if count <= 0:
                        return True

    # 获取周围存在棋子的点
    def get_chess(self, board):
        chess = []
        score = 0
        for i in range(15):
            for j in range(15):
                if self.has_neighbor(board, i, j) and board[i][j] == 0:
                    chess.append([score, i, j])
        # print(chess)
        chess.sort(reverse=True)
        return chess

    # 获得棋盘得分
    def get_chess_score(self, board, role):
        chess = self.get_chess(board)
        for che in chess:
            board[che[1]][che[2]] = role
            score = self.get_score(board, che[1], che[2], role)
            board[che[1]][che[2]] = -role
            score1 = self.get_score(board, che[1], che[2], -role)
            board[che[1]][che[2]] = 0
            che[0] = score - score1
            # print(che[1], che[2], score, score1)
        for i in range(len(chess)):
            for j in range(1, len(chess) - i):
                if abs(chess[j - 1][0]) < abs(chess[j][0]):  # 如果前者比后者大
                    chess[j - 1], chess[j] = chess[j], chess[j - 1]  # 则交换两者
        return chess

    def alpha_beta(self, board, role, depth, alp=-0x7fffffff, beta=0x7fffffff):
        chess = self.get_chess_score(board, role)
        score = 0
        if len(chess) > 0:
            score = chess[0][0]
            if depth <= 0 or score >= self.score['EFive']:
                self.best_move = (chess[0][1], chess[0][2])
                return score
        moves = chess[:5]  # 获取前5个点进行扩展
        best_move = None
        self.alpha += len(moves)
        if len(moves) == 0:
            return score
        for _, x, y in moves:
            board[x][y] = role
            score = -self.alpha_beta(board, -role, depth - 1, -beta, -alp)
            board[x][y] = 0
            self.belta += 1
            # if depth % 2 == 0:
            if score > alp:
                alp = score
                best_move = (x, y)
            if alp >= beta:
                break
            # else:
            #     if score < beta:
            #         beta = score
            #     if alp >= beta:
            #         break
        if depth == self.depth and best_move:
            self.best_move = best_move
        return alp

    def get_best_chess(self, board, role):
        chess_stack = gobal.get_value('chess_stack')
        depth = self.depth
        chess = []
        if len(chess_stack) == 0:
            return 0, 7, 7
        if len(chess_stack) <= 6:
            depth = 4
        score = self.alpha_beta(board, role, depth)
        print(score, self.best_move)
        return score, self.best_move[0], self.best_move[1]


if __name__ == '__main__':
    gobal.init()
    ai = SimpleAi()
    a = '-1-1-1-1-1'
            #  0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15
    board1 = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 0
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 1
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 2
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 3
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 4
             [0, 0, 0, 0, 0, 0, 0, -1, -1, -1, 0, 0, 0, 0, 0, 0],  # 5
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 6
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 7
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 8
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 9
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 10
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 11
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 12
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 13
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 14
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 15
             ]
    print(ai.get_chess_score(board1, 1))
