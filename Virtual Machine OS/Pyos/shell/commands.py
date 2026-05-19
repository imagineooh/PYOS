def help(command:str=None):
    commands_help = {
        "mkdir": "Adds a single folder with no first file name",
        "mkdirfull": "Adds a single file with first file name",
        "lsram": "Prints ram"
    }
    if command is not None:
        print(commands_help[command])
    else:
        print('For specific help on a command, type help <command>')
        print(f"Documented commands: {', '.join(x for x in list(commands_help.keys()))}")


