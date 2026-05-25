def help(command:str=None):
    commands_help = {
        "mkdir": "Adds a single folder with no first file name",
        "mkdirfull": "Adds a single file with first file name",
        "lsram": "Prints ram",
        "help": "Help function for the TameOS. Type help <command> for specific command, or help to list all commands",
        "mod": "Edit file in ram",
        "write": "Stores value in disk",
        "ramstage": "Migrates objects in disk to ram",
        "df": "returns percentage use of ram",
        "pidasync": "updates PID for all objects in ram",
        "idlescan": "Tracks inactive slots in RAM",
        "purge": "Deletes inactive slots in ram",
        "next": "returns index of next process to run",
        "sched": "schedules next processess to run",
        "exec": "executes next process to run. Has blueprint (file_name, process_extensions, process_name)",
        "malloc": "allocates RAM area to object",
        "lsdisk": 'Prints Disk ',
        "deldata": "deletes the data for a folder, but keeps the folder as inactive in ram.",
        "hostex":"executes path from the host os",
        "hostmig":"migrates objects from host os to ram",
        "comem":"Enables or Disables auto communication between RAM and Disk, if enabled, finished ram processes will automatically be written to Disk",
        "refpopstat":"refreshes the population status of ram",
        "popstat":'outputs population status of ram'
    }
    if command is not None:
        if command in commands_help:
            print(commands_help[command])
        else:
            print("Command might not exist, or no documentation is given for it")
    else:
        print('For specific help on a command, type help <command>')
        print(f"Documented commands: {', '.join(x for x in list(commands_help.keys()))}")


