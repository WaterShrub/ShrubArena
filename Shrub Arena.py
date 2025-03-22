'''

INF360 - Programming in Python

Midterm

The goal of the game is to defeat your opponent in combat.
    To do this, you will both select a weapon and fight each other.
    While fighting, you may choose to either attack your opponent 
        or ready your shield to block. 

I, Justin Beshirs , affirm that the work submitted for this assignment is entirely my own. 
I have not engaged in any form of academic dishonesty, including but not limited to cheating, plagiarism, 
or the use of unauthorized materials. This includes, but is not limited to, the use of resources such as Chegg, 
MyCourseHero, StackOverflow, ChatGPT, or other AI assistants, except where explicitly permitted by the instructor. 
I have neither provided nor received unauthorized assistance and have accurately cited all sources in adherence 
to academic standards. I understand that failing to comply with this integrity statement may result in consequences, 
including disciplinary actions as determined by my course instructor and outlined in institutional policies. 
By signing this statement, I acknowledge my commitment to upholding the principles of academic integrity.
'''
from time import sleep
from random import randint
from sys import exit

#Determines who is attacking or blocking
# and outputs each players health after
# attack sequence
def attack(player1, player1Move, player2, player2Move):
    player1Move = str(player1Move)
    player2Move = str(player2Move)

    #Both attack
    if player1Move == 'Attack' and player2Move == 'Attack':
        print(f"{player1['name']} and {player2['name']} attacked each other!")
        
        #Both attackers have same speed and a player is CPU
        if player1['weapon']['speed'] == player2['weapon']['speed'] and \
            (player1['bot'] == True ^ player2['bot'] == True):
            if randint(0,9) < 6:
                damage(player1, player2)
                if not isDead(player2):
                    damage(player2, player1)
            else:
                damage(player2, player1)
                if not isDead(player1):
                    damage(player1, player2)

        #Both attackers have same speed
        if player1['weapon']['speed'] == player2['weapon']['speed']:
            if randint(0,9) < 5:
                damage(player1, player2)
                if not isDead(player2):
                    damage(player2, player1)
            else:
                damage(player2, player1)
                if not isDead(player1):
                    damage(player1, player2)

        #Player has a faster speed
        elif player1['weapon']['speed'] > player2 ['weapon']['speed']:
            damage(player1, player2)
            if not isDead(player2):
                damage(player2, player1)

        #Enemy has a faster speed
        else:
            damage(player2, player1)
            if not isDead(player1):
                damage(player1, player2)

    #Only player attacks
    elif player1Move == 'Attack' and player2Move == 'Block':
        print(f"{player1['name']} attacked and {player2['name']} blocked:")
        block(player2)
        damage(player1, player2)       

    #Only enemy attacks
    elif player2Move == 'Attack' and player1Move == 'Block':
        print(f"{player2['name']} attacked and {player1['name']} blocked:")
        block(player1)
        damage(player2, player1)

    #Both block
    else:
        print(f"{player1['name']} and {player2['name']} both blocked.\n")


    sleep(0.5)
    print(f"{player1['name']}'s health is: {player1['health']}")
    print(f"{player2['name']}'s health is: {player2['health']}")
    printBuffer() 
    sleep(1.2)
    return

#Sets the value of the 'blocking' key to True for the blocker
def block(blocker):
    blocker['blocking'] = True
    return

#Clears the terminal of text
def clearScreen():
    print("\n" * 60)
    return

