def movement(move, x_empty, y_empty):
    match move:
        case 'w':
            if x_empty - 1 >= 0:
                game_board[x_empty - 1][y_empty], game_board[x_empty][y_empty] = game_board[x_empty][y_empty], game_board[x_empty - 1][y_empty]
                game_logic(game_board)
            else:
                text("Стена!")
                game_logic(game_board)
        case 'a':
            if y_empty - 1 >= 0:
                game_board[x_empty][y_empty - 1], game_board[x_empty][y_empty] = game_board[x_empty][y_empty], game_board[x_empty][y_empty - 1]
                game_logic(game_board)
            else:
                text("Стена!")
                game_logic(game_board)
        case 's':
            if x_empty + 1 <= 3:
                game_board[x_empty + 1][y_empty], game_board[x_empty][y_empty] = game_board[x_empty][y_empty], game_board[x_empty + 1][y_empty]
                game_logic(game_board)
            else:
                text("Стена!")
                game_logic(game_board)
        case 'd':
            if y_empty + 1 <= 3:
                game_board[x_empty][y_empty + 1], game_board[x_empty][y_empty] = game_board[x_empty][y_empty], game_board[x_empty][y_empty + 1]
                game_logic(game_board)
            else:
                text("Стена!")
                game_logic(game_board)
