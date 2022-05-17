import game_logic
import gl_var


# 111 000 -- unoccupied positions on the board
# w_c w_k -- white checkers and kings
# b_c b_k -- black checkers and kings

def rules():
    for text in gl_var.rules:
        print(text)


def simple_display():
    for row in gl_var.board:
        print(row)
    print("\n")


def set_board():
    for i in range(0, 2):
        for j in range(0, 4):
            game_logic.change_board(i, i + 2*j, "w_c")
    for i in range(6, 8):
        for j in range(0, 4):
            game_logic.change_board(i, (i - 6) + 2*j, "b_c")


rules()
set_board()
simple_display()

while True:
    print(("white" if gl_var.turn == 1 else "black") + " turn:")
    while True:
        x, y = input("checker: ").split()
        x, y = int(x), int(y)
        gl_var.figure = [x, y]
        if game_logic.check_piece():
            break

    while gl_var.move_continuation:
        x_new, y_new = input("move to: ").split()
        x_new, y_new = int(x_new), int(y_new)
        # do the move if possible, request new coordinates otherwise
        while game_logic.single_move(x_new, y_new):
            x_new, y_new = input("move to: ").split()
            x_new, y_new = int(x_new), int(y_new)

        game_logic.remove_pieces()

        # gl_var.figure = [x_new, y_new]

        simple_display()

        if game_logic.cannot_eat():
            gl_var.move_continuation = False

    if game_logic.check_victory():
        break

    gl_var.move_continuation = True
    gl_var.turn *= (-1)
