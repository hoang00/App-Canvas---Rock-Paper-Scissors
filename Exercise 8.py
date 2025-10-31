
# # Testing some inputs
# quit = input('Type "enter" to quit:' )
# while quit != "enter":
#     quit = input('Type "enter" to quit:' )

# Rock Paper Scissors Program - my first try
# ask for input from player1
# start = input("Do you want to start a new game (Y/N)? ").lower()
# while start != "n":
#     p1_input = (input("Player 1: Select Rock/Paper/Scissors: ")).lower()
#     # have a loop to wait until they choose rock paper or scissors
#     while p1_input not in ("rock", "paper", "scissors"):
#         p1_input = (input("Player 1: Select Rock/Paper/Scissors: "))

#     # Repeat for p2
#     p2_input = (input("Player 2: Select Rock/Paper/Scissors: ")).lower()
#     while p2_input not in ("rock", "paper", "scissors"):
#         p2_input = (input("Player 2: Select Rock/Paper/Scissors: "))

#     # LogicTree - is there an easier way to do this?
#     if p2_input == "rock" and p1_input == "rock":
#         print("Tie")
#     if p2_input == "paper" and p1_input == "paper":
#         print("Tie")
#     if p2_input == "scissors" and p1_input == "scissors":
#         print("Tie")
#     if p2_input == "rock" and p1_input == "paper":
#         print("Player 1 wins")
#     if p2_input == "rock" and p1_input == "scissors":
#         print("Player 2 wins")
#     if p2_input == "paper" and p1_input == "rock":
#         print("Player 2 wins")
#     if p2_input == "paper" and p1_input == "scissors":
#         print("Player 1 wins")
#     if p2_input == "scissors" and p1_input == "rock":
#         print("Player 1 wins")
#     if p2_input == "scissors" and p1_input == "paper":
#         print("Player 2 wins")
#     start = input("Do you want to start a new game (Y/N)? ").lower()


# More refined way of doing it
print('''Please pick one:
            rock
            scissors
            paper''')

while True:
    game_dict = {'rock': 1, 'scissors': 2, 'paper': 3}
    player_a = str(input("Player a: "))
    player_b = str(input("Player b: "))
    a = game_dict.get(player_a)
    b = game_dict.get(player_b)
    dif = a - b

    if dif in [-1, 2]:
        print('player a wins.')
        if str(input('Do you want to play another game, yes or no?\n')) == 'yes':
            continue
        else:
            print('game over.')
            break
    elif dif in [-2, 1]:
        print('player b wins.')
        if str(input('Do you want to play another game, yes or no?\n')) == 'yes':
            continue
        else:
            print('game over.')
            break
    else:
        print('Draw.Please continue.')
        print('')