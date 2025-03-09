import random

def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 9)

def check_winner(board, player):
    for row in board:
        if all(s == player for s in row):
            return True
    
    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True
    
    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True
    
    return False

def is_full(board):
    return all(cell != " " for row in board for cell in row)

def get_available_moves(board):
    return [(r, c) for r in range(3) for c in range(3) if board[r][c] == " "]

def main():
    board = [[" " for _ in range(3)] for _ in range(3)]
    players = ["X", "O"]
    turn = random.choice(players)
    
    while True:
        print_board(board)
        print(f"{turn}'s turn")
        
        row, col = map(int, input("Enter row and column (0-2): ").split())
        if board[row][col] != " ":
            print("Invalid move, try again.")
            continue
        
        board[row][col] = turn
        
        if check_winner(board, turn):
            print_board(board)
            print(f"{turn} wins!")
            break
        
        if is_full(board):
            print_board(board)
            print("It's a draw!")
            break
        
        turn = "X" if turn == "O" else "O"

if __name__ == "__main__":
    main()
