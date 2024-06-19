import os

def user_input():
    usrKeyboardName = input ("Enter the keyboard name: ")
    #print ("Keyboard name is: " + keyboardName)

    isSplit = input("is this a split keyboard? (y/n): ")
    if isSplit == "y":
        isSplit = True
        #print("split keyboard generation")
    elif isSplit == "n" : 
        isSplit = False
        #print("monoblock keyboard generation")
    else:
        print ("Invalid input, Please answer with 'y' or 'n'")

    return isSplit, usrKeyboardName

def file_creation(issPlit):
    #put file & folder heiarchy creation here
    if issPlit == true:
        #create files with regards to a split keyboard
    elif issPlit == false:
        #create files with regards to a monoblock keyboard

def matrix_generation(rows,cols,transform):
    #put matrix generation stuff here




issPlit, keyboardName = user_input() 
print (f"Keyboard Name: {keyboardName},  \nSplit?: {issPlit}")