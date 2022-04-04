import game_logic
import gl_var


# 111 000 -- unoccupied positions on the board
# w_c w_k -- white checkers and kings
# b_c b_k -- black checkers and kings

def rules():
    print("Welcome to CHECKERS! Here is how you play:")
    print("111 000 -- unoccupied positions on the board \n",
          "w_c w_k -- white checkers and kings \n", "b_c b_k -- black checkers and kings")
    print("Input the choosen piece's row and column: 3 5")
    print("The rows and columns are numbered from zero.")
    print("Once a player selects a piece, they have to move it.")
    print("You will continue inputting coordinates until you select your piece.")
    print("When moving the piece, you must input the destination position just after the taken piece.")
    print("A taken piece is immediately removed from the board.")
    print("You will continue inputting coordinates until your move is correct.")
    print("The game stops when one player has no pieces left.")


def simple_display():
    for i in range(0, 8):
        # for j in range(0, 8):
        print(gl_var.board[i])
    print("\n")


simple_display()


def set_board():
    for i in range(0, 2):
        for j in range(0, 8):
            gl_var.board[i][j] = ("w_c" if (i + j) % 2 == 0 else "000")

    for i in range(2, 6):
        for j in range(0, 8):
            gl_var.board[i][j] = ("111" if (i + j) % 2 == 0 else "000")

    for i in range(6, 8):
        for j in range(0, 8):
            gl_var.board[i][j] = ("b_c" if (i + j) % 2 == 0 else "000")



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

        gl_var.figure[0] = x_new
        gl_var.figure[1] = y_new

        simple_display()

        if game_logic.cannot_eat():
            gl_var.move_continuation = False

    gl_var.turn *= (-1)
    gl_var.move_continuation = True
    if game_logic.check_victory():
        break

