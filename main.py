import cmd
import os
import random
import sys
import textwrap
import time

import keyboard
from colorama import Back, Fore, Style
import PySimpleGUI as sg


class Fighter:

    def __init__(self, name, description, hp, physique, finesse, weapon, loot, exp, chat_friendly):
        self.name = name
        self.description = description
        self.hp = hp
        self.physique = physique
        self.finesse = finesse
        self.weapon = weapon
        self.loot = loot
        self.exp = exp
        self.chat_friendly = chat_friendly

    def attack(self, other):
        time.sleep(1.50)
        print(f'\n{self.name} hit {other.name} with their {self.weapon.name}!')
        roll = random.randint(1, 6)
        damage = self.weapon.attack + round(self.physique/2) + roll
        time.sleep(1.50)
        print(f'Attack did ' + str(damage) + " damage!")
        other.hp -= damage
        time.sleep(1.50)
        print(f'{other.name} has {other.hp} HP remaining!')


class Weapon:
    def __init__(self, name, attack):
        self.name = name
        self.attack = attack


class Scene:
    def __init__(self, name, scene_transition, description, scene_attackables, proceed_conditions, next_scene):
        self.name = name
        self.scene_transition = scene_transition
        self.description = description
        self.scene_attackables = scene_attackables
        self.proceed_conditions = proceed_conditions
        self.next_scene = next_scene


# variables for NPCs and items

bow = Weapon('bow', 3)
sword = Weapon('sword', 5)
fists = Weapon('fists', 1)
silence = Weapon('silent treatment', 0)
pistol = Weapon('pistol', 8)
blank_weapon = Weapon('', int())
fight_object = Fighter('', int(), int(), int(), blank_weapon, '', '', 0, False)


employer = Fighter('the Benefactor', 'a well-dressed man grinning back at you', 30, 4, 9, fists,
                   ["Assignment Contract", "Assignment Contract"], 100, True)
goblin = Fighter('the Goblin', 'a stout green goblin picking his nose', 10, 3, 6, fists, ["Junk", "Junk"], 100, True)
bow_guard = Fighter('the Guard', 'a dour-looking guard, bow in hand', 20, 4, 8, bow, ["Ferry Pass", "Bow"], 200, True)
ferry_man = Fighter('the Ferryman', 'a silent operator of the boat', 20, 3, 3, fists, ["Junk", "Junk"], 100, False)
sword_guard = Fighter('the Sword Guard', 'a dour-looking guard, sword in hand', 20, 4, 8, sword, ["Signed Pass", "Sword"], 300, True)
mutant_beggar = Fighter('the Mutant', 'a man in tattered robes with tentacle fingers', 30, 3, 3, fists, ["Junk", "Junk"], 100, True)
emergency_chest = Fighter('the Emergency Chest', 'a chest', 10, 0, 0, silence, ["Splinters", "Splinters"], 0, True)
forest_elyrian = Fighter('the Hijacker', 'a frenzied looking Elyrian', 35, 4, 9, pistol, ["Ship Chest Key", "Pistol"], 600, True)
captain = Fighter('the Captain', "a dour-looking captain", 30, 5, 7, fists, ["Junk", "Captain's Badge"], 200, True)
no_attackables = Fighter('nothing', '', 0, 0, 0, 'nothing', 'nothing', 0, '')
mel = Fighter("Mel", "a young woman in black dress", 30, 10, 8, fists, ["Charcoal Ring", "Junk"], 300, True)
lyle = Fighter("Lyle", "a young man in black dress", 30, 10, 8, fists, ["Charcoal Ring", "Junk"], 300, False)
jess = Fighter("Jess", "a young woman in black dress", 30, 10, 8, fists, ["Charcoal Ring", "Junk"], 300, False)
kel = Fighter("Kel", "a young woman in black dress", 30, 10, 8, fists, ["Charcoal Ring", "Junk"], 300, False)
erik = Fighter("Erik", "a brutishly large man", 40, 12, 6, fists, ["Bellwood Map", "Junk"], 800, True)

# The player variables and scene variables
'''
name = "TEST CHARACTER"     # character for testing code
player_class = ""
player_culture = "Elyrian (Forest)"
luck = 0
resilience = 8
finesse = 4
insight = 3
physique = 10
total_hp = 50
exp = 0
'''
name = ""                   #real character
player_class = ""
player_culture = ""
luck = int()
resilience = int()
finesse = int()
insight = int()
physique = int()
total_hp = int()
exp = 0

level = 1
player_weapon = fists
inventory = set([])
money = 0
total_roll = 0
player = Fighter(name, player_class, total_hp, physique, finesse, player_weapon, inventory, exp, True)

scene_attackables = [Fighter('', '', int(), int(), int(), blank_weapon, '', exp, False)]
current_zone = Scene("", "", scene_attackables, '','', '')


# TODO: game progression post character generation. Scenes

g1 = ""

f2 = Scene("Delia - Brackwater Council Building",
            "\nYou flee the terrorists' house and follow the original instructions provided by the contract.\nYou find the large Brackwater council\n" \
            "building right in the center of the Delia settlement.",
            "The Crimson banners of the Brackwater company adorn the wooden halls of the building.\n" \
            "Near the center of the main councilroom you see a hulking Northerner, eating an entire\n" \
            "wheel of cheese by himself. This is definitely the guy you are looking for.",
            [erik], ["Bellwood Map"], g1)

f1 = Scene("Delia - Brackwater Council Building",
           "\nFreeranger Mel instructs you to meet with the Northerner at the Brackwater\nCouncil building near " \
           "the center of town. You leave the\nlittle house and make your way there, intending to feign commitment\n" \
           "to the original contract.",
           "The Crimson banners of the Brackwater company adorn the wooden halls of the building.\n" \
           "Near the center of the main councilroom you see a hulking Northerner, eating an entire\n" \
           "wheel of cheese by himself. This is definitely the guy you are looking for.",
           [erik], ["Bellwood Map"], g1)

e1 = Scene("A Small House in Delia",
           "\nIt feels like no time has passed but when you open your eyes again, you see\n" \
           "that you are now somewhere far from Thunder River. You are inside a dim shack\n" \
           "made of wood and stone, and are surrounded on all sides of your bed by black-clothed\n" \
           "figures.",
           "You are laying in bed, healing from the ship crash. The house you are in is dingy\n" \
           "and reeks of the uncleanliness of frontier life. You must be on the edge of the Bellwood.\n" \
           "There are people in tight, black clothes surrounding your rest bed.",
           [mel, lyle, jess, kel], ["Charcoal Ring"], f2)

d1 = Scene("Aboard the Naughty Gull",
           "\nYou make your way onto the Naughty Gull, flashing your signed pass to board.\n" \
           "You feel relieved to be getting away from Dark Harbor proper, finding a small\n" \
           "sense of gratitude to be heading East to the wild frontiers of the Bellwood.\n" \
           "Your calm is cut short as the ship jerks with a loud bang. The ship has stopped!\n" \
           "You feel as though time has frozen and when you come to your senses again, all\n" \
           "You can hear is the frenzied shouting of the people on board. You hear the\n" \
           "captain yell something about 'life jackets' in the emergency chest.",
           "People are running around the sinking ship, it's chaos. You see the chest\n" \
           "the captain must have been referring to. A small Forest Elyrian with long ears\n" \
           "and the dress of Bombolor stands before the chest, gun and key in hand, keeping\n" \
           "passengers from getting to the life jackets.",
           [captain, forest_elyrian, emergency_chest], ["Life Jacket"], e1)

c1 = Scene("Thunder River",
           "\nAfter your odd exchange with the guard and the goblin, you finally push onward.\nWith the Ferry Pass in " \
           "hand, you make your way to Thunder River.\nThe river is actually comprised of several rivers, flowing down from\n" \
           "the mountains of Hillsrun and feeding into one another down to the coast of Dark Harbor.\nYou can understand " \
           "how the river got its name, as your ears are filled with the loud rushing\nsounds of flowing water.",
           "The roaring of water fills your ears. You see a ferry ahead, loading travelers to cross.",
           [ferry_man, mutant_beggar, sword_guard], ["Signed Pass"], d1)

