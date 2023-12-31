import pygame, sys, math
from random import randint
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
pygame.init()

global client_list
global master_dict
client_list=[]
master_dict={}

s = socket(AF_INET, SOCK_STREAM)
print("socket created")
port = 9999
s.bind(('192.168.250.85', port))


def accept_client_connections():
    while True:
        i = len(client_list)
        client, client_address = s.accept()
        print("%s:%s has connected" % client_address)
        client_list.append([f"client{i}", client])
        if i==0:
            Thread(target=client1_handler, args=(client,)).start()
        elif i==1:
            Thread(target=client2_handler, args=(client,)).start()

        #Thread(target=client_handler, args=(client,)).start()

def client1_handler(client1):
    global sensor1
    global data
    global connect1
    connect1 = pygame.image.load('Images\\connected.png').convert_alpha()
    sensor1='orientation sensor'
    while True:

        try:
            data= eval(client1.recv(1024).decode())[sensor1]
            print(data)



        except Exception as e:
            pass
def client2_handler(client2):
    global data2
    global sensor2
    global connect2
    connect2 = pygame.image.load('Images\\connected.png').convert_alpha()
    sensor2='rotation vector'

    while True:

        try:
            data2 = eval(client2.recv(1024).decode())[sensor2]
            #print("data from client 2 is" ,data)
        except Exception as e:
            pass

class Player (pygame.sprite.Sprite):
     def __init__(self,pos):
        super().__init__()
        ship_list=['ship1','ship2','ship3','ship4','ship5']
        self.image=pygame.image.load(f'Images\\{ship_list[randint(0,4)]}.png').convert_alpha()
        self.rect=self.image.get_rect(center=pos)
        self.ready = True
        self.laser_time = 0
        self.laser_cooldown = 1000

        self.lasers = pygame.sprite.Group()
        self.laser_sound = pygame.mixer.Sound('audio\\laser.mp3')
        self.laser_sound.set_volume(0.1)
    
     def player_input(self,x,y):
        Keys=pygame.key.get_pressed()
        self.rect.x -= x


        if y<35:
            if self.ready==True:
                self.laser_shoot()
                self.ready = False
                self.laser_time = pygame.time.get_ticks()
                self.laser_sound.play()
    
     def recharge(self):
        if not self.ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_time >= self.laser_cooldown:
                self.ready = True
    
     def laser_shoot(self):
        self.lasers.add(Laser(self.rect.center,-8))

     def mov_const(self):
        if self.rect.right>=1400: self.rect.right=1400
        if self.rect.left<=0: self.rect.left=0

     def mov_forward(self):
        global game_event
        global player_event
        start_val = int(pygame.time.get_ticks() / 1000)
        if self.rect.top <= 0:
            game_event=2
            player_event = 2
        self.rect.y -= math.sin(start_val)
        if start_val >= 10 and start_val <= 12:
            self.rect.top -= 0.6
        elif start_val >= 22 and start_val <= 22.5:
            self.rect.top += 0.6
        elif start_val >= 34 and start_val <= 35:
            self.rect.top -= 0.6
        
         

     def update(self,x,y):
        self.mov_forward()
        self.player_input(x,y)
        self.mov_const()
        self.recharge()
        self.lasers.update()
 
