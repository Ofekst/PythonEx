from numpy import *

#class for ex6
class DecoratorCache(dict):
    """ Constructor of DecoartorCache class """
    def __init__(self, function):
        self.function = function

    """ Return result of function call if cached"""
    def __call__(self, *args):
        return self[args]

    """ Return result of function call and cache the result """
    def __missing__(self, key):
        result = self[key] = self.function(*key)
        return result
######################################################################################
#exersise 1
"""
Function sums the numbers in 2 ways
"""
def sumOfListA():
    count=0
    message= input("Please enter number or stop if you finished\n")
    while(message.lower()!="stop"):
        count+=int(message)
        message = input()
    return count

def sumOfListB():
    count = 0
    lst = input("Enter a list of numbers with , between each other ").split(",")
    for num in lst:
        if num.isdigit():
            count += int(num)
    return count
######################################################################################
#exersise 2
"""
Function gets a matrix of tictactoe game
Function checks who wins the game
"""
def tictactoe(mat):
    if (mat[0][0]== mat[0][1]== mat[0][1]==1) or (mat[1][0]== mat[1][1]== mat[2][1]==1) or \
            (mat[2][0]== mat[2][1]== mat[2][2]==1):
        print("Player 1 won the game")
    elif(mat[0][0]== mat[1][0]== mat[2][0]==1) or (mat[1][0]== mat[1][1]== mat[2][1]==1) or \
            (mat[0][2]== mat[1][2]== mat[2][2]==1):
        print("Player 1 won the game")
    elif (mat[0][0] == mat[1][1] == mat[2][2] == 1) or (mat[2][0] == mat[1][1] == mat[2][0] == 1) :
        print("Player 1 won the game")

    elif (mat[0][0]== mat[0][1]== mat[0][1]==2) or (mat[1][0]== mat[1][1]== mat[2][1]==2) or \
            (mat[2][0]== mat[2][1]== mat[2][2]==2):
        print("Player 2 won the game")
    elif(mat[0][0]== mat[1][0]== mat[2][0]==2) or (mat[1][0]== mat[1][1]== mat[2][1]==2) or \
            (mat[0][2]== mat[1][2]== mat[2][2]==2):
        print("Player 2 won the game")
    elif (mat[0][0] == mat[1][1] == mat[2][2] == 2) or (mat[2][0] == mat[1][1] == mat[2][0] == 2) :
        print("Player 2 won the game")

    else:
        print("tie")

######################################################################################
# exersise 3
"""
Function gets from user a sentence
Function deletes duplicates letters and put instead
the of the duplicates letters
"""
def string_contraction():
    sentence= input("Enter sentence with duplicates letters\n")
    shortSentence=""
    counter=1
    if len(sentence)==1:
        shortSentence += sentence[0]
        shortSentence += str(counter)
        print("The short sentence with numbers is:")
        print(shortSentence)
    else:
        for i in range(len(sentence)-1):
            if sentence[i]==sentence[i+1]:
                counter+=1
            else:
                shortSentence+=sentence[i]
                shortSentence+=str(counter)
                counter=1
        shortSentence += sentence[i+1]
        shortSentence += str(counter)
        print("The short sentence with numbers is:")
        print(shortSentence)

######################################################################################
# exersise 4
"""
Function gets an ID
Function checks validity of a given ID
"""
def roundNum(num):
    num = num+(10-num%10)
    return num

def checkIDValidity(id):
    sum=0
    checker=1
    if len(id)>9 or id==" ":
        print("Invalid ID ")
    for i in range(len(id)-1):
        sumOfNum= checker*int(id[i])
        if sumOfNum>9:
            sumOfNum=sumOfNum%10+int(sumOfNum/10)
        sum+=sumOfNum
        if checker==1:
            checker=2
        else:
            checker=1
    digit=roundNum(sum)-sum
    print(sum)
    print(digit)
    if digit==int(id[len(id)-1]):
        print("Valid ID!!!")
    else:
        print("Invalid ID-2")
######################################################################################
# exersise 5
"""
Function that implement Map function
"""
def tempF(num):
    newNum=num**num
    return newNum
def map(tempF,list):
    return [tempF(ele) for ele in list]
######################################################################################
# exersise 6
"""
Function gets 2 numbers: num1,num2
The function returns the multiply of num1 and num2
"""
@DecoratorCache
def multiply(num1,num2):
    if num1 == 0 or num2 == 0:
        return 0
    return multiply(num1, num2 - 1) + num1
######################################################################################

def main():
    print ("Welcome to Ofek's sigit project")
     
    #exersise 1
    print("exersise 1")
    sum=sumOfListA()
    print("The sum of the numbers is: {} ".format(sum))

    sum2=sumOfListB()
    print("The sum of the numbers in list is: {} ".format(sum2))
    print("----------------------------------------------")

#######################################################################################
    #exersise 2
    print("exersise 2")
    mat =   array([[1,2,0],
                   [2,1,0],
                   [2,1,1]])
    tictactoe(mat)
    print("----------------------------------------------")

#######################################################################################
# exersise 3
    print("exersise 3")
    string_contraction()
    print("----------------------------------------------")
#######################################################################################
# exersise 4

    print("exersise 4")
    id=input("Please enter your ID:")
    checkIDValidity(id)
    print("----------------------------------------------")
#######################################################################################
# exersise 5
    print("exersise 5")
    list=[2,4,6,8]
    print("The old list is: ")
    print(list)
    list=map(tempF,list)
    print("The new list is: ")
    print(list)
    print("----------------------------------------------")

#######################################################################################
# exersise 6
    print("exersise 6")
    num1=int(input("Enter first operand to multiply: "))
    num2=int(input("Enter second operand to multiply: "))
    print("{0} * {1} = {2} ".format(num1,num2,multiply(num1,num2)))
    print("Cached Results: ", multiply)
    num2=int(input("Enter second operand to multiply: "))
    print("{0} * {1} = {2} ".format(num1,num2,multiply(num1,num2)))
    print("Cached Results: ", multiply)
    print("----------------------------------------------")


if __name__ == '__main__':
    main()