b1 = Scene("Road to Thunder River",
           "\nYou should leave before someone sees what has just happened. After reading the assignment contract you gained, \n" \
           "you decide to head East, the contract says that a Northerner in the small settlement of Delia, across Thunder River\n" \
           "will be very interested to meet with you.",
           "The oppressive heat of the orange sun burns your neck. You see a guard laying near a broken cart, bow by his side.\n"
           "You also spot a little goblin some ways in the distance.",
           [bow_guard, goblin], ["Ferry Pass"], c1)

a1 = Scene("Outside the Hammersgate prison",
           "You step outside into the blistering heat of Dark Harbor, you see a man standing before you, feet planted in the sand.",
           "There is a stinging hot breeze outside with air that tastes of salt.\n" \
           "The guards have removed your shackles and you are on the beach. There is a man before you.",
           [employer], ["Assignment Contract"], b1)

def flush_input():
    try:
        import msvcrt
        while msvcrt.kbhit():
            msvcrt.getch()
    except ImportError:
        import sys, termios    #for linux/unix
        termios.tcflush(sys.stdin, termios.TCIOFLUSH)

def start_game():   # start_game() will run the entire game, starting with the title text
    print(r'__________.__                __ ')
    print(r'\______   \ | _____    ____ |  | __')
    print(r'|    |  _/  | \__  \ _/ ___\|  |/ /')
    print(r'|    |   \  |__/ __ \\  \___|    <')
    print(r'|______  /____(____  /\___  >__|_ \ ')
    print(r'       \/          \/     \/     \/')
    print(r'  ____  __.__                   .___')
    print(r' |    |/ _|__| ____    ____   __| _/____   _____')
    print(r' |      < |  |/    \  / ___\ / __ |/  _ \ /     \ ')
    print(r' |    |  \|  |   |  \/ /_/  > /_/ (  <_> )  Y Y  \ ')
    print(r' |____|__ \__|___|  /\___  /\____ |\____/|__|_|  /')
    print(r'         \/       \//_____/      \/            \/ ')

    print("\n Press enter to continue")
    keyboard.wait('enter')
    main_menu()

# TODO: Change play to New Game, add Load Game option
def main_menu():
    print("------------------------------------")
    print("|            Main Menu             |")
    print("|----------------------------------|")
    print("|              play                |")
    print("|              about               |")
    print("|              quit                |")
    print("------------------------------------")
    print("\n You can interact with the menu by typing \'play\', \'about\', or \'quit\' after the \'>\' prompt and" +
          " hitting enter.")
    flush_input()
    selection = (input("\n> "))
    while selection.upper() not in ["PLAY", "ABOUT", "QUIT"]:
        selection = (input("Enter a valid input:\n> "))
    if selection.upper() == "PLAY":
        new_game()
    elif selection.upper() == "ABOUT":
        about_screen()
    elif selection.upper() == "QUIT":
        sys.exit()
    else:
        print("Please enter a valid input. ")
        main_menu()
    #else:
       # print("\nCommands \'play\', \'about\', or \'quit\' after the \'>\' must be spelled correctly.")
        #main_menu()

# optional information that can be accessed if the player chooses 'about' at title menu
# once exited, restarts the game back at the main menu


def about_screen():
    print("#################################################")
    print("#   Black Kingdom is a text-based RPG project   #")
    print("#################################################")
    print("#                                               #")
    print("#  - Interact with the game by typing commands  #")
    print("#                                               #")
    print("#  - The game will prompt you for input as you  #")
    print("#    as you play, and starts with character     #")
    print("#    creation and a tutorial                    #")
    print("#                                               #")
    print("#    Return to main menu by typing 'menu' in    #")
    print("#    the space after the '>' below and hit      #")
    print("#    enter on your keyboard                     #")
    print("#                                               #")
    print("#################################################")
    back = input("\n> ")
    if back.upper() == "MENU":
        main_menu()
    else:
        print("To go back to the main menu, enter 'menu' after the '>' prompt and hit enter.")
        about_screen()


def class_info():
    time.sleep(1.00)
    print("-----------------------------------------------------------------------------------------------------------------------")
    print("\n- Starchildren are those chosen by the Fates of Shihua. They have incredible luck and skills.")
    time.sleep(0.50)
    print("\n- Nomads are wanderers and adventurers. They have endured the worst of conditions.")
    time.sleep(0.50)
    print("\n- Artisans are craftsman, merchants or talented performers. They are dextrous and smooth-talkers.")
    time.sleep(0.50)
    print("\n- Seers are strangers to this world. They have insights into realms and realities different than our own.")
    time.sleep(0.50)
    print("\n- Brutes are athletically talented. Brutes often work jobs as guards, doormen, bouncers, or knights.")
    print("-----------------------------------------------------------------------------------------------------------------------")
    time.sleep(0.50)
    back = input("\nType 'back' and hit enter to go back and select class.\n> ")
    while back.upper() != "BACK":
        back = input("'back' must be entered to return to class selection.\n> ")
    pick_class()


def culture_info():
    time.sleep(1.00)
    print("-----------------------------------------------------------------------------------------------------------------------")
    print("\n- Dark Harbor is the hot, humid, south-eastern coastline of Glennduran.\nBustling trade region and home to the Brackwater company.")
    time.sleep(0.50)
    print("\n- Bombolor is the region of green forests and fields of central Glennduran.\nPrimarily home to the short, chivalrous, long-eared Elyrians.\nThe last King in Glennduran lives here.")
    time.sleep(0.50)
    print("\n- The North is a cold, arid region to the North of Glennduran, right on the southern edge of the Everwhite.")
    time.sleep(0.50)
    print("\n- Bloodwater or Bloodwater Bay refers to the western coast of Glennduran.\nIt's a place of concentrated abnormalities in our reality.")
    time.sleep(0.50)
    print("\n- Hillsrun refers to the mountains of central Glennduran.\nPrimarily home to the stout Elyrian people who clip their long ears short and keep war dogs as pets.\nMountain Elyrians are also known as the Dog People.")
    time.sleep(0.50)
    print("-----------------------------------------------------------------------------------------------------------------------")
    back = input("\nType 'back' and hit enter to go back and select culture.\n> ")
    while back.upper() != "BACK":
        back = input("'back' must be entered to return to culture selection.\n> ")
    pick_background()


# Confirms if the player really wants to start a new game or return to the main menu
# TODO: Add an option for loading a saved game

def new_game():
    play = input("Do you want to start a new game? Enter Y or N:"
                 "\n> ")
    if play.upper() == "Y":
        roll_stats()
    elif play.upper() == "N":
        print("Okay maybe next time.")
        main_menu()
    else:
        print("Please enter \"Y\" or \"N\" for Yes/No")
        new_game()

def speaking(text):
    speed = 0.05
    for letter in text:
        if keyboard.is_pressed('space'):
            speed = 0
        sys.stdout.write(letter)
        sys.stdout.flush()
        time.sleep(speed)
    flush_input()

# Rolls initial stats and variables for the player's character after new game proceeds

def roll_stats():
    global name
    global luck
    global resilience
    global finesse
    global insight
    global physique
    global total_hp
    speech1 = "\n\"Let me take a look at you, prisoner.\""
    print(Fore.BLUE)
    speaking(speech1)
    print(Style.RESET_ALL)

    luck = random.randint(0, 10)
    resilience = random.randint(1, 10)
    physique = random.randint(1, 10)
    finesse = random.randint(1, 10)
    insight = random.randint(1, 10)
    total_hp = 1+(3*resilience)
    print("\nLuck: " + str(luck) + "\nResilience: " + str(resilience) + "\nPhysique: " + str(physique) +
          "\nFinesse: " + str(finesse) + "\nInsight: " + str(insight) + "\nHP: " + str(total_hp))

    speech2 = "\n\"Am I seeing you correctly there in the dark?\""
    print(Fore.BLUE)
    speaking(speech2)
    print(Style.RESET_ALL)

    all_set = input("\n(Y/N)" +
                    "\n> ")

    speech3 = "\n\"I thought so, come with me, it's your lucky day.\""
    speechLuck0 = "\n\"Okay cool.\""
    speech4 = "\n\"What's your name again, prisoner?\""
    speech5 = "\n\"That's right, it says so right here in your papers.\""
    speech6 = "\n\"It is a little hard to see you in that cell.\""

    if all_set.upper() == "Y":
        try:
            if luck == 0:
                print(Fore.BLUE)
                speaking(speechLuck0)
                print(Style.RESET_ALL)
                time.sleep(0.5)
                speaking("\nThe guard explains that someone was going to post your bail today but died on the trip over.\n" + 
                         "\nThat's pretty unlucky isn't it? \n")
                time.sleep(2.0)
                print(Fore.RED)
                speaking("Game over you unlucky little freak\n")
                print(Style.RESET_ALL)
                time.sleep(2.0)
                start_game()
        except:
            print(Fore.BLUE)
            speaking(speech3)
            speaking(speech4)
            print(Style.RESET_ALL)
            name = input("\n> ")
            print(Fore.BLUE)
            speaking(speech5)
            print(Style.RESET_ALL)
            return name, luck, resilience, finesse, insight, physique, total_hp
        finally:
            pick_class()
    elif all_set.upper() == "N":
        print(Fore.BLUE)
        speaking(speech6)
        print(Style.RESET_ALL)
        roll_stats()
    else:
        print("\nPlease enter \"Y\" or \"N\" for Yes/No")
        roll_stats()


