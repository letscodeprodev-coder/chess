from tkinter import*
from tkinter import messagebox
class ChessGame(Tk):
    def __init__(self) -> None:
        super().__init__()
        self.geometry("800x700+10+10")
        self.title("Chess Game")
        self.chess_piece = {
            'a1': ('♖',0), 'b1': ('♘',0), 'c1': ('♗',0), 'd1': ('♕',0), 'e1': ('♔',0), 'f1': ('♗',0), 'g1': ('♘',0), 'h1': ('♖',0),
            'a2': ('♙',0), 'b2': ('♙',0), 'c2': ('♙',0), 'd2': ('♙',0), 'e2': ('♙',0), 'f2': ('♙',0), 'g2': ('♙',0), 'h2': ('♙',0),
            'a8': ('♜',1), 'b8': ('♞',1), 'c8': ('♝',1), 'd8': ('♛',1), 'e8': ('♚',1), 'f8': ('♝',1), 'g8': ('♞',1), 'h8': ('♜',1),
            'a7': ('♟',1), 'b7': ('♟',1), 'c7': ('♟',1), 'd7': ('♟',1), 'e7': ('♟',1), 'f7': ('♟',1), 'g7': ('♟',1), 'h7': ('♟',1)
        }

        self.chess_piece_routes = {
            '♖': [(0, 1), (1, 0), (0, -1), (-1, 0), 'continuos'],
            '♜': [(0, 1), (1, 0), (0, -1), (-1, 0), 'continuos'],
            '♘': [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1), 'step'],
            '♞': [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1), 'step'],
            '♗': [(-1, -1), (-1, 1), (1, -1), (1, 1), 'continuos'],
            '♝': [(-1, -1), (-1, 1), (1, -1), (1, 1), 'continuos'],
            '♕': [(-1, -1), (-1, 1), (1, -1), (1, 1), (0, 1), (1, 0), (0, -1), (-1, 0), 'continuos'],
            '♛': [(-1, -1), (-1, 1), (1, -1), (1, 1), (0, 1), (1, 0), (0, -1), (-1, 0), 'continuos'],
            '♔': [(-1, -1), (-1, 1), (1, -1), (1, 1), (0, 1), (1, 0), (0, -1), (-1, 0), 'step'],
            '♚': [(-1, -1), (-1, 1), (1, -1), (1, 1), (0, 1), (1, 0), (0, -1), (-1, 0), 'step'],
            '♙': [(1, 0), 'step'],
            '♟': [(-1, 0), 'step'],
        }
        self.turn = 0
        self.init_ui()
    def init_ui(self):
        ROW = "12345678"
        COLUMN = "abcdefgh"
        for row_index, row in enumerate(ROW):
            for col_index, col in enumerate(COLUMN):
                color = 'tomato' if (row_index + col_index) % 2 == 0 else "white"
                
                
                box = Label(self,text='',bg=color,anchor='center',font=("Consolas",25),highlightbackground='black',highlightthickness=1)
                box.grid(row=row_index, column=col_index, sticky='nsew')
                box.position = col+row 
                

                if self.chess_piece.get(box.position):
                    box.piece = self.chess_piece.get(box.position)[0]
                    box.team = self.chess_piece.get(box.position)[1]
                    box.hold_piece = True
                else:
                    box.piece = ''
                    box.team = 2
                    box.hold_piece = False
                box.config(text=box.piece)


                box.coord = (row_index, col_index)
                box.default_color = color 
                box.highlight_color = box.default_color
                box.status = 'normal'
                box.routes = []

                box.bind("<Button-1>",self.click)
        for k in range(8):
            self.rowconfigure(k, weight=1)
            self.columnconfigure(k, weight=1, minsize=100)
    def click(self, event):
        box = event.widget 

        is_white_turn = True if self.turn % 2 == 0 else False 
        if is_white_turn:
            if box.hold_piece:
                if box.team != 1:
                    if box.status == 'selected':

                        box.config(bg=box.default_color)
                        box.higlight_color = box.default_color
                        box.status = 'normal'
                        self.clear_highlights()
                    else:
                        
                        self.clear_highlights()
                        self.show_routes(box) 
                        box.status = 'selected'
                        box.config(bg='steelblue')
                        box.highlight_color = 'steelblue'
                else:
                    if box.status == 'path':
                        self.movement(box)
                        self.clear_highlights()
                    else:
                        print("not your turn")
                        messagebox.showerror('not your turn','this is not you turn')
            else:
                if box.status == 'path':
                    self.movement(box)
                    self.clear_highlights()
                else:
                    print("please click on the box which have a piece")
                    messagebox.showerror('empty box','please click on the box which have a piece')
        else:
            if box.hold_piece:
                if box.team != 0:
                    if box.status == 'selected':
                        
                        box.config(bg=box.default_color)
                        box.higlight_color = box.default_color
                        box.status = 'normal'
                        self.clear_highlights()
                        
                    
                    else:
                        
                        self.clear_highlights()
                        self.show_routes(box) 
                        box.status = 'selected'
                        box.config(bg='steelblue')
                        box.highlight_color = 'steelblue'
                else:
                    if box.status == 'path':
                        self.movement(box)
                        self.clear_highlights()
                    else:
                        print("not your turn")
                        messagebox.showerror('not your turn','this is not you turn')
                        
            else:
                if box.status == 'path':
                    self.movement(box)
                    self.clear_highlights()
                else:
                    print("please click on the box which have a piece")
                    messagebox.showerror('empty box','please click on the box which have a piece')

    def add_extra_move(self,direction:list,coord:tuple,default_coord:tuple,string):
        try:
            new_row, new_col = coord 
            row, col = default_coord 
            square = self.grid_slaves(row=row+new_row,column=col+new_col)[0]
            if square.hold_piece:
                if string == 'append':
                    direction.append(coord)
                elif string == 'remove':
                    direction.remove(coord)
        except Exception as e:
            pass
    def show_routes(self, box):
        box.routes = self.chess_piece_routes.get(box.piece)
        
        piece_type = box.routes[-1]
        direction = box.routes[:-1]
        row, col = box.coord
        if box.piece == '♙':
           
            self.add_extra_move(direction,(1,-1),box.coord,'append')
            
            self.add_extra_move(direction,(1,0),box.coord,'remove')
            
            self.add_extra_move(direction,(1,1),box.coord,'append')
            
            if row == 1:
                direction.append((2,0))
        elif box.piece == '♟':
            
            self.add_extra_move(direction,(-1,-1),box.coord,'append')
            
            self.add_extra_move(direction,(-1,0),box.coord,'remove')
            
            self.add_extra_move(direction,(-1,1),box.coord,'append')
            
            if row == 6:
                direction.append((-2,0))
        if box.hold_piece:
            for dx, dy in direction:
                new_row, new_col = row + dx, col + dy 
                
                while 0 <= new_row <= 7 and ord('a') <= new_col + ord('a') <= ord('h'):
                    square = self.grid_slaves(row=new_row,column=new_col)[0]
                    if square.team == box.team:
                        break
                    square.walker = box 
                    square.status = 'path'
                    square.highlight_color = 'yellow'
                    square.config(bg='yellow')

                    new_row += dx
                    new_col += dy
                    if square.team != box.team and square.team != 2:
                        break
                    if piece_type == 'step':
                        break 
    def movement(self,square):
        box = square.walker
        if box.hold_piece:
            square['text'] = box['text']
            box['text'] = ''
            square.routes = box.routes
            box.routes = []
            square.hold_piece = True 
            box.hold_piece = False 
            square.team = box.team 
            box.team = 2 
            square.piece = box.piece 
            box.piece = ''

            self.turn += 1
            
    def clear_highlights(self):
        for box in self.grid_slaves():
            if box.status != 'normal':
                box.status ='normal'
                box.highlight_color = box.default_color 
                box.config(bg=box.default_color)
    
        

def main():
    game = ChessGame()
    game.mainloop()
if __name__ == '__main__':
    main()