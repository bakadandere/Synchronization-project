from filecmp import dircmp
from datetime import datetime
import time
import os
import shutil
import argparse


class ArgumentParser:
    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser(prog='Synchronization Program', description='Synchronize replica folder with the Source folder')
        self.parser.add_argument('-source', metavar='<Input Dir>', type=str, nargs=1, required=True, help='Input source folder path')
        self.parser.add_argument('-target', metavar='<Input Dir>', type=str, nargs=1, required=True, help='Input target folder path')
        self.parser.add_argument('-interval', metavar='<Sync Interval>', type=float, nargs=1, required=True, help='Input time interval for Synchronization')
        self.parser.add_argument('-IO', metavar='<Sync Interval unit>', type=str, nargs=1, required=False, default='m', help='Sync time unit [Possible time unit: m(minute) h(hour) d(day)]')
        self.parser.add_argument('-log', metavar='<Log File>', type=str, required=False, default='Logfile', help='Log file name')


class FILE:
    def __init__(self,name, source_path, target_path) -> None:
        self.name = name
        self.source_path = source_path
        self.target_path = target_path

class Sync:
    def __init__(self, source_path, target_path) -> None:
        self.source_path = source_path
        self.target_path = target_path
        self.dcmp = dircmp(source_path,target_path)
        self.diff_files_list = []
        self.file_in_source = []
        self.file_in_target = []
        self.dir_in_source = []
        self.dir_in_target = []

    def diff_files(self):
        self._diff_files_recursion(self.dcmp)

    def _diff_files_recursion(self, dcmp): # Find files with same name but different content
        for name in dcmp.diff_files:
            self.diff_files_list.append(FILE(name, dcmp.left, dcmp.right))

        for name in dcmp.left_only: # Find files or dirs that are only in Source folder
            path = dcmp.left + '\\' + name
            if os.path.isfile(path):
                self.file_in_source.append(FILE(name, dcmp.left, dcmp.right))
            else:
                self.dir_in_source.append(FILE(name, dcmp.left, dcmp.right))

        for name in dcmp.right_only: # Find files or dirs that are only in target folder
            path = dcmp.right + '\\' + name
            if os.path.isfile(path):
                self.file_in_target.append(FILE(name, dcmp.left, dcmp.right))
            else:
                self.dir_in_target.append(FILE(name, dcmp.left, dcmp.right))

        for sub_dcmp in dcmp.subdirs.values():
            self._diff_files_recursion(sub_dcmp)

    def print_list(self):
        print('\nModified File(s):')
        if len(self.diff_files_list) != 0:
            for item in self.diff_files_list:
                print(item.name,item.source_path,item.target_path)
        else:
            print('None')

        print('\nFile(s) only in Source:')
        if len(self.file_in_source) != 0:
            for item in self.file_in_source:
                print(item.name, item.source_path, item.target_path)
        else:
            print('None')

        print('\nDir(s) only in Source:')
        if len(self.dir_in_source) != 0:
            for item in self.dir_in_source:
                print(item.name, item.source_path, item.target_path)
        else:
            print('None')
        
        print('\nFile(s) only in Target:')
        if len(self.file_in_target) != 0:
            for item in self.file_in_target:
                print(item.name, item.source_path, item.target_path)
        else:
            print('None')

        print('\nDir(s) only in Target:')
        if len(self.dir_in_target) != 0:
            for item in self.dir_in_target:
                print(item.name, item.source_path, item.target_path)
        else:
            print('None')
    
    def Overwrite(self):
        if len(self.diff_files_list) != 0:
            print('Copy and overwrite modified File(s)')
            for file in self.diff_files_list:
                shutil.copy(file.source_path +'\\'+ file.name, self.target_path)
            self.diff_files_list.clear()
        else:
            print('No modified File(s) to overwrite')

        if len(self.file_in_source) != 0:
            print('Copy File(s) only in Source')
            for file in self.file_in_source:
                shutil.copy(file.source_path +'\\'+ file.name, file.target_path)
            self.file_in_source.clear()
        else:
            print('No new File(s) to update')

        if len(self.dir_in_source) != 0:
            print('Copy Dirs only in Source')
            for dir in self.dir_in_source:
                shutil.copytree(dir.source_path + '\\' + dir.name, dir.target_path + '\\' + dir.name)
            self.dir_in_source.clear()
        else:
            print('No new Dir(s) to update')

        if len(self.file_in_target) != 0:
            print('Delete File(s) in Target')
            for file in self.file_in_target:
                os.remove(file.target_path +'\\'+ file.name)
            self.file_in_target.clear()
        else:
            print('No redundant File(s) in target')
        
        if len(self.dir_in_target) != 0:
            print('Delete Dir(s) in Target')
            for dir in self.dir_in_target:
                shutil.rmtree(dir.target_path + '\\' + dir.name)
            self.dir_in_target.clear()
        else:
            print('No redundant Dir(s) in target')