# modifies initial stats based on class choice

def pick_class():
    global luck
    global resilience
    global finesse
    global insight
    global physique
    global player_class
    global total_hp
    speech1 = "So, " + name + ", who were you before you were locked up?\"\n"
    speech_starchild = "\n\"I could see that, you seem a bit blessed.\""
    speech_nomad = "\n\"I could see that, you seem a bit hardy.\""
    speech_artisan = "\n\"I could see that, you seem a bit handy.\""
    speech_seer = "\n\"I could see that, you seem a bit touched.\""
    speech_brute = "\n\"I could see that, you seem a bit strong.\""
    speech2 = "\n\"What's that? Sorry you'll have to speak up.\""
    print(Fore.BLUE)
    speaking(speech1)
    print(Style.RESET_ALL)
    time.sleep(0.75)
    print("\nLuck: " + str(luck) + "\nResilience: " + str(resilience) + "\nPhysique: " + str(physique) +
          "\nFinesse: " + str(finesse) + "\nInsight: " + str(insight) + "\nHP: " + str(total_hp))
    time.sleep(1.25)
    class_choice = input("\nYou were a(n): \n" +
                         "\n* Starchild (luck + 2) " +
                         "\n* Nomad (resilience + 2)" +
                         "\n* Artisan (finesse + 2)" +
                         "\n* Seer (insight + 2)" +
                         "\n* Brute (physique + 2) \n" +
                         "\nEnter your selection by typing the name of the class below (ex: 'Nomad') or enter 'info' for more" +
                         "\n> ")
    if class_choice.upper() == "INFO":
        class_info()
    elif class_choice.upper() == "STARCHILD":
        try:
            print(Fore.BLUE)
            speaking(speech_starchild)
            print(Style.RESET_ALL)
            luck = luck + 2
            player_class = "Starchild"
            return luck, player_class
        finally:
            pick_background()
    elif class_choice.upper() == "NOMAD":
        try:
            print(Fore.BLUE)
            speaking(speech_nomad)
            print(Style.RESET_ALL)
            resilience = resilience + 2
            total_hp = total_hp + 6
            player_class = "Nomad"
            return resilience, player_class, total_hp
        finally:
            pick_background()
    elif class_choice.upper() == "ARTISAN":
        try:
            print(Fore.BLUE)
            speaking(speech_artisan)
            print(Style.RESET_ALL)
            finesse = finesse + 2
            player_class = "Artisan"
            return finesse, player_class
        finally:
            pick_background()
    elif class_choice.upper() == "SEER":
        try:
            print(Fore.BLUE)
            speaking(speech_seer)
            print(Style.RESET_ALL)
            insight = insight + 2
            player_class = "Seer"
            return insight, player_class
        finally:
            pick_background()
    elif class_choice.upper() == "BRUTE":
        try:
            print(Fore.BLUE)
            speaking(speech_brute)
            print(Style.RESET_ALL)
            physique = physique + 2
            player_class = "Brute"
            return physique, player_class
        finally:
            pick_background()
    else:
        print(Fore.BLUE)
        speaking(speech2)
        print(Style.RESET_ALL)
        print("\nEnter either \'Starchild\', \'Nomad\', \'Artisan\', \'Seer\', or \'Brute\'")
        pick_class()


# modifies initial stats further based on background choice

def pick_background():
    global luck
    global resilience
    global finesse
    global insight
    global physique
    global player_culture
    global total_hp
    print("\nLuck: " + str(luck) + "\nResilience: " + str(resilience) + "\nPhysique: " + str(physique) +
          "\nFinesse: " + str(finesse) + "\nInsight: " + str(insight) + "\nHP: " + str(total_hp))
    time.sleep(0.05)
    speech1 = "\n\"Tell me, " + name + ", where are you from?\"\n"
    speech_dh = "\n\"Ah! a proper harbor rat, just like myself. I thought I liked you.\""
    speech_bomb = "\n\"A bit of a joke, I could already tell by those long ears of yours, shorty.\""
    speech_north = "\n\"A bit of a joke, your accent already gave you away.\""
    speech_blood = "\n\"I wouldn't have guessed it. You seem pretty sane to me.\""
    speech_hills = "\n\"A bit of a joke, I could already tell by your clipped ears, shorty.\""
    speech2 = "\n\"What's that? Sorry you'll have to speak up.\""
    print(Fore.BLUE)
    speaking(speech1)
    print(Style.RESET_ALL)
    time.sleep(0.75)
    culture = input("\nYou grew up in: \n" +
                    "\n* Dark Harbor (luck + 1) " +
                    "\n* Bombolor (finesse + 1)" +
                    "\n* The North (resilience + 1)" +
                    "\n* Bloodwater (insight + 1)" +
                    "\n* Hillsrun (physique + 1) \n" +
                    "\nEnter your selection by typing the name of the class below (ex: 'The North') or type 'info' for more" +
                    "\n> ")
    if culture.upper() == "INFO":
        culture_info()
    elif culture.upper() == "DARK HARBOR":
        try:
            print(Fore.BLUE)
            speaking(speech_dh)
            print(Style.RESET_ALL)
            luck = luck + 1
            player_culture = "Dark Harbor"
            return luck, player_culture
        finally:
            redo_character_creation()
    elif culture.upper() == "BOMBOLOR":
        try:
            print(Fore.BLUE)
            speaking(speech_bomb)
            print(Style.RESET_ALL)
            finesse = finesse + 1
            player_culture = "Elyrian (Forest)"
            return finesse, player_culture
        finally:
            redo_character_creation()
    elif culture.upper() == "THE NORTH":
        try:
            print(Fore.BLUE)
            speaking(speech_north)
            print(Style.RESET_ALL)
            resilience = resilience + 1
            total_hp = total_hp + 3
            player_culture = "Northern"
            return resilience, player_culture, total_hp
        finally:
            redo_character_creation()
    elif culture.upper() == "BLOODWATER":
        try:
            print(Fore.BLUE)
            speaking(speech_blood)
            print(Style.RESET_ALL)
            insight = insight + 1
            player_culture = "Bloodwater"
            return insight, player_culture
        finally:
            redo_character_creation()
    elif culture.upper() == "HILLSRUN":
        try:
            print(Fore.BLUE)
            speaking(speech_hills)
            print(Style.RESET_ALL)
            physique = physique + 1
            player_culture = "Elyrian (Mountain)"
            return physique, player_culture
        finally:
            redo_character_creation()
    else:
        print(Fore.BLUE)
        speaking(speech2)
        print(Style.RESET_ALL)
        print("\nEnter either \'Dark Harbor\', \'Bombolor\', \'The North\', \'Bloodwater\', or \'Hillsrun\'")
        pick_class()