class EnemyPlayer(pygame.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        ship_list=['ship1','ship2','ship3','ship4','ship5']
        self.image=pygame.image.load(f'Images\\{ship_list[randint(0,4)]}.png').convert_alpha()
        self.rect=self.image.get_rect(center=pos)
        self.ready = True
        self.laser_time = 0
        self.laser_cooldown = 1000

        self.lasers = pygame.sprite.Group()
        self.laser_sound = pygame.mixer.Sound('audio\\laser.mp3')
        self.laser_sound.set_volume(0.1)
    
    def player_input(self,x,y):
        Keys = pygame.key.get_pressed()
        self.rect.x -= x

        if y<40:
            if self.ready==True:
                self.laser_shoot()
                self.ready = False
                self.laser_time = pygame.time.get_ticks()
                self.laser_sound.play()
    
    def recharge(self):
        if not self.ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_time >= self.laser_cooldown:
                 self.ready = True
    
    def laser_shoot(self):
        self.lasers.add(Laser(self.rect.center,-12))

    def mov_const(self):
        if self.rect.right>=1400: self.rect.right=1400
        if self.rect.left<=0: self.rect.left=0

    def update(self,x,y):
        self.player_input(x,y)
        self.mov_const()
        self.recharge()
        self.lasers.update()

class Laser(pygame.sprite.Sprite): 
	def __init__(self,pos,speed):
		super().__init__()
		self.image = pygame.Surface((7,10))
		self.image.fill('green')
		self.rect = self.image.get_rect(center = pos)
		self.speed = speed
		self.height_y_constraint = 750

	def destroy(self):
		if self.rect.y <= -50 or self.rect.y >= self.height_y_constraint + 50:
			self.kill()

	def update(self):
		self.rect.y += self.speed
		self.destroy()

class asteroid(pygame.sprite.Sprite):
    def __init__(self):
        asteroid_index=randint(0,2)
        aster_list=['asteroid1','asteroid2','asteroid3']
        aster=aster_list[asteroid_index]
        super().__init__()
        self.image=pygame.image.load(f'Images\\{aster}.png')
        self.rect = self.image.get_rect(midbottom = (randint(200,1400),0))

    def update(self,spx,spy):
        self.rect.x -= spx
        self.rect.y += spy
        self.destroy()
    
    def destroy(self):
        if self.rect.x <= -100: 
             self.kill()    
        if self.rect.y >= 900:
             self.kill()

class Garbage(pygame.sprite.Sprite):
    def __init__(self):
        garbage_index=randint(0,3)
        garbage_list=['banana','paper','trash','Metal']
        garbage=garbage_list[garbage_index]
        super().__init__()
        self.image=pygame.image.load(f'Images\\{garbage}.png')
        self.rect = self.image.get_rect(midbottom = (randint(200,1400),0))

    def update(self,spx,spy):
        self.rect.x -= spx
        self.rect.y += spy
        self.destroy()
    
    def destroy(self):
        if self.rect.x <= -100: 
             self.kill()    
        if self.rect.y >= 900:
             self.kill()
    
    def collide(self):
        if self.rect.colliderect(Laser.rect):
            print ('gg')
				

class Game:
    def __init__(self):
        global lasers_g1
        global lasers_g2
        global score1
        global score2
        self.player1_ship=Player((300,500))
        self.playermp=pygame.sprite.GroupSingle(self.player1_ship)
        self.player2_ship=EnemyPlayer((1000,700))
        self.playerep=pygame.sprite.GroupSingle(self.player2_ship)
        lasers_g1 = self.player1_ship.lasers
        lasers_g2 = self.player2_ship.lasers
        score1=0
        score2=0


    def run_ep(self,x1,x2,y1,y2):
        global game_event
        global player_event
        global score1
        global score2
        self.playermp.update(x1,y1)
        self.playermp.draw(Main_surf)
        self.playermp.sprite.lasers.draw(Main_surf)
        self.playerep.update(x2,y2)
        self.playerep.draw(Main_surf)
        self.playerep.sprite.lasers.draw(Main_surf)

        colid_laser1=pygame.sprite.spritecollide(self.playermp.sprite, lasers_g2,dokill=False)

        collided1 = pygame.sprite.spritecollide(self.playermp.sprite, asteroid2, dokill=False)
        collided2 = pygame.sprite.spritecollide(self.playermp.sprite, garbage, dokill=False)
        collided3 = pygame.sprite.spritecollide(self.playerep.sprite, asteroid2, dokill=False)
        collided4 = pygame.sprite.spritecollide(self.playerep.sprite,garbage,dokill=False)
        if collided1:
            game_event=2
            player_event = 2
        if collided3:
            game_event = 2
            player_event = 1
        for i in garbage.sprites():
            if pygame.sprite.spritecollide(i, lasers_g1, dokill=True):
                garbage.remove(i)
                score1+=1
            if pygame.sprite.spritecollide(i, lasers_g2,dokill=True):
                garbage.remove(i)
                score2+=1
        if collided2:
            count1 = 1
            if count1 == 0.5:
                game_event = 2
                player_event = 1
            count1 -= 0.5
        if collided4:
            count2 = 1
            if count2 == 0.5:
                game_event = 2
                player_event = 2
            count2 -= 0.5
        if colid_laser1:
            print("collison is working")
            game_event=2
            player_event = 2


def initFunction():

    global Main_surf
    global logo
    global asteroid1
    global asteroid2
    global garbage
    global connect1
    global connect2
    global game_event
    global player_event
    Main_surf = pygame.display.set_mode((1400, 750))

    pygame.display.set_caption('Elysium')
    logo = pygame.image.load('Images\\logo.png')
    pygame.display.set_icon(logo)
    font_20 = pygame.font.Font('pixel.ttf', 20)
    font_40 = pygame.font.Font('pixel.ttf', 40)
    font_60 = pygame.font.Font('pixel.ttf', 60)
    bg_music0 = 0
    bg_music1 = 0
    bg_music2 = 0
    clock = pygame.time.Clock()
    start_time = 0
    game_event = 0
    player_event = 0
    intro_load = 1
    game = Game()

    if intro_load == 1:
        intro_scrn = pygame.image.load('Images\\Space Background 1.png').convert_alpha()
        intro_x1 = 1400
        intro_x2 = 0
        intro_msg_1 = font_20.render('Dog in a Box Studio presents:', False, 'Green')
        intro_msg_rect1 = intro_msg_1.get_rect(center=(700, 50))
        intro_msg_2 = font_60.render('ELYSIUM', False, 'blue')
        intro_msg_rect2 = intro_msg_2.get_rect(center=(700, 150))
        Start_button = font_40.render('press space to begin', False, (255, 0, 100))
        Start_button_rect = Start_button.get_rect(center=(700, 400))
        ship_list=['ship1','ship2','ship3','ship4','ship5']
        spaceship_show = pygame.image.load(f'Images\\{ship_list[randint(0,4)]}.png').convert_alpha()
        connect1 = pygame.image.load('Images\\disconnect.png').convert_alpha()
        connect1_rect = connect1.get_rect(center=(300, 600))
        connect1_text = font_20.render('Connection 1', False, 'Green')
        connect1_text_rect = connect1_text.get_rect(center=(300, 700))

        connect2 = pygame.image.load('Images\\disconnect.png').convert_alpha()
        connect2_rect = connect2.get_rect(center=(1100, 600))
        connect2_text = font_20.render('Connection 2', False, 'Green')
        connect2_text_rect = connect1_text.get_rect(center=(1100, 700))


    asteroid1 = pygame.sprite.Group()
    asteroid2 = pygame.sprite.Group()
    garbage = pygame.sprite.Group()
    astrid_timer = pygame.USEREVENT + 1
    pygame.time.set_timer(astrid_timer, randint(500, 2500))
    garbage_timer = pygame.USEREVENT + 1
    pygame.time.set_timer(garbage_timer, randint(4000, 5000))

    # playing screen1 setup
    scrn1 = pygame.image.load('Images\\Space Background 2.png').convert_alpha()
    intro_y1 = -750
    intro_y2 = 0

    #gameover screen
    game_over_text=font_40.render('GAME OVER', False, 'White')
    game_over_text_rect=game_over_text.get_rect(center=(700,500))
    player_wins = font_60.render('PLAYER WINS', False, 'White')
    player_wins_rect = player_wins.get_rect(center=(700, 400))
    enemy_wins = font_60.render('ENEMY WINS', False, 'White')
    enemy_wins_rect = enemy_wins.get_rect(center=(700, 400))

    def timer_disp():
        timer = int(pygame.time.get_ticks() / 1000) - start_time
        timer_msg = font_20.render(f'Timer:{timer}', False, 'Green')
        timer_msg_rect = timer_msg.get_rect(bottomleft=(100, 50))
        Main_surf.blit(timer_msg, timer_msg_rect)

    def score_disp():
        Player_Score_msg = font_20.render(f'Player Score: {score1}', False, 'Blue')
        Player_Score_msg_rect = Player_Score_msg.get_rect(bottomleft=(500, 50))
        Main_surf.blit(Player_Score_msg, Player_Score_msg_rect)
        Enemy_Score_msg = font_20.render(f'Enemy Score: {score2}', False, 'red')
        Enemy_Score_msg_rect = Player_Score_msg.get_rect(bottomleft=(1000, 50))
        Main_surf.blit(Enemy_Score_msg, Enemy_Score_msg_rect)
    
    def final_score():
        Player_Score_msg = font_20.render(f'Player Score: {score1}', False, 'Blue')
        Player_Score_msg_rect = Player_Score_msg.get_rect(bottomleft=(300, 100))
        Main_surf.blit(Player_Score_msg, Player_Score_msg_rect)
        Enemy_Score_msg = font_20.render(f'Enemy Score: {score2}', False, 'red')
        Enemy_Score_msg_rect = Player_Score_msg.get_rect(bottomleft=(850, 100))
        Main_surf.blit(Enemy_Score_msg, Enemy_Score_msg_rect)
        Player_instruct_msg = font_20.render('Press Space to Begin Again', False, 'Blue')
        Player_instruct_msg_rect = Player_Score_msg.get_rect(center=(550, 600))
        Main_surf.blit(Player_instruct_msg, Player_instruct_msg_rect)


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if game_event == 0:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    game_event = 1
                    start_time = int(pygame.time.get_ticks() / 1000)
                if event.type == astrid_timer:
                    asteroid1.add(asteroid())

            elif game_event == 1:
                if event.type == astrid_timer:
                    asteroid2.add(asteroid())
                if event.type == garbage_timer:
                    garbage.add(Garbage())

            elif game_event == 2:
                global score1
                global score2
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    asteroid2.remove(asteroid2.sprites())
                    garbage.remove(garbage.sprites())
                    lasers_g1.remove(lasers_g1.sprites())
                    lasers_g2.remove(lasers_g2.sprites())
                    game_event = 1
                    start_time = int(pygame.time.get_ticks() / 1000)
                    score1=0
                    score2=0
                    bg_music1 = 0
                    bg_music2 = 0
                    bg_music_play2.fadeout(200)




        if game_event == 0:
            # background animations
            Main_surf.blit(intro_scrn, (intro_x1, 0))
            Main_surf.blit(intro_scrn, (intro_x2, 0))
            intro_x1 -= 1
            intro_x2 -= 1
            if intro_x1 < 0: intro_x1 = 1400
            if intro_x2 < -1400: intro_x2 = 0
            asteroid1.draw(Main_surf)
            asteroid1.update(2, 2)
            Main_surf.blit(intro_msg_1, intro_msg_rect1)
            Main_surf.blit(intro_msg_2, intro_msg_rect2)
            pygame.draw.rect(Main_surf, (255, 0, 100), Start_button_rect, 2)
            Main_surf.blit(Start_button, Start_button_rect)
            Main_surf.blit(connect1, connect1_rect)
            Main_surf.blit(connect2, connect2_rect)
            Main_surf.blit(connect1_text, connect1_text_rect)
            Main_surf.blit(connect2_text, connect2_text_rect)
            if bg_music0 == 0:
                bg_music_play0 = pygame.mixer.Sound('audio\\music.mp3')
                bg_music_play0.play(loops=-1)
                bg_music0 += 1

            # spaceship move weird animation
            x_sine = pygame.time.get_ticks() / 5 % 1400
            y_sine = int(math.sin(x_sine / 50.0) * 50 + 400)
            Main_surf.blit(spaceship_show, (x_sine, y_sine))

        elif game_event == 1:

            # background animation for level1
            Main_surf.blit(scrn1, (0, intro_y1))
            Main_surf.blit(scrn1, (0, intro_y2))
            intro_y1 += 1
            intro_y2 += 1
            if intro_y1 > 750: intro_y1 = -750
            if intro_y2 > 750: intro_y2 = -750
            if bg_music1 == 0:
                bg_music_play1 = pygame.mixer.Sound('audio\\level_1.mp3')
                bg_music_play0.fadeout(200)
                bg_music_play1.play(loops=-1)
                bg_music1 += 1

            asteroid2.draw(Main_surf)
            asteroid2.update(0, 3)
            garbage.draw(Main_surf)
            garbage.update(0, randint(0, 3))

            x1 = (data[1]+12)*0.25
            x2 = (data2[1]-8)*0.3
            y1=data[2]
            y2=data2[2]
            timer_disp()
            score_disp()
            game.run_ep(x1, x2,y1,y2)

        elif game_event==2:

            Main_surf.fill('black')
            if player_event == 2:
                Main_surf.blit(enemy_wins, enemy_wins_rect)
                Main_surf.blit(game_over_text,game_over_text_rect)
            elif player_event == 1:
                Main_surf.blit(player_wins, player_wins_rect)
                Main_surf.blit(game_over_text,game_over_text_rect)
            if bg_music2==0:
                bg_music_play2 = pygame.mixer.Sound('audio\\game_over.mp3')
                bg_music_play1.fadeout(200)
                bg_music_play2.play(loops = -1)
                bg_music2+=1
            final_score()

        pygame.display.update()
        clock.tick(60)

    
if __name__=='__main__':
    s.listen(5)
    print("Waiting for connection...")
    game_thread = Thread(target=initFunction)
    game_thread.start()
    ACCEPT_THREAD = Thread(target=accept_client_connections)

    ACCEPT_THREAD.start()

    ACCEPT_THREAD.join()
    game_thread.join()

    s.close()