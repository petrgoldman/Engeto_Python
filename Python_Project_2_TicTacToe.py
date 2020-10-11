import numpy as np  # to be able to work with diagonals easily
import random

delimiter = '=' * 80


def game_params():  # get game parameters from user, field size and difficulty
    # print(delimiter)
    size = input('Select the size of the field (3 - 9): ')
    while not(size.isdigit() and int(size) in range(3, 10)):
        size = input('Try again please: ')

    if int(size) > 3:
        difficulty = input(f'Select difficulty level (3 - {size}): ')
    else:
        print('Difficulty set to a default value 3.')
        return int(size), 3

    # difficulty corresponds with the number of consecutive marks
    # needed for victory
    while True:
        if not difficulty.isdigit():
            difficulty = input('Try again please: ')
        elif int(difficulty) < 3 or int(difficulty) > int(size):
            difficulty = input('Try again please: ')
        else:
            break
    return int(size), int(difficulty)


def create_board(size):
    board = np.array([[' '] * size] * size)
    return board


def print_board(board, size):  # this just prints the current board
    first_row = '  ' + '|{:^3}' * size + '|'
    temp_row = '{:<2}' + '|{:^3}' * size + '|'
    print(first_row.format(*range(1, size + 1)))
    for i in range(size):
        print('--' + '-' * 4 * size + '-')
        print(temp_row.format(i + 1, *board[i, :]))
    print('--' + '-' * 4 * size + '-')


def users_choice(board, turn, size):  # enter two digit number XY, X = row, Y = column
    print('\n' + delimiter)
    choice = input(f'Player {turn} | '
                   f'Please enter the position: ')
    while True:
        if not choice.isdigit():
            choice = input('Try again please: ')
        elif int(choice[0]) not in range(1, size + 1) or int(choice[1]) not in range(1, size + 1):
            choice = input('Try again please: ')
        elif board[int(choice[0]) - 1, int(choice[1]) - 1] != ' ':
            choice = input('Already taken, please select another one: ')
        else:
            print(delimiter + '\n')
            return int(choice[0]) - 1, int(choice[1]) - 1


def update_board(board, turn, choice):
    board[choice] = turn
    return board


def is_board_full(board):  # check if the board is full
    for row in board:
        if ' ' in ''.join(row):
            return False
    return True


def win(board, turn, difficulty, size):  # checks rows, columns and diagonals
    for row in board:
        if turn * difficulty in ''.join(row):
            return True
    for i in range(size):
        if turn * difficulty in ''.join(board[:, i]):
            return True
    for offset in range(- size + 1, size):
        if turn * difficulty in ''.join(board.diagonal(offset)):
            return True
    for offset in range(- size + 1, size):
        if turn * difficulty in ''.join(np.flipud(board).diagonal(offset)):
            return True
    return False


def main():
    intro = '''
Welcome to Tic Tac Toe
GAME RULES:
Each player can place one mark (or stone) per turn on the grid
The WINNER is who succeeds in placing selected number of their marks in a
* horizontal,
* vertical or
* diagonal row
You will be able to select field size and difficulty level.

During the game players will choose the position of the mark by entering
a two digit value, where the first digit corresponds with the row number and
the second second digit corresponds with the column number. 
    '''

    print(delimiter)
    print(intro)
    print(delimiter)
    turn = random.choice(['O', 'X'])  # whos turn it is to play, player 1 = 'O', player 2 = 'X'
    repeat = ''
    size, difficulty = game_params()

    while repeat.lower() != 'q':
        board = create_board(size)
        print(delimiter + '\n')
        print_board(board, size)
        win_flag = False
        while True:
            choice = users_choice(board, turn, size)
            update_board(board, turn, choice)
            print_board(board, size)
            if win(board, turn, difficulty, size):
                win_flag = True
                print(f'\nCONGRATS, PLAYER {turn} WINS!!!!\n')
                break
            elif is_board_full(board):
                break
            else:
                if turn == 'X':
                    turn = 'O'
                else:
                    turn = 'X'

        if not win_flag:
            print("It's a tie.\n")
        print(delimiter)
        repeat = input('Wanna play again? Press enter to continue,'
                       ' ''q'' to quit this game: ')


if __name__ == "__main__":
    main()
