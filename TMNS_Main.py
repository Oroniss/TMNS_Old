"""
Having another crack at TMNS for when I have some spare time away from home to work on it.
Going to keep the old structure to the classes/code and not try and put any major updates
from the Halfbreed work into the game.

It is all going to reside in a single file though, just for the sake of convenience.

Changelog for version 02

Current progress and changes.

7/10/17: Added the base entity class and started the data dictionary.
8/10/17: Fleshed out Entity, Actor, constructors and dictionaries.
9/10/17: Got entity drawing correctly in draw_map
10/10/17: Started work on the Furnishing class - got most of the basics sorted out.
11/10/17: Finished up the Furnishing class definition.
12/10/17: Added the furnishing related function to the MapLevel class.
12/10/17: Added the furnishing information to checks for LOS, drawing, etc.

Next Steps

Then add some furnishings to the map.

Start work on furnishings.
Add level 2.
Fix up level transition
Get movement up and running properly.
Clear out TODOs

Start version 03

Player stats and damage
Player death
Traps
Complete available functions/scripts

Start version 04

Items
Item functions
Available functions/scripts

Start version 05

Player spells and abilities

Start version 06

Need to define the move types somewhere 0 = walking, 1 = climb, 2 = fly, 3 = phase, 4 = impassible.
"""

import pygame
import pygcurse
import sys
import os
import pickle
import string
import textwrap
import collections
import copy
from TMNS_Levels import *
from TMNS_Data_Dictionaries import *


##################################################################################################################
#                                       Data
##################################################################################################################

# --------------------------------------------------------------------------------------------------------
#                                       Additions to the Color Dictionary
# --------------------------------------------------------------------------------------------------------

def add_new_colors():
    # Grays
    pygcurse.colornames["Stone Wall"] = (48, 48, 48, 255)
    pygcurse.colornames["Stone Floor"] = (192, 192, 192, 255)
    pygcurse.colornames["Stone Floor Fog"] = (142, 142, 142, 255)
    pygcurse.colornames["Steel Gray"] = (54, 100, 139, 255)
    # Blues
    pygcurse.colornames["Water"] = (0, 0, 238, 255)
    pygcurse.colornames["Water Fog"] = (0, 0, 115, 255)
    pygcurse.colornames["Midnight Blue"] = (9, 16, 35, 255)
    pygcurse.colornames["Midnight Blue Fog"] = (4, 8, 17, 255)
    pygcurse.colornames["Ice"] = (135, 206, 250, 255)
    pygcurse.colornames["Ice Fog"] = (85, 156, 200, 255)
    # Browns
    pygcurse.colornames["Wood Brown"] = (138, 54, 15, 255)
    pygcurse.colornames["Red Brown"] = (199, 97, 20, 255)
    pygcurse.colornames["Chitin Brown"] = (205, 175, 149, 255)
    pygcurse.colornames["Fur Brown"] = (205, 133, 63, 255)
    pygcurse.colornames["Leather Brown"] = (139, 71, 38, 255)
    # Greens
    pygcurse.colornames["Putrid Green"] = (173, 255, 47, 255)
    pygcurse.colornames["Scaly Green"] = (105, 139, 105, 255)
    pygcurse.colornames["Goblin Green"] = (189, 183, 107, 255)
    pygcurse.colornames["Forest Green"] = (0, 139, 69, 255)
    # Other
    pygcurse.colornames["Red"] = (255, 0, 0, 255)
    pygcurse.colornames["Black"] = (0, 0, 0, 255)
    pygcurse.colornames["White"] = (255, 255, 255, 255)
    pygcurse.colornames["Magic Purple"] = (148, 0, 211, 255)
    pygcurse.colornames["Red Purple"] = (208, 32, 144, 255)
    pygcurse.colornames["Gold"] = (255, 215, 0, 255)
    pygcurse.colornames["Copper"] = (173, 111, 105, 255)
    pygcurse.colornames["Silver"] = (199, 199, 199, 255)


# --------------------------------------------------------------------------------------------------------
#                                       The basic racial unlock dictionary
# --------------------------------------------------------------------------------------------------------

unlocked_races = {  # Tier  Unlock
    "Human":                   1,
    "Forest Gnome":           10,
    "Halfling":               10,
    "Half-Elf":               10,
    "Half-Orc":               10,
    "High Elf":               10,
    "Hill Dwarf":             10,
    "Mountain Dwarf":         10,
    "Myconid":                10,
    "Warforged":              10,
    "Wood Elf":               10,
    # Tier 2
    "Aasimar":                20,
    "Air Genasi":             20,
    "Dragonkin":              20,
    "Drow":                   20,
    "Duergar":                20,
    "Earth Genasi":           20,
    "Fire Genasi":            20,
    "Svirfneblin":            20,
    "Tiefling":               20,
    "Water Genasi":           20,
    # Tier 3
    "Half-Celestial":         30,
    "Half-Construct":         30,
    "Half-Elemental":         30,
    "Half-Fiend":             30,
    "Half-Dragon":            30}


##################################################################################################################
#                                       Standalone Classes and Functions
##################################################################################################################

# --------------------------------------------------------------------------------------------------------
#                                       Timer Class
#                                       Borrowed extensively from:
# http://roguebasin.roguelikedevelopment.org/index.php?title=A_simple_turn_scheduling_system_--_Python_implementation
# --------------------------------------------------------------------------------------------------------

class Timer(object):
    """
    Class for keeping track of where everything is up to in the game.
    Anything that can "act" gets put in here.
    """

    def __init__(self):

        self.current_time = -1
        self.queue = dict()
        self.current_actors = []

    def insert(self, time, actor):
        """
        Adds an actor into the queue
        :param time: integer - the next time the actor is supposed to act.
        :param actor: an object that implements a get_next_move method and next_move attribute.
        """

        if time < self.current_time:
            interface.add_debug_text("{} added to timer {} at current time {}".format(actor, time, self.current_time))
            return
        elif time == self.current_time:
            self.current_actors.append(actor)
        else:
            self.queue.setdefault(time, []).append(actor)

    def remove(self, actor):
        """
        Pulls something out of the timer
        :param actor: an object that implements get_next_move method and next_move attribute.
        """

        if actor.next_move in self.queue.keys():
            if actor in self.queue[actor.next_move]:
                self.queue[actor.next_move].remove(actor)

        if actor in self.current_actors:
            self.current_actors.remove(actor)

    def run_turn(self):
        """ Runs the next turn in the game. """

        self.current_actors = self.queue.pop(self.current_time, [])
        while self.current_actors:
            actor = self.current_actors.pop(0)
            actor.get_next_move(interface.game.current_level, interface.game.player, self)

        self.current_time += 1


##################################################################################################################
#                                       Interface class
##################################################################################################################

