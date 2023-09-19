# Synchronization-project
Synchronizing 2 folders

The program does the following tasks:

- Overwrite files with the same name but different in content

- Files/Dirs that only exist in source folder are copied into target folder

- Files/Dirs that only exist in target folder are deleted

- Log the process into a txt file

Run the following command in the cmd terminal to see all available arguments:

python .\sync.py -h

Example command: 

python .\sync.py -source C:\Users\phamh\OneDrive\Desktop\Test\SYNC-master -target C:\Users\phamh\OneDrive\Desktop\Test\Sync_prj -interval 0.1 -log Logfile
