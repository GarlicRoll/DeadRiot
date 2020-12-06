'''
Created on 9 мая 2020 г.

@author: Gleb
'''
import pygame

from menubutton import Menu, Button
from upgrades import UpgradeButton

from json import dump

class MainMenu(Menu):
    #основное меню
    def __init__(self, x, y, filename, parent):
        super(MainMenu, self).__init__(x, y, filename, parent)
        
        self.difficulties = [self.parent.texts[self.parent.language]["ButtonDifficultyEasy"], self.parent.texts[self.parent.language]["ButtonDifficultyNormal"], self.parent.texts[self.parent.language]["ButtonDifficultyHard"]]
        #self.add_buttons()
        
    def add_buttons(self):
        #добавление кнопок
        super(MainMenu, self).add_buttons()
        
        self.change_difficulty_button = Button(self.rect.x + self.rect.w//2 - self.offsetx,self.rect.y + self.offsety*4, self.normal, self.hover, self.pressed, self)
        self.change_difficulty_button.set_text(self.parent.texts[self.parent.language]["ButtonDifficultyNormal"])
        
        self.change_screen_mode_button = Button(self.rect.x + self.rect.w//2 - self.offsetx,self.rect.y + self.offsety*5, self.normal, self.hover, self.pressed, self)
        self.change_screen_mode_button.set_text(self.parent.texts[self.parent.language]["ButtonFullScreen"])
        
        self.change_language_button = Button(self.rect.x + self.rect.w//2 - self.offsetx,self.rect.y + self.offsety*6, self.normal, self.hover, self.pressed, self)
        self.change_language_button.set_text(self.parent.texts[self.parent.language]["ButtonLanguage"])
        
        self.story_button = Button(self.rect.x + self.rect.w//2 - self.offsetx//2 - self.offsetx,self.rect.y + self.offsety*2, self.normal, self.hover, self.pressed, self)
        self.story_button.set_text(self.parent.texts[self.parent.language]["ButtonStory"])
        
        self.arena_button = Button(self.rect.x + self.rect.w//2 + self.offsetx//2 - self.offsetx,self.rect.y + self.offsety*2, self.normal, self.hover, self.pressed, self)
        self.arena_button.set_text(self.parent.texts[self.parent.language]["ButtonArena"])
        
        self.credits_button = Button(self.rect.x + self.rect.w//2 - self.offsetx,self.rect.y + self.offsety*7, self.normal, self.hover, self.pressed, self)
        self.credits_button.set_text(self.parent.texts[self.parent.language]["ButtonCredits"])
        
        self.exit_button = Button(self.rect.x + self.rect.w//2 - self.offsetx,self.rect.y + self.offsety*9, self.normal, self.hover, self.pressed, self)
        self.exit_button.set_text(self.parent.texts[self.parent.language]["ButtonExit"])
        
        
    def render(self, screen):
        #отрисовка меню
        super(MainMenu, self).render(screen)
        self.change_difficulty_button.render(screen)
        self.change_screen_mode_button.render(screen)
        self.change_language_button.render(screen)
        self.arena_button.render(screen)
        self.story_button.render(screen)
        self.credits_button.render(screen)
        self.exit_button.render(screen)
        
        if self.exit_button.up:
            self.parent.running = False
        
        if self.story_button.up:
            self.story_button.up = False
            pygame.mouse.set_visible(False) #курсор скроется
            self.parent.story = True
            self.parent.new_game()
            self.activate()
        
        if self.arena_button.up:
            self.arena_button.up = False
            pygame.mouse.set_visible(False) #курсор скроется
            self.parent.story = False
            self.parent.new_game()
            self.activate()
        
        if self.change_difficulty_button.up:
            #self.change_difficulty_button.up = False
            self.up = False
            if self.parent.difficulty == 2:
                self.parent.difficulty = 0
            else:
                self.parent.difficulty += 1
            self.change_difficulty_button.set_text(self.difficulties[self.parent.difficulty])
            
            if self.parent.difficulty == 2 or self.parent.difficulty == 1: k = 2
            else: k = 0.25
            for mob in range(len(self.parent.types["Mob"])):
                self.parent.types["Mob"][mob]["HP"]  *= k
                self.parent.types["Mob"][mob]["Damage"] *= k
        
        if self.change_screen_mode_button.up:
            self.change_screen_mode_button.up = False
            if self.parent.fullScreen:
                self.parent.fullScreen = False
                self.parent.set_window_screen()
                self.change_screen_mode_button.set_text(self.parent.texts[self.parent.language]["ButtonWindowScreen"])
            else:
                self.parent.fullScreen = True
                self.parent.set_full_screen()
                self.change_screen_mode_button.set_text(self.parent.texts[self.parent.language]["ButtonFullScreen"])
        
        if self.change_language_button.up:
            self.up = False
            
            if self.parent.language == "English":
                self.parent.language = "Russian"
                self.change_language_button.set_text(self.parent.texts[self.parent.language]["ButtonRussian"])

                
                text = open("language.json", "w")
                language = {"Language":"Russian"}
                dump(language, text)
                text.close()
            else:
                self.parent.language = "English"
                self.change_language_button.set_text(self.parent.texts[self.parent.language]["ButtonEnglish"])
                
                text = open("language.json", "w")
                language = {"Language":"English"}
                dump(language, text)
                text.close()
        
        if self.credits_button.up:
            self.up = False
            
            if self.parent.creditsOn:
                self.parent.creditsOn = False
            else:
                self.parent.creditsOn = True
            
        
        
class SideMenu(Menu):
    #побочное меню
    def __init__(self, x, y, filename, parent):
        super(SideMenu, self).__init__(x, y, filename, parent)
        
        
    def add_buttons(self):
        #добавление кнопок
        super(SideMenu, self).add_buttons()
        
        self.upgrades_button = Button(self.rect.x + self.rect.w//2,self.rect.y + self.offsety*5, self.normal, self.hover, self.pressed, self)
        self.upgrades_button.set_text(self.parent.texts[self.parent.language]["ButtonUpgrades"])
        
        self.heal_button = UpgradeButton(self.rect.x + self.rect.w//2,self.rect.y + self.offsety*4, self.normal, self.hover, self.pressed, self, points = 30)
        self.heal_button.set_text(self.parent.texts[self.parent.language]["ButtonHeal"])
        
        self.main_menu_button = Button(self.rect.x + self.rect.w//2,self.rect.y + self.offsety*3, self.normal, self.hover, self.pressed, self)
        self.main_menu_button.set_text(self.parent.texts[self.parent.language]["ButtonMainMenu"])
        
        self.new_game_button = Button(self.rect.x + self.rect.w//2,self.rect.y + self.offsety*2, self.normal, self.hover, self.pressed, self)
        self.new_game_button.set_text(self.parent.texts[self.parent.language]["ButtonNewGame"])
        
        self.exit_button = Button(self.rect.x + self.rect.w//2,self.rect.y + self.offsety*6, self.normal, self.hover, self.pressed, self)
        self.exit_button.set_text(self.parent.texts[self.parent.language]["ButtonExit"])
        
        
    def render(self, screen):
        #отрисовка меню
        super(SideMenu, self).render(screen)
        self.upgrades_button.render(screen)
        self.heal_button.render(screen)
        self.main_menu_button.render(screen)
        self.new_game_button.render(screen)
        self.exit_button.render(screen)
        
        if self.exit_button.up:
            self.parent.running = False
        
        if self.heal_button.up:
            #self.heal_button.up = False
            self.up = False
            if self.parent.player.points >= self.heal_button.points and not self.parent.stop and self.parent.player.hp != self.parent.player.HP:
                self.parent.player.points -= self.heal_button.points
                self.parent.player.hp = self.parent.player.HP
        
        if self.upgrades_button.up:
            self.upgrades_button.up = False
            self.parent.upgradesMenu.activate()
            self.activate()
            
        if self.main_menu_button.up:
            self.main_menu_button.up = False
            self.parent.mainMenu.up = False
            self.parent.battle_music.stop()
            self.parent.game_channel.pause()
            self.parent.menu_music.play(-1)
            self.parent.mainMenu.activate()
            self.activate()
        
        if self.new_game_button.up:
            self.new_game_button.up = False
            pygame.mouse.set_visible(False) #курсор скроется
            self.parent.new_game()
            self.activate()
            
            
            
            
        
