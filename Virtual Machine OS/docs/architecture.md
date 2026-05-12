```
Virtual Machine OS/
│
├── Pyos/                        # Main package
│   ├── __init__.py
│   ├── __main__.py              # Entry point — runs the shell
│   │
│   ├── memory/                  
│   │   ├── __init__.py
│   │   └── ram.py
│   │   └── storage.py
│   │
│   ├── process/                 # Process Manager
│   │   ├── __init__.py
│   │   ├── pcb.py               # ProcessControlBlock data structure
│   │   ├── scheduler.py         # Ready queue, tick logic
│   │   └── manager.py           # The main ProcessManager class
│   │
│   ├── fs/                      # File System
│   │   ├── __init__.py
│   │   ├── inode.py             # Inode structure
│   │   ├── directory.py         # Directory tree logic
│   │   └── filesystem.py        # Main FileSystem class
│   │
│   ├── shell/                   # Shell / REPL
│   │   ├── __init__.py
│   │   ├── repl.py              # Input loop and dispatcher
│   │   ├── commands.py          # Individual command handlers
│   │   └── context.py           # Session state (cwd, current user, etc.)
│   │
│   └── editor/                  # Vim-like editor
│       ├── __init__.py
│       ├── buffer.py            # Line buffer, cursor logic
│       ├── modes.py             # Normal / Insert / Command mode
│       └── editor.py            # Main Editor class
│
├── tests/
│   ├── test_memory.py
│   ├── test_process.py
│   ├── test_fs.py
│   └── test_shell.py
│
├── docs/
│   └── ARCHITECTURE.md          
│
├── pyproject.toml               # Packaging config
├── README.md
├── CONTRIBUTING.md
└── LICENSE
```

## Low level orga
# 11/05/2026
RAM can only be modified by Inode (and sometimes PCB), and can be accessed (without modification) by filesystem. This gives a 2 degree security layer.
