import tkinter
from random import randint

window = tkinter.Tk()
label = tkinter.Label(window, text="Игра начнется через...")
canvas = tkinter.Canvas(window, bg='black', height=600, width=600)
speed = 100


class Snake:
    def __init__(self):
        self.appleCoor = self.generateApple()
        self.appleCoor = [self.appleCoor[0], self.appleCoor[1], self.appleCoor[0] + 10, self.appleCoor[1] + 10]
        self.toStart = 3
        self.blocks = []
        self.game_over = False
        self.direction = 1
        self.gameStarted = False
        self.first_coor = [295, 295, 305, 305]
        self.blocks.append(canvas.create_rectangle(295, 295, 305, 305, fill="green"))
    
    def create_block(self):
        if self.direction == 1:
            self.blocks.append(canvas.create_rectangle(self.first_coor[0], self.first_coor[1] - 11, self.first_coor[2], self.first_coor[3] - 11, fill="green"))
            self.first_coor = [self.first_coor[0], self.first_coor[1] - 11, self.first_coor[2], self.first_coor[3] - 11]
        elif self.direction == 2:
            self.blocks.append(canvas.create_rectangle(self.first_coor[0] + 11, self.first_coor[1], self.first_coor[2] + 11, self.first_coor[3], fill="green"))
            self.first_coor = [self.first_coor[0] + 11, self.first_coor[1], self.first_coor[2] + 11, self.first_coor[3]]
        elif self.direction == 3:
            self.blocks.append(canvas.create_rectangle(self.first_coor[0], self.first_coor[1] + 11, self.first_coor[2], self.first_coor[3] + 11, fill="green"))
            self.first_coor = [self.first_coor[0], self.first_coor[1] + 11, self.first_coor[2], self.first_coor[3] + 11]
        else:
            self.blocks.append(canvas.create_rectangle(self.first_coor[0] - 11, self.first_coor[1], self.first_coor[2] - 11, self.first_coor[3], fill="green"))
            self.first_coor = [self.first_coor[0] - 11, self.first_coor[1], self.first_coor[2] - 11, self.first_coor[3]]

    def moving(self):
        if not(self.game_over):
            canvas.delete(self.blocks[0])
            del self.blocks[0]
            self.create_block()
    
    def change_dir(self, event):
        if self.toStart == 0 and not(self.game_over) and self.gameStarted:
            if event.keysym == "Up" and self.direction != 3 and self.direction != 1:
                self.direction = 1
                self.moving()
                if self.checkColission():
                    self.game_over = True
            elif event.keysym == "Right" and self.direction != 4 and self.direction != 2:
                self.direction = 2
                self.moving()
                if self.checkColission():
                    self.game_over = True
            elif event.keysym == "Down" and self.direction != 1 and self.direction != 3:
                self.direction = 3
                self.moving()
                if self.checkColission():
                    self.game_over = True
            elif event.keysym == "Left" and self.direction != 2 and self.direction != 4:
                self.direction = 4
                self.moving()
                if self.checkColission():
                    self.game_over = True
            elif event.keysym == "Escape":
                self.game_over = True
        elif self.game_over:
            if event.keysym == "r":
                self.game_over = False
                self.toStart = 3
                window.after(500, self.onTimer)
                for i in self.blocks:
                    canvas.delete(i)
                canvas.delete(self.apple)
                self.__init__()

    
    def onTimer(self):
        if self.toStart == 0:
            if not(self.game_over):
                label.config(text="Ешьте как можно больше яблок!")
                self.gameStarted = True
                self.moving()
                if self.checkColission():
                    self.game_over = True
                    self.gameStarted = False
                if self.checkColApple():
                    self.create_block()
                    self.create_block()
                    self.create_block()
                    canvas.delete(self.apple)
                    self.appleCoor = self.generateApple()
                    self.appleCoor = [self.appleCoor[0], self.appleCoor[1], self.appleCoor[0] + 10, self.appleCoor[1] + 10]
                window.after(speed, self.onTimer)
            else:
                label.config(text="Игра окончена:(")
        else:
            label.config(text=f"Игра начнется через {self.toStart}")
            self.toStart -= 1
            window.after(1000, self.onTimer)
    
    def generateApple(self):
        x, y = (randint(0, 590) // 5) * 5, (randint(0, 590) // 5) * 5
        self.apple = canvas.create_rectangle(x, y, x + 10, y + 10, fill="red")
        return [x, y]
    
    def checkColission(self):
        for i in self.blocks[:-1]:
            if self.first_coor == canvas.coords(i):
                return True
        if not(0 < self.first_coor[0] < 600 and 0 < self.first_coor[1] < 600 and 0 < self.first_coor[2] < 600 and 0 < self.first_coor[3] < 600):
            return True
        return False
    
    def checkColApple(self):
        x1, y1, x2, y2 = 0, 0, 0, 0
        if self.first_coor[0] > self.appleCoor[0]:
            x1 = self.first_coor[0]
        else:
            x1 = self.appleCoor[0]
        if self.first_coor[2] < self.appleCoor[2]:
            x2 = self.first_coor[2]
        else:
            x2 = self.appleCoor[2]
        if self.first_coor[1] > self.appleCoor[1]:
            y1 = self.first_coor[1]
        else:
            y1 = self.appleCoor[1]
        if self.first_coor[3] < self.appleCoor[3]:
            y2 = self.first_coor[3]
        else:
            y2 = self.appleCoor[3]
        if x2 <= x1:
            return False
        if y2 <= y1:
            return False
        return True



snake = Snake()
label.pack()
canvas.pack()
window.bind_all("<Key>", snake.change_dir)
window.after(speed, snake.onTimer)
window.mainloop()
