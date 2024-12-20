from tkinter import *

WINDOW_SIZE = 400
GRID_LINE_WIDTH = 2
SYMBOL_WIDTH = WINDOW_SIZE / 80
SYMBOL_SIZE = 0.375
X_COLOR = 'deep sky blue4'
O_COLOR = 'tomato'
DRAW_SCREEN_COLOR = 'light sea green'
GRID_COLOR = 'black'
FIRST_PLAYER = 2
CELL_SIZE = WINDOW_SIZE / 3
STATE_TITLE_SCREEN = 0
STATE_X_TURN = 1
STATE_O_TURN = 2
STATE_GAME_OVER = 3
EMPTY = 0
X = 1
O = 2

class Game(Tk):

    def __init__(self):
        Tk.__init__(self)        
        self.canvas = Canvas(height=WINDOW_SIZE, width=WINDOW_SIZE, bg='white')
        self.canvas.pack()
        self.bind('<x>', self.exit)
        self.bind('<X>', self.exit)
        self.canvas.bind('<Button-1>', self.click)
        self.gamestate = STATE_TITLE_SCREEN
        self.title_screen()
        self.board = [
                [EMPTY, EMPTY, EMPTY],
                [EMPTY, EMPTY, EMPTY],
                [EMPTY, EMPTY, EMPTY]
            ]

    def title_screen(self):
        self.canvas.delete('all')
        self.canvas.create_rectangle(0, 0, WINDOW_SIZE, WINDOW_SIZE, fill='white', outline='')
        self.canvas.create_rectangle(int(WINDOW_SIZE / 15),
                                     int(WINDOW_SIZE / 15),
                                     int(WINDOW_SIZE * 14 / 15),
                                     int(WINDOW_SIZE * 14 / 15),
                                     outline='')
        self.canvas.create_rectangle(int(WINDOW_SIZE / 10),
                                     int(WINDOW_SIZE / 10),
                                     int(WINDOW_SIZE * 9 / 10),
                                     int(WINDOW_SIZE * 9 / 10),
                                     fill='light blue', outline='')
        self.canvas.create_text(WINDOW_SIZE / 2, WINDOW_SIZE / 3,
                                text='TIC TAC TOE', fill='black',
                                font=('Calibri', int(-WINDOW_SIZE / 12), 'bold underline'))
        self.canvas.create_text(int(WINDOW_SIZE / 2),
                                int(WINDOW_SIZE / 2.5),
                                text='[click to play]', fill='purple',
                                font=('Arial', int(-WINDOW_SIZE / 25)))
    
    def new_board(self):
        self.canvas.delete('all')
        self.board = [
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]
        ]
        for n in range(1, 3):
            self.canvas.create_line(CELL_SIZE * n, 0,
                                    CELL_SIZE * n, WINDOW_SIZE,
                                    width=GRID_LINE_WIDTH,
                                    fill=GRID_COLOR)
            self.canvas.create_line(0, CELL_SIZE * n,
                                    WINDOW_SIZE, CELL_SIZE * n,
                                    width=GRID_LINE_WIDTH, fill=GRID_COLOR)

    def gameover_screen(self, outcome):
        self.canvas.delete('all')
        if outcome == 'X WINS':
            wintext = 'X wins'
            wincolor = 'light green'
        elif outcome == 'O WINS':  
            wintext = 'O wins'
            wincolor = 'gold2'
        elif outcome == 'DRAW':
            wintext = 'Draw'
            wincolor = DRAW_SCREEN_COLOR
        else:
            wintext = 'Game Over'
            wincolor = 'gray'
        self.canvas.create_rectangle(0, 0,
                                     WINDOW_SIZE, WINDOW_SIZE,
                                     fill=wincolor, outline='')
        self.canvas.create_text(int(WINDOW_SIZE / 2), int(WINDOW_SIZE / 2),
                                text=wintext, fill='black',
                                font=('Calibri', int(-WINDOW_SIZE / 6), 'bold'))
        self.canvas.create_text(int(WINDOW_SIZE / 2), int(WINDOW_SIZE / 1.65),
                                text=' [Click to play again]',
                                fill='purple', font=('Arial',
                                int(-WINDOW_SIZE / 25)))

    def click(self, event):
        x = self.pixel_to_grid(event.x)
        y = self.pixel_to_grid(event.y)
        if self.gamestate == STATE_TITLE_SCREEN:
            self.new_board()
            self.gamestate = FIRST_PLAYER
        elif(self.gamestate==STATE_X_TURN and self.board[y][x]==EMPTY):
            self.new_move(X, x, y)
            if self.has_won(X):
                self.gamestate = STATE_GAME_OVER
                self.gameover_screen('X WINS')
            elif self.is_a_draw():
                self.gamestate = STATE_GAME_OVER
                self.gameover_screen('DRAW')
            else:
                self.gamestate = STATE_O_TURN
        elif(self.gamestate==STATE_O_TURN and self.board[y][x]==EMPTY):
            self.new_move(O, x, y)
            if self.has_won(O):
                self.gamestate = STATE_GAME_OVER
                self.gameover_screen('O WINS')
            elif self.is_a_draw():
                self.gamestate = STATE_GAME_OVER
                self.gameover_screen('DRAW')
            else:
                self.gamestate = STATE_X_TURN
        elif self.gamestate == STATE_GAME_OVER:
            self.new_board()
            self.gamestate = FIRST_PLAYER
    
    def new_move(self, player, grid_x, grid_y):
        if player == X:
            self.draw_X(grid_x, grid_y)
            self.board[grid_y][grid_x] = X
        elif player == O:
            self.draw_O(grid_x, grid_y)
            self.board[grid_y][grid_x] = O

    def draw_X(self, grid_x, grid_y):
        x = self.grid_to_pixel(grid_x)
        y = self.grid_to_pixel(grid_y)
        delta = CELL_SIZE / 2 * SYMBOL_SIZE
        self.canvas.create_line(x-delta, y-delta,
                                x+delta, y+delta,
                                width=SYMBOL_WIDTH, fill=X_COLOR)
        self.canvas.create_line(x-delta, y+delta,
                                x+delta, y-delta,
                                width=SYMBOL_WIDTH, fill=X_COLOR)

    def draw_O(self, grid_x, grid_y):
        x = self.grid_to_pixel(grid_x)
        y = self.grid_to_pixel(grid_y)
        delta = CELL_SIZE / 2 * SYMBOL_SIZE
        self.canvas.create_oval(x-delta, y-delta,
                                x+delta, y+delta,
                                width=SYMBOL_WIDTH, outline=O_COLOR)

    def has_won(self, symbol):
        for y in range(3):
            if self.board[y] == [symbol, symbol, symbol]:
                return True
        for x in range(3):
            if self.board[0][x] == self.board[1][x] == self.board[2][x] == symbol:
                return True
        if self.board[0][0] == self.board[1][1] == self.board[2][2] == symbol:
            return True
        elif self.board[0][2] == self.board[1][1] == self.board[2][0] == symbol:
            return True
        return False

    def is_a_draw(self):
        for row in self.board:
            if EMPTY in row:
                return False
        return True

    def grid_to_pixel(self, grid_coord):
        pixel_coord = grid_coord * CELL_SIZE + CELL_SIZE / 2
        return pixel_coord

    def pixel_to_grid(self, pixel_coord):
        if pixel_coord >= WINDOW_SIZE:
            pixel_coord = WINDOW_SIZE - 1
        return int(pixel_coord // CELL_SIZE)

    def exit(self, event):
        self.destroy()

def main():
    root = Game()
    root.title("TIC TAC TOE")
    root.mainloop()
main()