import os
import re
import sys
import tempfile
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

def find_file_in_directory(filename, directory='.'):
    """
    Recursively search for a file in the specified directory and its subfolders.
    Returns the full path if found, else None.
    """
    # Use case-insensitive search with glob
    for path in Path(directory).rglob('*'):
        if path.is_file() and path.name.lower() == filename.lower():
            return path
    return None

def process_boilerplate(issplit, kbdnm, mcu, cols, rows, matr):
    replacements = {'kbdnm': kbdnm,
                    'kbdnm.caps':kbdnm.upper(), 
                    'mcu':mcu,
                    'cols':cols,
                    'rows':rows,
                    'matrix gen':matr
                    }
                
    if cols is not None:
        replacements['cols'] = str(cols)
    if rows is not None:
        replacements['rows'] = str(rows)

    # Read the boilerplate file content
    input_file = 'boiler.plate'
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            content = file.read()
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        return
    except Exception as e:
        print(f"Error reading '{input_file}': {e}")
        return

    # Replace placeholders in the entire content
    for key, value in replacements.items():
        if key.endswith('.caps'):
            original_key = key[:-5]  # Remove .caps suffix
            placeholder = f'{{{key}}}'
            value = value.upper()
        else:
            placeholder = f'{{{key}}}'
        
        content = content.replace(placeholder, value)

    # Temporarily write modified content to a temp file
    temp_filename = 'temp_boilerplate.tmp'
    try:
        with open(temp_filename, 'w', encoding='utf-8') as temp_file:
            temp_file.write(content)
    except Exception as e:
        print(f"Error writing temporary file '{temp_filename}': {e}")
        return

    # Read from the temporary file
    try:
        with open(temp_filename, 'r', encoding='utf-8') as file:
            temp_content = file.read()
    except Exception as e:
        print(f"Error reading temporary file '{temp_filename}': {e}")
        return
    
    # Determine the patterns to match
    if issplit:
        patterns = ['base', 'split']
    else:
        patterns = ['base', 'unibody']

    # Find matching sections in the temporary content
    matches = []
    for pattern in patterns:
        matches.extend(re.findall(rf'\[\[\[{pattern} (.*?) start\]\]\](.*?)\[\[\[{pattern} \1 end\]\]\]', temp_content, re.DOTALL))

    if not matches:
        print("No matching sections found in the boilerplate file.")
        return

    print(f"Matches found: {matches}")

    # Process each match and overwrite the corresponding file if not empty
    for match in matches:
        filename, file_content = match
        filename = filename.strip()
        file_content = file_content.strip()
        
        target_path = find_file_in_directory(filename)
        
        if not target_path:
            print(f"File '{filename}' not found.")
            continue

        print(f"Overwriting file: {target_path}")
        
        try:
            with open(target_path, 'w', encoding='utf-8') as target_file:
                target_file.write(file_content + '\n')
            print(f"Successfully overwritten {target_path}.")
        except Exception as e:
            print(f"Error overwriting '{target_path}': {e}")

    # Leave the temporary file for inspection
    print(f"Temporary file created: {temp_filename}")

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
            usrMCUchoice = "nice_nano_v2"
            #print(usrMCUchoice)
            # sets nice!nano as the mcu
        elif usrMCUchoice == 1:
            usrMCUchoice = "seeeduino_xiao_ble"
            #print(usrMCUchoice)
            # sets the xiaoble as the mcu
        else:
            print("Invalid selection")
    except ValueError:
        print("Please enter a valid number [between 0 & 1]")

    #userRows = input("enter the number of Rows in your keyboard: ")
    userCols = input("enter the number of Columns in your keyboard: ")

    return isSplit, usrKeyboardName, usrMCUchoice, userCols

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

def matrix_generation(kle_json, num_cols):
    """
    Generate a key matrix from a Keyboard Layout Editor (KLE) JSON file.
    
    Args:
    kle_json (str): The path to the KLE JSON file.
    num_cols (int): Number of columns to organize the keys into.
    
    Returns:
    list: A 2D list representing the ZMK key matrix.
    """
    with open(kle_json, 'r') as file:
        layout = json.load(file)
    
    keys = []
    for item in layout:
        if isinstance(item, list):
            for subitem in item:
                if isinstance(subitem, str):
                    keys.append(subitem)
    
    # Calculate number of rows needed based on total keys and desired columns
    num_rows = (len(keys) + num_cols - 1) // num_cols
    
    # Initialize the matrix
    matrix = []
    key_index = 0

    for row_index in range(num_rows):
        current_row = []
        for col_index in range(num_cols):
            if key_index < len(keys):
                current_row.append(f"RC({row_index},{col_index})")
                key_index += 1
        matrix.append(current_row)

    matrix_str = ""

    for row_index in range(num_rows):
        current_row = []
        for col_index in range(num_cols):
            key_index = row_index * num_cols + col_index
            if key_index < len(keys):
                current_row.append(f"RC({row_index},{col_index})")
        matrix_str += " ".join(current_row) + "\n"
    
    return matrix_str, num_rows

issPlit, keyboardName, mcuChoice, uCols = user_input() 
print (f"MCU: {mcuChoice} \nKeyboard Name: {keyboardName} \nSplit?: {issPlit}") 
userConfirmation = input("Is this correct? (y/n) : ")
if userConfirmation == 'y':
    file_creation(issPlit, keyboardName)
    uMatrix, uRows = matrix_generation(userKLE, uCols)
    process_boilerplate(issPlit, keyboardName, mcuChoice, uCols, uRows, uMatrix)
elif userConfirmation == 'n':
    print("restarting script")
    restart_script(15)
else: 
    print("something went wrong. restart the script.")