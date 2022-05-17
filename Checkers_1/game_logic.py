import functools
import gl_var


# returns the value on board with coordinates gl_var.figure[0] + horiz and gl_var.figure[1] + vert
def figure_value(horiz: int, vert: int) -> str:
    if not gl_var.figure[0] + horiz in range(0, 8) or not gl_var.figure[1] + vert in range(0, 8):
        print("out of bounds figure")
        return
    return gl_var.board[gl_var.figure[0] + horiz][gl_var.figure[1] + vert]


def board_value(x: int, y: int) -> str:
    if x in range(0, 8) and y in range(0, 8):
        return gl_var.board[x][y]
    print("out of bounds board")


def change_figure(horiz: int, vert: int, value: str):
    if gl_var.figure[0] + horiz in range(0, 8) and gl_var.figure[1] + vert in range(0, 8):
        gl_var.board[gl_var.figure[0] + horiz][gl_var.figure[1] + vert] = value
        return
    print("out of bounds figure")
    return


def change_board(x: int, y: int, value: str):
    if x in range(0, 8) and y in range(0, 8):
        gl_var.board[x][y] = value
        return
    print("out of bounds board")


def reset_figure(x: int, y: int):
    if x in range(0, 8) and y in range(0, 8):
        gl_var.figure = [x, y]


def check_piece():
    if (gl_var.figure[0] not in range(0, 8)) or (gl_var.figure[1] not in range(0, 8)):
        print("out of bounds")
        return False
    if gl_var.turn == 1 and (
            figure_value(0, 0) == "w_c" or
            figure_value(0, 0) == "w_k"):
        return True
    if gl_var.turn == -1 and (
            figure_value(0, 0) == "b_c" or
            figure_value(0, 0) == "b_k"):
        return True
    print("not a " + ("white" if gl_var.turn == 1 else "black") + " piece")
    return False


def cannot_eat():
    # check for simple checker
    if figure_value(0, 0) in ["w_c", "b_c"]:
        if not gl_var.figure[0] + 2 * gl_var.turn in range(0, 8):
            return True
        if gl_var.figure[1] > 1:
            if figure_value(gl_var.turn, -1)[0] == ("w" if gl_var.turn == -1 else "b") and \
                    figure_value(2 * gl_var.turn, -2) == gl_var.black:
                return False
        if gl_var.figure[1] < 6:
            if figure_value(gl_var.turn, 1)[0] == ("w" if gl_var.turn == -1 else "b") and \
                    figure_value(2 * gl_var.turn, 2) == gl_var.black:
                return False
            return True
        return False

    # king check
    for sign in [(1, -1), (1, 1), (-1, -1), (-1, 1)]:  # 4 directions in which the king can move
        i = 1
        while gl_var.figure[0] + sign[0] * i in range(1, 7) and gl_var.figure[1] + sign[
            1] * i in range(1, 7) and figure_value(sign[0] * i, sign[1] * i) == gl_var.black:
            i += 1
        if gl_var.figure[0] + sign[0] * i in range(1, 7) and \
                gl_var.figure[1] + sign[1] * i in range(1, 7):
            if figure_value(sign[0] * (i + 1), sign[1] * (i + 1)) == gl_var.black and \
                    (figure_value(sign[0] * i, sign[1] * i))[0] == \
                    ("w" if gl_var.turn == -1 else "b"):
                return False
    return True


