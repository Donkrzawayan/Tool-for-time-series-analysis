from sys import argv

import analizing_tool


if __name__ == '__main__':
    choice = 1
    if len(argv) > 1:
        choice = argv[1]
    if choice == 1:
        analizing_tool.ruptures()
    else:
        pass