def redo_character_creation():  # Option for the player to start over if they do not like their character
    global luck
    global resilience
    global finesse
    global insight
    global physique
    global player_class
    global player_culture
    global name
    global total_hp
    global current_zone
    global level
    speech1 = "\n\"Alright, everything seems to be in order. Lucky for you someone paid your bail, " \
              "he's waiting for you outside.\""
    time.sleep(0.75)
    print("\n | Name: " + str(name) +
          "\n | Class: " + str(player_class) +
          "\n | Culture: " + str(player_culture) +
          "\n | Level: " + str(level) +
          "\n | HP: " + str(total_hp) +
          "\n | Luck: " + str(luck) +
          "\n | Finesse: " + str(finesse) +
          "\n | Insight: " + str(insight) +
          "\n | Resilience: " + str(resilience) +
          "\n | Physique: " + str(physique))
    redo = input("\nDo you accept this character? (Y/N): " +
                 "\n> ")
    if redo.upper() == "N":
        speaking("\nStarting character generation over.")
        name = ""
        luck = int()
        resilience = int()
        finesse = int()
        insight = int()
        physique = int()
        player_class = ""
        player_culture = ""
        roll_stats()
    elif redo.upper() == "Y":
        try:
            speaking("\nCharacter creation is set.")
            print(Fore.BLUE)
            speaking(speech1)
            print(Style.RESET_ALL)
            current_zone = a1
            return current_zone
        finally:
            print("\n")
            speaking(current_zone.scene_transition)
            time.sleep(1.00)
            scene(current_zone)     # takes player to the main game, starting at the first scene
    else:
        print("\nPlease enter either a \'Y\' or a \'N\'")
        redo_character_creation()


# TODO: Create functions for the possible player actions

def attack():       # attack action that cycles through attackable enemies giving option to attack them or not
    global fight_object
    global scene_attackables
    for enemy in scene_attackables:    # look for attackable item/creature in scene
        print("\nDo you want to attack " + str(enemy.name) + "?")
        confirm = input("(Y/N)" + "\n> ")   # confirm the player wants to attack it
        if confirm.upper() == "Y":
            if enemy.hp <= 0:
                speaking("They are already dead. ")
                scene(current_zone)
            else:
                try:
                    fight_object = enemy
                    return fight_object
                finally:
                    battle()        # initiates battle function wherein the player Fighter object fights the enemy
        elif confirm.upper() == "N":
            speaking("You don't want to attack that.")
        else:
            print("Please enter \"Y\" or \"N\" for Yes/No")
            attack()
    scene(current_zone)     # ultimately puts player back at the scene if nothing is attacked


def battle():
    global fight_object
    global total_hp
    global name
    global physique
    global finesse
    global player_weapon
    global inventory
    global player_culture
    global level
    global current_zone
    global exp
    death_text = "You have died and passed through the gates of the Black Kingdom.\n" \
                 "The Fates will draw another hero from the deck."
    token_text = "\nA mystical force prevents you from dying. The green coin glows hot\n" \
                 "in your bag and fades to nothing. You've been given a second chance.\n" \
                 "You open your eyes and wake up to a time just a few moments before the battle.\n" \
                 "Your adversary seems weaker, but unaware of the fight that took place."
    fight_object.hp = fight_object.hp
    fight_object.physique = fight_object.physique
    fight_object.weapon = fight_object.weapon
    player.finesse = finesse
    player.physique = physique
    player.weapon = player_weapon
    player.name = name
    player.hp = total_hp
    player.attack(fight_object)
    # the global calls and variable statements are overkill, but provide assurance the right stats are set for battle
    while player.hp > 0 and fight_object.hp > 0:        # fight continues as long as neither Fighters are dead
        if fight_object.hp > 0:
            fight_object.attack(player)
        if player.hp > 0:
            player.attack(fight_object)
    if player.hp <= 0:      # if player dies, prints out the death text and takes player to main menu
        if "Green Token" in inventory:
            inventory.remove("Green Token")
            speaking(token_text)
            time.sleep(1.00)
            scene(current_zone)
        else:
            time.sleep(1.50)
            player_class = ''
            player_culture = ''
            player_weapon = fists
            name = ''
            exp = 0
            inventory = set([])
            print("\n")
            print(Fore.RED)
            speaking(death_text)
            print(Style.RESET_ALL)
            time.sleep(1.50)
            try:
                return player_class, player_culture, player_weapon, name, exp, inventory
            finally:
                main_menu()
    elif fight_object.hp <= 0:  # if the enemy dies, program will proceed to the loot function
        time.sleep(0.50)
        print("\n" + str(fight_object.name) + " has been defeated.")
        time.sleep(0.50)
        loot()
    else:
        fight_object.attack(player)


def loot():     # loot function is called after player survives a battle
    global inventory
    global luck
    global scene_attackables
    global current_zone
    global exp
    time.sleep(0.70)
    roll_luck = random.randint(1, 6) + luck     # this is the basic luck roll. Die is 1d6 simulated here, adds luck
    try:
        if roll_luck >= 12:     # if the player's roll + their luck stat exceeds 12, they get multiple loot if possible
            if fight_object.loot[0] != fight_object.loot[1]:
                inventory.add(fight_object.loot[0])
                inventory.add(fight_object.loot[1])
                speaking("Lucky find! " + str(fight_object.loot[1]) + " and " + str(fight_object.loot[0]) +
                      " found and added to inventory.")
                return inventory, exp
            else:
                inventory.add(fight_object.loot[0])
                exp = exp + fight_object.exp
                speaking(str(fight_object.loot[0]) + " found and added to inventory. Gained " + str(fight_object.exp) +
                      " experience.")
                return inventory, exp
        else:
            inventory.add(fight_object.loot[0])
            exp = exp + fight_object.exp
            speaking(str(fight_object.loot[0]) + " found and added to inventory. Gained " + str(fight_object.exp) +
                  " experience.")
            return inventory, exp
    finally:
        level_up()  # after loot function runs, it goes to the level up function

# TODO: add weapons as they come up later in development
def equip():
    global player_weapon
    equipable_items = ['Bow', 'Sword', 'Laser Visor']
    for i in inventory:
        if i in equipable_items:
            print("\nDo you want to equip the " + i + "?")
            print("(Y/N)")
            choice = input("> ")
            if choice.upper() == "Y":
                time.sleep(0.50)
                speaking("You equipped the " + i + "!")
                if i == 'Bow':
                    player_weapon = bow
                elif i == 'Sword':
                    player_weapon = sword
                try:
                    return player_weapon
                finally:
                    scene(current_zone)
            elif choice.upper() == "N":
                print("You don't want to equip that.")
                scene(current_zone)
            else:
                print("Please enter \"Y\" or \"N\" for Yes/No")
                equip()
    speaking("Nothing to equip.")
    time.sleep(0.75)
    scene(current_zone)


