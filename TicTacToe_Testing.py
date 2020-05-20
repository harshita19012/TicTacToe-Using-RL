# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 16:16:51 2019

@author: Harshita Pandey
"""

import itertools
import random
import pickle

def Next_Action(AllStates,position,board_rows,Qtable1):
    
    global state
    
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
        state = random.choice(empty)
    else:
        for k in range(0,len(empty)):
            a = empty[k]
            if(Qtable1[position][a] > maximum):
                maximum = Qtable1[position][a]
                state = a
    
    return state

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
        reward1 = 40
        reward2 = -20
        
    elif(player2 > 0):
        reward1 = -20
        reward2 = 40
    
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
    
    board_rows = int(input("Enter the number of rows in the board"))
    board_cols = int(input("Enter the number of columns in the board"))
    
    AllStates = Generate_AllStates()
    States = len(AllStates)
    
    
    print(States)
    table1 = open("Pickle_Qtable1.p","rb")
    Qtable1 = pickle.load(table1)
    
    table2 = open("Pickle_Qtable2.p","rb")
    Qtable2 = pickle.load(table2)
    
    Board1 = [ [' ' for i in range(board_cols)] for j in range(board_rows)]
        
    Flag = True
        
    game_end = 0
    while(game_end != 1):
        print("The state of the board is :")
        Print_Board(Board1,board_rows,board_cols)
            
        #print("Flag",Flag)
            
        position1 = Find_Position(AllStates,Board1)
            
        if(Flag == True):
            action = int(input("Enter the action to be performed"))
            print("Action",action)
            
            Board2 = Change_Board1(Board1,action,board_rows)
            Board1 = AllStates[position1]
            position2  = Find_Position(AllStates,Board2)
            Board1 = Board2
            game_end,winner = Game_End(Board2,board_rows,board_cols)
            Flag = False
            print()
                
        else:
            action = Next_Action(AllStates,position2,board_rows,Qtable2)
            print("Action",action)
                
            Board2 = Change_Board2(Board1, action, board_rows)
            Board1 = AllStates[position1]
            position2 = Find_Position(AllStates,Board2)
                
            Board1 = Board2
            game_end,winner = Game_End(Board2, board_rows, board_cols)
            Flag = True
            print()
                             
    Print_Board(Board2,board_rows,board_cols)
    if(winner == 1):
        print("--------------PLAYER1 WINS------------------")
    if(winner == 2):
        print("--------------PLAYER2 WINS------------------")
    if(winner == 0):
        print("--------------NO PLAYER WINS------------------")
    
if __name__=="__main__":
    main()