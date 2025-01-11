from random import Random

# globals
CountsOptions = 0
count_cell_occupied = 0
RUN_GAME = True
OPTIONS = ["1 PLAYER" ,"TWO PLAYERS", "EXIT"]
board = [["", "", ""], ["", "", ""], ["", "", ""]]
StateBoard = {"WINNER": False,"DRAW": False}
winner = ""

def UpdateBoard(row, col, player):
    global board   
    board[row][col] = player

def InvalidInputs(row, col) -> bool:
    if row > 3  or  row <= 0 or col > 3 or col <= 0 :  return True
    return False

def ResetGame() :
    global board, count_cell_occupied, StateBoard,  CountsOptions
    count_cell_occupied = 0
    StateBoard["DRAW"], StateBoard["WINNER"] = False, False
    for row in range(len(board)): board[row] = ["", "", ""]
    CountsOptions = 0
    
def Is_cell_occupied (RowCurrent, ColumnCurrent,  board) -> bool:
    return True if board[RowCurrent][ColumnCurrent] != "" else False
       
def FindWinner(board, player):
    global  StateBoard, winner    
     # check if there is winner
    for row in range(len(board)):
            if board[row][0] ==  board[row][1] ==  board[row][2]  == player:
               winner = player
               StateBoard["WINNER"] = True
               return
    for column in range(3):        
           if board[0][column] ==  board[1][column] == board[2][column] == player:
               StateBoard["WINNER"] = True
               winner = player
               return

    if board[0][0] == board[1][1] == board[2][2] == player:
        StateBoard["WINNER"] = True
        winner = player
        return
    if board[0][-1]  == board[1][1] == board[2][0] == player:
        StateBoard["WINNER"] = True
        winner = player
        return
 
def DrawBoard() -> None:
    global board
    print(" ", board[0][0], "|" , board[0][1], "|", board[0][2])
    print("---------------")
    print(" ", board[1][0], "|" , board[1][1], "|", board[1][2])
    print("---------------")
    print(" ", board[2][0], "|" , board[2][1], "|", board[2][2])
        
def play_for_two_players():
    global board, StateBoard, count_cell_occupied

    active = True

    player = input("player 1: select X OR O:").upper()
    player2 = ""
       
    while not player or  (not player == "X" and  not player =="O") : player = input("player 1: please select a character select X OR O").upper()
    
    if player == "X": player2 = "O"
    else: player2 = "X"
    
    print("player 2 is:", player2 )
    while active:
        for p in [player, player2]:       
            try: 
                user_row_input = int(input(f"Player character {p}:  select a one row (numbers):  1, 2, 3:"))
                user_col_input = int(input(f" Player charater{p}: select a one column (numbers): 1, 2, 3:"))
            
                if InvalidInputs(user_row_input, user_col_input ): 
                   print(f"error, invalid user_row_input or column. player: {p} lost his oportunity ")
                   continue   
                                    
                while  Is_cell_occupied(user_row_input - 1, user_col_input - 1 ,  board):
                       print("This cell is occupied. Try again")  
                       user_row_input = int(input(f"Player character {p}:  select a one row:  1, 2, 3:"))
                       user_col_input = int(input(f" Player charater{p}: select a one column: 1, 2, 3:"))
            
                UpdateBoard(user_row_input - 1, user_col_input - 1, p)
                count_cell_occupied += 1
                FindWinner(board, p)

                if StateBoard["WINNER"]:
                    DrawBoard()                   
                    print(f"winner: player 1 {player}" if winner ==  player else f"winner: player 2 {player2}")
                    active = False
                    break

                if count_cell_occupied == 9: StateBoard["DRAW"] = True

                if StateBoard["DRAW"]:
                    DrawBoard()                   
                    print("There is a draw")
                    active = False
                    break
            except ValueError:
                print(f"the player {p} entered a difference input (numbers). lost his oportunity  ")
                continue                                  
        DrawBoard()                   
    ResetGame()