def level_up():
    global exp
    global luck
    global resilience
    global finesse
    global insight
    global physique
    global total_hp
    global level
    if exp >= 100 and level < 2:
        level += 1
        print(Fore.GREEN)
        speaking("\nLevel up!")
        print(Style.RESET_ALL)
        time.sleep(0.50)
        speaking("Select physique, finesse, luck, insight, or resilience to improve")
        selection = input("\nChoose a stat to improve " + "\n> ")
        try:
            if selection.upper() == "PHYSIQUE":
                physique = physique + 2
                return physique
            elif selection.upper() == "FINESSE":
                finesse = finesse + 2
                return finesse
            elif selection.upper() == "LUCK":
                luck = luck + 2
                return luck
            elif selection.upper() == "INSIGHT":
                insight = insight + 2
                return insight
            elif selection.upper() == "RESILIENCE":
                resilience = resilience + 2
                total_hp = total_hp + 6
                return resilience, total_hp
            else:
                print("Enter a valid stat to improve. ")
                level_up()
        finally:
            time.sleep(0.50)
            print("\n | Name: " + str(name) +
                  "\n | Class: " + str(player_class) +
                  "\n | Culture: " + str(player_culture) +
                  "\n | Level: " + str(level) +
                  "\n | Total HP: " + str(total_hp) +
                  "\n | Luck: " + str(luck) +
                  "\n | Finesse: " + str(finesse) +
                  "\n | Insight: " + str(insight) +
                  "\n | Resilience: " + str(resilience) +
                  "\n | Physique: " + str(physique))
            scene(current_zone)
    if exp >= 300 and level < 3:
        level += 1
        print(Fore.GREEN)
        speaking("\nLevel up!")
        print(Style.RESET_ALL)
        time.sleep(0.50)
        speaking("Select physique, finesse, luck, insight, or resilience to improve")
        selection = input("\nChoose a stat to improve " + "\n> ")
        try:
            if selection.upper() == "PHYSIQUE":
                physique = physique + 2
                return physique
            elif selection.upper() == "FINESSE":
                finesse = finesse + 2
                return finesse
            elif selection.upper() == "LUCK":
                luck = luck + 2
                return luck
            elif selection.upper() == "INSIGHT":
                insight = insight + 2
                return insight
            elif selection.upper() == "RESILIENCE":
                resilience = resilience + 2
                total_hp = total_hp + 6
                return resilience, total_hp
            else:
                print("Enter a valid stat to improve. ")
                level_up()
        finally:
            time.sleep(0.50)
            print("\n | Name: " + str(name) +
                  "\n | Class: " + str(player_class) +
                  "\n | Culture: " + str(player_culture) +
                  "\n | Level: " + str(level) +
                  "\n | Total HP: " + str(total_hp) +
                  "\n | Luck: " + str(luck) +
                  "\n | Finesse: " + str(finesse) +
                  "\n | Insight: " + str(insight) +
                  "\n | Resilience: " + str(resilience) +
                  "\n | Physique: " + str(physique))
            scene(current_zone)
    if exp >= 700 and level < 4:
        level += 1
        print(Fore.GREEN)
        speaking("\nLevel up!")
        print(Style.RESET_ALL)
        time.sleep(0.50)
        speaking("Select physique, finesse, luck, insight, or resilience to improve")
        selection = input("\nChoose a stat to improve " + "\n> ")
        try:
            if selection.upper() == "PHYSIQUE":
                physique = physique + 2
                return physique
            elif selection.upper() == "FINESSE":
                finesse = finesse + 2
                return finesse
            elif selection.upper() == "LUCK":
                luck = luck + 2
                return luck
            elif selection.upper() == "INSIGHT":
                insight = insight + 2
                return insight
            elif selection.upper() == "RESILIENCE":
                resilience = resilience + 2
                total_hp = total_hp + 6
                return resilience, total_hp
            else:
                print("Enter a valid stat to improve. ")
                level_up()
        finally:
            time.sleep(0.50)
            print("\n | Name: " + str(name) +
                  "\n | Class: " + str(player_class) +
                  "\n | Culture: " + str(player_culture) +
                  "\n | Level: " + str(level) +
                  "\n | Total HP: " + str(total_hp) +
                  "\n | Luck: " + str(luck) +
                  "\n | Finesse: " + str(finesse) +
                  "\n | Insight: " + str(insight) +
                  "\n | Resilience: " + str(resilience) +
                  "\n | Physique: " + str(physique))
            scene(current_zone)
    if exp >= 1500 and level < 5:
        level += 1
        print(Fore.GREEN)
        speaking("\nLevel up!")
        print(Style.RESET_ALL)
        time.sleep(0.50)
        speaking("Select physique, finesse, luck, insight, or resilience to improve")
        selection = input("\nChoose a stat to improve " + "\n> ")
        try:
            if selection.upper() == "PHYSIQUE":
                physique = physique + 2
                return physique
            elif selection.upper() == "FINESSE":
                finesse = finesse + 2
                return finesse
            elif selection.upper() == "LUCK":
                luck = luck + 2
                return luck
            elif selection.upper() == "INSIGHT":
                insight = insight + 2
                return insight
            elif selection.upper() == "RESILIENCE":
                resilience = resilience + 2
                total_hp = total_hp + 6
                return resilience, total_hp
            else:
                print("Enter a valid stat to improve. ")
                level_up()
        finally:
            time.sleep(0.50)
            print("\n | Name: " + str(name) +
                  "\n | Class: " + str(player_class) +
                  "\n | Culture: " + str(player_culture) +
                  "\n | Level: " + str(level) +
                  "\n | Total HP: " + str(total_hp) +
                  "\n | Luck: " + str(luck) +
                  "\n | Finesse: " + str(finesse) +
                  "\n | Insight: " + str(insight) +
                  "\n | Resilience: " + str(resilience) +
                  "\n | Physique: " + str(physique))
            scene(current_zone)
    if exp >= 3100 and level < 5:
        level += 1
        print(Fore.GREEN)
        speaking("\nLevel up!")
        print(Style.RESET_ALL)
        time.sleep(0.50)
        speaking("Select physique, finesse, luck, insight, or resilience to improve")
        selection = input("\nChoose a stat to improve " + "\n> ")
        time.sleep(0.50)
        try:
            if selection.upper() == "PHYSIQUE":
                physique = physique + 2
                return physique
            elif selection.upper() == "FINESSE":
                finesse = finesse + 2
                return finesse
            elif selection.upper() == "LUCK":
                luck = luck + 2
                return luck
            elif selection.upper() == "INSIGHT":
                insight = insight + 2
                return insight
            elif selection.upper() == "RESILIENCE":
                resilience = resilience + 2
                total_hp = total_hp + 6
                return resilience, total_hp
            else:
                print("Enter a valid stat to improve. ")
                level_up()
        finally:
            time.sleep(0.50)
            print("\n | Name: " + str(name) +
                  "\n | Class: " + str(player_class) +
                  "\n | Culture: " + str(player_culture) +
                  "\n | Level: " + str(level) +
                  "\n | Total HP: " + str(total_hp) +
                  "\n | Luck: " + str(luck) +
                  "\n | Finesse: " + str(finesse) +
                  "\n | Insight: " + str(insight) +
                  "\n | Resilience: " + str(resilience) +
                  "\n | Physique: " + str(physique))
            scene(current_zone)
    if exp >= 6300 and level < 6:
        level += 1
        print(Fore.GREEN)
        speaking("\nLevel up!")
        print(Style.RESET_ALL)
        time.sleep(0.50)
        speaking("Select physique, finesse, luck, insight, or resilience to improve")
        selection = input("\nChoose a stat to improve " + "\n> ")
        try:
            if selection.upper() == "PHYSIQUE":
                physique = physique + 2
                return physique
            elif selection.upper() == "FINESSE":
                finesse = finesse + 2
                return finesse
            elif selection.upper() == "LUCK":
                luck = luck + 2
                return luck
            elif selection.upper() == "INSIGHT":
                insight = insight + 2
                return insight
            elif selection.upper() == "RESILIENCE":
                resilience = resilience + 2
                total_hp = total_hp + 6
                return resilience, total_hp
            else:
                print("Enter a valid stat to improve. ")
                level_up()
        finally:
            time.sleep(0.50)
            print("\n | Name: " + str(name) +
                  "\n | Class: " + str(player_class) +
                  "\n | Culture: " + str(player_culture) +
                  "\n | Level: " + str(level) +
                  "\n | Total HP: " + str(total_hp) +
                  "\n | Luck: " + str(luck) +
                  "\n | Finesse: " + str(finesse) +
                  "\n | Insight: " + str(insight) +
                  "\n | Resilience: " + str(resilience) +
                  "\n | Physique: " + str(physique))
            scene(current_zone)
    else:
        scene(current_zone)


def remove(item):
    global inventory
    if item in inventory:
        inventory.remove(item)


def help_menu():
    print('\n')
    print("#################################################")
    print("#                  Help Menu                    #")
    print("#################################################")
    print("#                                               #")
    print("#  Interact with the game by typing commands.   #")
    print("#                                               #")
    print("#  - 'Look' describes the current scene.        #")
    print("#                                               #")
    print("#  - 'Attack' cycles through things you can     #")
    print("#     fight in the scene.                       #")
    print("#                                               #")
    print("#  - 'inventory' shows your current items and   #")
    print("#     stats.                                    #")
    print("#                                               #")
    print("#  - 'proceed' checks to see if you can move to #")
    print("#     the next area.                            #")
    print("#                                               #")
    print("#  - 'equip' to cycle through equipable items.  #")
    print("#                                               #")
    print("#  - 'talk' to cycle through NPCs or objects    #")
    print("#     you can interact with.                    #")
    print("#################################################")
    print("\nType 'back' and hit enter after the prompt to return to game.")
    back = input("\n> ")
    while back.upper() != 'BACK':
        print("To go back to the game, enter 'back' after the '>' prompt and hit enter.")
        back = input("\n> ")
    scene(current_zone)

# a function that checks to see if the character can proceed to next zone
def proceed():
    global current_zone
    global inventory
    for i in current_zone.proceed_conditions:           # iterates through list of key items in inventory
        if i in inventory:
            current_zone = current_zone.next_scene      # if specific item is held, changes to next scene
            try:
                return current_zone
            finally:
                time.sleep(0.70)
                speaking(current_zone.scene_transition)
                time.sleep(0.50)
                scene(current_zone)
        else:
            speaking("Something inside you prevents you from leaving. There is still something to be done here.")
            scene(current_zone)


