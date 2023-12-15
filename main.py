import os
import shutil
import fnmatch

folder_loc = ["animCJK/svgsJa", "animCJK/svgsKana"]

def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)
        
def find_pat(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result

def main():
    print("Kanji SVG Getter")
    print("Type the kanji after the `>` then press `ENTER`")
    
    running = True
    delete = False
    while running:
        user_input = input("> ")
        user_input = user_input.split()
        
        match user_input[0]:
            case 'q':
                running = False
                
                if len(user_input) > 1 and user_input[1] == 'd':
                    delete = True
                    
                break
            case _:
                for char in user_input[0]: # Loop through each character in input
                    unicode = str(int(ord(char)))
                    
                    for folder in folder_loc: # Search through all folders for character
                        filename = find(unicode + ".svg", folder)
                        if filename:
                            break

                    if not filename: # Unable to find file with given character
                        print("Unable to find svg for {}".format(char))
                        continue
                
                    shutil.copyfile(filename, "./assets/{}.svg".format(char)) # Copy character into assets folder
    
    if delete:
        for file in find_pat("*.svg", "./assets"): # Remove all svg files
            os.remove(file)
            
    print("Exiting...")

if __name__ == "__main__":
    main()