class Interface(object):
    """
    Basically the class that is responsible for holding the game, as well as managing
    the menus and other interface options.
    Also handles the new game setup, etc.
    """

    key_dictionary = {
        # Special Keys
        pygcurse.K_ESCAPE:      "Escape",
        pygcurse.K_DELETE:      "Delete",
        pygcurse.K_BACKSPACE:   "Backspace",
        pygcurse.K_SPACE:       "Space",
        pygcurse.K_RETURN:      "Enter",
        # Direction Keys
        pygcurse.K_LEFT:        "Left",
        pygcurse.K_RIGHT:       "Right",
        pygcurse.K_UP:          "Up",
        pygcurse.K_DOWN:        "Down",
        # Key-pad Keys
        pygcurse.K_KP4:         "Left",
        pygcurse.K_KP6:         "Right",
        pygcurse.K_KP8:         "Up",
        pygcurse.K_KP2:         "Down",
        pygcurse.K_KP7:         "Up_Left",
        pygcurse.K_KP9:         "Up_Right",
        pygcurse.K_KP1:         "Down_Left",
        pygcurse.K_KP3:         "Down_Right",
        # Other Character Keys
        pygcurse.K_PERIOD:      ".",
        pygcurse.K_COMMA:       ",",
        pygcurse.K_MINUS:       "-",
        pygcurse.K_EQUALS:      "=",
        # Number Keys
        pygcurse.K_0:           "0",
        pygcurse.K_1:           "1",
        pygcurse.K_2:           "2",
        pygcurse.K_3:           "3",
        pygcurse.K_4:           "4",
        pygcurse.K_5:           "5",
        pygcurse.K_6:           "6",
        pygcurse.K_7:           "7",
        pygcurse.K_8:           "8",
        pygcurse.K_9:           "9",
        # Letter Keys
        pygcurse.K_a:           "A",
        pygcurse.K_b:           "B",
        pygcurse.K_c:           "C",
        pygcurse.K_d:           "D",
        pygcurse.K_e:           "E",
        pygcurse.K_f:           "F",
        pygcurse.K_g:           "G",
        pygcurse.K_h:           "H",
        pygcurse.K_i:           "I",
        pygcurse.K_j:           "J",
        pygcurse.K_k:           "K",
        pygcurse.K_l:           "L",
        pygcurse.K_m:           "M",
        pygcurse.K_n:           "N",
        pygcurse.K_o:           "O",
        pygcurse.K_p:           "P",
        pygcurse.K_q:           "Q",
        pygcurse.K_r:           "R",
        pygcurse.K_s:           "S",
        pygcurse.K_t:           "T",
        pygcurse.K_u:           "U",
        pygcurse.K_v:           "V",
        pygcurse.K_w:           "W",
        pygcurse.K_x:           "X",
        pygcurse.K_y:           "Y",
        pygcurse.K_z:           "Z"
    }

    def __init__(self, size=0, extra_keys=False, gm_view=False):
        """
        Setup for interface
        :param size: integer 1 - 4, -1 indicates that config is required.
        :param extra_keys: bool - Whether the laptop specific keys should be enabled.
        :param gm_view: bool - Whether the additional gm options should be enabled.
        """

        self.game = None
        self.version_number = "0.02"  # TODO: Keep this up to date

        # Now process the interface specific parameters.
        config = False
        self.extra_keys = extra_keys
        if self.extra_keys:
            Interface.add_extra_keys()
        self.gm_view = gm_view

        if size == 0:
            config = True
            self.size = 1
        else:
            self.size = size

        self.WINDOW_WIDTH = 68 + 10 * self.size
        self.WINDOW_HEIGHT = 40 + 10 * self.size

        # TODO: Setup the character and hot key regions here
        # Map region
        self.MAP_LEFT = 2
        self.MAP_TOP = 2
        self.MAP_WIDTH = 26 + 10 * self.size
        self.MAP_HEIGHT = 26 + 10 * self.size
        self.map_display = (self.MAP_LEFT, self.MAP_TOP, self.MAP_WIDTH, self.MAP_HEIGHT)

        # Status display region
        self.STATUS_LEFT = 2
        self.STATUS_TOP = self.MAP_TOP + self.MAP_HEIGHT + 2
        self.STATUS_WIDTH = self.MAP_WIDTH
        self.STATUS_HEIGHT = self.WINDOW_HEIGHT - self.STATUS_TOP - 2
        self.status_display = (self.STATUS_LEFT, self.STATUS_TOP, self.STATUS_WIDTH, self.STATUS_HEIGHT)

        # Text display region.
        self.TEXT_LEFT = self.MAP_LEFT + self.MAP_WIDTH + 4
        self.TEXT_TOP = 30  # TODO: Come back and check this once the other areas go in.
        self.TEXT_WIDTH = self.WINDOW_WIDTH - self.TEXT_LEFT - 2
        self.TEXT_HEIGHT = self.WINDOW_HEIGHT - self.TEXT_TOP - 2
        self.text_display = (self.TEXT_LEFT, self.TEXT_TOP, self.TEXT_WIDTH, self.TEXT_HEIGHT)

        # Menu region
        self.MENU_LEFT = 2
        self.MENU_TOP = 2
        self.MENU_WIDTH = self.WINDOW_WIDTH - 4
        self.MENU_HEIGHT = self.WINDOW_HEIGHT - 4
        self.menu_display = (self.MENU_LEFT, self.MENU_TOP, self.MENU_WIDTH, self.MENU_HEIGHT)

        # GM region
        if self.gm_view:
            self.WINDOW_WIDTH += 30

            self.GM_LEFT = self.WINDOW_WIDTH - 29
            self.GM_TOP = 2
            self.GM_WIDTH = 28
            self.GM_HEIGHT = 32
            self.gm_display = (self.GM_LEFT, self.GM_TOP, self.GM_WIDTH, self.GM_HEIGHT)

            self.DB_LEFT = self.WINDOW_WIDTH - 29
            self.DB_TOP = self.GM_TOP + self.GM_HEIGHT + 2
            self.DB_WIDTH = 28
            self.DB_HEIGHT = self.WINDOW_HEIGHT - self.DB_TOP - 2
            self.db_display = (self.DB_LEFT, self.DB_TOP, self.DB_WIDTH, self.DB_HEIGHT)

            self.debug_messages = [""] * self.DB_HEIGHT

        pygame.init()
        self.window = pygcurse.PygcurseWindow(self.WINDOW_WIDTH, self.WINDOW_HEIGHT, "The Mausoleum of Nightscale",
                                              fgcolor="Black", bgcolor="Black")
        self.window.autoupdate = False

        if config:
            self.run_config()

        self.game_messages = [("", "White")] * self.TEXT_HEIGHT

    # --------------------------------------------------------------------------------------------------------
    #                                       Input functions
    # --------------------------------------------------------------------------------------------------------

    @staticmethod
    def get_next_key():
        """
        Gets the next key press from the user.
        :return - A string representation of the key pressed.
        """

        while True:
            for event in pygame.event.get():
                if event.type == pygcurse.KEYDOWN and event.key in Interface.key_dictionary:
                    return Interface.key_dictionary[event.key]

    def get_confirmation(self, message):
        """
        Gets a yes or no answer from the player.
        Can only be used in the actual game, not from starting menus.
        :param message: Message prompt to seek confirmation over.
        :return: True or False - corresponding to Yes or No
        """

        self.add_output_text("Y or N?", color="Red")
        self.add_output_text(message)

        self.update_game_screen()

        while True:
            key = Interface.get_next_key()
            if key == "Y":
                return True
            elif key == "N":
                return False

    # --------------------------------------------------------------------------------------------------------
    #                                       Message functions
    # --------------------------------------------------------------------------------------------------------

    def add_output_text(self, message, color="White"):
        """
        Adds text to display to the player.
        :param message: string - the text to display
        :param color: string - the color of the text (if not White).
        """

        if message == "":
            if self.game_messages[-1][0] == "":
                return
            else:
                self.game_messages.append(("", "White"))
                return

        # Use text wrap to format them
        processed_message = textwrap.wrap(message, width=self.TEXT_WIDTH)
        # Have to append them in reverse order though
        for line in processed_message[::-1]:
            self.game_messages.append((line, color))

        if len(self.game_messages) > 50:
            self.game_messages = self.game_messages[-50::]

    def add_debug_text(self, message):
        """
        Adds a debug message - writes to gm text as well as the log file.
        :param message: The message to display
        """

        log_file = open(os.path.join(os.getcwd(), "Conf", "TMNS_Log.txt"), mode="a")
        log_file.write("{}, {}, {}, x = {}, y = {}\n".format(self.game.player.name, self.game.character_class,
                                                             self.game.current_level, self.game.player.x_loc,
                                                             self.game.player.y_loc))
        log_file.write(message + "\n")
        log_file.write("\n")
        log_file.close()

        if self.gm_view:
            self.debug_messages.append("")
            processed_message = textwrap.wrap(message, self.DB_WIDTH)
            for line in processed_message[::-1]:
                self.debug_messages.append(line)
            if len(self.debug_messages) > 50:
                self.debug_messages = self.debug_messages[-50::]

    # --------------------------------------------------------------------------------------------------------
    #                                       New game / config functions.
    # --------------------------------------------------------------------------------------------------------

    def main_menu(self):
        """
        Displays the main menu on start-up (unless first time in which case config comes first).
        """

        menu_options = ["New Game", "Load Game", "View Achievements", "Clear Achievements", "View Commands",
                        "View Back-Story", "Config"]

        if self.gm_view:
            menu_options.append("GM Options")

        while True:
            self.window.fill(bgcolor="Silver", region=self.menu_display)

            self.window.write("Welcome to the Mausoleum of Nightscale", x=self.MENU_LEFT + 5, y=self.MENU_TOP + 5,
                              bgcolor="Silver", fgcolor="Black")

            for index, option in enumerate(menu_options):
                self.window.write("{}: {}".format(index + 1, option), x=self.MENU_LEFT + 5,
                                  y=self.MENU_TOP + 10 + 2 * index, bgcolor="Silver", fgcolor="Black")

            self.window.write("Escape to Exit", x=self.MENU_LEFT + 5, y=self.MENU_TOP + 30, bgcolor="Silver",
                              fgcolor="Black")

            self.window.update()

            key = Interface.get_next_key()

            if key == "1":
                self.game = Game(*self.new_game_menus())
                self.game.run_game()
            elif key == "2":
                if self.load_game_menu():
                    self.game.run_game()
            elif key == "3":
                pass
            elif key == "4":
                pass
            elif key == "5":
                self.view_commands()
            elif key == "6":
                self.view_back_story()
            elif key == "7":
                self.run_config()
            elif key == "8" and self.gm_view:
                pass
            elif key == "Escape":
                pygame.quit()
                sys.exit(0)

    def new_game_menus(self):
        """
        Goes through the process of setting up a new game.
        :return: The player object and any gm_options.
        """

        player_name = self.choose_name()
        player_race, unlock_level = self.choose_race()
        player_class = self.choose_character_class()
        player = Player(player_name, player_race, unlock_level, player_class)
        if not self.gm_view:
            return player, None
        else:
            gm_options = self.set_gm_game_options()
            return player, gm_options

    def load_game_menu(self):
        """
        Displays the list of available save games.
        :return: True if one was loaded correctly, False otherwise.
        """

        save_dictionary = read_save_games()
        page_index = 0

        while True:

            self.window.fill(bgcolor="Silver", region=self.menu_display)

            # Case where there are no save games.
            if len(save_dictionary) == 0:

                self.window.write("Sorry, it looks like there are no existing characters", x=self.MENU_LEFT + 10,
                                  y=self.MENU_TOP + 10, bgcolor="Silver", fgcolor="Black")
                self.window.write("Press Escape or F to return", x=self.MENU_LEFT + 10, y=self.MENU_TOP + 12,
                                  bgcolor="Silver", fgcolor="Black")
                self.window.update()
                key = Interface.get_next_key()
                if key == "Escape" or key == "F":
                    return False

            # Case where we have to display some.
            else:
                character_list = sorted(save_dictionary.keys())
                for i in range(page_index * 10, min(len(character_list), (page_index + 1) * 10)):
                    character_details = save_dictionary[character_list[i]]
                    self.window.write("{}: {}, lvl {} {} on {}".format(i % 10 + 1, character_details[0],
                                                                       character_details[2],
                                                                       character_details[1], character_details[3]),
                                      x=self.MENU_LEFT + 5, y=self.MENU_TOP + 10 + 2 * (i % 10),
                                      bgcolor="Silver", fgcolor="Black")

                self.window.update()
                key = Interface.get_next_key()

                character = False
                if key in "123456789":
                    if (int(key)) <= i + 1:
                        character = character_list[page_index * 10 + int(key) - 1]
                elif key == "0":
                    if i == 9:
                        character = character_list[page_index * 10 + 9]

                if character:
                    success = self.load_game(save_dictionary[character])
                    del save_dictionary[character]
                    update_save_games(save_dictionary)

                    if success:
                        return True
                    else:
                        self.window.write("Something is wrong with that save game sorry", x=self.MENU_LEFT + 5,
                                          y=self.MENU_TOP + 30, bgcolor="Silver", fgcolor="Black")
                        self.window.update()
                        Interface.get_next_key()

                if key == "Escape":
                    return False
                elif key == "Left" and page_index > 0:
                    page_index -= 1
                elif key == "Right" and (page_index + 1) * 10 < len(character_list):
                    page_index += 1

    def view_commands(self):
        """
        Displays the keys and their actions to the user.
        """

        command_tuple = (("Key", "Action"), ("Arrow Keys", "Attack or move in that direction"),
                         ("Numpad Keys", "Attack or move in that direction"),
                         ("A", "Acquire an item on the ground"), ("C", "Display character achievements"),
                         ("D", "Drop and item"), ("E", "Examine an object or location"),
                         ("H", "Setup or clear a hotkey"), ("I", "Use an item"),
                         ("K", "View skills and spend skill points"), ("M", "View minions and allies"),
                         ("P", "Pray at an altar or kneel and pray"), ("R", "Make an attack with a ranged weapon"),
                         ("S", "Cast a spell or use a special ability"), ("T", "Talk or trade with someone"),
                         ("U", "Make use of an object like a level or door"), ("V", "View this list of commands"),
                         ("Period", "Pick up all items on the ground"), ("Space-bar", "Skip current turn"),
                         ("Escape", "Save and quit the game"))

        self.window.fill(bgcolor="Silver", region=self.menu_display)

        for index, val in enumerate(command_tuple):
            self.window.write("{:<14}: {}".format(*val), x=self.MENU_LEFT + 5, y=self.MENU_TOP + 5 + index,
                              bgcolor="Silver", fgcolor="Black")

        if self.extra_keys:
            extra_keys = (("[", "Up and left"), ("]", "Up and right"), (";", "Down and Left"), ("'", "Down and right"))

            for index, val in enumerate(extra_keys):
                self.window.write("{:<14}: {}".format(*val), x=self.MENU_LEFT + 5, y=self.MENU_TOP + 26 + index,
                                  bgcolor="Silver", fgcolor="Black")

        self.window.write("Escape or F to return", x=self.MENU_LEFT + 5, y=self.MENU_TOP + 34,
                          bgcolor="Silver", fgcolor="Black")
        self.window.update()
        while True:
            key = Interface.get_next_key()
            if key == "Escape" or key == "F":
                return

    def view_back_story(self):
        """
        Displays the back-story for the game.
        """

        back_story_part_1 = ["The story begins nearly 2,000 years ago.", "",
                             "In that time, the 20 deities roamed the earth freely.",
                             "They each had their different followers and agendas,",
                             "but mostly they settled their differences peacefully.",
                             "However, eventually the tension became too great,",
                             "and a massive conflict broke out.", "",
                             "On one side were the gods of good lead by Bahamut,",
                             "god of the good dragons.", "",
                             "On the other side were the gods of evil, lead by",
                             "Tiamat, goddess of the evil dragons.", "",
                             "After years of war it became clear that if the",
                             "conflict continued, the world itself would not survive.", "",
                             "Thus, a truce was brokered. To prevent the war from",
                             "ever restarting, the gods came together and cast",
                             "a mighty spell which bound each deity away in their",
                             "own plane. So powerful was this spell that only all",
                             "20 gods acting together could undo it.",
                             "They agreed that from this point forward they would",
                             "influence the world through their mortal followers.", "",
                             "At first this plan worked well.",
                             "While there were battles between the mortal followers",
                             "of the gods, the destruction was much less.", "",
                             "However, none of the other gods had counted on the",
                             "cunning of Tiamat.", "",
                             "While her mortal followers were few in number, they",
                             "were mighty in power. One in particular, Xar'Noxulus",
                             "or Nightscale in the common tongue, an ancient and",
                             "evil shadow dragon was so powerful in the ways of",
                             "magic that he hatched a plan to deliver the world",
                             "solely unto Tiamat."]

        back_story_part_2 = ["Nightscale constructed a vast mausoleum, ostensibly",
                             "to honour both himself and his goddess.", "",
                             "However, in the very depths of the mausoleum, he",
                             "sacrificed himself in a terrible ritual. The power",
                             "unleashed was so great, it weakened the boundary",
                             "between the mortal world and the plane where Tiamat",
                             "was contained.", "",
                             "Then, over the years, as they neared death, the",
                             "other followers of Tiamat came to the site when",
                             "their lives were ending and added their souls to",
                             "the ritual which still raged in the depths of the",
                             "mausoleum.", "",
                             "This continued for centuries, unbeknown to the",
                             "other deities.", "",
                             "It was only recently that they realised their peril",
                             "when they felt the fabric of the planes beginning",
                             "to tear open. However, the mighty spell cast by",
                             "the gods could not be broken if even one refused",
                             "to end it, and Tiamat gleefully rejected their",
                             "pleas, knowing that her domination of the mortal",
                             "world was near to hand.", "",
                             "This left the other gods no choice but to work",
                             "through their mortal agents.", "",
                             "Desperate, they each sent their champions to the",
                             "Mausoleum of Nightscale and tasked them with",
                             "descending into the depths to find and stop the",
                             "ritual.", "",
                             "You have been given as much power as your deity",
                             "can provide. The rest is up to you.", "",
                             "The future of the mortal world depends",
                             "on your success."]

        self.window.fill(bgcolor="Silver", region=self.menu_display)

        for ln, line in enumerate(back_story_part_1):
            self.window.write(line, x=self.MENU_LEFT + 5, y=self.MENU_TOP + 3 + ln,
                              bgcolor="Silver", fgcolor="Black")

        self.window.write("Press Enter to continue", x=self.MENU_LEFT + 5, y=self.MENU_TOP + 44,
                          bgcolor="Silver", fgcolor="Black")

        self.window.update()

        while True:
            key = Interface.get_next_key()
            if key == "Enter":
                break

        self.window.fill(bgcolor="Silver", region=self.menu_display)

        for ln, line in enumerate(back_story_part_2):
            self.window.write(line, x=self.MENU_LEFT + 5, y=self.MENU_TOP + 3 + ln,
                              bgcolor="Silver", fgcolor="Black")

        self.window.write("Press Enter to continue", x=self.MENU_LEFT + 5, y=self.MENU_TOP + 44,
                          bgcolor="Silver", fgcolor="Black")

        self.window.update()

        while True:
            key = Interface.get_next_key()
            if key == "Enter":
                return

    def run_config(self):
        """
        Runs the initial configuration for the game.
        Note that the size changes don't take effect until next startup.
        """

        while True:
            self.window.fill(bgcolor="Silver", region=self.menu_display)

            self.window.write("Mausoleum of Nightscale Configuration", x=self.MENU_LEFT + 5,
                              y=self.MENU_TOP + 5, bgcolor="Silver", fgcolor="Black")
            self.window.write("Please select your screen size:", x=self.MENU_LEFT + 5, y=self.MENU_TOP + 10,
                              bgcolor="Silver", fgcolor="Black")
            for i in range(1, 5):
                self.window.write("{}: Size {} X {}".format(i, 70 + 10 * i, 40 + 10 * i), x=self.MENU_LEFT + 5,
                                  y=self.MENU_TOP + 11 + 2 * i, bgcolor="Silver", fgcolor="Black")

            extra_keys = "Off"
            if self.extra_keys:
                extra_keys = "On"
            self.window.write("X: Toggle laptop keys. Currently {}".format(extra_keys), x=self.MENU_LEFT + 5,
                              y=self.MENU_TOP + 25, bgcolor="Silver", fgcolor="Black")
            self.window.write("Escape or F to save configuration and exit", x=self.MENU_LEFT + 5,
                              y=self.MENU_TOP + 30, bgcolor="Silver", fgcolor="Black")

            self.window.update()

            key = Interface.get_next_key()
            if key == "1":
                self.size = 1
            elif key == "2":
                self.size = 2
            elif key == "3":
                self.size = 3
            elif key == "4":
                self.size = 4
            elif key == "X":
                if self.extra_keys:
                    self.extra_keys = False
                    Interface.remove_extra_keys()
                else:
                    self.extra_keys = True
                    Interface.add_extra_keys()
            elif key == "Escape" or key == "F":
                config_file = open(os.path.join(os.getcwd(), "Conf", "config.tmns"), mode="wb")
                pickle.dump((self.size, self.extra_keys, self.gm_view), config_file)
                config_file.close()
                return

    def choose_name(self, save_dictionary=None):
        """
        Gets the player to choose a name for their character.
        :param save_dictionary: The current save dictionary - used to check the name isn't taken
        :return: The player's name
        """

        if save_dictionary is None:
            save_dictionary = read_save_games()

        allowed_chars = list(string.ascii_uppercase)
        name = ""

        while True:
            self.window.fill(bgcolor="Silver", region=self.menu_display)

            self.window.write("What is your name: {}".format(name), x=self.MENU_LEFT + 5, y=self.MENU_TOP + 5,
                              bgcolor="Silver", fgcolor="Black")
            self.window.write("Enter to finish, Escape to quit", x=self.MENU_LEFT + 5, y=self.MENU_TOP + 10,
                              bgcolor="Silver", fgcolor="Black")
            self.window.update()

            key = Interface.get_next_key()

            if key == "Delete" or key == "Backspace":
                if len(name) > 0:
                    name = name[0:-1]
            elif key == "Escape":
                pygame.quit()
                sys.exit(0)
            elif key == "Enter":
                if len(name) - name.count(" ") < 4:
                    self.window.write("Names must be at least 4 letters long", x=self.MENU_LEFT + 5,
                                      y=self.MENU_TOP + 8, bgcolor="Silver", fgcolor="Red")
                    self.window.update()
                    Interface.get_next_key()
                elif name in save_dictionary:
                    self.window.write("That name is already taken", x=self.MENU_LEFT + 5,
                                      y=self.MENU_TOP + 8, bgcolor="Silver", fgcolor="Red")
                    self.window.update()
                    Interface.get_next_key()
                else:
                    return name

            elif key == "Space":
                name += " "
            elif key in allowed_chars:
                if len(name) < 20:
                    name += key
                    name = name.title()
                else:
                    self.window.write("Names can be at most 20 characters long", x=self.MENU_LEFT + 5,
                                      y=self.MENU_TOP + 8, bgcolor="Silver", fgcolor="Red")
                    self.window.update()
                    Interface.get_next_key()
            else:
                self.window.write("Names can only contain letters and spaces", x=self.MENU_LEFT + 5,
                                  y=self.MENU_TOP + 8, bgcolor="Silver", fgcolor="Red")
                self.window.update()
                Interface.get_next_key()

    def choose_race(self, racial_dictionary=None):
        """
        Selects a race from the available options.
        :param racial_dictionary: A dictionary of available races, along with the level they are unlocked at.
        :return: (string, int) - The chosen race and unlock level.
        """

        if racial_dictionary is None:
            racial_dictionary = read_unlocked_races()

        options = [list(), list(), list(), list()]
        for key, val in racial_dictionary.items():
            options[val // 10].append((key, val))

        for option_list in options:
            option_list.sort()

        selected_tier = -1
        while True:
            self.window.fill(bgcolor="Silver", region=self.menu_display)
            self.window.write("What is your race?", x=self.MENU_LEFT + 5, y=self.MENU_TOP + 5,
                              bgcolor="Silver", fgcolor="Black")
            self.window.write("Backspace to deselect a tier, Escape to quit", x=self.MENU_LEFT + 5,
                              y=self.MENU_TOP + 35, bgcolor="Silver", fgcolor="Black")

            for tier in range(len(options)):
                if selected_tier != -1 and tier != selected_tier:
                    continue

                self.window.write("Tier {}".format(tier + 1), x=self.MENU_LEFT + 2 + 18 * tier,
                                  y=self.MENU_TOP + 10, bgcolor="Silver", fgcolor="Black")

                for i in range(len(options[tier])):
                    fgcolor = "Red"
                    if options[tier][i][1] % 10 > 0:
                        fgcolor = "Black"
                    self.window.write("{}: {}".format((i+1) % 10, options[tier][i][0]),
                                      x=self.MENU_LEFT + 2 + 18 * tier,
                                      y=self.MENU_TOP + 13 + 2 * i, bgcolor="Silver", fgcolor=fgcolor)

            self.window.update()
            key = Interface.get_next_key()
            if key == "Escape":
                pygame.quit()
                sys.exit(0)
            elif selected_tier == -1 and key in "1234":
                selected_tier = int(key) - 1
            elif selected_tier != -1 and key == "Backspace":
                selected_tier = -1
            elif selected_tier != -1 and key in "1234567890":
                choice = int(key) - 1
                if choice < 0:
                    choice += 10
                if choice < len(options[selected_tier]) and options[selected_tier][choice][1] % 10 > 0:
                    return options[selected_tier][choice]

    def choose_character_class(self):
        """
        Picks a character class for a new character.
        :return: The string name of the character class
        """

        options = ["Fighter", "Magic-User", "Thief", "Bard", "Paladin", "Ranger"]
        keys = "123456"
        if self.gm_view:
            options.append("GM")
            keys += "7"

        self.window.fill(bgcolor="Silver", region=self.menu_display)
        self.window.write("What is your calling?", x=self.MENU_LEFT + 5, y=self.MENU_TOP + 5,
                          bgcolor="Silver", fgcolor="Black")

        for index, char_class in enumerate(options):
            self.window.write("{}: {}".format(index + 1, char_class), x=self.MENU_LEFT + 5,
                              y=self.MENU_TOP + 8 + 2 * index, bgcolor="Silver", fgcolor="Black")

        self.window.update()
        while True:
            key = Interface.get_next_key()

            if key in keys:
                return options[int(key) - 1]
            elif key == "Escape":
                pygame.quit()
                sys.exit(0)

    def set_gm_game_options(self):
        """
        For now just returns the starting location, but in the future could add additional aspects.
        For example auto-levelling, adding equipment, etc.
        :return: (level_name, x_loc, y_loc)
        """

        starting_loc = (("Standard", "Level1a", 24, 54), ("Dragon", "Level1a", 7, 7),
                        ("Kobold Sorcerer", "Level1a", 45, 4), ("Kobold Ranger", "Level1a", 10, 12))

        # TODO: Think about what else could go in here.
        self.window.fill(bgcolor="Silver", region=self.menu_display)
        self.window.write("Select starting location", x=self.MENU_LEFT + 5, y=self.MENU_TOP + 5,
                          bgcolor="Silver", fgcolor="Black")
        for i in range(len(starting_loc)):
            self.window.write("{}: Level = {}, location = {}".format(i+1, starting_loc[i][1], starting_loc[i][0]),
                              x=self.MENU_LEFT + 5, y=self.MENU_TOP + 10 + 2 * i, bgcolor="Silver", fgcolor="Black")
        self.window.update()
        while True:
            key = Interface.get_next_key()

            if key in "1234567890"[0:len(starting_loc)]:
                return starting_loc[int(key)-1][1::]
            elif key == "Escape":
                pygame.quit()
                sys.exit(0)

    def save_game(self):  # Character Name, character class, character level, dungeon level, time.
        """
        Saves the state of the current game, and then exits.
        """

        # Update the summary save dictionary
        save_dict = read_save_games()
        save_dict[self.game.player.name] = (self.game.player.name, self.game.player.character_class,
                                            self.game.player.character_level, self.game.current_level.level_title,
                                            self.game.timer.current_time)
        update_save_games(save_dict)

        # Insert the player back into the timer and anything left in the current actors back into the queue.
        self.game.timer.current_actors.insert(0, self.game.player)
        self.game.timer.queue[self.game.timer.current_time] = self.game.timer.current_actors

        # TODO: Make sure any clean up that needs to happen before this is maintained.
        # TODO: Store the version number somewhere along with updating entity ID class attributes.
        # Create the actual save file
        file_name = self.game.player.name.replace(" ", "_")
        save_file = open(os.path.join(os.getcwd(), "Saves", file_name), mode="wb")
        pickle.dump(self.game, save_file)
        save_file.close()

    def load_game(self, character_details):
        """
        Loads up the game corresponding to the character details selected.
        :param character_details: A tuple of (Name, C_Class, C_Level, Dungeon_level, time).
        :return: True if loaded successfully, False otherwise.
        """

        # TODO: Need to verify the game version number and write a function to update accordingly.

        file_name = character_details[0].replace(" ", "_")
        if not os.path.exists(os.path.join(os.getcwd(), "Saves", file_name)):
            return False

        try:
            save_file = open(os.path.join(os.getcwd(), "Saves", file_name), mode="rb")
            game = pickle.load(save_file)
            save_file.close()
            os.remove(os.path.join(os.getcwd(), "Saves", file_name))

            # Now validate the save file
            if (game.player.name != character_details[0] or game.player.character_class != character_details[1] or
                game.player.character_level != character_details[2] or
                    game.current_level.level_title != character_details[3] or
                    game.timer.current_time != character_details[4]):
                return False

            self.game = game
            return True

        except (AttributeError, NameError, ValueError, IOError, EOFError):
            # Mostly here to catch malformed game object, which doesn't have the correct attributes, etc.
            return False

    @staticmethod
    def add_extra_keys():
        """ Adds the extra laptop keys to the key dictionary. """
        Interface.key_dictionary[pygcurse.K_SEMICOLON] = "Down_Left"
        Interface.key_dictionary[pygcurse.K_QUOTE] = "Down_Right"
        Interface.key_dictionary[pygcurse.K_LEFTBRACKET] = "Up_Left"
        Interface.key_dictionary[pygcurse.K_RIGHTBRACKET] = "Up_Right"

    @staticmethod
    def remove_extra_keys():
        """ Removes the extra laptop keys from the key dictionary. """
        if pygcurse.K_SEMICOLON in Interface.key_dictionary:
            del Interface.key_dictionary[pygcurse.K_SEMICOLON]
        if pygcurse.K_QUOTE in Interface.key_dictionary:
            del Interface.key_dictionary[pygcurse.K_QUOTE]
        if pygcurse.K_LEFTBRACKET in Interface.key_dictionary:
            del Interface.key_dictionary[pygcurse.K_LEFTBRACKET]
        if pygcurse.K_RIGHTBRACKET in Interface.key_dictionary:
            del Interface.key_dictionary[pygcurse.K_RIGHTBRACKET]

    # --------------------------------------------------------------------------------------------------------
    #                                       Display functions
    # --------------------------------------------------------------------------------------------------------

    def draw_map(self, level=None, x_centre=None, y_centre=None, visible_tiles=None):
        """
        Draws the provided map to the screen. Default is the current level centred on the player.
        :param level: integer array of tiles.
        :param x_centre: x_coordinate to centre on (only used if map is wider than display).
        :param y_centre: y_coordinate to centre on (only used if map is taller than display).
        :param visible_tiles: Set of tiles that the player can see and so should be shown 'lit'
        """

        # Get default parameters if none were supplied
        if level is None:
            level = interface.game.current_level
        if x_centre is None:
            x_centre = interface.game.player.x_loc
        if y_centre is None:
            y_centre = interface.game.player.y_loc
        if visible_tiles is None:
            visible_tiles = interface.game.player.visible_tiles

        # Do some math to determine the limits of what will be displayed
        x_min = 0
        x_max = level.map_width
        x_offset = self.MAP_LEFT

        y_min = 0
        y_max = level.map_height
        y_offset = self.MAP_TOP

        if level.map_width < self.MAP_WIDTH:
            x_offset += (self.MAP_WIDTH - level.map_width) // 2
        elif level.map_width > self.MAP_WIDTH:
            half_width = self.MAP_WIDTH // 2
            if x_centre - half_width < 0:
                x_max = self.MAP_WIDTH
            elif x_centre + half_width > level.map_width:
                x_min = level.map_width - self.MAP_WIDTH
                x_offset -= x_min
            else:
                x_min = x_centre - half_width
                x_max = x_centre + half_width - 1
                x_offset -= x_min

        if level.map_height < self.MAP_HEIGHT:
            y_offset += (self.MAP_HEIGHT - level.map_height) // 2
            y_max = level.map_height
        elif level.map_height > self.MAP_HEIGHT:
            half_height = self.MAP_HEIGHT // 2
            if y_centre - half_height < 0:
                y_max = self.MAP_HEIGHT
            elif y_centre + half_height > level.map_height:
                y_min = level.map_height - self.MAP_HEIGHT
                y_offset -= y_min
            else:
                y_min = y_centre - half_height
                y_max = y_centre + half_height - 1
                y_offset -= y_min

        self.window.fill(bgcolor="Black", region=self.map_display)

        # Draw the actual map.
        for y in range(y_min, y_max):
            for x in range(x_min, x_max):
                if not level.is_revealed(x, y):
                    self.window.putchar(" ", x=x + x_offset, y=y + y_offset, bgcolor="Black")
                elif (x, y) not in visible_tiles:
                    self.window.putchar(" ", x=x + x_offset, y=y + y_offset, bgcolor=level.get_bgcolor(x, y, False))
                else:
                    entity_details = level.get_drawing_entity_details(x, y)  # Gets False or (symbol, fgcolor)
                    if not entity_details:
                        self.window.putchar(" ", x=x + x_offset, y=y + y_offset, bgcolor=level.get_bgcolor(x, y, True))
                    else:
                        self.window.putchar(entity_details[0], x=x + x_offset, y=y + y_offset,
                                            bgcolor=level.get_bgcolor(x, y, True), fgcolor=entity_details[1])

        self.window.update()

    # TODO: Implement
    def draw_status(self):
        pass

    # TODO: Implement
    def draw_character(self):
        pass

    # TODO: Implement
    def draw_hot_keys(self):
        pass

    def draw_output_text(self):
        """
        Draws the player messages to the screen.
        """

        self.window.fill(bgcolor="Black", region=self.text_display)

        self.window.write("Message Log", x=self.TEXT_LEFT + self.TEXT_WIDTH // 2 - 6, y=self.TEXT_TOP + 1,
                          bgcolor="Black", fgcolor="White")
        for index, (message, color) in enumerate(self.game_messages[-1:-self.TEXT_HEIGHT - 4:-1]):
            self.window.write(message, x=self.TEXT_LEFT + 2, y=self.TEXT_TOP + 3 + index,
                              bgcolor="Black", fgcolor=color)
        self.window.update()

    # TODO: Implement
    def draw_gm_view(self):
        pass

    def draw_db_log(self):
        """
        Draws the debug log if gm_view is set.
        """

        self.window.fill(bgcolor="Black", region=self.db_display)

        self.window.write("Error Log", x=self.DB_LEFT + self.DB_WIDTH // 2 - 6, y=self.DB_TOP + 1,
                          bgcolor="Black", fgcolor="White")
        for index, message in enumerate(self.debug_messages[-1:-self.DB_HEIGHT - 4:-1]):
            self.window.write(message, x=self.DB_LEFT + 2, y=self.DB_TOP + 3 + index,
                              bgcolor="Black", fgcolor="White")
        self.window.update()

    def update_game_screen(self):
        """
        Draws all the standard areas - if non-default parameters are required, the individual functions should
        be used instead.
        """

        self.window.fill(bgcolor="black")

        self.draw_map()
        self.draw_status()
        self.draw_character()
        self.draw_hot_keys()
        self.draw_output_text()

        if self.gm_view:
            self.draw_gm_view()
            self.draw_db_log()


##################################################################################################################
#                                       Entity class definition
##################################################################################################################

class Entity(object):
    """
    Basic class for anything that shows up in the game - Actors, Items and Furnishings.
    Likely to end up being fairly slim
    """

    entity_id = 0

    def __init__(self, entity_name):
        """
        Basic setup for an entity.
        :param entity_name: string - self explanatory.
        """

        self.entity_id = Entity.entity_id
        Entity.entity_id += 1

        self.entity_class = "Entity"  # If we ever encounter this in game, we know something has gone wrong.

        self.entity_name = entity_name
        self.description = ""
        self.x_loc = None
        self.y_loc = None
        self.destroyed = False
        self.traits = collections.Counter()

        # Controls non-standard behaviour - on_destruction, on is_attacked, etc. Attack related ones elsewhere.
        self.functions = []
        self.effects = []

        # Lookup everything else in the data dictionary.
        self.symbol = " "
        self.fgcolor = "Black"
        self.current_hp = 1
        self.max_hp = 1

        # Simple attributes
        self.visibility = 0
        self.player_spotted = True

        # Defensive stats - Set in the derived classes
        self.armor_class = 10
        self.damage_reduction = 0
        self.hardness = 0
        self.spell_resist = 0
        self.acid_res = 0
        self.cold_res = 0
        self.elec_res = 0
        self.fire_res = 0
        self.necr_res = 0

        # Saving throws aren't here for all derived classes - since many objects just auto-fail them.
        # There is a make_save method on this class though.

    # TODO: Think through what arguments this should take
    def process_damage(self, damage_amount, damage_type, attack, attacker):
        pass

    def saving_throw(self, save_type, save_dc):
        pass

    # TODO: Think through what arguments this should take
    def destroy(self, attack):
        pass

    def __str__(self):
        pass

    def recalculate_statistics(self, reason="None"):
        pass

    def has_trait(self, trait):
        """
        Checks whether the entity has the given trait or not.
        :param trait: string - trait
        :return: True if the entity has the trait, False if not.
        """

        return self.traits[trait] > 0

    def add_trait(self, trait):
        """
        Adds the given trait to the entity.
        :param trait: string - the trait in question.
        """

        self.traits[trait] += 1

    def remove_trait(self, trait):
        """
        Removes one instance of the trait from the entity
        :param trait: string - the trait in question.
        """

        if self.traits[trait] <= 0:
            interface.add_debug_text("Tried to remove trait {} from entity {} but not present.".format(trait, self))
            return

        self.traits[trait] -= 1

    def apply_effect(self, effect):
        pass

    def remove_effect(self, effect):
        pass


##################################################################################################################
#                                       Furnishing class definition
##################################################################################################################

class Furnishing(Entity):
    """
    Class for anything that is basically a map object. Also includes as derived classes:
    Traps, Fountains, Containers, Altars, Doors and anything with movement or interaction triggers.
    """

    def __init__(self, entity_name, material=None):
        """
        Standard setup for an entity.
        :param entity_name:
        """

        Entity.__init__(self, entity_name)

        details = furnishing_details[entity_name]

        self.symbol = details[0]
        self.block_los = details[1]
        self.block_move = details[2]
        self.safe_move = details[3]
        self.volume = details[4]  # A measure of how big the object is - basically determines hp

        self.bgcolor = details[5]
        self.fogcolor = details[6]

        if material is None:
            self.material = details[7]  # This should drive a lot of the defensive stats.
        else:
            self.material = material

        # Any functions related to triggers or usage.
        self.functions = []
        for furnishing_function in furnishing_functions[self.entity_name]:
            self.functions.append(furnishing_function)

        # Properties set by material.
        self.armor_class = material_properties[self.material][0]
        self.damage_reduction = material_properties[self.material][1]
        self.hardness = material_properties[self.material][2]
        self.spell_resist = material_properties[self.material][3]
        self.acid_res = material_properties[self.material][4]
        self.cold_res = material_properties[self.material][5]
        self.elec_res = material_properties[self.material][6]
        self.fire_res = material_properties[self.material][7]
        self.necr_res = material_properties[self.material][8]

        self.current_hp = material_properties[self.material][9] * self.volume
        self.max_hp = self.current_hp

        self.fgcolor = material_properties[self.material][10]
        self.description = ""  # TODO: Add something to do with the material adjective here.

        for trait in material_properties[self.material][12]:
            self.add_trait(trait)

        # Saves not set by design - they are auto fails anyway.

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def make_saving_throw(self, save_type, dc):
        """ Auto fails all saves, but is immune to a lot of things that might require them. """
        return "Fail"


##################################################################################################################
#                                       Actor class definition
##################################################################################################################

class Actor(Entity):
    """
    Subclass of entity - has two derived classes of its own, Player and Monster.
    """

    def __init__(self, entity_name):
        """
        Standard creation script for an Actor - just looks up things from the appropriate dictionary.
        :param entity_name: string - entity name
        """

        Entity.__init__(self, entity_name)

        # Now set the Entity attributes
        self.entity_class = "Actor"

        details = actor_details[entity_name]

        # Actor details
        self.symbol = details[0]
        self.fgcolor = details[1]
        self.alignment = details[2]
        self.subject_object = details[3]
        self.possessive = details[4]
        self.character_level = details[5]
        self.view_distance = details[6]
        self.visibility = details[7]
        if self.visibility < 0:
            self.player_spotted = False

        stats = actor_stats[entity_name]

        # Actor stats
        self.strength = stats[0]
        self.intelligence = stats[1]
        self.wisdom = stats[2]
        self.dexterity = stats[3]
        self.constitution = stats[4]
        self.move_level = stats[5]
        self.move_speed = stats[6]
        self.fort = stats[7]
        self.refl = stats[8]
        self.will = stats[9]
        self.current_hp = stats[10]  # TODO: Fix this to a random when dice go in.
        self.max_hp = self.current_hp
        # self.next_move = interface.game.timer.current_time + 1  # TODO: Put some randomness here too.

        defenses = actor_defenses[entity_name]

        # Actor defenses
        self.armor_class = defenses[0]
        self.damage_reduction = copy.copy(defenses[1])
        self.hardness = defenses[2]
        self.spell_resist = defenses[3]
        self.acid_res = defenses[4]
        self.cold_res = defenses[5]
        self.elec_res = defenses[6]
        self.fire_res = defenses[7]
        self.necr_res = defenses[8]

        # Add any traits that apply
        for trait in actor_traits[entity_name]:
            self.add_trait(trait)

    def get_next_move(self, level, player, timer):
        pass

    # TODO: Think through the arguments here
    def move(self):
        pass


##################################################################################################################
#                                       Player class definition
##################################################################################################################

# TODO: This needs to inherit from Actor eventually
class Player(Actor):
    """
    Pretty self explanatory - an extension of the Actor class, which represents the player character
    """

    def __init__(self, name, race="Human", unlock_level=1, character_class="Fighter"):
        """
        This is going to get really messy eventually.
        :param name: String - the player's name
        :param race: String - the player's race
        :param character_class: String - the player's character class
        """

        Actor.__init__(self, "Player")

        self.name = name
        self.race = race
        self.character_class = character_class

        self.next_move = 0
        self.visible_tiles = set()

        # TODO: Setup the base values for the derived stats.
        # TODO: Apply the racial modifiers.
        if unlock_level > 1:
            pass

    # noinspection PyUnusedLocal
    def get_next_move(self, level, player, timer):
        """
        Takes an action
        :param level - The current level object
        :param player - The player object
        :param timer - The timer object running the game - so can insert back in if need be.
        """

        interface.add_output_text("")

        # Update what the player can see.
        self.visible_tiles = level.get_field_of_view(self.x_loc, self.y_loc, self.view_distance)

        for tile in self.visible_tiles:
            level.reveal_tile(*tile)

        while True:
            interface.update_game_screen()
            key = Interface.get_next_key()
            x_dif = 0
            y_dif = 0
            move = False
            if key == "Escape":
                if interface.get_confirmation("Really quit?"):
                    if interface.get_confirmation("Save current game?"):
                        interface.save_game()
                    pygame.quit()
                    sys.exit(0)
            elif key == "Up":
                y_dif = -1
                move = True
            elif key == "Down":
                y_dif = 1
                move = True
            elif key == "Left":
                x_dif = -1
                move = True
            elif key == "Right":
                x_dif = 1
                move = True
            elif key == "V":
                interface.view_commands()
                interface.update_game_screen()

            # TODO: If still here, update when move types go in
            if move:
                if (level.is_valid_map_coord(self.x_loc + x_dif, self.y_loc + y_dif) and
                        level.is_passible(self.x_loc + x_dif, self.y_loc + y_dif)):

                    level.remove_actor(self)

                    self.x_loc += x_dif
                    self.y_loc += y_dif

                    level.add_actor(self)

                    self.next_move += 10

                    timer.insert(self.next_move, self)
                    break

                else:
                    interface.add_output_text("You can't move there!", color="Red")


##################################################################################################################
#                                       MapLevel class definition
##################################################################################################################

class MapLevel(object):
    """
    Basic building block of the game experience.
    """

    # Dictionary of tiles
    tile_dict = {  # Tile       bgcolor         fogcolor            description     allowLOS    minMove
        0:      ("wall",        "Stone Wall",   "Stone Wall",       "a wall",       False,      3),
        1:      ("floor",       "Stone Floor",  "Stone Floor Fog",  "",             True,       0),
        3:      ("space",       "Midnight Blue", "Midnight Blue Fog", "a long drop", True,      2)}

    # Translation tables for the FOV and LOS calculations
    #
    #       0   3
    #   1           2
    #   6           5
    #       7   4
    #
    octant_translate = (
        (1, 0,  0,  -1, -1, 0,  0,  1),
        (0, 1,  -1, 0,  0,  -1, 1,  0),
        (0, 1,  1,  0,  0,  -1, -1, 0),
        (1, 0,  0,  1,  -1, 0,  0,  -1)
    )

    def __init__(self, level_name):
        """
        Creates the level by lookup - currently from imported sub-module
        :param level_name: A string description of the level
        """

        # Setup the common storage
        self.furnishing_ids = dict()
        self.furnishing_locations = dict()
        self.item_ids = dict()
        self.item_locations = collections.defaultdict(list)
        self.actors_ids = dict()
        self.actors_locations = dict()

        # Get the level specific stuff
        level_details = LEVEL_DETAILS[level_name]

        self.level_name = level_name

        self.level_title = level_details[0]
        self.map_height = level_details[2]
        self.map_width = level_details[3]
        self.challenge_rating = level_details[4]
        self.light_modifier = level_details[5]
        self.level_number = level_details[6]
        self.level_denotation = level_details[7]  # Main, side or sub
        self.updates_statistics = level_details[8]  # Whether the "levels visited" should be incremented.
        self.entry_text = level_details[9::]

        self.map_grid = LEVEL_MAPS[level_name]
        # noinspection PyUnusedLocal
        self.revealed = [[False] * len(self.map_grid[0]) for i in self.map_grid]

        # TODO: Get all the other objects here

    # --------------------------------------------------------------------------------------------------------
    #                                       Information functions
    # --------------------------------------------------------------------------------------------------------

    def is_valid_map_coord(self, x_loc, y_loc):
        """
        Checks whether a particular coordinate is actually valid for the map.
        :param x_loc: The x coordinate - integer
        :param y_loc: The y coordinate - integer
        :return: True if it is valid, False otherwise
        """

        return (0 <= x_loc < self.map_width) and (0 <= y_loc < self.map_height)

    def is_passible(self, x_loc, y_loc, move_type=0):
        """
        Checks whether the tile is passible given the best move type
        :param x_loc: integer - the x coordinate
        :param y_loc: integer - the y coordinate
        :param move_type: integer - the best available move type
        :return: True if the square is passible, False otherwise
        """

        # TODO: Test this is working ok
        if not self.is_valid_map_coord(x_loc, y_loc):
            interface.add_debug_text("Checked passible for non-existent map coordinate, x = {}, y = {}".format(
                x_loc, y_loc))
            return False

        if (x_loc, y_loc) in self.actors_locations:
            return False

        if (x_loc, y_loc) in self.furnishing_locations:
            if move_type < self.furnishing_locations[(x_loc, y_loc)].block_move:
                return False

        return move_type >= MapLevel.tile_dict[self.map_grid[y_loc][x_loc]][5]

    def allow_los(self, x_loc, y_loc):
        """
        Checks whether the specified tile allows visibility or not.
        :param x_loc: integer - the x coordinate
        :param y_loc: integer - the y coordinate
        :return: True if the tile allows visibility, False otherwise
        """

        # TODO: Test this properly.
        if not self.is_valid_map_coord(x_loc, y_loc):
            interface.add_debug_text("Checked los on an invalid coordinate {}, {}, level = {}".format(
                x_loc, y_loc, self.level_name))
            return False

        if (x_loc, y_loc) in self.furnishing_locations and self.furnishing_locations[(x_loc, y_loc)].block_los:
            return False

        return MapLevel.tile_dict[self.map_grid[y_loc][x_loc]][4]

    def get_field_of_view(self, x_loc, y_loc, view_distance):
        """
        Returns a set of (x, y) coordinate pairs that are in the field of view from the coordinate given.

        FOV and light are largely taken from:
        http://www.roguebasin.com/index.php?title=PythonShadowcastingImplementation
        Page current at 16 January 2014

        :param x_loc: integer - the x coordinate
        :param y_loc: integer - the y coordinate
        :param view_distance: integer - how far the viewer can see (in tiles)
        :return: A set of (x, y) coordinate pairs that are visible.
        """

        view_set = set()

        # Go through each of the 8 octants and add the tiles in that direction to the view set
        for octant in range(8):
            self.cast_light(y_loc, x_loc, 1, 1.0, 0.0, view_distance,
                            MapLevel.octant_translate[0][octant], MapLevel.octant_translate[1][octant],
                            MapLevel.octant_translate[2][octant], MapLevel.octant_translate[3][octant], 0, view_set)
        view_set.add((x_loc, y_loc))
        return view_set

    def cast_light(self, y_loc, x_loc, row, start, end, view_distance, xx, xy, yx, yy, recursion_number, view_set):
        """

        :param y_loc: integer - the y coordinate
        :param x_loc: integer - the x coordinate
        :param row: how many rows up from the horizontal we are currently scanning
        :param start: gradient of the start point (usually 1.0 but can be less in child scans if there were blockages)
        :param end: gradient of the end point (usually 0.0, but as above)
        :param view_distance: The distance in tiles that the viewer can see.
        :param xx: octant translate of xx
        :param xy: octant translate of xy
        :param yx: octant translate of yx
        :param yy: octant translate of yy
        :param recursion_number: Number of levels into the child scans we are
        :param view_set: Currently found lit tiles
        :return: None - Function updates the provided view set as a side effect
        """

        # Since it's defined recursively, end if initial conditions aren't met.
        if start < end:
            return

        view_distance_squared = view_distance * view_distance
        new_start = start

        # Loop through the tiles in the current row
        for j in range(row, view_distance + 1):

            dx, dy = -j-1, -j
            blocked = False

            # Look at the tile in the next row
            while dx <= 0:
                dx += 1
                # Translate into map coordinates
                map_x, map_y = x_loc + dx * xx + dy * xy, y_loc + dx * yx + dy * yy

                # l_slope and r_slope are the slopes at the left and right
                # extremities of the square we are considering
                l_slope, r_slope = (dx - 0.5) / (dy + 0.5), (dx + 0.5) / (dy - 0.5)

                if start <= r_slope:
                    continue
                elif end >= l_slope:
                    break
                else:
                    # We can see this square
                    if dx * dx + dy * dy < view_distance_squared and self.is_valid_map_coord(map_x, map_y):
                        view_set.add((map_x, map_y))
                    if blocked:
                        # We are scanning blocked squares
                        if not self.is_valid_map_coord(map_x, map_y) or not self.allow_los(map_x, map_y):
                            new_start = r_slope
                            continue
                        else:
                            blocked = False
                            start = new_start
                    else:
                        if ((not self.is_valid_map_coord(map_x, map_y) or not self.allow_los(map_x, map_y))
                                and j <= view_distance):
                            # Start a child scan
                            blocked = True
                            self.cast_light(y_loc, x_loc, j + 1, start, l_slope, view_distance, xx, xy, yx, yy,
                                            recursion_number + 1, view_set)
                            new_start = r_slope

            # Row is scanned, do next row unless last tile is blocked
            if blocked:
                break

    def get_adjacent_tiles(self, x_loc, y_loc, centre=False):
        """
        Gets a list of valid tiles adjacent to the specified location
        :param x_loc: integer - The x coordinate
        :param y_loc: integer - The y coordinate
        :param centre: whether the specified tile should be included.
        :return: a list of (x, y) tuple tiles coordinates.
        """

        tile_list = []

        for y in (-1, 0, 1):
            for x in (-1, 0, 1):
                if self.is_valid_map_coord(x_loc + x, y_loc + y) and (x != 0 or y != 0 or centre):
                    tile_list.append((x_loc + x, y_loc + y))

        return tile_list

    def get_bgcolor(self, x_loc, y_loc, in_view):
        """
        Checks the map to get the tile type that is present.
        :param x_loc: The x coordinate - integer
        :param y_loc: The y coordinate - integer
        :param in_view: Whether the location is in sight or not - determines whether to pull bg or fog color.
        :return: The color of the background
        """

        if not self.is_valid_map_coord(x_loc, y_loc):
            interface.add_debug_text("Tried to draw tile at {}, {} on level {} but it doesn't exist".format(
                x_loc, y_loc, self))
            return "Black"

        if in_view:  # bgcolor
            if ((x_loc, y_loc) in self.furnishing_locations and
                    self.furnishing_locations[(x_loc, y_loc)].bgcolor is not None):
                return self.furnishing_locations[(x_loc, y_loc)].bgcolor
            return MapLevel.tile_dict[self.map_grid[y_loc][x_loc]][1]
        else:  # fogcolor
            if ((x_loc, y_loc) in self.furnishing_locations and
                    self.furnishing_locations[(x_loc, y_loc)].fogcolor is not None):
                return self.furnishing_locations[(x_loc, y_loc)].fogcolor
            return MapLevel.tile_dict[self.map_grid[y_loc][x_loc]][2]

    def get_drawing_entity_details(self, x_loc, y_loc):
        """
        Gets the symbol and fgcolor for whatever entity should be on top.
        :param x_loc: integer - the x coordinate
        :param y_loc: integer - the y coordinate
        :return: (symbol, fgcolor) tuple - both elements are strings - returns False if nothing there.
        """

        if not self.is_valid_map_coord(x_loc, y_loc):
            interface.add_debug_text("Looked up drawing for invalid coordinates x = {}, y = {}, lvl = {}").format(
                x_loc, y_loc, self.level_name)
            return False

        # TODO: Update once other entity types go in
        if (x_loc, y_loc) in self.actors_locations and self.actors_locations[(x_loc, y_loc)].fgcolor is not None:
            return self.actors_locations[(x_loc, y_loc)].symbol, self.actors_locations[(x_loc, y_loc)].fgcolor

        elif ((x_loc, y_loc) in self.furnishing_locations and
              self.furnishing_locations[(x_loc, y_loc)].fgcolor is not None):
            return self.furnishing_locations[(x_loc, y_loc)].symbol, self.furnishing_locations[(x_loc, y_loc)].fgcolor

        return False

    def reveal_tile(self, x_loc, y_loc):
        """
        Uncovers the specified tile.
        :param x_loc: integer - the x coordinate
        :param y_loc: integer - the y coordinate
        """

        # TODO: Think about whether these should be done as asserts so they can be skipped.
        if not self.is_valid_map_coord(x_loc, y_loc):
            interface.add_debug_text("Tried to reveal invalid coordinate {}, {} for level {}".format(
                x_loc, y_loc, self.level_name))
            return

        self.revealed[y_loc][x_loc] = True

    def is_revealed(self, x_loc, y_loc):
        """
        Checks whether the specified tile has been revealed or not.
        :param x_loc: integer - the x coordinate
        :param y_loc: integer - the y coordinate
        :return: True if the tile has been revealed, False otherwise
        """

        # TODO: Think about whether these should be done as asserts so they can be skipped.
        if not self.is_valid_map_coord(x_loc, y_loc):
            interface.add_debug_text("Checked reveal of invalid coordinate {}, {} for level {}".format(
                x_loc, y_loc, self.level_name))
            return False

        return self.revealed[y_loc][x_loc]

    # --------------------------------------------------------------------------------------------------------
    #                                       Furnishing functions
    # --------------------------------------------------------------------------------------------------------

    def get_furnishing(self, x_loc, y_loc):
        """
        Gets any furnishing object at the specified location.
        :param x_loc: integer - the x coordinate
        :param y_loc: integer - the y coordinate
        :return: A furnishing object if one is there, or False otherwise.
        """

        if (x_loc, y_loc) in self.furnishing_locations:
            return self.furnishing_locations[(x_loc, y_loc)]
        else:
            return False

    def get_all_furnishings(self):
        """
        Gets all the furnishings on the level
        :return: a list of all furnishing objects on the level.
        """

        return list(self.furnishing_ids.values())

    def add_furnishing(self, furnishing):
        """
        Adds the given furnishing to the level.
        :param furnishing: The furnishing object to add
        """

        if (furnishing.x_loc, furnishing.y_loc) in self.actors_locations:
            interface.add_debug_text("Tried to add a furnishing at {}, {}, but {} already there".format(
                furnishing.x_loc, furnishing.y_loc, self.actors_locations[(furnishing.x_loc,
                                                                           furnishing.y_loc)]))
            return

        self.actors_ids[furnishing.entity_id] = furnishing

        if furnishing.x_loc is None and furnishing.y_loc is None:
            return
        elif (furnishing.x_loc is None or furnishing.y_loc is None or not
              self.is_valid_map_coord(furnishing.x_loc, furnishing.y_loc)):
            interface.add_debug_text("Tried to add a furnishing {} with invalid coordinates {}, {}".format(
                furnishing, furnishing.x_loc, furnishing.y_loc))
            return
        else:
            self.actors_locations[(furnishing.x_loc, furnishing.y_loc)] = furnishing

    def remove_furnishing(self, furnishing):
        """
        Removes the specified furnishing from the level
        :param furnishing: The furnishing object to be removed.
        """

        if furnishing.entity_id not in self.furnishing_ids:
            interface.add_debug_text("Tried to remove furnishing {} with id {} but it wasn't there".format(
                furnishing, furnishing.entity_id))
            return

        del self.furnishing_ids[furnishing.entity_id]

        if furnishing.x_loc is None and furnishing.y_loc is None:
            return

        if ((furnishing.x_loc, furnishing.y_loc) not in self.furnishing_locations or
                self.furnishing_locations[(furnishing.x_loc, furnishing.y_loc)] is not furnishing):
            interface.add_debug_text("Tried to remove furnishing {} from {}, {} but it wasn't there".format(
                furnishing, furnishing.x_loc, furnishing.y_loc))
            return

        del self.furnishing_locations[(furnishing.x_loc, furnishing.y_loc)]

    # --------------------------------------------------------------------------------------------------------
    #                                       Actor functions
    # --------------------------------------------------------------------------------------------------------

    def get_actor(self, x_loc, y_loc):
        """
        Gets any actor present at the specified location. Returns False if none are present.
        :param x_loc: integer - the X coordinate
        :param y_loc: integer - the Y coordinate
        :return: an Actor if one is present, otherwise False
        """

        if (x_loc, y_loc) in self.actors_locations:
            return self.actors_locations[(x_loc, y_loc)]
        else:
            return False

    def get_all_actors(self):
        """
        Gets all actors currently registered on the level - includes those without a specified location.
        :return: a list of all actors present on the level.
        """

        return list(self.actors_ids.values())

    def add_actor(self, actor):
        """
        Adds an actor to the level. If it has a location it will be added to both dictionaries.
        If it should only go in the id one, it needs x_loc and y_loc set to None.
        :param actor: The actor in question.
        """

        if (actor.x_loc, actor.y_loc) in self.actors_locations:
            interface.add_debug_text("Tried to add an actor at {}, {}, but {} already there".format(
                actor.x_loc, actor.y_loc, self.actors_locations[(actor.x_loc, actor.y_loc)]))
            return

        self.actors_ids[actor.entity_id] = actor

        if actor.x_loc is None and actor.y_loc is None:
            return
        elif actor.x_loc is None or actor.y_loc is None or not self.is_valid_map_coord(actor.x_loc, actor.y_loc):
            interface.add_debug_text("Tried to add actor {} with invalid coordinates {}, {}".format(
                actor, actor.x_loc, actor.y_loc))
            return
        else:
            self.actors_locations[(actor.x_loc, actor.y_loc)] = actor

    def remove_actor(self, actor):
        """
        Removes the actor from the level.
        :param actor: The actor to remove.
        """

        if actor.entity_id not in self.actors_ids:
            interface.add_debug_text("Tried to remove actor {} with id {} but it wasn't there".format(
                actor, actor.entity_id))
            return

        del self.actors_ids[actor.entity_id]

        if actor.x_loc is None and actor.y_loc is None:
            return

        if ((actor.x_loc, actor.y_loc) not in self.actors_locations or
                self.actors_locations[(actor.x_loc, actor.y_loc)] is not actor):
            interface.add_debug_text("Tried to remove actor {} from {}, {} but it wasn't there".format(
                actor, actor.x_loc, actor.y_loc))
            return

        del self.actors_locations[(actor.x_loc, actor.y_loc)]


##################################################################################################################
#                                       Game Class
##################################################################################################################

class Game(object):
    """
    Main engine - everything hangs off this to make it nice and easy to pickle up.
    """

    def __init__(self, player, gm_options):
        """
        Setup for the game class - just takes a player as an argument unless some GM options are set.
        :param player: The player character for the game.
        :param gm_options:
        """

        self.version_number = "0.02"  # TODO: Keep this up to date

        self.player = player
        self.character_class = player.character_class
        self.current_level = None
        self.level_dict = dict()
        self.timer = Timer()

        if gm_options is None:
            self.level_transition("Level1a", 24, 54)
        else:
            self.level_transition(*gm_options)

        self.timer.insert(0, player)

    def level_transition(self, level_name, x_loc, y_loc):
        """
        Moves the player to the specified location at the other level
        :param level_name: string - the new level
        :param x_loc: integer - the new x_coordinate
        :param y_loc: integer - the new y_coordinate
        """

        if self.current_level is not None:
            # TODO: Pack up the old level
            pass

        # Check if the player has visited the level before.
        if level_name in self.level_dict:
            # TODO: Fix this up properly
            pass

        else:
            new_level = MapLevel(level_name)
            self.level_dict[level_name] = new_level
            self.current_level = new_level

            # TODO: Fix this up properly
            self.player.x_loc = x_loc
            self.player.y_loc = y_loc
            self.current_level.add_actor(self.player)

    def run_game(self):
        """
        Actually gets the game going.
        """

        while True:
            self.timer.run_turn()

##################################################################################################################
#                                       Initial Setup
##################################################################################################################


def setup_directories_and_config():
    """
    Checks for the sub-directories and creates them if not present.
    Also looks for the config file, and if present, returns the config parameters.
    :return: (size, extra_keys, gm_view) tuple.
    """

    if not os.path.exists(os.path.join(os.getcwd(), "Conf")):
        os.mkdir(os.path.join(os.getcwd(), "Conf"))

    # Create the unlocked racial file if there isn't one yet.
    if not os.path.exists(os.path.join(os.getcwd(), "Conf", "ULR.tmns")):
        unlocked_race_file = open(os.path.join(os.getcwd(), "Conf", "ULR.tmns"), mode="wb")
        pickle.dump(unlocked_races, unlocked_race_file)
        unlocked_race_file.close()

    # Create the save game summary file if there isn't one yet
    if not os.path.exists(os.path.join(os.getcwd(), "Conf", "SGS.tmns")):
        unlocked_race_file = open(os.path.join(os.getcwd(), "Conf", "SGS.tmns"), mode="wb")
        pickle.dump(dict(), unlocked_race_file)
        unlocked_race_file.close()

    # Create the error log if there isn't one there yet.
    if not os.path.exists(os.path.join(os.getcwd(), "Conf", "TMNS_Log.t")):
        unlocked_race_file = open(os.path.join(os.getcwd(), "Conf", "TMNS_Log.txt"), mode="w")
        unlocked_race_file.close()

    if not os.path.exists(os.path.join(os.getcwd(), "Saves")):
        os.mkdir(os.path.join(os.getcwd(), "Saves"))

    if not os.path.exists(os.path.join(os.getcwd(), "Conf", "config.tmns")):
        return 0, False, False
    else:
        config_file = open(os.path.join(os.getcwd(), "Conf", "config.tmns"), mode="rb")
        params = pickle.load(config_file)
        config_file.close()
        return params


# TODO: Write these functions
def read_achievement_file():
    pass


def update_achievement_file():
    pass


def read_save_games():
    """
    Reads in the save game summary file.
    :return: a dictionary containing the summary information for the save games.
    """

    save_file = open(os.path.join(os.getcwd(), "Conf", "SGS.tmns"), mode="rb")
    save_dictionary = pickle.load(save_file)
    save_file.close()
    return save_dictionary


def update_save_games(save_dictionary):
    """
    Writes the save dictionary to the save file.
    :param save_dictionary: Update save dictionary.
    """

    save_file = open(os.path.join(os.getcwd(), "Conf", "SGS.tmns"), mode="wb")
    pickle.dump(save_dictionary, save_file)
    save_file.close()


def read_unlocked_races():
    """
    Reads the unlocked racial dictionary in.
    :return: dictionary of currently unlocked racial options.
    """

    racial_file = open(os.path.join(os.getcwd(), "Conf", "ULR.tmns"), mode="rb")
    racial_dictionary = pickle.load(racial_file)
    racial_file.close()
    return racial_dictionary


def update_unlocked_races():
    pass


##################################################################################################################
#                                       Main Program
##################################################################################################################

add_new_colors()
config_params = setup_directories_and_config()
interface = Interface(*config_params)
interface.main_menu()
