# TicTacToe-Using-RL
The tic tac toe game is implemented with the help of reinforcement learning and the game is played between two bots and then the trained bot is played against human.

The Q table created defines states as all the possible states of the board (19,683 states) and the actions as the all the possible moves in the board (9 actions).
The reward table created consists of 19,683 states (all possible states possible of the board) and their respective rewards. 

Various rewards are provided to the bots who win the game according to the following rules:
If Player 1 wins and Player 2 looses:
  Player 1: 20     Player 2: -40
If Player 2 wins and player 1 looses:
  Player 1: -40     Player 2: 20
If both the players win:
  Player1: 10       Player2: 10
If none wins:
  Player1: -10      Player2: -10

