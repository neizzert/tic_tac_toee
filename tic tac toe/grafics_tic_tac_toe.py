from flet import *
from random import Random

def main(page: Page):
    page.bgcolor = "#01579B"
    page.horizontal_alignment = CrossAxisAlignment.CENTER     
    CountCells = 0
    winner = ""
    StateBoard = {"WINNER": False, "DRAW": False}
    CurrentPlayer = Text(value="",color="white", size=16)  
    turn = Text(value="1")
    PLAYER_1 = ""
    CPU_CHARACTER = ""
    
    def ViewShowMenu(content) -> Container:
        return  Container(
                    border_radius=5, 
                    width=300,
                    height=350, 
                    content=content,
                     alignment=alignment.center
                )
    
    def view_two_players(content) -> Container:
        return  Container(
                    width=580, 
                    height=450,
                    padding=8, 
                    content=content,
                    visible=False,
                )     
    def view_you_versus_computer(content) -> Container:
        return Container (
            width=585,
            height=500,
            content=content,
            visible=False ,
            alignment=alignment.center,
        )
        
    def GenerateBoard(GameLogic) -> GridView:
        AssignNumber = 0 
        board = GridView(
               expand=1,
               runs_count=5,      
               max_extent=170,
               child_aspect_ratio= 1.0,
               spacing=2,
               run_spacing=2,
               width= 170 * 3,
            )            
        for _ in range(1, 9 + 1):
            AssignNumber += 1
            board.controls.append(
                 Container(
                        data = AssignNumber,
                        content=Text(value="", size=20), 
                        on_click= GameLogic, 
                        shadow=BoxShadow(
                        spread_radius=1,
                        blur_radius=8,
                        color=Colors.BLACK87,
                        offset=Offset(0, 0),
                        blur_style=ShadowBlurStyle.OUTER), 
                        alignment=alignment.center, 
                        bgcolor="#E0E0E0"
                    )
                )     
        return board
            
    def ResetGame():
        nonlocal CountCells, StateBoard
        CountCells = 0
        StateBoard["WINNER"] = False
        StateBoard["DRAW"] = False
        CurrentPlayer.value = ""
        SetTurn(int("1"))
        for control in grid.controls: 
            control.content.value = ""
            control.update()
            
    def winner_in_diagonals(grid, player):
        # detect in diagonals
        if grid.controls[0].content.value ==  grid.controls[4].content.value ==  grid.controls[8].content.value == player: return True        
        elif grid.controls[2].content.value ==  grid.controls[4].content.value ==  grid.controls[6].content.value == player: return True
        else: return False

    def winner_in_column(grid, player) -> bool:
        # detect in column
        if grid.controls[0].content.value == grid.controls[3].content.value == grid.controls[6].content.value == player: return True        
        elif grid.controls[1].content.value == grid.controls[4].content.value == grid.controls[7].content.value == player: return True    
        elif grid.controls[2].content.value == grid.controls[5].content.value == grid.controls[8].content.value == player: return True
        else: return False
        
    def winner_in_rows(grid, player) -> bool:
       # detect in rows
       if grid.controls[0].content.value ==  grid.controls[1].content.value == grid.controls[2].content.value == player: return True
       elif grid.controls[3].content.value ==  grid.controls[4].content.value == grid.controls[5].content.value == player: return True
       elif  grid.controls[6].content.value ==  grid.controls[7].content.value == grid.controls[8].content.value == player: return True
       else: return False
       
    def cancel_view(e):
        view_players.visible = False
        menu.visible = True
        ResetGame()
        page.update()
        
    def UpdateCell(cell, character, color): 
        cell.content.value = character
        cell.content.color = color
        cell.content.size = 18
        cell.update()
        
    def update_current_player(character):
        CurrentPlayer.value = character
        page.update()

    def there_is_space_free(cell) -> bool:
        return cell.content.value == ""
     
    def SetTurn(value):
        turn.value = value
        
    def context(e):
        nonlocal CountCells, winner
        
        if there_is_space_free(grid.controls[e.control.data - 1]):
            if int(turn.value) == 1:
               UpdateCell(grid.controls[e.control.data - 1], "X", "red")
               update_current_player("X")
               SetTurn(int("2"))
               CountCells += 1       
            else:
                UpdateCell(grid.controls[e.control.data - 1], "O", "blue")
                update_current_player("O")
                SetTurn(int("1"))
                CountCells += 1    
        else:
            snack = SnackBar(
                     bgcolor=Colors.AMBER_500,
                     content=Text( "This cell is occupied. Try again", color="black", size=17,  weight=FontWeight.BOLD),
                    )
            page.snack_bar = snack
            page.snack_bar.open = True
            page.update()
            return 
        
        if winner_in_rows(grid, grid.controls[e.control.data - 1].content.value) or winner_in_column(grid, grid.controls[e.control.data - 1].content.value) or winner_in_diagonals(grid, grid.controls[e.control.data - 1].content.value) : 
            StateBoard["WINNER"] = True
                     
        if StateBoard["WINNER"]:
            alert = AlertDialog(
                bgcolor=Colors.GREEN_500,
                content=Text(value=f" winnenr Player 1: {CurrentPlayer.value}" if CurrentPlayer.value == "X" else f" winner Player 2: {CurrentPlayer.value}" , text_align="center", size=18)
            )
            page.open(alert)
            ResetGame()
            page.update()
            return 
        if CountCells == 9: StateBoard["DRAW"] = True
        
        if StateBoard["DRAW"]:
            alert = AlertDialog(
                bgcolor="#212121",
                content= Text("it is DRAW!", color="WHITE", size=18, text_align="center")
            )
            page.open(alert) 
            ResetGame()
            page.update()
            return
    
    def ChangeContent():
        nonlocal grid2, you_and_computer, turn
        for control in you_and_computer.content.controls:
            control.visible = False
            page.update()     
        you_and_computer.content = Row(
            controls = [
                grid2,
                Row(
                    spacing=25,
                    controls=[
                        Column(
                            alignment=MainAxisAlignment.CENTER,
                            controls = [
                                Row(controls=[Text("Current player:", size=16, weight=FontWeight.BOLD),
                               CurrentPlayer]),
                               Row(controls = [
                                TextButton(text="rest", style=ButtonStyle(padding=5,color="black",bgcolor="#FFC400"), on_click=lambda e: Reset_game_option_2()),
                                TextButton(on_click=cancel_view_2, text="cancel", style=ButtonStyle(padding=5, color="white",bgcolor="#455A64"))]) 
                            ]
                        )
                    ]
                )
            ]
        )
        page.update()
    
    def cancel_view_2(e):
        nonlocal you_and_computer, menu, PLAYER_1, CPU_CHARACTER, grid2
        PLAYER_1 = ""
        CPU_CHARACTER = ""
            
        for control in grid2.controls:
            control.content.value = ""
            
        you_and_computer.content = Row(
                    alignment=MainAxisAlignment.CENTER,
                     controls=[
                         Text("Select a character:", color="white", size=18, weight=FontWeight.BOLD),
                        TextButton(content=Text("X", size=18, color=Colors.RED_500), on_click=get_value_player_1_x, style=ButtonStyle(bgcolor=Colors.LIGHT_BLUE_200)),
                        TextButton(content=Text("O", size=18, color=Colors.BLUE_500), on_click=get_value_player_1_o, style=ButtonStyle(bgcolor=Colors.LIGHT_BLUE_200))
                ]
            )
        you_and_computer.visible = False
        menu.visible = True
        page.update()
    
    def get_value_player_1_x(e):
        nonlocal PLAYER_1, CPU_CHARACTER
        PLAYER_1 = e.control.content.value
        CPU_CHARACTER = "O"
        ChangeContent()
              
    def get_value_player_1_o(e):
        nonlocal PLAYER_1, CPU_CHARACTER
        PLAYER_1 = e.control.content.value
        CPU_CHARACTER = "X"
        ChangeContent()
              
    def ContextTwo(e):
        nonlocal StateBoard, CountCells, PLAYER_1, CPU_CHARACTER, grid2, turn, winner
                
        if there_is_space_free(grid2.controls[e.control.data - 1]):
            if int(turn.value) == 1:
              ChangeColor =  "red" if PLAYER_1 == "X" else "blue"
              
              UpdateCell(grid2.controls[e.control.data - 1], PLAYER_1,  ChangeColor)
              update_current_player(PLAYER_1)
              CountCells += 1
              SetTurn(int(2))
              
              if winner_in_rows(grid2, PLAYER_1) or winner_in_column(grid2, PLAYER_1) or winner_in_diagonals(grid2, PLAYER_1): StateBoard["WINNER"] = True
              if StateBoard["WINNER"]:
                 winner = PLAYER_1
                 alert = AlertDialog(
                       bgcolor=Colors.GREEN_500,
                       content=Text(f"winner player 1: {winner}", text_align="center", size=18)
                    )
                 page.open(alert)
                 page.update()
                 Reset_game_option_2()
                 return
              if CountCells == 9: StateBoard["DRAW"] = True
             
              if StateBoard["DRAW"]:
                alert = AlertDialog(
                bgcolor="#212121",
                content= Text("it is DRAW!", color="WHITE", size=18, text_align="center")
            )
                page.open(alert)
                page.update()
                Reset_game_option_2()
                return
            
            if turn.value == 2:
                ChangeColor =  "red" if CPU_CHARACTER == "X" else "blue" 
                position_of_cpu = Random().randrange(1, 9 + 1)
                
                while not there_is_space_free(grid2.controls[position_of_cpu - 1]):
                        position_of_cpu = Random().randrange(1, 9 + 1)
                        snack = SnackBar(
                                  bgcolor=colors.AMBER_500,
                                  content=Text(
                                   "This cell is occupied. Try again (computer)",
                                    color="black",
                                   size=17,
                                   weight=FontWeight.BOLD
                            )
                        )
                        page.snack_bar = snack
                        page.snack_bar.open = True
                        page.update()
                                
                UpdateCell(grid2.controls[position_of_cpu - 1], CPU_CHARACTER, ChangeColor)
                update_current_player(CPU_CHARACTER)
                SetTurn(int(1))
                CountCells += 1
                
                if winner_in_rows(grid2, CPU_CHARACTER) or winner_in_column(grid2, CPU_CHARACTER) or winner_in_diagonals(grid2, CPU_CHARACTER): StateBoard["WINNER"] = True
                if StateBoard["WINNER"]:
                    winner = CPU_CHARACTER
                    alert = AlertDialog(
                       bgcolor=colors.GREEN_500,
                       content=Text(f"Winner computer: {winner}", text_align="center", size=18)
                    )
                    page.open(alert)
                    Reset_game_option_2()
                    page.update()
                    return
                
                if CountCells == 9: StateBoard["DRAW"] = True
             
                if StateBoard["DRAW"]:
                   alert = AlertDialog(
                          bgcolor="#212121",
                          content= Text("it is DRAW!", color="WHITE", size=18, text_align="center")
                   )
                   page.open(alert)
                   page.update()
                   Reset_game_option_2()
                   return     
        else:
            snack = SnackBar(
                     bgcolor=colors.AMBER_500,
                     content=Text(
                              f"This cell is occupied. Try again (player)",
                               color="black",
                            size=17,
                                weight=FontWeight.BOLD
                        ),
                    )
            page.snack_bar = snack
            page.snack_bar.open = True
            page.update()
            return 
    
    def Reset_game_option_2():
        nonlocal grid2, CountCells, CurrentPlayer
        CountCells = 0
        StateBoard["WINNER"] = False
        StateBoard["DRAW"] = False
        CurrentPlayer.value = ""
        
        for control in grid2.controls:
            control.content.value = ""
            page.update()
                               
    def open_view_two_players(e):
        menu.visible = False
        view_players.visible = True
        page.update()
  
    def open_you_versus_computer(e):
        menu.visible  = False
        you_and_computer.visible = True
        page.update()
  
    menu =  ViewShowMenu( 
                    content=Column(
                              alignment=MainAxisAlignment.CENTER,
                              spacing=20,
                              controls=[
                    Text(
                          value="Welcome to tic tac toe",
                          color="white",
                          size=19,
                          weight=FontWeight.BOLD
                    ),
               
                    TextButton(   
                       text="1 player",
                       style= ButtonStyle(bgcolor="#455A64",color="white"),
                       width=180,
                       on_click=open_you_versus_computer
                    ),
            
                TextButton(
                    "2 players",
                    style= ButtonStyle(bgcolor="#455A64", color="white"),
                    width=180,
                    on_click=open_view_two_players

                )
            
            ]
        )
    )     
    grid = GenerateBoard(context)
    grid2 = GenerateBoard(ContextTwo)
    you_and_computer = view_you_versus_computer(
                content= Row(
                    alignment=MainAxisAlignment.CENTER,
                     controls=[
                        Text("Select a character:", color="white", size=18, weight=FontWeight.BOLD),
                        TextButton(content=Text("X", size=18, color=Colors.RED_500), on_click=get_value_player_1_x, style=ButtonStyle(padding=4, bgcolor=Colors.LIGHT_BLUE_200)),
                        TextButton(content=Text("O", size=18, color=Colors.BLUE_500), on_click=get_value_player_1_o, style=ButtonStyle(padding=4, bgcolor=Colors.LIGHT_BLUE_200))
                ]
            )
    
        )
    view_players = view_two_players(
                content=Row(
                    spacing=20,
                   
                    controls=[
                        grid,
                        Column(
                            spacing=10,
                            alignment=MainAxisAlignment.CENTER,
                            controls=[
                                Row(controls=[
                                    Text("Current player:", color="white", size=16),
                                    CurrentPlayer
                                ]                     
                                ),
                                Row(
                                    spacing=8,
                                    controls=[
                                        TextButton(text="rest", style=ButtonStyle(padding=3,color="black",bgcolor="#FFC400"), on_click=lambda e: ResetGame()),
                                        TextButton(on_click=cancel_view, text="cancel", style=ButtonStyle(padding=3, color="white",bgcolor="#455A64"))    
                                ]
                            )
                        ]
                    )
                ]      
            )
        )
    
    page.add(
        Container(
            width=980,
            height=600,
            alignment=alignment.center,
            padding=10,
            content= Column(
                        spacing=30,
                        alignment=MainAxisAlignment.CENTER,
                           controls= [
                           menu,
                           view_players,
                           you_and_computer
                    ]
                )               
            )
        )
app(target=main, view=AppView.WEB_BROWSER, port=8000)