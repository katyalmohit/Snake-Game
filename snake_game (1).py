import pygame
from pygame.locals import *
import time
import random
from tkinter import *
from PIL import ImageTk, Image
SIZE = 40
BACKGROUND_COLOR = (25, 51, 0)
class GameGUI:
    def __init__(self, master):
        pygame.mixer.init()
        pygame.mixer.music.load('bg_music_1.mp3')
        pygame.mixer.music.play(-1, 0)
        
        self.master = master
        master.title("SAAMP- Da Incredible Snake")

        # Load and resize image
        img = Image.open('snake.png')
        resized_img = img.resize((400, 300))
        self.img = ImageTk.PhotoImage(resized_img)
        
        # Create labels and buttons
        img_label = Label(master, image=self.img)
        img_label.pack(pady=(10,5))
        text_label = Label(master, text="SAAMP - DISs", fg='green', bg='#013220')
        text_label.pack()
        text_label.config(font=('impact', 24))
        self.start_button = Button(master, text="START", bg='white', fg='black', command=self.start_game)
        self.start_button.pack(pady=(10, 10))
        self.start_button.config(font=('consolas', 20))
        quit_button = Button(master, text="QUIT", bg='white', fg='black', command=self.quit_game)
        quit_button.pack(pady=(0, 10))
        quit_button.config(font=('consolas', 20))
        
    def quit_game(self):
        self.master.destroy()
        pygame.quit()
        
    def start_game(self):
        self.master.destroy()
        # Call your game logic here
        
        SIZE = 40
        class Apple:
            def __init__(self, parent_screen):
                self.parent_screen = parent_screen
                self.image = pygame.image.load("apple.jpg").convert()
                self.x = 120
                self.y = 120

            def draw(self):
                self.parent_screen.blit(self.image, (self.x, self.y))
                pygame.display.flip()               #whenever we update any value we use flip or update.

            def move(self):
                self.x = random.randint(1,24)*SIZE
                self.y = random.randint(1,19)*SIZE

        class Snake:
            def __init__(self, parent_screen):
                self.parent_screen = parent_screen
                self.image = pygame.image.load("block.jpg").convert()
                self.direction = 'down'

                self.length = 1
                self.x = [40]
                self.y = [40]

            def move_left(self):
                self.direction = 'left'

            def move_right(self):
                self.direction = 'right'

            def move_up(self):
                self.direction = 'up'

            def move_down(self):
                self.direction = 'down'

            def walk(self):
                # update body
                for i in range(self.length-1,0,-1):
                    self.x[i] = self.x[i-1]
                    self.y[i] = self.y[i-1]

                # update head
                if self.direction == 'left':
                    self.x[0] -= SIZE
                elif self.direction == 'right':
                    self.x[0] += SIZE
                elif self.direction == 'up':
                    self.y[0] -= SIZE
                elif self.direction == 'down':
                    self.y[0] += SIZE

                self.draw()

            def draw(self):
                for i in range(self.length):
                    self.parent_screen.blit(self.image, (self.x[i], self.y[i]))
                pygame.display.flip()

            def increase_length(self):
                self.length += 1
                self.x.append(-1)
                self.y.append(-1)

        class Game:
            def __init__(self):
                pygame.init()
                pygame.display.set_caption("SAAMP- Da Incredible Ssnake.")
                pygame.mixer.init()
                self.play_background_music()
                self.surface = pygame.display.set_mode((1000, 600))
                self.snake = Snake(self.surface)
                self.snake.draw()
                self.apple = Apple(self.surface)
                self.apple.draw()

            def play_background_music(self):
                pygame.mixer.music.load('rick.mp3')
                pygame.mixer.music.play(-1, 0)
            
            def play_sound(self, sound_name):
                if sound_name == "crash":
                    sound = pygame.mixer.Sound("crash.mp3")
                elif sound_name == 'ding':
                    sound = pygame.mixer.Sound("ding.mp3")

                pygame.mixer.Sound.play(sound)
                
            def render_background(self):
                bg = pygame.image.load("background.jpg")
                self.surface.blit(bg, (0,0))
                pygame.display.flip()
                
            def reset(self):
                self.snake = Snake(self.surface)
                self.apple = Apple(self.surface)
                pygame.display.flip()

            def is_collision(self, x1, y1, x2, y2):
                if x1 >= 1000 or x1 < 0 or y1 >= 600 or y1 < 0:
                    return True
                if x1 >= x2 and x1 < x2 + SIZE:
                    if y1 >= y2 and y1 < y2 + SIZE:
                        return True
                return False
            
                
            def play(self):
                self.render_background()
                self.snake.walk()
                self.apple.draw()
                self.display_score()
                pygame.display.flip()

                # snake eating apple scenario
                if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
                    self.play_sound("ding")
                    self.snake.increase_length()
                    self.apple.move()

                # snake colliding with itself
                for i in range(1, self.snake.length):
                    if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                        self.play_sound("crash")
                        raise "Game over"
                

            def display_score(self):
                with open("highscore.txt", "r") as file:
                    self.highscore = int(file.read())
                font = pygame.font.SysFont('consolas',30)
                score = font.render(f"Score: {self.snake.length-1}",True,(200,200,200))
                self.surface.blit(score,(850,10))
                #to display highscore
                hsc = font.render(f"High Score: {self.highscore}",True,(200,200,200))
                self.surface.blit(hsc,(600,10))
                pygame.display.flip()
                

            def show_game_over(self):
                self.render_background()
                font = pygame.font.SysFont('times new roman', 50)
                line1 = font.render(f"YOU DIED!! Game is over! Your score is {self.snake.length-1}.", True, (255, 255, 255))
                self.surface.blit(line1, (50, 300))
                pygame.mixer.music.pause()
                #to write high score into file
                if int(self.snake.length-1) > int(self.highscore):                        
                    with open("highscore.txt", "w") as file:
                        file.write(str(self.snake.length-1))
                pygame.display.flip()


            def run(self):
                running = True
                pause = False
                while running:
                    for event in pygame.event.get():
                        if event.type == KEYDOWN:
                            if event.key == K_ESCAPE:
                                running = False
                                pygame.quit()

                            if event.key == K_RETURN:
                                pygame.mixer.music.unpause()
                                pause = False

                            if not pause:
                                if event.key == K_LEFT:
                                    self.snake.move_left()

                                elif event.key == K_RIGHT:
                                    self.snake.move_right()

                                elif event.key == K_UP:
                                    self.snake.move_up()

                                elif event.key == K_DOWN:
                                    self.snake.move_down()
                        elif event.type == pygame.QUIT:
                            running = False
                            pygame.quit()
                    try:

                        if not pause:
                            self.play()

                    except Exception as e:
                        self.show_game_over()
                        pause = True
                        self.reset()
                    time.sleep(.015)

        if __name__ == '__main__':
            game = Game()
            game.run()
        print("Starting game...")

root = Tk()
game_gui = GameGUI(root)
root.mainloop()