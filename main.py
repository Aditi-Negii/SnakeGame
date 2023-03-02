import pygame as py
from pygame.locals import *           # for using functions like keydown, keyup
import time
import random

SIZE = 40 # size of block

class Apple:
    def __init__(self, parent_screen):
        self.image = py.image.load("resources/apple.jpg").convert() # loads image of apple on screen
        self.parent_screen = parent_screen
        self.x = SIZE*3   # to align apple with snake, should be multiple of 40 only
        self.y = SIZE*3

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))  # blit(a method)-first arguement:what figure you want to draw(block) and second arguement: where do you want to draw meaning the dimensions of the block
        py.display.flip()  # allows only a portion of screen to get updated, not the whole screen

    def move(self):
        # whenever collision occurs move the apple to a random position using randint from random module
        self.x = random.randint(0,24)*SIZE   # since 1000(dimension of screen)/4 =25 and * size so that the value always less than1000 and lies within the screen but the apple was moving out of the screen so decreased it by 1
        self.y = random.randint(0,19)*SIZE   # since 800/4= 20

class Snake:
    def __init__(self, parent_screen, length):
        self.parent_screen = parent_screen
        self.block = py.image.load("resources/block.jpg").convert()  # for loading the image of the block
        self.direction = 'down'

        self.length = length
        self.x = [SIZE] * length  # written here so that i can easily change the dimensions by just changing the values of block_x and y
        self.y = [SIZE] * length  # have not specified length of snake since it keeps changing

    def increase_length(self):
        self.length += 1
        # adding new element to an array
        self.x.append(-1)
        self.y.append(-1)

    def move_left(self):   # moving the snake by 10 on the left and then drawing it
        self.direction = 'left' # to move the block of snake towards left

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def walk(self):

        for i in range(self.length-1, 0, -1): # for loop in reverse order so that next block comes in place of first block
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.direction == 'left':
            self.x[0] -= SIZE
        if self.direction == 'right':
            self.x[0] += SIZE
        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE

        self.draw()

    def draw(self):
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))  # blit-what figure you want to draw(block) and inside blit- where do you want to draw meaning the dimensions of the block

        py.display.flip()


class Game:
    def __init__(self):
        py.init()  # initialization of module
        py.display.set_caption("Snake Game by Aditi Negi")

        py.mixer.init() # to initialize mixer module: helps control the music used in pygame programs
        self.play_background_music()

        self.surface = py.display.set_mode((1000, 800))  # initialization of window or screen
        self.snake = Snake(self.surface, 1)  # initial length of block is 1
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True # there is a collision

        return False

    def display_score(self):
        font = py.font.SysFont('comic sans ms', 30)
        # storing font in variable called score
        score = font.render(f"Score: {self.snake.length}", True, (255,255,255)) # score is equal to length of snake
        self.surface.blit(score,(850,10))  #

    def play_background_music(self):
        py.mixer.music.load("resources/bg_music_1.mp3")  # music plays for more duration than sound hence music written
        py.mixer.music.play()

    def play_sound(self, sound):
        sound = py.mixer.Sound(f"resources/{sound}.mp3")
        py.mixer.Sound.play(sound)

    def render_background(self):
        bg = py.image.load("resources/background.jpg")  # green colour background
        self.surface.blit(bg, (0, 0))

    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        py.display.flip()  # to update some portion of the screem

        # snake eating apple
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.play_sound("ding")  # when snake collides with apple, play ding sound
            self.snake.increase_length()  # play the ding sound and increase length of snake by one
            self.apple.move()  # increase length and move apple to random position using randint

        # snake colliding with itself
        for i in range(3, self.snake.length):  # collision of head with remaining blocks except the ones which are just afer it i.e. block no.1 and 2
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound("crash")  # when head of snake(first block) collides with any other block, play crash sound
                raise "Collision occurred"   # throw or raise an exception if this condition occurs

        # snake colliding with the boundaries of the window
        if not (0 <= self.snake.x[0] <= 1000 and 0 <= self.snake.y[0] <= 800): # if head of snake is neither less nor equal to the boundary coordinates
            self.play_sound("crash")  # play crash sound
            raise "Hit the boundary error"  # and raise an exception when head of snake more than boundary coordinates

    def show_game_over(self):
        self.render_background()  # to show a one line message when game gets over
        font = py.font.SysFont('comic sans ms', 30)  # print the message in this font
        line1 = font.render(f"Score: {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(line1, (200, 300)) # will print score of player in a line
        line2 = font.render(" To play again press ENTER. To exit press ESCAPE!", True, (255, 255, 255))
        self.surface.blit(line2, (200, 350))  # will print the above message on the screen
        py.display.flip()

        py.mixer.music.pause()  # to pause bg music when game is over

    def reset(self):
        self.snake = Snake(self.surface, 1)  # if the player hits enter, length of snake should be one
        self.apple = Apple(self.surface) # apple should appear on screen at random position

    def run(self):
        running = True  # run while loop when true
        pause = False  # don't run when false

        while running:
            for event in py.event.get():  # running is true all the time expect when we have quit the event
                if event.type == KEYDOWN:  # when a key is pressed
                    if event.key == K_ESCAPE:  # check whether escape key has been pressed
                        running = False  # if escape pressed, exit the while loop

                    if event.key == K_RETURN:  # enter pressed
                        py.mixer.music.unpause()  # to start music again when enter pressed
                        pause = False

                    if not pause:
                        if event.key == K_LEFT:  # y remains same x changes, left arrow pressed
                            self.snake.move_left()

                        if event.key == K_RIGHT:  # right arrow key pressed
                            self.snake.move_right()

                        if event.key == K_UP:  # x remains same y changes
                            self.snake.move_up()  # since I want my snake to move up when up is pressed

                        if event.key == K_DOWN:
                            self.snake.move_down()

                elif event.type == QUIT:
                    running = False

            try:

                if not pause:
                    self.play()

            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset() # to begin the game again not from where the game got over

            time.sleep(.2)  # intoduced since while loop runs very fast so snake will move fast hence we need time delay


if __name__ == '__main__':
    game = Game()
    game.run()






