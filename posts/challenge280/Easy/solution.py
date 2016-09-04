#! /usr/bin/env python3

def Validate(num):
    number = str(num)
    binarycheck = [i for i in list(number) if i not in ['0','1']]
    if len(number) != 10:
        return "Invalid input. Please include only 10 digits"
    elif len(binarycheck) != 0:
        return "Invalid input. Please include only binary numbers"
    else:
        num1 = int("0b" + number[:5], 2)
        num2 = int("0b" + number[5:], 2)
        if num1 < 10 and num2 < 10:
            return str(num1) + str(num2)
        else:
            return "Invalid input. One hand cannot exceed a value of 9"

if __name__ == '__main__':
    print("The binary hands game. Enter `quit` to exit.")
    while True:
        number = input("Please enter a 10-digit binary number: ")
        if number == "quit":
            break
        else:
            print(Validate(number))
        
        