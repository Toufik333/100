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