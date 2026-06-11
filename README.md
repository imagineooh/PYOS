# TameOS, the fully python virtual operating system


This is, above all, a learning experience. I do not, and did not expect to make a fully optimised virtual OS software. The code is mainly a proof of concept, and is based on real systems and subsystems. The OS is fully written and designed by hand after thorough research through pretty much any resource and technology I could find and harness to learn, which also helped me discover new optimisation techniques. 
And, don’t forget, the project is just getting started.

## Functionalities
- Full Host OS (windows for now) TameOS communication, fully safe
- FIFO scheduler (working to refactor on CPU-based scheduling)
- Directory and FileSystem (working on Inode)
- Context and REPL, with commands help function
- ProcessControlBlock to track active and inactive slots (used for scheduling)
- Process Manager working on precise data packaging to decrypt and encrypt data (works on Cpython concepts)
\\For a full list of all commands, simply type help after running either repl.py or main.py (repl safer for now, testing is based there)

## How it works:
TameOS functions on a working, fully custom-made shell (shell->repl.py, made with custom function inspection for faster metadata analysis and dispatch), custom made file system and directory, built on an Inode manager. The inode’s main job is to format the files in ram, so that the process manager (which runs files) maps exactly to the data it needs. 
The process manager is the central piece of the computing unit: it dispatches the different multi pointers to threads, which run .txt, .wav and most importantly .exe files from the host OS. Once the files are migrated, TameOS takes full responsibility of file security and memory management for those files, as they do not require the user to fetch directly from the OS (TameOS does that on a separate thread automatically). There is a custom pager for inter-memory communication that was put in place, and handles migration between disk (non volatile memory) and RAM (volatile memory), and some portions of RAM are allocated to internal systems that ensure the proper functioning of the processing and filing. 
For thread and CPU security, a custom made system monitor (with thread ID tracker) tracks cpu usage vs expected max usage, and has custom made exceptions to halt processes and save CPU performance. 

## Struggles:
The main struggles were getting the opening of executable files and and saving to local TameOS memory, as you will be able to see in the commit log history. 
Dependency injection was also a struggle, as inter-communicating three separate systems with internal subsystems was a mess, and the use of OOP for this very struggle was mandatory.

## GIT history:
I recommend taking a look into the commit history for this project, as well as comments, as you can see my journey in learning this project.


## Final note:

This project took A LOT of my time, and I hope you will find it as exciting as me to discover the magical world of Virtual Operating System sandboxes. I am always free to contact on the issue or discussion if you want to contribute to this adventure, or simply as a question! 

Thank you,
Imagineooh

