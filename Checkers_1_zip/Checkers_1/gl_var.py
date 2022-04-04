# file with global variables
board = [[("111" if (i+j) % 2 == 0 else "000") for i in range(0, 8)] for j in range(0, 8)]
turn = 1 # -1 for black
move_continuation = True
figure = [0, 1] # the figure being moved
taken = []
