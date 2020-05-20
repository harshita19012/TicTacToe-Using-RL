# -*- coding: utf-8 -*-
"""
Created on Sat Nov  2 22:01:23 2019

@author: Harshita Pandey
"""
import itertools
import random
import pickle

def Update_Qtable(Qtable1,AllStates,Board2,reward,position1,action,gamma,learning):
    position2 = Find_Position(AllStates,Board2)
    
    maximum = 0
    length = len(Qtable1[0])
    for k in range(length):
        if(Qtable1[position2][k] > maximum):
            maximum = Qtable1[position2][k]
    
    Qtable1[position1][action] = float(Qtable1[position1][action]) + learning*(reward + float(gamma*maximum) - float(Qtable1[position1][action]))
    #print(Qtable1[position1])
    return Qtable1
    

def AvailablePositions(Board,board_rows,board_cols):
    Available = []
    for j in range(board_rows):
        for k in range(board_cols):
            if(Board[j][k] == ' '):
                Available.append(list((j,k)))       
    return Available

def Game_End(Board,board_rows,board_cols):
    
    flag = 0
    for j in range(board_rows):
        count1 = 0
        count2 = 0
        for k in range(board_cols):
            if(Board[j][k] == "X"):
                count1 = count1 + 1
            if(Board[j][k] == "O"):
                count2 = count2 + 1
        if(count1 == board_cols):
            flag = flag + 1
            return 1,1
        if(count2 == board_cols):
            flag = flag + 1
            return 1,2
    
    for j in range(board_cols):
        count1 = 0
        count2 = 0
        for k in range(board_rows):
            if(Board[k][j] == "X"):
                count1 = count1 + 1
            if(Board[k][j] == "O"):
                count2 = count2 + 1
        if(count1 == board_rows):
            flag = flag + 1
            return 1,1
        if(count2 == board_rows):
            flag = flag + 1
            return 1,2
        
    count1 = 0
    count2 = 0
    count3 = 0
    count4 = 0
    for j in range(board_rows):
        for k in range(board_cols):
            if(j == k and Board[j][k] == "X"):
                count1 = count1 + 1
            if(j == k and Board[j][k] == "O"):
                count2 = count2 + 1
            if(((j + k) == (board_rows - 1)) and (Board[j][k] == "X")):
                count3 = count3 + 1
            if(((j + k) == (board_rows - 1)) and (Board[j][k] == "O")):
                count4 = count4 + 1
                
    if(count1 == board_rows or count3 == board_rows):
        flag = flag + 1
        return 1,1
    if(count2 == board_rows or count4 == board_rows):
        flag = flag + 1
        return 1,2

    Available = AvailablePositions(Board,board_rows,board_cols)
    if(len(Available) == 0):
        flag = flag  + 1
        return 1,0
    
    if(flag == 0):
        return 0,-1


def Find_Position(AllStates,Board1):
    for k in range(0,len(AllStates)):
        if(Board1 == AllStates[k]):
            return k
        

def Generate_AllStates():
    AllStates = []
    lists = [' ','O','X']
    for item in list(itertools.product(lists,repeat = 9)):
        temp = []
        list1 = (list(item[0:3]))
        list2 = (list(item[3:6]))
        list3 = (list(item[6:9]))
        temp.append(list1)
        temp.append(list2)
        temp.append(list3)
        AllStates.append(temp)
    
    #for i in range(len(AllStates)):  
    #print(AllStates[i])
    return AllStates


def Next_Action(AllStates,position,board_rows,Qtable1):
    
    global action_performed
    
    New_Item = AllStates[position]
    empty = []
    for i in range(board_rows):
        for j in range(board_rows):
            if(New_Item[i][j] == ' '):
                Item = int((i * 3) + (j + 1) - 1)
                empty.append(Item)
    #print (empty)
    
    a = empty[0]
    maximum = Qtable1[position][a]
    
    flag = 0
    length = len(empty)
    for k in range(0,length-1):
        a = empty[k]
        b = empty[k + 1]
        if(Qtable1[position][a] != Qtable1[position][b]):
            flag = flag + 1
            break
    
    if(flag == 0):
        action_performed = random.choice(empty) 
    else:
        for k in range(0,len(empty)):
            a = empty[k]
            action_performed = a
            if(Qtable1[position][a] > maximum):
                maximum = Qtable1[position][a]
                action_performed = a
    
    return action_performed,empty

