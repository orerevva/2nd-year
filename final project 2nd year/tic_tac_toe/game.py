class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)]
        self.current_winner = None
        
    def print_board(self):
        for row in [self.board[i*3:(i+1)*3] for i in range(3)]:
            print('|' + '|'.join(row) + '|')
            
    def available_moves(self):
        return [i for i, spot in enumerate(self.board) if spot == ' ']
    
    def make_move(self, square, letter):
        if self.board[square] == ' ':
            self.board[square] = letter
            
            if self.winner(square, letter):
                self.current_winner = letter
            return True
        return False
    
    def winner(self, square, letter):
        row_ind = square // 3
        row = self.board[row_ind*3:(row_ind+1)*3]
        if all([sport == letter for sport in row]):
            return True
        
        col_ind = square % 3
        column = [self.board[col_ind + i*3] for i in range(3)]
        if all([spot == letter for spot in column]):
            return True
          
        if square % 2 == 0:
            diag1 = [self.board[i] for i in [0, 4, 8]]
            if all([spot == letter for spot in diag1]):
                return True
            diag2 = [self.board[i] for i in [2, 4, 6]]
            if all([spot == letter for spot in diag2]):
                return True
        return False
    
    def empty_squares(self):
        return ' ' in self.board
    
    def num_empty_squares(self):
        return self.board.count(' ')
    
    def reset(self):
        self.board = [' ' for _ in range(9)]
        self.current_winner = None          
    
            

if __name__ == "__main__":
    game = TicTacToe()
    moves = [4, 0, 6, 1, 2]
    for i, move in enumerate(moves):
        letter = 'X' if i % 2 == 0 else 'O'
        game.make_move(move, letter)
        game.print_board()
        print("Победитель:", game.current_winner)
    
    
    
    