#Deals damage to defender based on attackers weapon.
# if defended is blocking, unsets the block flag and ends
def damage(attacker, defender):
    blockChance = randint(1,5)
    
    #40% chance for block to parry
    if defender['blocking'] and blockChance >= 4:
        defender['blocking'] = False
        defender['health'] += randint(2,4)
        attacker['health'] -= randint(1,3)

        if defender['health'] > defender['max health']:
            defender['health'] = defender['max health'] 
        if attacker['health'] < 0:
            attacker['health'] = 0
    
        print(f"{defender['name']} parried the attack! Careful, {attacker['name']}!\n")
    
    #20% chance for block to block full damage
    elif defender['blocking'] and blockChance >=2:
        defender['blocking'] = False
        print(f"{defender['name']} fully blocked the attack!\n")
        if defender['health'] < 0:
            defender['health'] = 0

    #40% chance for block to block partial damage
    elif defender['blocking']:
        defender['blocking'] = False
        defender['health'] -= round(attacker['weapon']['damage'] * .5, None)
        print(f"{defender['name']} partially blocked the attack and still lost some health!\n")
        if defender['health'] < 0:
            defender['health'] = 0

    #No block, deals full damage
    else:
        defender['health'] -= attacker['weapon']['damage']
        if defender['health'] < 0:
            defender['health'] = 0
    return

#Takes 2 players and determines which one has a positive health
# value and updates their wins accordingly
def determineWinner(player1, player2):
    if player1['health'] > 0:
        print(f"The winner is {player1['name']}!")
        global player1Wins
        player1Wins += 1
    else:
        print(f"The winner is {player2['name']}!")
        global player2Wins
        player2Wins += 1

#Returns a dictionary of default player attributes
# and supplied player name
def initializePlayer(name, bot = False):
    if str(name).islower():
        name = str(name).title()
    return {'name' : str(name), 
            'bot' : bot,
            'weapon' : {},
            'health' : PLAYER_START_HEALTH, 
            'max health' : PLAYER_MAX_HEALTH, 
            'attacking' : False, 
            'blocking' : False}

#Checks if player is alive or dead.
def isDead(player):
    return player['health'] <= 0

#Asks if player would like to read the manual.
# Prints game manual if requested. 
def printManual():
    choice = input("Would you like to read the manual? y/n: ").lower().strip()

    if choice == 'y':
        manual = """
This is the manual for Shrub Arena
__________________________________

1) Overview
    The goal of the game is to defeat your opponent in combat.
    To do this, you will both select a weapon and fight each other.
    While fighting, you may choose to either attack your opponent 
        or ready your shield to block. 

2) Weapons
    You have two choices for weaponry: a trusty sword or a mighty axe.
    The sword deals a moderate amount of damage (5) but is fast.
    The axe deals a substansial amount of damage (7) but takes more time to swing. 

3) Attacking
    When attacking, your weapon speed decides who goes first. 
    If a weapon is faster than the opponents, they will always attack first.
    If both opponents have the same weapon speed, a random draw determines 
        who goes first. If one opponent is a bot, this draw favors the player.

4) Blocking
    When you block an attack, 1 of 3 things can happen.
    1)You have a slight chance to block all damage
    2)You have an increased chance to block half of the damage (rounded to the nearest whole number)
    3)You have a chance to parry the attack, dealing a 1-3 damage to the attacker and healing 2-4 health
        *Your health cannot go above 1.2 times your starting health
                """
        clearScreen()
        print(manual)       
        sleep(2)

    printBuffer() 
    return

#Requests input from the player to determine their next move.
#If the player already knows their choice, they can supply 
# that choice at function call as a str.
def moveSelect(player, choice = '0'):
    choice = str(choice)
    global MOVES

    #Default selection, requests choice from terminal
    if choice not in MOVES:
        print("Choose your next move:")
        for number, move in MOVES.items():
            print(f"{number}) {move}")
        choice = input().strip()
        print()

    while choice not in MOVES:
        print("Invalid input.")
        choice = input("Please enter the number corresponding to your move choice: ").strip()

    return MOVES[choice]

#Prints text buffer.
def printBuffer():
    print("*-" * 16 + "*") 
    return

#Asks user if they would like to replay.
# Returns 'y' or 'n'.
def replayChoice():
    choice = input("Would you like to play again? y/n: ").lower().strip()

    while choice != 'y' and choice != 'n':
        print("Invalid input.")
        choice = input("Would you like to play again? y/n: ").lower().strip()
    
    return choice