def talk():
    global fight_object
    global scene_attackables
    global current_zone
    no = "You don't want to talk after all."
    NPC_no = "They are not interested in talking with you."
    for NPC in scene_attackables:
        print("\n")
        print("\nDo you want to talk to " + str(NPC.name) + "?")  # confirm the player wants to talk to it
        confirm = input("(Y/N)" + "\n> ")
        if confirm.upper() == "Y":
            if NPC.chat_friendly is False:
                speaking(NPC_no)
                scene(current_zone)
            else:
                try:
                    fight_object = NPC
                    return fight_object
                finally:
                    chat()
        elif confirm.upper() == "N":
            speaking(no)
        else:
            print("Please enter \"Y\" or \"N\" for Yes/No")
            talk()
    scene(current_zone)

# TODO: Add characters as project develops
def chat():     # checks selected NPC against associated names to proceed to the correct interaction function
                # there is one function per NPC at the moment. Each interaction is a specific and unique instance
    global fight_object
    if fight_object.name == 'the Benefactor':
        employer_chat()
    elif fight_object.name == 'the Goblin':
        goblin_chat()
    elif fight_object.name == 'the Guard':
        bow_guard_chat()
    elif fight_object.name == 'the Sword Guard':
        sword_guard_chat()
    elif fight_object.name == 'the Mutant':
        mutant_chat()
    elif fight_object.name == 'the Emergency Chest':
        emergency_chest_chat()
    elif fight_object.name == 'the Hijacker':
        hijacker_chat()
    elif fight_object.name == 'the Captain':
        captain_chat()
    elif fight_object.name == 'Mel':
        mel_chat()
    elif fight_object.name == 'Erik':
        erik_chat()
    else:
        scene(current_zone)


def roll(stat):
    roll_dice = random.randint(1, 6)
    total_roll = roll_dice + stat
    text1 = "Making a six-sided die roll: "
    text2 = "This plus your stat value is: "
    speaking(text1)
    time.sleep(1.00)
    print(str(roll_dice))
    time.sleep(1.00)
    speaking(text2)
    time.sleep(1.00)
    print(str(total_roll))
    time.sleep(1.00)
    return total_roll


def scene(zone):
    global current_zone
    global luck
    global resilience
    global finesse
    global insight
    global physique
    global player_culture
    global total_hp
    global level
    global scene_attackables
    inv_text = "\nYou check your things and reassess yourself. \n"
    current_zone = zone
    scene_attackables = current_zone.scene_attackables
    acceptable_inputs = ['attack', 'look', 'talk', 'proceed', 'inventory', 'equip', 'talk', 'help']
    time.sleep(0.75)
    print("\n------------------------------------")
    print(str(current_zone.name))
    print("------------------------------------")
    time.sleep(1.00)
    print("\nWhat would you like to do?")
    print("(Enter 'help' to see your options.)\n")
    action = input("> ")
    if action not in acceptable_inputs:
        print("\nPlease enter an acceptable input. ")
        scene(current_zone)
    else:
        if action.upper() == "ATTACK":
            try:
                return scene_attackables
            finally:
                attack()
        elif action.upper() == "LOOK":
            print("\nYou take a look around. \n")
            time.sleep(0.50)
            speaking(current_zone.description)
            scene(current_zone)
        elif action.upper() == "INVENTORY":
            speaking(inv_text)
            time.sleep(0.50)
            print("Bag: ")
            print(inventory)
            time.sleep(0.50)
            print("Money: ")
            print(str(money))
            time.sleep(0.50)
            print("\n | Name: " + str(name) +
                  "\n | Class: " + str(player_class) +
                  "\n | Culture: " + str(player_culture) +
                  "\n | Level: " + str(level) +
                  "\n | Total HP: " + str(total_hp) +
                  "\n | Weapon: " + player_weapon.name + " (+" + str(player_weapon.attack) + " damage)"
                  "\n | Luck: " + str(luck) +
                  "\n | Finesse: " + str(finesse) +
                  "\n | Insight: " + str(insight) +
                  "\n | Resilience: " + str(resilience) +
                  "\n | Physique: " + str(physique))
            time.sleep(0.50)
            scene(current_zone)
        elif action.upper() == "HELP":
            help_menu()
        elif action.upper() == "EQUIP":
            equip()
        elif action.upper() == "PROCEED":
            proceed()
        elif action.upper() == "TALK":
            talk()
        else:
            print("\nPlease enter an acceptable input. ")
            scene(current_zone)


def employer_chat():
    global inventory
    global current_zone
    speech1 = "What are you still doing here? You have a job to do, and remember to keep this between us."
    speech2 = "I bet you're wondering why I bailed you out, huh? Listen I've got a job for you.\nTake this and head East," \
              " to the settlement of Delia, near the edge of the Bellwood.\nDon't tell anyone this took place. I expect " \
              "discretion... for your sake."
    inventory_update = "\nAssignment Contract added to your inventory!"
    dead_text = "\nHe seems a little too dead to talk."
    if employer.hp <= 0:
        time.sleep(0.50)
        speaking(dead_text)
        time.sleep(0.50)
        scene(current_zone)
    else:
        if "Assignment Contract" in inventory:
            print(Fore.CYAN)
            speaking(speech1)
            print(Style.RESET_ALL)
            scene(current_zone)
        else:
            print(Fore.CYAN)
            speaking(speech2)
            print(Style.RESET_ALL)
            inventory.add("Assignment Contract")
            speaking(inventory_update)
            scene(current_zone)


def bow_guard_chat():
    global current_zone
    global inventory
    speech1 = "You must be that prisoner that just got released.\nListen, there's some stinky " \
              "good-for-nothing, goblin over there."
    speech2 = "\nEw, did you see that? Anyways, kill it for me and I'll give you a Ferry Pass to get across Thunder River.\n" \
              "If you don't kill it, I'll throw you back in prison where you belong."
    speech3 = "Oh good, you killed him. What? No he didn't do anything to me, I just hate goblins.\nHere's the pass. " \
              "I'll throw that junk away for you too.\n"
    dead_text = "\nHe seems a little too dead to talk."
    goblin_wave = "\nYou see a green little goblin a little ways off, it smiles and waves at you."
    if bow_guard.hp <= 0:
        time.sleep(0.50)
        speaking(dead_text)
        time.sleep(0.50)
        scene(current_zone)
    else:
        if goblin.hp <= 0:
            print(Fore.BLUE)
            speaking(speech3)
            print(Style.RESET_ALL)
            inventory.add("Ferry Pass")
            remove("Junk")
            time.sleep(0.50)
            speaking("Ferry Pass added to inventory.")
            speaking("Junk removed from inventory.")
            scene(current_zone)
        else:
            print(Fore.BLUE)
            speaking(speech1)
            print(Style.RESET_ALL)
            time.sleep(1.00)
            speaking(goblin_wave)
            time.sleep(1.50)
            print(Fore.BLUE)
            speaking(speech2)
            print(Style.RESET_ALL)
            time.sleep(0.75)
            scene(current_zone)


def goblin_chat():
    global current_zone
    speech1 = "Hi there! You seem a lot friendlier than that man over there.\n" \
              "He's been giving me funny looks all day.\n" \
              "I'm just taking a break from my walk, really nice day for a walk!"
    speech2 = "Oh hello! I see you killed that man over there.\nSo sad that it had to come to violence, but he's been " \
              "giving me weird looks all day.\nIn a way I'm relieved.\nOh I see you have the Ferry Pass, have a good " \
              "trip!"
    dead_text = "\nHe seems a little too dead to talk."
    if goblin.hp <= 0:
        time.sleep(0.50)
        speaking(dead_text)
        time.sleep(0.50)
        scene(current_zone)
    elif bow_guard.hp <= 0:
        print(Fore.GREEN)
        speaking(speech2)
        print(Style.RESET_ALL)
        scene(current_zone)
    else:
        print(Fore.GREEN)
        speaking(speech1)
        print(Style.RESET_ALL)
        scene(current_zone)


