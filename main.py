import os
import re
import sys
from pathlib import Path

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
    elif isSplit == "n" : 
        isSplit = False
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
            #print(usrMCUchoice)
            # sets nice!nano as the mcu
        elif usrMCUchoice == 1:
            usrMCUchoice = "XIAO BLE nrf52840"
            #print(usrMCUchoice)
            # sets the xiaoble as the mcu
        else:
            print("Invalid selection")
    except ValueError:
        print("Please enter a valid number [between 0 & 1]")

    return isSplit, usrKeyboardName, usrMCUchoice

def fill_files(split, kbdnm):
    if split == True:
        user_values={
            "kbdnm":kbdnm,
            "cols":cols,
            "rows":rows
        }
        print("filling files for a split keyboard")
        #fill split files with the correct info
    elif split == False:
        pass
        print("Filling files for a unibody keyboard")
        #fill unibody files with the correct info
    else:
        print("something went wrong, please restart the script")

def file_creation(split, kbdnm):
    #put file & folder heiarchy creation here
    #create folder structure here:

    current_directory = Path.cwd()
    current_directory.joinpath(kbdnm).mkdir(parents=True,exist_ok=True)
    print(f"Creating files in: {current_directory}/{kbdnm}")          
    zmk_folders = [
        kbdnm,
        kbdnm+"/.github/workflows", 
        kbdnm+"/config/boards/shields/"+kbdnm]

    for folder in zmk_folders:
        folder_path = current_directory / folder
        try:
            folder_path.mkdir(parents=True, exist_ok=True)
            print(f"Successfully created: {folder_path}")
        except OSError as error:
            print(f"Error creating {folder_path}: {error}")

    open(Path.cwd()/kbdnm/"build.yaml",'w')
    print("Successfully created: build.yaml")
    open(Path.cwd()/kbdnm/".github/workflows/build.yml",'w')
    print("Successfully created: build.yml")
    open(Path.cwd()/kbdnm/"config/west.yml",'w')
    print("Successfully created: west.yml")

    if issPlit == True:
        #create files for a split keyboard
        splitFiles = [
            'Kconfig.shield',
            'Kconfig.defconfig',
            f'{kbdnm}.conf',
            f'{kbdnm}.dtsi',
            f'{kbdnm}.zmk.yml',
            f'{kbdnm}_left.conf',
            f'{kbdnm}_left.overlay',
            f'{kbdnm}_right.conf',
            f'{kbdnm}_right.overlay'
        ]
        working_directory = os.path.join(kbdnm,"config","boards","shields",kbdnm)

        for thing in splitFiles:
            file_path = os.path.join(working_directory, thing)
            try:
                with open(file_path, 'w'):  # Open the file in write mode to create it
                    pass  # Do nothing, just create the file
                print(f"Successfully created: ~/{file_path}")
            except OSError as error:
                print(f"Error creating ~/{file_path}: {error}")

    elif issPlit == False:
        #create files for a unibody keyboard
        unibodyFiles = [
            'Kconfig.shield',
            'Kconfig.defconfig',
            f'{kbdnm}.overlay',
            f'{kbdnm}.keymap'
        ]
        working_directory = os.path.join(kbdnm,"config","boards","shields",kbdnm)

        for thing in unibodyFiles:
            file_path = os.path.join(working_directory, thing)
            try:
                with open(file_path, 'w'):  # Open the file in write mode to create it
                    pass  # Do nothing, just create the file
                print(f"Successfully created: ~/{file_path}")
            except OSError as error:
                print(f"Error creating ~/{file_path}: {error}")

        fill_files(issPlit, kbdnm)

    else:
        print("something went wrong. please restart the script")

def matrix_generation(rows,cols):
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