import math
import random

def stringth(x):
    return math.log2(x+1)+x/10

def utility(str_max, str_min):
    
    n = random.randint(0, 1)
    utility = stringth(str_max) - stringth(str_min)+ ((-1)**n)*(random.randint(1, 10)/10)
    return round(utility, 2)

def alphaBeta(level , maxim , alpha,beta, str_max, str_min):
    if level == 0:
        return utility(str_max, str_min)
    if maxim:
        v = float('-inf')
        for i in range(2):
            res =alphaBeta(level-1, False, alpha, beta, str_max, str_min)
            v = max(v,res)
            alpha = max(alpha, v)
            if beta <= alpha:
                break
        return v
    else:
        v = math.inf
        for i in range(2):
            res = alphaBeta(level-1, True, alpha, beta, str_max, str_min)
            v = min(v, res)
            beta = min(beta, v)
            if beta <= alpha:
                break
        return v
    
def chessAB(start , magnus, fabiano):
    magnusCount = 0
    fabianoCount = 0
    draw = 0
    
    result = []
    players=["Magnus Carlsen", "Fabiano Caruana"]
    
    for i in range(4):
        
        if(i%2 ==0 and start == 0) or (i%2 ==1 and start == 1):
            maxim = 0
            maxStr = magnus
            minStr = fabiano
        else:
            maxim = 1
            maxStr = fabiano
            minStr = magnus
        alphabetaAnswer = alphaBeta(5,True, float('-inf'), math.inf, maxStr, minStr)
        
        if alphabetaAnswer > 0:
            win = players[maxim]
            role = "Max"
            if maxim == 0:
                magnusCount += 1
            else:
                fabianoCount += 1
        elif alphabetaAnswer < 0:
            win = players[1-maxim]
            role = "Min"
            if 1-maxim == 0:
                magnusCount += 1
            else:
                fabianoCount += 1
        else:
            win = "Draw"
            draw += 1
            role = ""
        result.append((i+1, win, role, alphabetaAnswer))
    return result, magnusCount, fabianoCount, draw

def main():
    start = int(input("Enter the starting player (0 for Magnus, 1 for Fabiano): "))
    magnus = int(input("Enter the strength of Magnus Carlsen: "))
    fabiano = int(input("Enter the strength of Fabiano Caruana: "))
    
    result, magnusCount, fabianoCount, draw = chessAB(start, magnus, fabiano)
    
    for game, winner, role, value in result:
        if winner != "Draw":
            print(f"Game {game}:Winner: {winner}  ({role}) (Utility value {value})")
        else:
            print(f"Game {game}:Result: {winner}  ({role}) (Utility value {value})")
    
    print("\n Overall Results:")
    print(f"Magnus Carlsen: {magnusCount}")
    print(f"Fabiano Caruana: {fabianoCount}")
    print(f"Draw: {draw}")
    
    if magnusCount > fabianoCount:
        print("Overall Winner: Magnus Carlsen")
    elif fabianoCount > magnusCount:
        print("Overall Winner: Fabiano Caruana")
    else:
        print("Overall Winner: Draw")

if __name__ == "__main__":
    main()
    
# Part 2: ............................................................................................
'''
import math
import random

def stringth(x):
    return math.log2(x+1)+x/10

def utility(str_max, str_min):
    
    n = random.randint(0, 1)
    utility = stringth(str_max) - stringth(str_min)+ ((-1)**n)*(random.randint(1, 10)/10)
    return round(utility, 2)

def alphaBeta(level , maxim , alpha,beta, str_max, str_min):
    if level == 0:
        return utility(str_max, str_min)
    if maxim:
        v = float('-inf')
        for i in range(2):
            res =alphaBeta(level-1, False, alpha, beta, str_max, str_min)
            v = max(v,res)
            alpha = max(alpha, v)
            if beta <= alpha:
                break
        return v
    else:
        v = math.inf
        for i in range(2):
            res = alphaBeta(level-1, True, alpha, beta, str_max, str_min)
            v = min(v, res)
            beta = min(beta, v)
            if beta <= alpha:
                break
        return v
    
def alphaBetaMindControl(level , maxim , alpha,beta, str_max, str_min):
    if level == 0:
        return utility(str_max, str_min)
    if maxim:
        v = float('-inf')
        for i in range(2):
            res =alphaBetaMindControl(level-1, False, alpha, beta, str_max, str_min)
            v = max(v,res)
            alpha = max(alpha, v)
            if beta <= alpha:
                break
        return v
    else:
        v = float('-inf')
        for j in range(2):
            res = alphaBetaMindControl(level-1, True, alpha, beta, str_max, str_min)
            v = max(v, res)
        return v
    
def main():
    start = int(input("Enter the starting player (0 for Light 1 for L): "))
    cost = float(input("Enter the cost of the mind control: "))
    lightS = float(input("Enter the strength of Light: "))
    ls = float(input("Enter the strength of L: "))
    
    if start == 0:
        maxStr = lightS
        minStr = ls
        maxPlayer = "Light"
    else:
        maxStr = ls
        minStr = lightS
        maxPlayer = "L"
        
    normal = alphaBeta(5, True, float('-inf'), float('inf'),maxStr, minStr)
    mindControl = alphaBetaMindControl(5, True, float('-inf'), float('inf'), maxStr, minStr)
    
    finalVal = mindControl - cost
    
    print(f"Minimax value without mind control: {normal}")
    print(f"Minimax value with mind control: {mindControl}")
    print(f"Final value with mind control after including cost: {finalVal}")
    
    if normal >0 and finalVal > 0:
        print(f"{maxPlayer} should NOT use mind control as the position is already winning")
    elif normal <= 0 and finalVal > 0:
        print(f"{maxPlayer} should use mind control")
    elif normal <= 0 and finalVal <= 0:
        print(f"{maxPlayer} should NOT use mind control as the position is loosing either way")
    elif normal > 0 and finalVal <= 0:
        print(f"{maxPlayer} should NOT use mind control as it backfires")
        
if __name__ == "__main__":
    main() 
    
'''

# part 3: ............................................................................................

'''
1. the stronger player wont necessarlily always win as the utility value is random and the mind control cost is also random.
2. inclding randomness in the utility function has both positive and negative effects.
advantages: adds a level of unpredictability to the game, makes the game more interesting.
disadvantages: the game might be biased towards one player due to the randomness.
3. increasing depth: increasing the depth of the tree will increase the time complexity of the algorithm. the time complexity of the algorithm is O(b^d) where b is the branching factor and d is the depth of the tree.
increasing branching factor: increasing the branching factor will increase the time complexity of the algorithm. the time complexity of the algorithm is O(b^d) where b is the branching factor and d is the depth of the tree.
4.the first player isnt always the maximizer this is a design decision 
5.alpha beta pruning doesnt work well in fully stochastic scenarios as it is based on the assumption that the opponent will always make the best move.
'''