#weaponSelect asks player to choose a weapon and stores 
# the choice in the player dictionary. If the player
# already knows their choice, they can supply that choice
# at function call as a str.
def weaponSelect(chooser, weaponSelection = '-1'):
    weaponSelection = str(weaponSelection)
    global WEAPONS

    #Default selection, requests choice from terminal
    if weaponSelection not in WEAPONS:
        print("Select a weapon:")
        for number, weapon in WEAPONS.items():
            print(f"{number}) {str(weapon['name']).title()} - {weapon['damage']} damage and {weapon['speed']} speed")
        weaponSelection = input().strip()

    while weaponSelection not in WEAPONS:
        print("Invalid input.")
        weaponSelection = input("Please enter the number corresponding to your weapon choice: ").strip()

    chooser['weapon'] = WEAPONS[weaponSelection]

    return


#Game variables
playGame = True
player1Wins = 0
player2Wins = 0 #Currently unused, could be used in future local co-op iterations
enemyNames = ("Bob", "Leonidas", "Boss-man", "One-eyed Duck", "Calzoni", 
              "Nebula", "Cymbal Monkey", "AIDAN", "&$!'@$#", "Nemo",
              "Dev", "Crabcake", "a Slice of 'za", "Your future self",
              "Err-or!", "A chocolate chip", "The Doors", "ENEMY_NAME")

#Game constants
PLAYER_START_HEALTH = 25
PLAYER_MAX_HEALTH = int(PLAYER_START_HEALTH * 1.2)

#Enter new weapons below this line:

WEAPON_SWORD = {'name' : 'sword', 
                'damage' : 5, 
                'speed' : 7}
WEAPON_AXE = {'name' : 'axe', 
              'damage' : 7, 
              'speed' : 4}
WEAPONS = {'1' : WEAPON_SWORD, 
           '2' : WEAPON_AXE}

MOVES = {'1' : 'Attack', 
         '2' : 'Block'}

#Exits on unpredicted errors
try:
    #Intro
    clearScreen()
    print("Welcome to the Shrub Arena!")
    print("___________________________")
    playerName = str(input("What should we call you? : "))
    if playerName == "":
        playerName = "Player"
    printManual()
    sleep(0.3)

    #Main Game Loop
    while playGame:
        
        #Define players here
        player1 = initializePlayer(playerName)
        cpuNameChoice = enemyNames[randint(0, len(enemyNames) - 1)]
        player2 = initializePlayer(cpuNameChoice, True)
        print(f"Hello, {player1['name']}! Your enemy is {player2['name']}.\n")

        #Weapon selections
        weaponSelect(player1)
        weaponSelect(player2, str(randint(1,len(WEAPONS))))
        print(f"\n{player1['name']} chose the {player1['weapon']['name']}.")
        print(f"{player2['name']} chose the {player2['weapon']['name']}.\n")
        sleep(1)

        #Play until a players health <= 0
        print(f"All players are starting with {PLAYER_START_HEALTH} health.")
        print("*-" * 10 + "*")
        while not isDead(player1) and not isDead(player2):
            player1Move = moveSelect(player1)
            player2Move = moveSelect(player2, str(randint(1,2)))

            attack(player1, player1Move, player2, player2Move)

        #Determine winner
        determineWinner(player1, player2)
        
        #Display wins and ask to replay
        print(f"\nYour total wins: {player1Wins}")
        replay = replayChoice()

        if replay == 'n':
            playGame = False
        else:
            clearScreen()
            print(f"Welcome Back to the Shrub Arena, {player1['name']}!")
            print("___________________________")
            sleep(1)

    #End game
    if player1Wins > 1:
        print(f"Congrats, {player1['name']}, on the {player1Wins} wins!")
    elif player1Wins == 1:
        print(f"Congrats on the win, {player1['name']}!")
    print("\nThank you for playing.")
    exit()
except KeyboardInterrupt:
    if player1Wins > 1:
        print(f"Congrats, {player1['name']}, on the {player1Wins} wins!")
    elif player1Wins == 1:
        print(f"Congrats on the win, {player1['name']}!")
    print("\nThank you for playing.")
    exit()
except Exception as e:
    print(f"Unexpected error: {e}.\nExiting game.")
    exit()