def Change_Board1(Board1,action,board_rows):
    
    for k in range(board_rows):
        for j in range(board_rows):
            if(int((j * 3) + (k + 1) - 1) == action):
                Board1[j][k] = 'X'
    return Board1

def Change_Board2(Board1,action,board_rows):
    
    for k in range(board_rows):
        for j in range(board_rows):
            if(int((j * 3) + (k + 1) - 1) == action):
                Board1[j][k] = 'O'
    return Board1
               
    
def Print_Board(Board, board_rows, board_cols):
    for i in range(board_rows):
        print("------------")
        for j in range(board_cols):
            print(Board[i][j], end = " | ")
        print()
    print("------------")
        
    
def Reward(Board,board_rows,board_cols):
    player1, player2 = Find_Winner(Board,board_rows,board_cols)
    
    if(player1 > 0 and player2 > 0):
        reward1 = 10
        reward2 = 10
    
        
    elif(player1 > 0):
        reward1 = 20
        reward2 = -40
        
    elif(player2 > 0):
        reward1 = -40
        reward2 = 20
    
    else:
        reward1 = -10
        reward2 = -10
        
    return reward1,reward2
        
           
def Find_Winner(Board,board_rows,board_cols):
    
    player1 = 0
    player2 = 0
    for j in range(board_rows):
        count1 = 0
        count2 = 0
        for k in range(board_cols):
            if(Board[j][k] == "X"):
                count1 = count1 + 1
            if(Board[j][k] == "O"):
                count2 = count2 + 1
        if(count1 == board_cols):
            player1 = player1 + 1
        if(count2 == board_cols):
            player2 = player2 + 1
    
    for j in range(board_cols):
        count1 = 0
        count2 = 0
        for k in range(board_rows):
            if(Board[k][j] == "X"):
                count1 = count1 + 1
            if(Board[k][j] == "O"):
                count2 = count2 + 1
        if(count1 == board_rows):
            player1 = player1 + 1
        if(count2 == (-board_rows)):
            player2 = player2 + 1
    
    count1 = 0
    count2 = 0
    count3 = 0
    count4 = 0
    for j in range(board_rows):
        for k in range(board_cols):
            if(j == k and Board[j][k] == "X"):
                count1 = count1 + 1
            if(j == k and Board[j][k] == "O"):
                count2 = count2 + 1
            if(((j + k) == (board_rows - 1)) and (Board[j][k] == "X")):
                count3 = count3 + 1
            if(((j + k) == (board_rows - 1)) and (Board[j][k] == "O")):
                count4 = count4 + 1
                
    if(count1 == board_rows or count3 == board_rows):
        player1 = player1 + 1
    if(count2 == board_rows or count4 == board_rows):
        player2 = player2 + 1
            
    return player1,player2

