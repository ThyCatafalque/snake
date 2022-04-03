from tkinter import *
from random import *
from PIL import ImageTk, Image
from pygame import mixer

class Snake:
    def __init__(self, cell_size, x_size, y_size):
        self.__CELL_SIZE = 20 if cell_size == None else cell_size
        self.__X_SIZE = 30 if x_size == None else x_size 
        self.__Y_SIZE = 30 if y_size == None else y_size 
        self.__MAP = [i for i in range(0, self.__X_SIZE*self.__Y_SIZE)]
        self.__after = None

        self._REC_PADDING = 3
        self._ALLOWED_KEYS = ['Right', 'Left', 'Up', 'Down']

        self.__tk = Tk()
        self.__tk.title('snake')
        self.__tk.bind('<Key>', self.__key_pressed)
        self.__tk.title = 'SNAKE'

        self.__score = StringVar()
        self.__score_label = Label(self.__tk, textvariable = self.__score, bg="black", font=("Courier", 25), fg='white')
        self.__score_label.grid(row=0,sticky=N+S+W+E)

        self.__can = Canvas(self.__tk, width=self.__X_SIZE*self.__CELL_SIZE, height=self.__Y_SIZE*self.__CELL_SIZE, bg = "black")
        self.__can.grid(row=1, columnspan=2)

        self.__new_game_btn = Button(text='new game', background='black', font=("Courier", 25), fg='white', command=self.__new_game)
        self.__new_game_btn.grid(row=0, column=1, sticky=N+S+W+E)

        self.__SNAKE_CLR = 'white'

        image = Image.open("conf.jpg").resize((self.__X_SIZE*self.__CELL_SIZE, self.__Y_SIZE*self.__CELL_SIZE))
        self.__PHOTO = ImageTk.PhotoImage(image)
        self._game_over_label = Label(self.__tk, image = self.__PHOTO)
        self._game_over_label.image = self.__PHOTO
        self._game_over_label.grid_forget()

        mixer.init()
        mixer.music.load('oof.mp3')

        self.__can.focus_set()

        self.__new_game()

    def __new_game(self):
        if self.__after != None:
            self.__tk.after_cancel(self.__after)
        self._game_over_label.grid_forget()
        self.__FOOD = randint(1, self.__X_SIZE * self.__Y_SIZE)
        self.__ROTTEN_FOOD = randint(1, self.__X_SIZE * self.__Y_SIZE) if randint (1, 3) == 1 else None
        self.__SNAKE = [2, 1, 0]
        self.__DIRECTION = 'R'
        self.__DELAY = 100
        self.__GAME_OVER = False
        self.__score.set(str(len(self.__SNAKE)))
        self.__start()

    def __key_pressed(self, event):
        if event.keysym in self._ALLOWED_KEYS:
            self.__DIRECTION = event.keysym[0]

    def __move(self):
        head = self.__SNAKE[0]
        tail = self.__SNAKE[-1]

        if self.__DIRECTION == 'R':
            head = head - (self.__X_SIZE if (head + 1) % self.__X_SIZE == 0 else 0) + 1
        elif self.__DIRECTION == 'L':
            head = head + (self.__X_SIZE if head % self.__X_SIZE == 0 else 0) - 1
        elif self.__DIRECTION == 'U':
            head = head + (self.__X_SIZE * (self.__Y_SIZE - 1) if head // self.__X_SIZE == 0 else - self.__X_SIZE)
        elif self.__DIRECTION == 'D':
            head = head - (self.__X_SIZE * (self.__Y_SIZE - 1) if head // self.__X_SIZE == self.__Y_SIZE - 1 else - self.__X_SIZE)

        if len(self.__SNAKE) == 0 or head in self.__SNAKE[1:]:
            self.__GAME_OVER = True
            mixer.music.play()

        self.__SNAKE = [head] + self.__SNAKE[:-1]

        if head == self.__FOOD:
            self.__FOOD = choice([i for i in self.__MAP if i not in self.__SNAKE])
            self.__SNAKE.append(tail)
            self.__DELAY = self.__DELAY - 1 if self.__DELAY > 1 else self.__DELAY
            self.__ROTTEN_FOOD = choice([i for i in self.__MAP if i not in self.__SNAKE]) if randint (1, 3) == 1 else self.__ROTTEN_FOOD
            
        if head == self.__ROTTEN_FOOD:
            self.__ROTTEN_FOOD = None
            self.__SNAKE = self.__SNAKE[:-2]
            mixer.music.play()

        self.__score.set(str(len(self.__SNAKE)))

    def __draw_rec(self, cell, color):
        x = ((cell) % self.__X_SIZE) * self.__CELL_SIZE     
        y = ((cell) // self.__X_SIZE) * self.__CELL_SIZE

        self.__can.create_rectangle(x + self._REC_PADDING, y + self._REC_PADDING, x + self.__CELL_SIZE - self._REC_PADDING, y + self.__CELL_SIZE - self._REC_PADDING, fill=color)

    def __draw(self):
        self.__can.delete('all')

        self.__draw_rec(self.__FOOD, 'red')
        if not self.__ROTTEN_FOOD == None:
            self.__draw_rec(self.__ROTTEN_FOOD, 'yellow')

        for i in self.__SNAKE:
            self.__draw_rec(i, self.__SNAKE_CLR)

    def __go_on(self):
        self.__move()
        self.__draw()

        if self.__GAME_OVER:
            self.__game_over()
            return

        self.__after = self.__tk.after(self.__DELAY, self.__go_on)

    def __game_over(self):
        self._game_over_label.grid(row=1, columnspan=2)

    def __start(self):
        self.__go_on()
        self.__tk.mainloop()

def main():
    s = Snake(20, 30, 30)

if __name__ == '__main__':
    main()