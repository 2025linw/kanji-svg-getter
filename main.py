import os
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

    if not os.path.isdir("./animCJK"):
        print("Unable to find animCJK git repo folder, exiting...")
        return

    if not os.path.isdir("./assets"):
        print("Couldn't find an `assets` folder, creating an `assets` folder...")
        os.mkdir("./assets")

    print("Type the kanji after the `>` then press `ENTER`")

    running = True
    delete = False
    while running:
        user_input = input("> ")
        user_input = user_input.split()

        if len(user_input) == 0:
            continue

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

                    with open(filename, "r") as src, open("./assets/{}.svg".format(char), "w") as dest:
                        skip = False

                        while True:
                            line = src.readline()

                            if line == '':
                                break

                            if line == "svg.acjk path[clip-path] {\n":
                                skip = True
                                dest.write("/* ")

                            if line == "svg.acjk path[id] {fill:#ccc;}\n":
                                line = "svg.acjk path[id] {fill:#000;}"

                            dest.write(line.rstrip('\n'))

                            if skip and line == "}\n":
                                skip = False
                                dest.write(" */")

                            dest.write("\n")

    if delete:
        print("Deleting svg's in assets folder")
        for file in find_pat("*.svg", "./assets"): # Remove all svg files
            os.remove(file)

    print("Exiting...")

if __name__ == "__main__":
    main()