def mutant_chat():
    global current_zone
    speech1 = "Spare some money for my fare? Oh...\n" \
              "Yes, I see you " + player.name + " I see special things.\n" \
              "Give me your pass, and in return I will give you something special."
    speech2 = "Thank you stranger, I see great things ahead for you.\nWe are a lot alike, you and I."
    speech3 = "Suit yourself, but I am not going anywhere."
    dead_text = "\nYou hear a distant laughter. His corpse is unresponsive."
    coin_text = "You give the strange beggar your pass.\nHe twirls his tentacle fingers and you see a green coin appear,\n" \
                "seemingly out of nowhere. He places it in your hand."
    inv_text = "Green Token added to inventory, it's hot to the touch. Lost Ferry Pass."
    gone_text = "You look for the mutant beggar but he's gone!"
    if mutant_beggar.hp <= 0:
        time.sleep(0.50)
        speaking(dead_text)
        time.sleep(0.50)
        scene(current_zone)
    elif "Ferry Pass" in inventory:
        print(Fore.MAGENTA)
        speaking(speech1)
        print(Style.RESET_ALL)
        print("\n")
        choice = input("Give the strange mutant your pass?\n(Y/N)\n> ")
        if choice.upper() == "Y":
            inventory.remove("Ferry Pass")
            inventory.add("Green Token")
            time.sleep(0.50)
            print(Fore.MAGENTA)
            speaking(speech2)
            print(Style.RESET_ALL)
            time.sleep(1.00)
            print('\n')
            speaking(coin_text)
            time.sleep(1.00)
            print('\n')
            speaking(inv_text)
        elif choice.upper() == "N":
            time.sleep(0.50)
            print(Fore.MAGENTA)
            speaking(speech3)
            print(Style.RESET_ALL)
        else:
            print("Please enter \"Y\" or \"N\" for Yes/No")
            mutant_chat()
    else:
        time.sleep(1.00)
        speaking(gone_text)
    scene(current_zone)


def sword_guard_chat():
    global current_zone
    global inventory
    speech1 = "You must be that prisoner that just got released, " + player.name + ".\nPresent your pass to the ferryman " \
              "if you want to cross.\nStay out of trouble."
    speech2 = "Sure, just hand it over to him now."
    speech3 = "Uh okay, whatever. Don't come aboard then."
    speech4 = "Hey! You can't come up here without a pass! Nice try prisoner scum."
    speech5 = "Get away from there!"
    speech6 = "You already have the Brackwater stamp, you can proceed."
    speech7 = "Hey I saw you kill that man!"
    if sword_guard.hp <= 0:
        time.sleep(0.50)
        speaking("\nHe seems a little too dead to talk.")
        time.sleep(0.50)
        scene(current_zone)
    elif ferry_man.hp <= 0 or mutant_beggar.hp <= 0:
        print(Fore.BLUE)
        speaking(speech7)
        print(Style.RESET_ALL)
        sword_guard.attack(player)
        battle()
    elif "Signed Pass" in inventory:
        print(Fore.BLUE)
        speaking(speech6)
        print(Style.RESET_ALL)
    elif "Ferry Pass" in inventory:
        print(Fore.BLUE)
        speaking(speech1)
        print(Style.RESET_ALL)
        choice = input("Give the ferryman your pass?\n(Y/N)\n> ")
        if choice.upper() == "Y":
            inventory.remove("Ferry Pass")
            inventory.add("Signed Pass")
            time.sleep(0.50)
            print(Fore.BLUE)
            speaking(speech2)
            print(Style.RESET_ALL)
            speaking(
                "You give the ferryman your pass.\nHe stamps it with the seal of the Brackwater Company,\n"
                "the reigning authority in Dark Harbor.\n"
                "He places the signed pass back into your hand and waves you to come aboard.")
            time.sleep(1.00)
            speaking("\nSigned Pass added to inventory.")
        elif choice.upper() == "N":
            time.sleep(0.50)
            print(Fore.BLUE)
            speaking(speech3)
            print(Style.RESET_ALL)
        else:
            print("Please enter \"Y\" or \"N\" for Yes/No")
            sword_guard_chat()
    elif "Ferry Pass" not in inventory:
        print(Fore.BLUE)
        speaking(speech1)
        print(Style.RESET_ALL)
        choice = input("Give the ferryman your pass?\n(Y/N)\n> ")
        if choice.upper() == "Y":
            time.sleep(0.50)
            print(Fore.BLUE)
            speaking(speech4)
            print(Style.RESET_ALL)
            roll_option = input("Make a finesse roll?\n(Y/N)\n> ")
            if roll_option.upper() == "Y":
                speaking("\nFinesse Roll - ")
                roll(finesse)
                if total_roll >= 8:
                    print("Success!")
                    time.sleep(0.50)
                    inventory.add("Ferry Pass")
                    speaking("You manage to swipe a Ferry Pass from the guard while he's rambling on.")
                    speaking("Ferry Pass added to inventory!")
                    time.sleep(0.50)
                    scene(current_zone)
                else:
                    print("Failed.")
                    time.sleep(0.50)
                    print(Fore.BLUE)
                    speaking(speech5)
                    print(Style.RESET_ALL)
                    scene(current_zone)
            elif roll_option.upper() == "N":
                speaking("You decide not to push it.")
                time.sleep(0.50)
                scene(current_zone)
            else:
                print("Please enter \"Y\" or \"N\" for Yes/No")
                sword_guard_chat()

        elif choice.upper() == "N":
            time.sleep(0.50)
            print(Fore.BLUE)
            speaking(speech3)
            print(Style.RESET_ALL)
        else:
            print("Please enter \"Y\" or \"N\" for Yes/No")
            sword_guard_chat()
    scene(current_zone)


def emergency_chest_chat():
    global current_zone
    global inventory
    global insight
    text1 = "You pop open the chest and grab a Life Jacket from within.\n" \
            "Time to go."
    text2 = "You already got the Life Jacket! Time to go."
    text3 = "You do not have a key to open the chest. Maybe you could try\nsomething else."
    text4 = "You try to speak with the object. To your surprise, the chest\nbegins to speak back. "
    text5 = "What? Who disturbs my turbulent slumber? "
    text6 = "\nLife Jacket? Yeah sure, here let me open my mouth real quick\njust grab it and let me sleep."
    if "Life Jacket" in inventory:
        speaking(text2)
        scene(current_zone)
    else:
        choice = input("\nDo you want to open the chest with a key?\n(Y/N)\n> ")
        while choice.upper() != "Y" and choice.upper() != "N":
            choice = input("Please enter Y or N\n> ")
        if choice.upper() == 'Y':
            if "Ship Chest Key" in inventory:
                inventory.remove("Ship Chest Key")
                remove("Junk")
                remove("Splinters")
                inventory.add("Life Jacket")
                speaking(text1)
                time.sleep(1.00)
                act_one()
            else:
                speaking(text3)
                choice = input("\nDo you want to make an Insight roll?\n(Y/N)\n> ")
                while choice.upper() != "Y" and choice.upper() != "N":
                    choice = input("Please enter Y or N\n> ")
                if choice.upper() == "Y":
                    speaking("\nInsight Roll - ")
                    total_roll = roll(insight)
                    if total_roll >= 10:
                        time.sleep(0.50)
                        print("Success!")
                        time.sleep(0.50)
                        remove("Junk")
                        remove("Splinters")
                        print(Fore.MAGENTA)
                        speaking(text4)
                        time.sleep(0.50)
                        speaking(text5)
                        time.sleep(0.50)
                        speaking(text6)
                        print(Style.RESET_ALL)
                        time.sleep(0.50)
                        speaking("You got the Life Jacket!")
                        time.sleep(0.50)
                        act_one()
                    else:
                        time.sleep(0.50)
                        print("Failed.")
                        time.sleep(0.50)
                        scene(current_zone)
                elif choice.upper() == "N":
                    time.sleep(0.50)
                    speaking("You decide against it.")
                    scene(current_zone)
        elif choice.upper() == "N":
                    time.sleep(0.50)
                    speaking("You decide against it.")
                    scene(current_zone)


def captain_chat():
    global current_zone
    global inventory
    if captain.hp <= 0:
        speaking("He seems a little too dead to talk.")
        scene(current_zone)
    else:
        print(Fore.BLUE)
        speaking("Ya need ta grab a Life Jacket from the safety chest\nand abandon ship! The Naughty Gull, she be sinking!")
        print(Style.RESET_ALL)
        time.sleep(0.50)
        scene(current_zone)


