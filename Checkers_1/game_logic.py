import functools
import gl_var


# from global_variables import turn, board, move_continuation, figure, taken


def check_piece():
    # print("check", gl_var.turn, gl_var.figure, gl_var.board[gl_var.figure[0]][gl_var.figure[1]])
    if (gl_var.figure[0] not in range(0, 8)) or (gl_var.figure[1] not in range(0, 8)):
        print("out of bounds")
        return False
    if gl_var.turn == 1 and (
            gl_var.board[gl_var.figure[0]][gl_var.figure[1]] == "w_c" or
            gl_var.board[gl_var.figure[0]][
                gl_var.figure[1]] == "w_k"):
        return True
    if gl_var.turn == -1 and (
            gl_var.board[gl_var.figure[0]][gl_var.figure[1]] == "b_c" or
            gl_var.board[gl_var.figure[0]][
                gl_var.figure[1]] == "b_k"):
        return True
    print("not a " + ("white" if gl_var.turn == 1 else "black") + " piece")
    return False


def cannot_eat():
    # check for simple checker
    if (gl_var.board[gl_var.figure[0]][gl_var.figure[1]])[2] == "c":
        if gl_var.figure[1] > 1 and \
                (gl_var.board[gl_var.figure[0] + gl_var.turn][gl_var.figure[1] - 1])[0] == (
                "w" if gl_var.turn == -1 else "b"):
            if gl_var.board[gl_var.figure[0] + gl_var.turn][gl_var.figure[1] - 2] == "111":
                return False
            return True
        if gl_var.figure[1] < 6 and \
                (gl_var.board[gl_var.figure[0] + gl_var.turn][gl_var.figure[1] + 1])[0] == (
                "w" if gl_var.turn == -1 else "b"):
            if gl_var.board[gl_var.figure[0] + gl_var.turn][gl_var.figure[1] + 2] == "111":
                return False
            return True
        return False

    # king check

    for sign in [(1, -1), (1, 1), (-1, -1), (-1, 1)]:
        i = 1
        while gl_var.figure[0] + sign[0] * i in range(1, 7) and gl_var.figure[1] + sign[
            1] * i in range(1, 7) and gl_var.board[gl_var.figure[0] + sign[0] * i][
            gl_var.figure[1] + sign[1] * i] == "111":
            i += 1
        if gl_var.figure[0] + sign[0] * i in range(1, 7) and gl_var.figure[1] + sign[
            1] * i in range(1, 7):
            if gl_var.board[gl_var.figure[0] + sign[0] * (i + 1)][
                gl_var.figure[1] + sign[1] * (i + 1)] == "111" and \
                    (gl_var.board[gl_var.figure[0] + sign[0] * i][gl_var.figure[1] + sign[1] * i])[
                        0] == ("w" if gl_var.turn == -1 else "b"):
                return False
    return True


