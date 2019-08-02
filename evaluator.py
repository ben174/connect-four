from collections import Counter

class ConnectFourEvaluator:
    def __init__(self, board):
        self.winners = set()
        self.win_type = None
        self.board = board
        self.error = None
        self.response = {
            'error': None,
            'winner': None,
            'win_type': None,
            'player_turn': None,
        }

    def validate(self):
        if not all(isinstance(row, list) for row in self.board):
            return False
        if len(self.board) != 6:
            return False
        if not all(len(row) == 7 for row in self.board):
            return False
        return True

    def evaluate(self):
        # validate board shape/type
        if not self.validate():
            self.response['error'] = 'Invalid board body'
            return self.response

        # vertical and diagonal
        for row_index in range(3):
            row = self.board[row_index]
            for col_index in range(7):
                piece = row[col_index]
                if piece == 0:
                    continue
                # down
                try:
                    line = [
                        piece,
                        self.board[row_index+1][col_index],
                        self.board[row_index+2][col_index],
                        self.board[row_index+3][col_index],
                    ]
                    pieces = set(line)
                    if len(pieces) == 1:
                        self.win_type = 'down'
                        self.winners.add(pieces.pop())
                except IndexError:
                    pass

                # diagonal right
                try:
                    line = [
                        piece,
                        self.board[row_index+1][col_index+1],
                        self.board[row_index+2][col_index+2],
                        self.board[row_index+3][col_index+3],
                    ]
                    if len(pieces) == 1:
                        self.win_type = 'diagonal right'
                        self.winners.add(pieces.pop())
                except IndexError:
                    pass

                # down left
                try:
                    line = [
                        piece,
                        self.board[row_index+1][col_index-1],
                        self.board[row_index+2][col_index-2],
                        self.board[row_index+3][col_index-3],
                    ]
                    if len(pieces) == 1:
                        self.win_type = 'diagonal left'
                        self.winners.add(pieces.pop())
                except IndexError:
                    pass

        piece_list = []

        # horizontal
        for row in self.board:
            piece_list.extend(row)
            for col_index in range(4):
                if row[col_index] == 0:
                    continue
                line = row[col_index:col_index+4]
                piece_set = set(line)
                if len(piece_set) == 1:
                    self.win_type = 'horizontal'
                    self.winners.add(piece_set.pop())
                else:
                    continue

        # evaluate player turns
        piece_counter = Counter(piece_list)
        if piece_counter[1] == piece_counter[2]:
            self.response['player_turn'] = 1
        elif piece_counter[1] - 1 == piece_counter[2]:
            self.response['player_turn'] = 2
        else:
            self.response['error'] = 'Invalid Board State (move count mismatch)'
            return self.response

        # determine winner
        if len(self.winners) == 1:
            self.response['winner'] = self.winners.pop()
            self.response['win_type'] = self.win_type
            self.response['player_turn'] = None
        else:
            self.response['error'] = 'Invalid Board State (multiple winners)'
            self.response['player_turn'] = None
