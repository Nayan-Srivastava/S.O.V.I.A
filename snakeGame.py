import pygame
import random
import os
def snakegame():
    pygame.mixer.init()
    pygame.init()
    #colours
    white=(255,255,255)
    red=(255,0,0)
    black=(0,0,0)
    screen_width=900
    screen_height=600
    gameWindow= pygame.display.set_mode((screen_width,screen_height))
    #bacgroung image
    home=pygame.image.load("home.jpg")
    home=pygame.transform.scale(home,(screen_width,screen_height)).convert_alpha()
    bgimg=pygame.image.load("snakebg.jpg")
    bgimg=pygame.transform.scale(bgimg,(screen_width,screen_height)).convert_alpha()
    go=pygame.image.load("gameover.jpg")
    go=pygame.transform.scale(go,(screen_width,screen_height)).convert_alpha()

    pygame.display.set_caption("Snakes by S.O.V.I.A.")

    pygame.display.update()

    font=pygame.font.SysFont(None,55)


    def text_score(text,color,x,y):
        screen_text=font.render(text,True,color)#second argument is antialias
        gameWindow.blit(screen_text,[x,y])
    def plot_snake(gameWindow,color,snk_list,snake_size):
        for x,y in snk_list:

            pygame.draw.rect(gameWindow,color, [x, y, snake_size, snake_size])


    # game loop
    clock=pygame.time.Clock()
    def welcome():
        exit_game=False
        while not exit_game:
            gameWindow.fill(white)
            gameWindow.blit(home,(0,0))
            text_score("Welcome to snake game",white,260,250)
            text_score("Press Space Bar To Play", white, 230, 290)
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    exit_game=True
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_SPACE:
                        pygame.mixer.music.load('bgmusic.mpeg')
                        pygame.mixer.music.play()
                        gameloop()
            pygame.display.update()
            clock.tick(60)
    def gameloop():

        # game specific variable
        exit_game = False
        game_over = False
        snake_x = 45
        snake_y = 55
        velocity_x = 0
        velocity_y = 0
        snake_size = 30
        fps = 40
        food_x = random.randint(20, screen_width / 2)
        food_y = random.randint(20, screen_height / 2)
        score = 0
        init_velocity = 5
        snk_list = []
        snk_length = 1
        #check if highscore file exist
        if(not os.path.exists("highscore.txt")):
            with open("highscore.txt","w") as f:
                f.write("0")

        with open("highscore.txt", "r") as f:
            highsocre = f.read()
        while not exit_game:
            if game_over:
                with open("highscore.txt","w") as f:
                    f.write(str(highsocre))
                gameWindow.fill(white)
                gameWindow.blit(go, (0, 0))

                text_score("Press enter to continue",black,220,550)
                for event in pygame.event.get():

                    if event.type==pygame.QUIT:
                        exit_game=True
                    if event.type==pygame.KEYDOWN:
                        if event.key==pygame.K_RETURN:
                            welcome()
            else:
                for event in pygame.event.get():

                    if event.type==pygame.QUIT:
                        exit_game=True
                    if event.type==pygame.KEYDOWN:
                        if event.key==pygame.K_RIGHT:
                            velocity_x=init_velocity
                            velocity_y=0
                        if event.key==pygame.K_LEFT:
                            velocity_x=-init_velocity
                            velocity_y=0
                        if event.key==pygame.K_UP:
                            velocity_y=-init_velocity
                            velocity_x=0
                        if event.key==pygame.K_DOWN:
                            velocity_y=init_velocity
                            velocity_x=0
                        if event.key==pygame.K_q:#cheat code
                            score+=5
                snake_x+=velocity_x
                snake_y+=velocity_y
                if abs(snake_x-food_x)<10 and abs(snake_y-food_y)<10:

                    score+=10
                    # print("Score:",score *  10)
                    # text_score("Score:"+str(score *  10),red,5,5)
                    food_x = random.randint(20, screen_width / 2)
                    food_y = random.randint(20, screen_height / 2)
                    snk_length+=5
                    if score>int(highsocre):
                        highsocre= score



                gameWindow.fill(white)
                gameWindow.blit(bgimg, (0, 0))

                text_score("Score: " + str(score)+" HighScore: "+str(highsocre), white, 5, 5)
                pygame.draw.rect(gameWindow, red, [food_x, food_y, snake_size, snake_size])
                head=[]
                head.append(snake_x)
                head.append(snake_y)
                snk_list.append(head)
                if len(snk_list)>snk_length:
                    del snk_list[0]
                if head in snk_list[:-1]:#[:-1]return all element of list exclude last one
                    pygame.mixer.music.load('gameover.mpeg')
                    pygame.mixer.music.play()
                    game_over=True
                if snake_x<0 or snake_x>screen_width or snake_y<0 or snake_y>screen_height:
                    pygame.mixer.music.load('gameover.mpeg')
                    pygame.mixer.music.play()
                    game_over=True

                plot_snake(gameWindow,black,snk_list,snake_size)

            pygame.display.update()
            clock.tick(fps)#frame per second
        pygame.quit()
        quit()
    welcome()
