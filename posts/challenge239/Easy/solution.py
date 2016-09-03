#! /usr/bin/env python3

import pandas as pd

def GameStep(num):
    numlist = [num]
    steplist = []
    while num != 1:
        if num % 3 == 0:
            num //= 3
            steplist.append(0)
        elif (num - 1) % 3 == 0:
            num -= 1
            steplist.append(-1)
        elif (num + 1) % 3 == 0:
            num += 1
            steplist.append(1)
        numlist.append(num)
    steplist.append('NA')
    frame = pd.DataFrame([numlist,steplist]).transpose()
    frame.columns = ['Number', 'Step']
    return frame
    

if __name__ == '__main__':    
    print(GameStep(100))
    print('\n\n')
    print(GameStep(31337357))
            