class Interval:
    def __init__(self, time, unit) -> None:
        self.time = time
        self.unit = unit

    def get_Interval(self):
        if self.unit == 'm':
            return self.time*60
        elif self.unit == 'h':
            return self.time*3600
        elif self.unit == 'd':
            return self.time*86400
        else:
            raise Exception('Wrong time unit! [Possible time unit: m(minute) h(hour) d(day)]')
        
    def get_day(self):
        pass

class Log:
    def __init__(self, filename) -> None:
        self.file_name = filename + '.txt'
        self.log_date =None
        self.log_time = None
        self.logging = None

    def Write(self, diff_files_list, file_in_source, file_in_target, dir_in_source, dir_in_target):
        self.logging = open(self.file_name, "a")
        self.log_date = datetime.now().strftime('%d/%m/%Y')
        self.log_time = datetime.now().strftime('%H:%M:%S')
        self.logging.write(f'###############Sync on {self.log_date} at {self.log_time}###############\n')

        #Logging modifed files
        self.logging.write('Modifies File(s):\n')
        if len(diff_files_list) != 0:
            for item in diff_files_list:
                self.logging.write(f'{item.name} found in {item.source_path} and {item.target_path}\n')
        else:
            self.logging.write('None\n')
        
        #Logging files only in source
        self.logging.write('File(s) only in Source:\n')
        if len(file_in_source) != 0:
            for item in file_in_source:
                self.logging.write(f'{item.name} found in {item.source_path}\n')
        else:
            self.logging.write('None\n')

        #Logging files only in target
        self.logging.write('File(s) only in Target:\n')
        if len(file_in_target) != 0:
            for item in file_in_target:
                self.logging.write(f'{item.name} found in {item.target_path}\n')
        else:
            self.logging.write('None\n')

        #Logging dirs only in source
        self.logging.write('Dir(s) only in Source:\n')
        if len(dir_in_source) != 0:
            for item in dir_in_source:
                self.logging.write(f'{item.name} found in {item.source_path}\n')
        else:
            self.logging.write('None\n')

        #Logging dirs only in target
        self.logging.write('Dir(s) only in  Target:\n')
        if len(dir_in_target) != 0:
            for item in dir_in_target:
                self.logging.write(f'{item.name} found in {item.target_path}\n')
        else:
            self.logging.write('None\n')
        self.logging.write('\n')
        print('Logging Done !\n')

def main():
    args = ArgumentParser().parser.parse_args()

    Time = Interval(args.interval[0], args.IO).get_Interval()
    Log_file = Log(args.log)
    while(True):
        Sync_files = Sync(args.source[0], args.target[0])
        Sync_files.diff_files()
        Sync_files.print_list()
        Log_file.Write(Sync_files.diff_files_list, Sync_files.file_in_source, Sync_files.file_in_target, Sync_files.dir_in_source, Sync_files.dir_in_target)
        Sync_files.Overwrite()
        time.sleep(Time)

if __name__=='__main__':
    main()