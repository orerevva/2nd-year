import random
import json
import os
from game import TicTacToe

class QLearningAgent:
    def __init__(self, alpha=0.1, gamma=0.9, epsilon=0.1):
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.q_table = {}
        self.letter = 'O'
        
    def get_state_key(self, board):
        return tuple(board)
    
    def choose_action(self, board, available_moves):
        state = self.get_state_key(board)
        
        if state not in self.q_table:
            self.q_table[state] = {move: 0.0 for move in available_moves}
        
        if random.random() < self.epsilon:
            return random.choice(available_moves)
        
        q_values = self.q_table[state]

        for move in available_moves:
            if move not in q_values:
                q_values[move] = 0.0

        max_q = max(q_values.values())
        best_moves = [move for move, q in q_values.items() if q == max_q]
        return random.choice(best_moves)
    
    def update(self, old_board, action, reward, new_board, done):
        old_state = self.get_state_key(old_board)
        new_state = self.get_state_key(new_board)
        
        if old_state not in self.q_table:
            self.q_table[old_state] = {}
        if new_state not in self.q_table:
            self.q_table[new_state] = {}
        
        current_q = self.q_table[old_state].get(action, 0.0)
        
        if done:
            future_q = 0.0
        else:
            future_q = max(self.q_table[new_state].values()) if self.q_table[new_state] else 0.0
            
        new_q = current_q + self.alpha * (reward + self.gamma * future_q - current_q)
        self.q_table[old_state][action] = new_q
        
    def train(self, episodes=100000, verbose=True):
        for episode in range(episodes):
            game = TicTacToe()
            current_player = 'X'
            done = False
            
            while not done:
                available = game.available_moves()
                old_board = game.board.copy()  
                
                if current_player == 'O':
                    action = self.choose_action(game.board, available)
                else:
                    action = random.choice(available)
                    
                game.make_move(action, current_player)
                
                reward = 0
                if game.current_winner == 'O':
                    reward = 50
                    done = True
                elif game.current_winner == 'X':
                    reward = -50
                    done = True
                elif game.num_empty_squares() == 0:
                    reward = 45
                    done = True
                
                self.update(old_board, action, reward, game.board, done)
                    
                current_player = 'X' if current_player == 'O' else 'O'
                
            if verbose and (episode % 1000 == 0 or episode == 0 or episode == episodes - 1):
                print(f"Эпизод {episode}/{episodes} завершен")
            
        print("Обучение завершено")
        
    def save_q_table(self, filename='q_table.json'):
        serializable = {}
        for state, actions in self.q_table.items():
            state_str = ''.join(state)
            serializable[state_str] = actions
        with open(filename, 'w') as f:
            json.dump(serializable, f, indent=4)
        print(f"Q-таблица сохранена в {filename}")
        
    def load_q_table(self, filename="q_table.json"):
        if not os.path.exists(filename):
            print("Файл с Q-таблицей не найден. Будет запущено обучение.")
            return False
        with open(filename, 'r') as f:
            data = json.load(f)
        self.q_table = {}
        for state_str, actions in data.items():
            state = tuple(state_str)
            self.q_table[state] = {int(k): v for k, v in actions.items()}
        print(f"Q-таблица загружена из {filename}")
        return True
    
    def get_best_move(self, board):
        state = self.get_state_key(board)
        available = self.get_available_moves(board)
        
        if state not in self.q_table:
            self.q_table[state] = {move: 0.0 for move in available}
            return random.choice(available)
        
        q_values = self.q_table[state]
        for move in available:
            if move not in q_values:
                q_values[move] = 0.0
                
        max_q = max(q_values.values())
        best_moves = [move for move, q in q_values.items() if q == max_q and move in available]
        return random.choice(best_moves) if best_moves else random.choice(available)
    
    def get_available_moves(self, board):
        return [i for i, spot in enumerate(board) if spot == ' ']


if __name__ == "__main__":
    print("обучение")
    agent = QLearningAgent(alpha=0.1, gamma=0.9, epsilon=0.1)
    agent.train(episodes=1000000, verbose=True)
    
    agent.save_q_table("q_table.json")
    
    print("\nЗагрузка обученного агента")
    new_agent = QLearningAgent()
    new_agent.load_q_table("q_table.json")
    
    print(f"Размер Q-таблицы: {len(new_agent.q_table)} состояний")
    
  