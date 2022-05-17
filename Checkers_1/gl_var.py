# file with global variables
black = "111"
white = "000"
board = [[(black if (i + j) % 2 == 0 else white) for i in range(0, 8)] for j in range(0, 8)]
turn = 1  # -1 for black
move_continuation = True
figure = [0, 1]  # the figure being moved
taken = []
rules = ["Welcome to CHECKERS! Here is how you play:",
         "111 000 -- unoccupied positions on the board",
         "w_c w_k -- white checkers and kings", "b_c b_k -- black checkers and kings",
         "Input the choosen piece's row and column: 3 5",
         "The rows and columns are numbered from zero.",
         "Once a player selects a piece, they have to move it.",
         "You will continue inputting coordinates until you select your piece.",
         "When moving the piece, you must input the destination position just after the taken piece.",
         "A taken piece is immediately removed from the board.",
         "You will continue inputting coordinates until your move is correct.",
         "The game stops when one player has no pieces left."]