def play_for_me_and_computer():
    global board, count_cell_occupied, StateBoard    
    characters = ["X", "O"] 
    cpu = int(Random().randrange(1,  len(characters) + 1 ))
    CPU_CHAR,  ME_CHAR, = "", ""
    TurnComputer, TurnMe = False, True
       
    CPU_CHAR = characters[cpu - 1]
    print("CPU is selecting a character")
    print("cpu chose:", CPU_CHAR)
  
    me = int(input("select a character with number  1 or 2: \n 1. X: \n 2. O:"))
   
    while me > len(characters) or  me == cpu or me <= 0: me = int(input("select a character: \n 1. X \n 2. O")) 
        
    ME_CHAR = characters[me - 1]                          
    print("my character is:", ME_CHAR )
    #start tic tac toe 
    while True:              
        if TurnMe:
            try:
                user_row_input = int(input(f"Player character {ME_CHAR}:  select a one row:  1, 2, 3:"))
                user_col_input = int(input(f" Player charater{ME_CHAR}: select a one column: 1, 2, 3:"))
            
                if InvalidInputs(user_row_input, user_col_input ): 
                   print(f"error, invalid user_row_input or column. Player: {ME_CHAR} lost his oportunity ")
                   TurnComputer, TurnMe = True, False
                   continue            
                else:
                    if Is_cell_occupied(user_row_input - 1, user_col_input - 1 ,  board):  
                        print("CELL OCUPPIED. Try again")
                        continue
                
                UpdateBoard(user_row_input - 1, user_col_input - 1, ME_CHAR)
                count_cell_occupied += 1
                TurnComputer, TurnMe = True, False
                FindWinner(board, ME_CHAR)  

                if StateBoard["WINNER"]:
                   print(f"winnner: {winner}. Game over")
                   DrawBoard()
                   break  

                if count_cell_occupied == 9: StateBoard["DRAW"] = True
                if  StateBoard["DRAW"]:
                    print("it is tie. Game over")
                    DrawBoard()
                    break
            except:
                print(f"You lost your turn, you entered a difference input (numbers)")
                continue

        if TurnComputer:
            print("cpu is selecting a row and col")
            
            cpu_row_input = Random().randrange(1, 3 + 1)
            cpu_col_input = Random().randrange(1, 3 + 1)
    
            while  Is_cell_occupied(cpu_row_input - 1, cpu_col_input - 1 ,  board):  
                   print("CELL OCUPPIED. Try again computer ")
                   cpu_row_input = Random().randrange(1, 3 + 1)
                   cpu_col_input = Random().randrange(1, 3 + 1 )
                                           
            UpdateBoard(cpu_row_input - 1, cpu_col_input - 1, CPU_CHAR)
            count_cell_occupied += 1
            TurnComputer, TurnMe = False, True
            FindWinner(board, CPU_CHAR)
            
            if StateBoard["WINNER"]:
               print("\n", "winnner CPU:",winner)
               DrawBoard()
               break

            if count_cell_occupied == 9: StateBoard["DRAW"] = True
            if StateBoard["DRAW"]:
               print("it is tie. Game over") 
               DrawBoard()
               break
        print("\n")      
        DrawBoard()    
    ResetGame()            
         
def ShowMenu(run) -> None:
    global CountsOptions
    while run:
        sp = ""
        for option in OPTIONS:
            CountsOptions += 1
            sp +=  str(CountsOptions) + "." + " "   + option  + "\n"   
        print("----------------------------")
        print("| WELCOME A TIC TAC TOE |")
        print("----------------------------")
        print("______________________________________")    
        print("\n", sp)
        print("______________________________________")
        user = input("select one option: ")    
        match user:
            case "1": play_for_me_and_computer()
            case "2": play_for_two_players()
            case "3": run = False 
            case _ : 
                print("invalid option. Try again")
                run = False
                
    else: print("thanks for trying the tic tac toe :) ")
                        
def RunGame(run):
    ShowMenu(run)

RunGame(True)                                                 