def hijacker_chat():
    global current_zone
    global inventory
    global player_culture
    global exp
    speech1 = "\nStand back! No one is making it off this Brackwater mule-ship!"
    speech2 = "\nBrother, you must understand my duty to my group.\nThe Freerangers of Delia are taking the settlement from the\nBrackwater tyrants." \
        " We must sink this ship, it is carrying valuable supplies to the\nBrackwater goons on the frontier. Take this key and go; tell no one I did this."
    speech3 = "\nStay back, clipped-ear! One more step and I shoot.\nThis Brackwater supply ship must sink! Glory to the Freerangers!\nI wouldn't expect a Hills dog" \
        " like you to understand the meaning of honor."
    speech4 = "\nStay back you Brackwater dog! This ship will not make it to Delia, not on my watch.\nLong live the Freerangers, death to the Brackwater company!"
    if forest_elyrian.hp <= 0:
        time.sleep(0.50)
        speaking("He seems a little too dead to talk.")
        scene(current_zone)
    else:
        if player_culture == "Elyrian (Forest)":
            time.sleep(0.50)
            print(Fore.GREEN)
            print("\nYou and the hijacker are both from Bombolor.")
            time.sleep(1.00)
            print(Style.RESET_ALL)
            print(Fore.CYAN)
            speaking(speech2)
            print(Style.RESET_ALL)
            time.sleep(0.50)
            inventory.add("Ship Chest Key")
            exp = exp + forest_elyrian.exp
            speaking("\nShip Chest Key added to inventory.")
            try:
                return exp
            finally:
                level_up()
        elif player_culture == "Elyrian (Mountain)":
            time.sleep(0.50)
            print(Fore.CYAN)
            speaking(speech3)
            print(Style.RESET_ALL)
            time.sleep(0.50)
            speaking("\nThe long-eared Elyrian hijacker aims the pistol at you. You decide to back away.")
        else:
            time.sleep(0.50)
            speaking("\nThe long-eared Elyrian man with a gun has a wild look in his eye, he is blocking the chest.")
            time.sleep(0.50)
            print(Fore.CYAN)
            speaking(speech4)
            print(Style.RESET_ALL)
            time.sleep(0.50)
            speaking("\nThe Elyrian is wild-eyed and threatening all passengers who approach.\nDo you want to make a Finesse and Physique roll?")
            choice = input("\n> ")
            while choice.upper() != "Y" and choice.upper() != "N":
                choice = input("Please enter either Y or N\n> ")
            if choice.upper() == "Y":
                speaking("\nPhysque Roll - ")
                total_roll_physique = roll(physique)
                speaking("\nFinesse Roll - ")
                total_roll_finesse = roll(finesse)
                if total_roll_physique >= 8 and total_roll_finesse >= 6:
                    time.sleep(0.50)
                    print("\nSuccess!")
                    time.sleep(0.50)
                    inventory.add("Ship Chest Key")
                    speaking("\nYou wait for him to take his eyes off you and when he does you\nrush toward him, tackling him off the side of the ship " + 
                    "and\ngrabbing the chest key from his hand.")
                    forest_elyrian.hp = 0
                    exp = exp + forest_elyrian.exp
                    try:
                        return exp
                    finally:
                        level_up()
                else:
                    time.sleep(0.50)
                    print("\nFailed.")
                    time.sleep(0.50)
                    speaking("\nYou decide not to try anything stupid.")
                    scene(current_zone)
            elif choice.upper() == "N":
                time.sleep(0.50)
                speaking("\nYou decide not to try anything stupid.")
                time.sleep(0.50)
                scene(current_zone)
        scene(current_zone)


def act_one():
    global inventory
    text1 = "\nYou quickly put on the Life Jacket and rush to the side of the sinking\nship. The powerful current of Thunder River roars all around you as you jump overboard." \
    "\nYou wake up some time later. You are laying down prone in the rocky banks of\nthe eastern side of Thunder River. Your body aches but you seem relatively okay." \
    "\nThere is no trace left of the Naughty Gull."
    text2 = "\nYou try to get up but the pain is too much. You begin to wait for some time......\nEventually you fall asleep."
    text3 = "\nYou just want to lay here and rest..."
    speech1 = "\nHey! Hey, are you alive?"
    text4 = "\nYou open your eyes carefully and see a handful of figures before you. They are clothed in\nblack and look like shadows in this light."
    speech2 = "\nThere you are, take it easy. Lyle, get them on the stretcher, it'll be dark soon\nin the Bellwood."
    text5 = "\nYou feel yourself lift off from the rocky shore bank, and drift back to sleep..."
    print("\n")
    speaking(text1)
    print("\n")
    choice = input("\nDo you want to try and get up?\n> ")
    while choice.upper() != "Y" and choice.upper() != "N":
        choice = input("\nEnter a Y or a N to get up.\n> ")
    if choice.upper() == "Y":
        speaking(text2)
    elif choice. upper() == "N":
        speaking(text3)
    remove("Life Jacket")
    remove("Assignment Contract")
    remove("Splinters")
    remove("Junk")
    remove("Signed Pass")
    time.sleep(1.00)
    print(Fore.MAGENTA)
    speaking(speech1)
    print(Style.RESET_ALL)
    time.sleep(0.50)
    speaking(text4)
    time.sleep(0.50)
    print(Fore.MAGENTA)
    speaking(speech2)
    print(Style.RESET_ALL)
    time.sleep(0.50)
    speaking(text5)
    time.sleep(1.00)
    scene(e1)


def mel_chat():
    global inventory
    global current_zone
    speech1 = "\nHey, you survived the Naughty Gull crash. I think you were the only one.\nMy friends here won't talk, don't worry about them.\nThey're saving their energy for the big Delia Dance."
    text1 = "\nThe figure in tight black clothes leans in to inspect you closer.\nShe pulls your Assignment Contract from your bag."
    speech2 = "\nYou must be the prisoner who got 'bailed out' of Hammersgate prison....\nDid you know you're working for Brackwater?"
    text2 = "\nShe shakes the contract in front of your face."
    speech3 = "\nI'm going to give you a choice, you can either keep working for the Company\nlike a dog, or you can help the Freerangers " \
        "take control of Delia.\nWhat do you say?"
    speech4 = "\nExcellent! Delia will be a free settlement thanks to you. Take this as a\nsymbol of allegiance to the Freerangers."
    speech5 = "\nYou killed them! AND RIGHT BEFORE THE BIG DANCE!!!"
    if mel.hp <= 0:
        speaking("They seem a little too dead to talk.")
        scene(e1)
    elif lyle.hp <= 0 or jess.hp <= 0:
        print(Fore.MAGENTA)
        speaking(speech5)
        print(Style.RESET_ALL)
        time.sleep(0.50)
        print("\nShe gets ready to attack you, but you manage to get the first strike.")
        current_zone = e1
        try:
            return current_zone
        finally:
            battle()
    print(Fore.MAGENTA)
    speaking(speech1)
    print(Style.RESET_ALL)
    time.sleep(0.50)
    speaking(text1)
    time.sleep(0.50)
    print(Fore.MAGENTA)
    speaking(speech2)
    print(Style.RESET_ALL)
    time.sleep(0.50)
    speaking(text2)
    time.sleep(0.50)
    print(Fore.MAGENTA)
    speaking(speech3)
    print(Style.RESET_ALL)
    time.sleep(0.50)
    print("\n")
    choice = input("Do you want to join the Freerangers?\n> ")
    while choice.upper() != "N" and choice.upper() != "Y":
        choice = input("Choose Y or N\n> ")
    if choice.upper() == "Y":
        time.sleep(0.50)
        print(Fore.MAGENTA)
        speaking(speech4)
        print(Style.RESET_ALL)
        inventory.add("Charcoal Ring")
        time.sleep(0.50)
        speaking("\nCharcoal Ring added to inventory!")
        time.sleep(0.50)
        speaking(f1.scene_transition)
        time.sleep(1.00)
        scene(f1)
    elif choice.upper() == "N":
        time.sleep(0.50)
        speaking("\nYou shake your head no. You won't join a bunch of terrorists.")
        time.sleep(0.50)
        speaking(f2.scene_transition)
        time.sleep(1.00)
        scene(f2)


def erik_chat():
    text1 = "\nThis is all there is for now. Thanks for playing this demo!\nReturning to Main Menu.\n"
    time.sleep(0.50)
    speaking(text1)
    time.sleep(0.50)
    main_menu()

start_game()