def main():
    
    player1 = 0
    player2 = 0
    NoPlayer = 0 
    board_rows = int(input("Enter the number of rows in the board"))
    board_cols = int(input("Enter the number of columns in the board"))
    
    Exploration_rate = 0.7
    epsilon = 0.005
    decay_rate = 0.9999
    
    gamma = float(input("Enter the value of gamma"))
    learning = float(input("Enter the learning Rate"))
    
    AllStates = Generate_AllStates()
    States = len(AllStates)
    Moves = 9
    
    Reward1 = []
    Reward2 = []
    for k in range(len(AllStates)):
        state = AllStates[k]
        r1, r2 = Reward(state,board_rows,board_cols)
        Reward1.append(r1)
        Reward2.append(r2)
    
    
    #print(States)
    Qtable1 = [ [ 0 for i in range(Moves)] for j in range(States)]
    Qtable2 = [ [ 0 for i in range(Moves)] for j in range(States)]
    #print(Qtable1)
    episodes = int(input("Enter the total number of episodes"))
    for k in range(episodes):
        print()
        print("-----------------Episodes: ",k,sep="")
        
        Board1 = [ [' ' for i in range(board_cols)] for j in range(board_rows)]
        #print("The state of the Board is",Board1)
        
        Flag = True
        
        game_end = 0
        while(game_end != 1):
            print("The state of the board is :")
            Print_Board(Board1,board_rows,board_cols)
            
            #print("Flag",Flag)
            
            position1 = Find_Position(AllStates,Board1)
            
            if(Flag == True):
                if(random.uniform(0,1) <= Exploration_rate):
                    x,empty = Next_Action(AllStates,position1,board_rows,Qtable1)
                    action = random.choice(empty)
                else:
                    action,empty = Next_Action(AllStates,position1,board_rows,Qtable1)
                #print("Action",action)
            
                Board2 = Change_Board1(Board1,action,board_rows)
                Board1 = AllStates[position1]
                position2  = Find_Position(AllStates,Board2)
                reward1 = Reward1[position2]
                reward2 = Reward2[position2]
            
                Qtable1 = Update_Qtable(Qtable1, AllStates, Board2, reward1, position1, action, gamma, learning)
                Qtable2 = Update_Qtable(Qtable2, AllStates, Board2, reward2, position1, action, gamma, learning)
                Board1 = Board2
                game_end,winner = Game_End(Board2,board_rows,board_cols)
                Flag = False
                print("First Player's Chance")
                print()
                
            else:
                if(random.uniform(0,1) <= Exploration_rate):
                    x,empty = Next_Action(AllStates,position2,board_rows,Qtable2)
                    action = random.choice(empty)
                else:
                    action,empty = Next_Action(AllStates,position2,board_rows,Qtable2)
                #print("Action",action)
                
                Board2 = Change_Board2(Board1, action, board_rows)
                Board1 = AllStates[position1]
                position2 = Find_Position(AllStates,Board2)
                reward1 = Reward1[position2]
                reward2 = Reward2[position2]
                
                Qtable1 = Update_Qtable(Qtable1, AllStates, Board2, reward1, position1, action, gamma, learning)
                Qtable2 = Update_Qtable(Qtable2, AllStates, Board2, reward2, position1, action, gamma, learning)
                Board1 = Board2
                game_end,winner = Game_End(Board2, board_rows, board_cols)
                Flag = True
                print("Second player's chance") 
                print()
            
                if(Exploration_rate > epsilon):
                    Exploration_rate = Exploration_rate * decay_rate
        
        print("The final state of the board is")                    
        Print_Board(Board2,board_rows,board_cols)
        if(winner == 1):
            player1 = player1 + 1
            print("--------------PLAYER1 WINS------------------")
        if(winner == 2):
            player2 = player2 + 1
            print("--------------PLAYER2 WINS------------------")
        if(winner == 0):
            NoPlayer = NoPlayer + 1
            print("--------------NO PLAYER WINS------------------")
            
    pickle1 = open("Pickle_Qtable1.p","wb")
    pickle.dump(Qtable1,pickle1)
    pickle1.close()
    
    pickle2 = open("Pickle_Qtable2.p","wb")
    pickle.dump(Qtable2,pickle2)
    pickle2.close()
    
    """print()
    print("The Updated Qtable1 is")
    for k in range(States):
        print(k,Qtable1[k])
    
    
    print()
    print("The Updated Qtable2 is")
    for k in range(States):
        print(k,Qtable2[k])"""
        
    print("The Number of games in which Player 1 wins is :",player1)
    print("The Number of games in which Player 2 wins is :",player2)
    print("The Number of games in which there is a tie in the game :", NoPlayer)
    
    
if __name__=="__main__":
    main()