def single_move(x_new: int, y_new: int):  # return True if incorrect
    if (x_new not in range(0, 8)) or (y_new not in range(0, 8)):
        print("out of bounds")
        return True
    if not (gl_var.board[x_new][y_new] == "111" or gl_var.board[x_new][y_new] == "000"):
        print("position occupied")
        return True

    # simple checker:
    if gl_var.board[gl_var.figure[0]][gl_var.figure[1]] == "w_c" or gl_var.board[gl_var.figure[0]][
        gl_var.figure[1]] == "b_c":
        if ((y_new - gl_var.figure[1]) == 1 or (y_new - gl_var.figure[1]) == -1) and (
                x_new - gl_var.figure[0]) == gl_var.turn:
            gl_var.board[x_new][y_new] = gl_var.board[gl_var.figure[0]][gl_var.figure[1]]
            gl_var.board[gl_var.figure[0]][gl_var.figure[1]] = "111"
            gl_var.move_continuation = False
            crown()
            return False
        if ((y_new - gl_var.figure[1]) == 2 or (y_new - gl_var.figure[1]) == -2) \
                and (x_new - gl_var.figure[0]) == 2 * gl_var.turn and \
                (gl_var.board[(gl_var.figure[0] + x_new) // 2][(gl_var.figure[1] + y_new) // 2] ==
                 ("w_c" if gl_var.turn == -1 else "b_c")
                 or gl_var.board[(gl_var.figure[0] + x_new) // 2][
                     (gl_var.figure[1] + y_new) // 2] == (
                         "w_k" if gl_var.turn == -1 else "b_k")):
            gl_var.board[x_new][y_new] = gl_var.board[gl_var.figure[0]][gl_var.figure[1]]
            gl_var.board[gl_var.figure[0]][gl_var.figure[1]] = "111"
            gl_var.taken.append(((gl_var.figure[0] + x_new) // 2, (gl_var.figure[1] + y_new) // 2))
            move_continuation = True
            crown()
            return False
        print("wrong checker move, try again")
        return True
    # king:
    sign = (
        (1 if x_new - gl_var.figure[0] > 0 else -1), (1 if y_new - gl_var.figure[1] > 0 else -1))
    if (x_new - gl_var.figure[0] == y_new - gl_var.figure[1]) or (
            x_new - gl_var.figure[0] == -y_new + gl_var.figure[1]):  # check diagonal
        if all((gl_var.board[gl_var.figure[0] + sign[0] * i][
                    gl_var.figure[1] + sign[1] * i] == "111") for i in
               range(1, abs(x_new - gl_var.figure[0]) - 1)):  # check absence of pieces on the way
            if gl_var.board[x_new - sign[0]][y_new - sign[1]] == "111":
                gl_var.board[x_new][y_new] = gl_var.board[gl_var.figure[0]][gl_var.figure[1]]
                gl_var.board[gl_var.figure[0]][gl_var.figure[1]] = "111"
                gl_var.move_continuation = False
                return False

            if (gl_var.turn == -1 and (gl_var.board[x_new - sign[0]][y_new - sign[1]] == "w_c" or
                                       gl_var.board[x_new - sign[0]][y_new - sign[1]] == "w_k")) \
                    or (gl_var.turn == 1 and (
                    gl_var.board[x_new - sign[0]][y_new - sign[1]] == "b_c" or
                    gl_var.board[x_new - sign[0]][y_new - sign[1]] == "b_k")):
                gl_var.board[x_new][y_new] = gl_var.board[gl_var.figure[0]][gl_var.figure[1]]
                gl_var.board[gl_var.figure[0]][gl_var.figure[1]] = "111"

                gl_var.taken.append((x_new - sign[0], y_new - sign[1]))
                gl_var.move_continuation = True
                return False

        print("pieces on the diagonal, try again")
        return True
    print("wrong king move, try again")
    return True


def crown():
    if (gl_var.figure[0] == 7 and gl_var.board[gl_var.figure[0]][gl_var.figure[1]] == "w_c") or \
            (gl_var.figure[0] == 0 and gl_var.board[gl_var.figure[0]][gl_var.figure[1]] == "b_c"):
        gl_var.board[gl_var.figure[0]][gl_var.figure[1]] = (gl_var.board[gl_var.figure[0]][
            gl_var.figure[1]])[0:2] + "k"
        return


def remove_pieces():
    for (x, y) in gl_var.taken:
        gl_var.board[x][y] = "111"
    gl_var.taken = []


def can_move():
    for x in range(0, 8):
        for y in range(0, 8):
            if (gl_var.board[x][y])[0] == ("w" if gl_var.turn == 1 else "b"):
                gl_var.figure[0] = x
                gl_var.figure[0] = y
                if not cannot_eat():
                    return True
                # non-eating moves
                # usual checker or king that moves one forward
                if gl_var.figure[1] > 0 and \
                        (gl_var.board[gl_var.figure[0] + gl_var.turn][gl_var.figure[1] - 1])[
                            0] == "111":
                    return True
                if gl_var.figure[1] < 7 and \
                        (gl_var.board[gl_var.figure[0] + gl_var.turn][gl_var.figure[1] + 1])[
                            0] == "111":
                    return True
                # king
                if (gl_var.board[x][y])[2] == "k":
                    if gl_var.figure[1] > 0 and (gl_var.figure[0] - gl_var.turn) in range(0, 8) and \
                            (gl_var.board[gl_var.figure[0] - gl_var.turn][gl_var.figure[1] - 1])[
                                0] == "111":
                        return True
                    if gl_var.figure[1] < 7 and (gl_var.figure[0] - gl_var.turn) in range(0, 8) and \
                            (gl_var.board[gl_var.figure[0] - gl_var.turn][gl_var.figure[1] + 1])[
                                0] == "111":
                        return True
    return False


def check_victory():
    white_pieces = 0
    black_pieces = 0
    for i in range(0, 8):
        for j in range(0, 8):
            if (gl_var.board[i][j])[0] == "w":
                white_pieces += 1
            if (gl_var.board[i][j])[0] == "b":
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