def single_move(x_new: int, y_new: int):  # return True if incorrect
    if (x_new not in range(0, 8)) or (y_new not in range(0, 8)):
        print("out of bounds")
        return True
    if board_value(x_new, y_new) not in [gl_var.black, gl_var.white]:
        print("position occupied")
        return True
    # simple checker:
    if figure_value(0, 0) in ["w_c", "b_c"]:
        # non-eating move
        if (y_new - gl_var.figure[1]) in [1, -1] and \
                (x_new - gl_var.figure[0]) == gl_var.turn:
            change_board(x_new, y_new, figure_value(0, 0))
            change_figure(0, 0, gl_var.black)
            gl_var.move_continuation = False
            reset_figure(x_new, y_new)
            crown()
            return False
        # eating move
        if (y_new - gl_var.figure[1]) in [2, -2] \
                and (x_new - gl_var.figure[0]) == 2 * gl_var.turn and \
                board_value(x_new, y_new) == gl_var.black and \
                board_value((gl_var.figure[0] + x_new) // 2,
                            (gl_var.figure[1] + y_new) // 2)[0] == \
                ("w" if gl_var.turn == -1 else "b"):
            change_board(x_new, y_new, figure_value(0, 0))
            change_figure(0, 0, gl_var.black)
            gl_var.taken.append(((gl_var.figure[0] + x_new) // 2, (gl_var.figure[1] + y_new) // 2))
            reset_figure(x_new, y_new)
            crown()
            move_continuation = True
            return False
        print("wrong checker move, try again")
        return True
    # king:
    # marking one of the 4 directions where the king will be moving
    sign = (
        (1 if x_new - gl_var.figure[0] > 0 else -1), (1 if y_new - gl_var.figure[1] > 0 else -1))
    if (x_new - gl_var.figure[0] == y_new - gl_var.figure[1]) or \
            (x_new - gl_var.figure[0] == -y_new + gl_var.figure[1]):  # check diagonal
        if all((figure_value(sign[0] * i, sign[1] * i) == gl_var.black) for i in
               range(1, abs(x_new - gl_var.figure[0]) - 1)):  # check absence of pieces on the way
            if board_value(x_new - sign[0], y_new - sign[1]) == gl_var.black:
                change_board(x_new, y_new, figure_value(0, 0))
                change_figure(0, 0, gl_var.black)
                reset_figure(x_new, y_new)
                gl_var.move_continuation = False
                return False

            if (gl_var.turn == -1 and (board_value(x_new - sign[0], y_new - sign[1]) == "w_c" or
                                       board_value(x_new - sign[0], y_new - sign[1]) == "w_k")) \
                    or (gl_var.turn == 1 and (
                    board_value(x_new - sign[0], y_new - sign[1]) == "b_c" or
                    board_value(x_new - sign[0], y_new - sign[1]) == "b_k")):
                change_board(x_new, y_new, figure_value(0, 0))
                change_figure(0, 0, gl_var.black)
                gl_var.taken.append((x_new - sign[0], y_new - sign[1]))
                reset_figure(x_new, y_new)
                gl_var.move_continuation = True
                return False
        print("pieces on the diagonal, try again")
        return True
    print("wrong king move, try again")
    return True


def crown():
    if (gl_var.figure[0] == 7 and figure_value(0, 0) == "w_c") or \
            (gl_var.figure[0] == 0 and figure_value(0, 0) == "b_c"):
        change_figure(0, 0, (figure_value(0, 0))[0:2] + "k")
        return


def remove_pieces():
    for (x, y) in gl_var.taken:
        change_board(x, y, gl_var.black)
    gl_var.taken = []


def can_move():
    for x in range(0, 8):
        for y in range(0, 8):
            if board_value(x, y)[0] == ("w" if gl_var.turn == 1 else "b"):
                gl_var.figure = [x, y]
                if not cannot_eat():
                    return True
                # non-eating moves
                # usual checker or king that moves one forward
                if gl_var.figure[1] > 0 and \
                        figure_value(gl_var.turn, -1) == gl_var.black:
                    return True
                if gl_var.figure[1] < 7 and \
                        figure_value(gl_var.turn, +1) == gl_var.black:
                    return True
                # king
                if board_value(x, y)[2] == "k":
                    if gl_var.figure[1] > 0 and (gl_var.figure[0] - gl_var.turn) in range(0, 8) and \
                            figure_value(-gl_var.turn, -1) == gl_var.black:
                        return True
                    if gl_var.figure[1] < 7 and (gl_var.figure[0] - gl_var.turn) in range(0, 8) and \
                            figure_value(-gl_var.turn, +1) == gl_var.black:
                        return True
    return False


def check_victory():
    white_pieces = 0
    black_pieces = 0
    for i in range(0, 8):
        for j in range(0, 8):
            if board_value(i, j)[0] == "w":
                white_pieces += 1
            if board_value(i, j)[0] == "b":
                black_pieces += 1
    if white_pieces == 0 and black_pieces > 0:
        print("BLACK WON!!!")
        return True
    if black_pieces == 0 and white_pieces > 0:
        print("WHITE WON!!!")
        return True
    if black_pieces == 0 and white_pieces == 0:
        print("empty board")
        return True

    if not can_move():
        if gl_var.turn == 1:
            print("BLACK WON!!!")
        else:
            print("WHITE WON!!!")
        return True

    return False
