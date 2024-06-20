import os
import sys

def restart_script(num_lines):
    for _ in range(num_lines):
        # Move the cursor up one line and clear it
        sys.stdout.write("\033[F")  # Move cursor up one line
        sys.stdout.write("\033[K")  # Clear the line
    sys.stdout.flush()  # Ensure the commands are executed immediately
    
    # Full path to the Python executable
    python_executable = sys.executable
    
    # Full path to the script
    script_path = os.path.abspath(sys.argv[0])
    
    # Restart the script
    os.execv(python_executable, [python_executable, script_path] + sys.argv[1:])

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

    print("[0] nice!nano")
    print("[1] XIAO BLE nrf52840")
    usrMCUchoice = input("Select MCU: ")

    # Convert the user input to an integer
    try:
        usrMCUchoice = int(usrMCUchoice)
        
        if usrMCUchoice == 0:
            usrMCUchoice = "nice!nano"
            print(usrMCUchoice)
            # sets nice!nano as the mcu
        elif usrMCUchoice == 1:
            usrMCUchoice = "XIAO BLE nrf52840"
            print(usrMCUchoice)
            # sets the xiaoble as the mcu
        else:
            print("Invalid selection")
    except ValueError:
        print("Please enter a valid number [between 0 & 1]")

    return isSplit, usrKeyboardName, usrMCUchoice

def file_creation(split, kbdnm, mcuSelec):
    #put file & folder heiarchy creation here
    if issPlit == True:
        #create files with regards to a split keyboard
        print(split)
        print(kbdnm)
    elif issPlit == False:
        #create files with regards to a monoblock keyboard
        print(split)
        print(kbdnm)
    else:
        print("something went wrong. please restart the script")

def matrix_generation(rows,cols,transform):
    #put matrix generation stuff here
    pass

issPlit, keyboardName, mcuChoice = user_input() 
print (f"MCU: {mcuChoice} \nKeyboard Name: {keyboardName} \nSplit?: {issPlit}") 
userConfirmation = input("Is this correct? (y/n) : ")
if userConfirmation == 'y':
    file_creation(issPlit,keyboardName)
elif userConfirmation == 'n':
    print("restarting script")
    restart_script(15)
else: 
    print("something went wrong. restart the script.")