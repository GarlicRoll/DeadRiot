'''
Created on 3 мая 2020 г.

@author: 08k0708
'''
from copy import copy

import pygame

from random import randint, choice

from json import loads, dump

from constants import WINDOW_W, WINDOW_H, SCREEN_W, SCREEN_H, BLOCK_SIZE, VOLUME
from sprite import Sprite
from gravity import Gravity
from menubutton import Menu
from menus import MainMenu, SideMenu
from collideobject import CollideObject
from playerbullet import Player
from animationanimtiontempdelay import Animation, AnimationTemp, Delay
from camera import Camera
from enemywave import Enemy, Wave
from dialogwindow import DialogWindow
from spikes import Spikes
from bossspell import Boss, Spell
from upgrades import Upgrades, UpgradeDamage1
from appInitAnims import initAnims
from triggers import triggers
from createplayer import create_player



class App():
    #управляющий приложением класс
    def __init__(self):
        self.running = True
        self.window = None
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.w_size = (WINDOW_W, WINDOW_H)
        self.s_size = (SCREEN_W, SCREEN_H) 
        self.collide_ent = []
        self.gravity_ent = []
        self.decor_ent_fore = []
        self.decor_ent_back = []
        self.spikes = []
        self.dialog_windows = []
        
        self.texts = []
        text = open("texts.json", "r", encoding = "utf-8")
        self.texts = loads(text.read())
        text.close()
        
        self.upgrades = []
        
        self.fullScreen = True
        self.difficulty = 1
        
        self.mainFont = "gui/font.ttf"
        
        text = open("language.json", "r")
        language = loads(text.read())
        text.close()
        self.language = language["Language"]
        
        self.creditsImage = (pygame.image.load("gui/credits.png"))
        self.creditsOn = False
        
        self.story = False
        self.level = 1
        
        #####
        self.nextWave = False

        self.pause = False
        self.stop = False  
        
        self.enemies = []
        #####
        
        self.dt = 0
    
    def credits(self, screen):
        if self.creditsOn:
            screen.blit(self.creditsImage, (WINDOW_W - self.creditsImage.get_width(), 0, self.creditsImage.get_width(), self.creditsImage.get_height()))
    
    def init_gamepad(self):
        #инициализация одного геймпада
        self.joystick_count = pygame.joystick.get_count()
        if self.joystick_count > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
        
    
    
    def save_game(self):
        #сохрание прогресса игрока
        text = open("save.json", "r")
        save = loads(text.read())
        text.close()
        save["hp"] = self.player.hp
        save["Points"] = self.player.points
        save["Wave"] = self.waves
        upgrades = []
        for upgrade in self.upgrades:
            upgrades.append(upgrade.bought)
        save["Upgrades"] = upgrades

        text = open("save.json", "w")
        dump(save, text)
        text.close()
        
    def next_wave(self):
        #вызов следующей волны        
        self.waves += 1
        
        
        if self.story: #story mode
            self.wave = Wave(5, self)
            self.nextWave = True
            if self.waves == 6:
                self.game_channel.pause()
                self.battle_music.play(-1)
        
        else: #arena mode
            if self.waves > 10:
                self.win()
            elif self.waves > 9:
            
                self.game_channel.pause()
                self.battle_music.play(-1)
                self.newboss.activate()
                self.create_enemy(type = 4, boss = True)

                self.wave = Wave(3, self)
                self.nextWave = True
            else:
                self.nextWave = True
                self.wave = Wave(randint(2, 5), self)
        
            
            #if self.waves % 2 == 0 and self.waves != 12 and self.player.hp > 0: #сохранение
            #self.save_game()
    

    def create_enemy(self, type = None, boss = False, x = None, y = None):
        #создание случайного врага
        if x == None:
            x = randint(20 * BLOCK_SIZE, SCREEN_W - 20 * BLOCK_SIZE)
        if y == None:
            y = SCREEN_H - BLOCK_SIZE

        speed = randint(2, 5)
        if not type:
            if self.waves > 3:
                type = randint(1,3)
            elif self.waves > 1:
                type = randint(1,2)
            elif self.waves == 1:
                type = 1
            '''
            if self.waves >= 7:
                #self.newmobgolem.activate()
                type = randint(0,3)
            elif self.waves >= 5:
                #self.newmobskeleton.activate()
                type = randint(0,2)
            elif self.waves >= 3:
                #self.newmobvampire.activate()
                type = randint(0,1)
            else:
                type = 0
            '''

        if boss:
            enemy = Boss(x, y, copy(self.types["Mob"][type]["Idle_r"]), copy(self.types["Mob"][type]["Idle_l"]), self, speed, copy(self.types["Mob"][type]["HP"]), copy(self.types["Mob"][type]["Damage"]), copy(self.types["Mob"][type]["Points"]))
        else:
            enemy = Enemy(x, y, copy(self.types["Mob"][type]["Idle_r"]), copy(self.types["Mob"][type]["Idle_l"]), self, speed, copy(self.types["Mob"][type]["HP"]), copy(self.types["Mob"][type]["Damage"]), copy(self.types["Mob"][type]["Points"]))
        
        self.enemies.append(enemy)
        
        enemy.set_target(self.player)

        enemy.initSpawn(copy(self.types["Mob"][type]["Anims"]["Anim_spawn"]))
        
        enemy.initAnim(copy(self.types["Mob"][type]["Anim_go_r"]), copy(self.types["Mob"][type]["Anim_go_l"]))
        
        effect = pygame.mixer.Sound("enemy/damage.ogg")
        effect.set_volume(VOLUME)
        enemy.initAttack(copy(self.types["Mob"][type]["Anim_attack_r"]), copy(self.types["Mob"][type]["Anim_attack_l"]), effect)
        
        effect_dead = pygame.mixer.Sound('enemy/dead.ogg')
        effect_dead.set_volume(VOLUME)
        effect_hit = pygame.mixer.Sound("enemy/hit.ogg")
        effect_hit.set_volume(VOLUME)
        enemy.initDead(copy(self.types["Mob"][type]["Anims"]["Anim_death_r"]), copy(self.types["Mob"][type]["Anims"]["Anim_death_l"]), effect_dead, effect_hit)
        
        if boss:
            spell = Spell(0, 0, self.types["Spell"][0]["Idle"], self.types["Spell"][0]["Damage"], self)
            effect = pygame.mixer.Sound(self.types["Spell"][0]["Sound"])
            effect.set_volume(VOLUME)
            spell.initAnim(self.types["Spell"][0]["Anims"]["Anim_r"], self.types["Spell"][0]["Anims"]["Anim_l"], effect)
            enemy.set_spell(spell)
    
    def play_a_different_song(self, songs):
        next_song = choice(songs)
        while next_song == self.currently_playing_song:
            next_song = choice(songs)
        self.currently_playing_song = next_song
        self.game_channel.queue(next_song)

    def new_game(self, wave = 0, load = False):
        #начало новой игры
        #pygame.mouse.set_visible(False) #курсор скроется
        
        self.upgradesMenu.set_button_colors()
        if not load: #обнуление улучшений
            for upgrade in self.upgrades:
                upgrade.bought = False
            
            for caption in self.dialog_windows:
                caption.count = 0
        
            if self.story:
                self.level = 1
                self.map = "level1.txt"
            else:
                self.greeting.activate()
                self.level = 0
                self.map = "map.txt"
            self.create_map(self.map)
        
       
        #self.nextWave = False
        self.waves = wave #счётчик волн
        
        self.creditsOn = False
        self.pause = False
        self.stop = False  
        
        self.menu_music.stop()
        self.battle_music.stop()
        self.end_music.stop()
        self.game_channel.stop()
        
        self.enemies = []
        
        create_player(self)
    
    def load_game(self):
        #загрузка игры с сохранения
        
        text = open("save.json")
        save = loads(text.read())
        text.close()
        
        self.new_game(wave = save["Wave"] - 1, load = True)
        
        upgrades = save["Upgrades"]
        for idUpgrade in range(len(self.upgrades)):
            self.upgrades[idUpgrade].bought = upgrades[idUpgrade]
        
        for upgrade in self.upgrades:
            if upgrade.bought:
                upgrade.bought = False
                upgrade.buy(noLimits = True)

        self.player.hp = save["hp"]
        self.player.points = save["Points"]
        
    def win(self):
        #завершение игры(победа)
        self.textend = pygame.font.Font(self.mainFont,100).render(self.texts[self.language]["Win"], True, (255, 0, 0))
        self.stop = True
        
    def game_over(self):
        #завершение игры(поражение)
        self.textend = pygame.font.Font(self.mainFont,100).render(self.texts[self.language]["GameOver"], True, (255, 0, 0))
        self.stop = True
    
    
    def delete_map(self):
        #удаление карты
        self.collide_ent = []
        self.decor_ent_fore = []
        self.decor_ent_back = []
        self.spikes = []
        
    def create_map(self, map):
        #карта
        
        #newmap = Map()
        
        #newmap.generate()
        
        #newmap.write()
        
        self.delete_map()
        
        text = open(map)
        blocks = ["", "tiles/block.png", "tiles/grass.png", "tiles/stone.png", "tiles/decor1.png", "tiles/tree.png", "tiles/decor2.png", "tiles/decor3.png", "tiles/spikes.png", "tiles/wall.png", "tiles/backwall.png", "tiles/door.png", "tiles/backblock.png", "tiles/roof.png"]
        
        i = 10
        for line in text:
            j = 0
            for block in line:
                if block == " ":
                    continue
                elif block in ("1", "2", "3", "9"):
                    object = CollideObject(BLOCK_SIZE * j, SCREEN_H - BLOCK_SIZE * i, blocks[int(block)])
                    self.collide_ent.append(object)
                elif block in ("4","5","6","7"):
                    decor = Sprite(BLOCK_SIZE * j ,SCREEN_H - BLOCK_SIZE * i, blocks[int(block)])
                    #self.decor_ent_fore.append(decor)
                    self.decor_ent_back.append(decor)
                elif block in ("8"):
                    spikes = Spikes(BLOCK_SIZE * j ,SCREEN_H - BLOCK_SIZE * i, blocks[int(block)], self)
                    self.spikes.append(spikes)
                elif block in ("B"):
                    decor = Sprite(BLOCK_SIZE * j ,SCREEN_H - BLOCK_SIZE * i, blocks[10])
                    self.decor_ent_back.append(decor)
                elif block in ("D"):
                    decor = Sprite(BLOCK_SIZE * j ,SCREEN_H - BLOCK_SIZE * i, blocks[11])
                    self.decor_ent_back.append(decor)
                elif block in ("C"):
                    decor = Sprite(BLOCK_SIZE * j ,SCREEN_H - BLOCK_SIZE * i, blocks[12])
                    self.decor_ent_back.append(decor)
                elif block in ("R"):
                    decor = Sprite(BLOCK_SIZE * j ,SCREEN_H - BLOCK_SIZE * i, blocks[13])
                    self.decor_ent_back.append(decor)
                    
                j += 1 
            i -= 1 #тк генерируем снизу (зеркально)
        text.close()
            
    def set_full_screen(self):
        #полноэкранный режим
        self.window = pygame.display.set_mode(self.w_size, pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)
        
    def set_window_screen(self):
        #оконный режим
        self.window = pygame.display.set_mode(self.w_size)
        
    def on_init(self):
        #инициализация игры
        pygame.init()
        self.init_gamepad()
        self.set_full_screen()
        pygame.display.set_caption('Dead riot') #строчка на панели управления
        pygame.display.set_icon(pygame.image.load("enemy/zombie/idle_r.png")) #иконка
        self.running = True
        
        self.map = "level1.txt" 
        
        self.battle_music = pygame.mixer.Sound("music/battle_music.ogg")
        self.battle_music.set_volume(VOLUME)
        self.end_music = pygame.mixer.Sound("music/end_music.ogg")
        self.menu_music = pygame.mixer.Sound("music/menu_music.ogg")
        self.menu_music.set_volume(VOLUME)
        self.music1 = pygame.mixer.Sound("music/music1.ogg")
        self.music2 = pygame.mixer.Sound("music/music2.ogg")
        self.music3 = pygame.mixer.Sound("music/music3.ogg")
        self.music4 = pygame.mixer.Sound("music/music4.ogg")
        self.music1.set_volume(VOLUME)
        self.music2.set_volume(VOLUME/3)
        self.music3.set_volume(VOLUME*3)
        self.music4.set_volume(VOLUME)
        self.songs = []
        self.songs.append(self.music1)
        self.songs.append(self.music2)
        self.songs.append(self.music3)
        self.songs.append(self.music4)
        self.currently_playing_song = None
        self.SONGEND = pygame.USEREVENT + 1
        self.game_channel = pygame.mixer.Channel(0)
        self.game_channel.set_endevent(self.SONGEND)
        
        self.screen = pygame.Surface(self.s_size)
        self.subscreen = pygame.Surface(self.w_size)

        self.gravity = Gravity(0.1) 
        
        #главное меню
        self.mainMenu = MainMenu(0, 0, "gui/back.png", self)
        self.mainMenu.activate()
        
        
        #self.create_map(self.map)
        
        initAnims(self)
    
        #меню
        self.menu = SideMenu(0, 0, "gui/window.png", self)
        
        
        #вывод диалогового окна
        print(self.texts[self.language]["Msg1.1"])
        self.msg11 = DialogWindow(self.texts[self.language]["Msg1.1"], self, 1)
        self.msg12 = DialogWindow(self.texts[self.language]["Msg1.2"], self, 1)
        self.msg13 = DialogWindow(self.texts[self.language]["Msg1.3"], self, 1)
        self.msg14 = DialogWindow(self.texts[self.language]["Msg1.4"], self, 1)
        self.msg21 = DialogWindow(self.texts[self.language]["Msg2.1"], self, 1)
        self.msg22 = DialogWindow(self.texts[self.language]["Msg2.2"], self, 1)
        self.msg23 = DialogWindow(self.texts[self.language]["Msg2.3"], self, 1)
        self.msg31 = DialogWindow(self.texts[self.language]["Msg3.1"], self, 1)
        self.msg32 = DialogWindow(self.texts[self.language]["Msg3.2"], self, 1)
        self.msg33 = DialogWindow(self.texts[self.language]["Msg3.3"], self, 1)
        self.msg41 = DialogWindow(self.texts[self.language]["Msg4.1"], self, 1)
        self.msg42 = DialogWindow(self.texts[self.language]["Msg4.2"], self, 1)
        self.msg43 = DialogWindow(self.texts[self.language]["Msg4.3"], self, 1)
        self.msg44 = DialogWindow(self.texts[self.language]["Msg4.4"], self, 1)
        self.msg45 = DialogWindow(self.texts[self.language]["Msg4.5"], self, 1)
        '''
        self.newmobvampire = DialogWindow("Beware of bloodsuckers... ", self, 1)
        self.newmobskeleton = DialogWindow("Bones are ringing... ", self, 1)
        self.newmobgolem = DialogWindow("Something big is coming... ", self, 1)
        '''
        self.greeting = DialogWindow(self.texts[self.language]["MsgA1"], self, 1)
        self.newboss = DialogWindow(self.texts[self.language]["MsgA2"], self, 1)
        
        
        #меню улучшений
        self.upgradesMenu = Upgrades(0, 0, "gui/windowWide.png", self)
        
        create_player(self)
        #self.new_game()
        
        self.pause = True
        self.game_channel.pause()
        self.menu_music.play(-1)
        
        #вывод надписи с номером волны
        text = pygame.font.Font(self.mainFont, 100).render(self.texts[self.language]["WaveCaption"] + str(0), True, (150, 150, 0)) #изначальный
        self.waveCaption = Delay(text, 500)
    
    def menu_activation(self):
        pygame.mouse.set_pos([WINDOW_W//2, BLOCK_SIZE*3])
        if not self.mainMenu.working:
            if self.pause:
                self.pause = False
                pygame.mouse.set_visible(False) #курсор скроется
            else:
                self.pause = True
                pygame.mouse.set_visible(True)
                        
            if not self.upgradesMenu.working:
                self.menu.activate()
            else:
                self.upgradesMenu.activate()
                
    def mouse_move(self):
        #движение мыши с помощью джойстика
        x, y = pygame.mouse.get_pos()
            
        y += round(self.joystick.get_axis(1), 1) * 10
        x += round(self.joystick.get_axis(0), 1) * 10
        pygame.mouse.set_pos([x, y])
    
    def keyboard(self, event):
        #клавиатура
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                self.player.left = False
            if event.key == pygame.K_d:
                self.player.right = False
            if event.key == pygame.K_w:
                self.player.up = False
            #if event.key == pygame.K_s:
                #self.player.down = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                self.player.left = True
            if event.key == pygame.K_d:
                self.player.right = True
            if event.key == pygame.K_w:
                self.player.up = True
                
            #if event.key == pygame.K_s:
                #self.player.down = True
            
            if event.key == pygame.K_ESCAPE: #меню
                self.menu_activation()
                        
            if event.key == pygame.K_x: #экстренный выход
                self.running = False
            
            if event.key == pygame.K_SPACE: #стрельба
                self.player.shoot()
            if event.key == pygame.K_h: #не для публичного использования!
                self.player.hp += 50
            if event.key == pygame.K_p: #не для публичного использования!
                self.player.points += 50
        
    def gamepad(self, event):
        #геймпад
        
        if event.type == pygame.JOYHATMOTION: #ходьба
            if self.joystick.get_hat(0)[0] == -1:
                self.player.left = True
            else:
                self.player.left = False
            if self.joystick.get_hat(0)[0] == 1:
                self.player.right = True
            else:
                self.player.right = False

        

        if event.type == pygame.JOYBUTTONDOWN:
            if self.joystick.get_button(9) == 1: #меню
                self.menu_activation()
        
            if self.joystick.get_button(0) == 1: #стрельба
                self.player.shoot()
            
            if self.joystick.get_button(6) == 1: #прыжок
                self.player.up = True
        
        if event.type == pygame.JOYBUTTONUP:
            
            if self.joystick.get_button(6) == 0: #прыжок
                self.player.up = False
            
                
    

        
            
    def on_event(self, event):
        #отслеживание событий
        
        self.keyboard(event)
        if self.joystick_count > 0:
            self.gamepad(event)
        
        if event.type == pygame.QUIT:
            self.running = False
            
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.JOYBUTTONDOWN:
            self.menu.down = True
            self.mainMenu.down = True
            self.upgradesMenu.down = True
            
            self.menu.up = False
            self.mainMenu.up = False
            self.upgradesMenu.up = False
            
        if event.type == pygame.MOUSEBUTTONUP or event.type == pygame.JOYBUTTONUP:
            self.menu.up = True
            self.mainMenu.up = True
            self.upgradesMenu.up = True
    
            
            self.menu.down = False
            self.mainMenu.down = False
            self.upgradesMenu.down = False
        else:
            self.menu.up = False
            self.mainMenu.up = False
            self.upgradesMenu.up = False

        
        if event.type == self.SONGEND:
            print("New song in queue")
            self.play_a_different_song(self.songs)
        
    def on_loop(self):
        #игровые вычисления в цикле    
        if self.joystick_count > 0 and self.pause:
            self.mouse_move()
        
        if not self.stop and not self.pause:
            
            if self.story:
                triggers(self)
            
            self.gravity.force(self.gravity_ent)
            self.player.move(self.collide_ent, self.dt)
            for spikes in self.spikes:
                spikes.collide()
            
            for enemy in self.enemies:
                enemy.move(self.collide_ent, self.dt)
                try:
                    enemy.spell.anim_hit_l.anim(self.dt)
                    enemy.spell.anim_hit_r.anim(self.dt)
                except:
                    pass
                
            if len(self.enemies) == 0:
                if not self.story:
                    self.next_wave()
                elif self.level == 2 and self.waves > 0 and self.waves < 3:
                    self.next_wave()
                elif self.level == 4 and self.waves > 0 and self.waves < 5:
                    self.next_wave()
            
            if self.nextWave:
                if (self.waves == 6 and self.story) or (self.waves == 10 and not self.story):
                    caption = self.texts[self.language]["BossWaveCaption"]
                else:
                    caption = self.texts[self.language]["WaveCaption"] + str(self.waves)
                text = pygame.font.Font(self.mainFont, 100).render(caption, True, (150, 150, 0))
                self.waveCaption = Delay(text, 1000)
                self.waveCaption.working = True
                self.nextWave = False
            
            for caption in self.dialog_windows:
                if caption.textOutput.working:
                    caption.textOutput.anim(self.dt)
                elif caption.delay.working:
                    caption.delay.update(self.dt)
                
                
        if self.waveCaption.working:
            self.waveCaption.update(self.dt)
        
        
    def on_render(self):
        #отрисовка объектов
        #self.draw_background()
        self.screen.fill((0, 20, 100))
        
        
        for spikes in self.spikes: #шипы
            spikes.render(self.screen)
        
        for entity in self.collide_ent: #все объекты взаимодействия
            entity.render(self.screen)
              
            
        for entity in self.decor_ent_back: #объекты декора заднего плана
            entity.render(self.screen)
            
        self.player.render(self.screen) #игрок
        
        for enemy in self.enemies: #враги
            enemy.render(self.screen)
        
        for item in self.player.bullets: #пули
            item.render(self.screen)
        
        for entity in self.decor_ent_fore: #все объекты декора переднего плана
            entity.render(self.screen)
                   
        subscreen = self.screen.subsurface(self.look.update())
        
        for caption in self.dialog_windows:
            caption.render(subscreen)
        
        self.player.render_hp(subscreen)
        
        if self.stop:
            textw = self.textend.get_width()
            texth = self.textend.get_height()
            subscreen.blit(self.textend, (WINDOW_W//2 - textw//2, WINDOW_H//2 - texth//2))
        
        if self.upgradesMenu.working:
            self.upgradesMenu.render(subscreen)
        
        self.player.render_points(subscreen)
        
        if self.waveCaption.working:
            text = pygame.font.Font(self.mainFont,100).render(self.texts[self.language]["WaveCaption"] + str(self.waves), True, (255, 0, 0))
            textw = text.get_width()
            texth = text.get_height()
            subscreen.blit(self.waveCaption.get_sprite(), (WINDOW_W//2 - textw//2, WINDOW_H//2 - texth//2))
            
        if self.mainMenu.working:
            self.mainMenu.render(subscreen)
        if self.menu.working:
            self.menu.render(subscreen)
        
        self.credits(self.screen)
        
        
            
        self.window.blit(subscreen, (0, 0))

        
        pygame.display.flip()
        
    def on_cleanup(self):
        #завершение работы программы
        pygame.quit()
        
    def draw_background(self):
        #отрисовка фона
        self.window.blit(self.screen, (0, 0))
        
    
    def on_execute(self):
        #цикл работы приложения
        if self.on_init() == False:
            self.running = False
            
        while (self.running):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
            self.dt = self.clock.tick(self.fps)
        self.on_cleanup()
        