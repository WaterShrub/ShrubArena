'''

INF360 - Programming in Python

Midterm

I, Justsin Beshirs , affirm that the work submitted for this assignment is entirely my own. 
I have not engaged in any form of academic dishonesty, including but not limited to cheating, plagiarism, 
or the use of unauthorized materials. This includes, but is not limited to, the use of resources such as Chegg, 
MyCourseHero, StackOverflow, ChatGPT, or other AI assistants, except where explicitly permitted by the instructor. 
I have neither provided nor received unauthorized assistance and have accurately cited all sources in adherence 
to academic standards. I understand that failing to comply with this integrity statement may result in consequences, 
including disciplinary actions as determined by my course instructor and outlined in institutional policies. 
By signing this statement, I acknowledge my commitment to upholding the principles of academic integrity.

'''
##Description of game here
from time import sleep
from random import randint

playGame = True
wins = 0
playerStartHealth = 20
playerMaxHealth = playerStartHealth * 1.25

#attack deals damage to opponent based on attackers
# weapon and the status of blockers 'blocking' status.
# The quickest weapon goes first. If both weapons have the same
# speed, first attacker is randomly determined, favoring the player.
def attack(player, playerMove, enemy, enemyMove):
    playerMove = str(playerMove)
    enemyMove = str(enemyMove)
    if playerMove == '1' and enemyMove == '2':
        block(enemy)
        damage(player, enemy)
        print("Player attacked and enemy blocked.")

    elif enemyMove == '1' and playerMove == '2':
        block(player)
        damage(enemy, player)
        print("Enemy attacked and player blocked.")

    elif playerMove == '1' and enemyMove == '1':
        print("Player and enemy attacked each other!")
        if randint(0,9) < 6:
            damage(player, enemy)
            if not isDead(enemy):
                damage(enemy, player)
        else:
            damage(enemy, player)
            if not isDead(player):
                damage(player, enemy)

    print("Player health is: " + str(player['health']))
    print("Enemy health is: " + str(enemy['health']))
    print()    
    return

#block function will set the value of the 'blocking' key 
# to True for the blocker
def block(blocker):
    blocker['blocking'] = True
    return

#Deals damage to defender based on attackers weapon.
# if defended is blocking, unsets the block flag and ends
def damage(attacker, defender):
    blockChance = randint(1,3)
    if defender['blocking'] and blockChance == 3:
        defender['blocking'] = False
        defender['health'] += randint(1,3)
        if defender['health'] > defender['max health']:
            defender['health'] = defender['max health']
        print(defender['name'] + " fully blocked the attack and gained some health!")
        return
    elif defender['blocking']:
        defender['blocking'] = False
        defender['health'] -= round(attacker['damage'] * .5, None)
        if defender['health'] < 0:
            defender['health'] = 0
    else:
        defender['health'] -= attacker['damage']
        if defender['health'] < 0:
            defender['health'] = 0
    return

#checks if player is alive or dead
def isDead(player):
    if player['health'] <= 0:
        return True
    return False

#
def moveSelect(player, choice = '0'):
    choice = str(choice)
    if choice == '0':
        print("Choose your next move:")
        print("1) Attack")
        print("2) Block")
        choice = input("\nPlease enter the number corresponding to your move choice: ")
        print()

    while choice != '1' and choice != '2':
        print("Invalid input.")
        choice = input("Please enter the number corresponding to your move choice: ")

    if choice == '1': 
        return 1
    elif choice == '2':
        return 2

#weaponSelect asks player to choose a weapon and stores 
# the choice in the player dictionary. If the player
# already knows their choice, they can supply that choice
# at function call as a str.
def weaponSelect(chooser, weaponSelection = '0'):
    weaponSelection = str(weaponSelection)
    if weaponSelection != '1' and weaponSelection != '2':
        print("Select a weapon:")
        print("1) Sword  - moderate damage, moderate speed.")
        print("2) Axe    - greater damage, slower speed.")
        weaponSelection = input("\nPlease enter the number corresponding to your weapon choice: ")

    while weaponSelection != '1' and weaponSelection != '2':
        print("Invalid input.")
        weaponSelection = input("Please enter the number corresponding to your weapon choice: ")

    if weaponSelection == '1': 
        chooser['weapon'] = 'sword'
        chooser['damage'] = 5
    elif weaponSelection == '2':
        chooser['weapon'] = 'axe'
        chooser['damage'] = 7
    return

#Main
#Welcome page
#player selects weapon
#enemy is initialized with random weapon choice
#battle loop
#   player choice to attack or block
#   enemy choice to attack or block
#   if either choose block, set block flag
#   if block flag is set, that player takes no damage
#   see who attacks first
#       sword always before axe
#       random choice to see who attacks first if same weapon
#           (weighted in player favor, if rand > 6 then emeny first)
#   check after each attack to see if a player is dead
#       if a player is dead, no more attacks run
#   If player dies, display dead message
#   If enemy looses, update win count 
#  display total wins and ask to play again


#Main Game Loop
print("Welcome to the Shurb Arena!")
print("___________________________")
sleep(1)

while playGame:   
    player = {'name' : 'player', 'weapon' : '', 'damage' : 0, 'health' : playerStartHealth, 
              'max health' : playerMaxHealth, 'attacking' : False, 'blocking' : False}
    enemy = {'name' : 'enemy', 'weapon' : '', 'damge' : 0, 'health' : playerStartHealth, 
             'max health' : playerMaxHealth, 'attacking' : False, 'blocking' : False}

    weaponSelect(player)
    weaponSelect(enemy, randint(1,2))
    print("\nYou chose the " + player['weapon'] + ".")
    print("The enemy chose the " + enemy['weapon'] + ".\n" )
    sleep(1)

    while not isDead(player) and not isDead(enemy):
        playerMove = moveSelect(player)
        enemyMove = moveSelect(enemy, randint(1,2))

        attack(player, playerMove, enemy, enemyMove)

    if player['health'] > 0:
        print("Congrats, you win!")
        wins += 1
    else:
        print("Better luck next time!")
    
    print("\nYour total wins: " + str(wins))

    replay = input("Would you like to play again? y/n: ").lower()
    while replay != 'y' or replay != 'n':
        print("Invalid input.")
        replay = input("Would you like to play again? y/n: ").lower()

    if replay == 'n':
        playGame = False

print("Thank you for playing. Congrats on the " + str(wins) + " wins!")

    
#add output for weak block
#restore health on successful strong block
# add output for weak block, partial damage
        


#ideas for final
#   add more enemys with more health
#   add basic XP system to improve weapon strength
#       after battle, gets some xp. if xp reaches amount, weapon levels up and deals percent more damage
#   add dagger as 3rd weapon, attacks twice. second attack cannot be blocked
#convert dictionaries to objects