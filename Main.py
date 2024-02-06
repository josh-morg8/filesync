import hashlib
import os
import shutil
import time
import logging
from pathlib import Path



#User input and instructions
source_folder = input("Enter Source Folder Path ")
parent = Path(source_folder).resolve().parents[0]
replica_folder = input("Enter Replica Folder Path or enter 'no' to ignore. ")
if replica_folder == "no":
    replica_folder = f"{parent}/replica/"
else:
    replica_folder = input("")
log_file = input("Enter Log File Path or enter 'no' to ignore. ")
if log_file == "no":
    log_file = f"{parent}/logs.log/"
else:
    log_file = input("")
time_interval = int(input("Synchronization: Enter time interval (sec): "))


#Program mechanism
def sync():

    if not os.path.isdir(source_folder):
        input("The source folder doesn't exist. Enter source folder Path: ")
        os.makedirs(source_folder)

    if not os.path.isdir(replica_folder):
        os.makedirs(replica_folder)


    while True:
        time.sleep(time_interval)
        try:
            print(f"Start with parameters:\nsource:{source_folder}\nreplica:{replica_folder}\nlog:{log_file}\ntime_interval:{time_interval}\n")
            date_2()


        except KeyboardInterrupt:
            print("The Program is terminated manually!")
            raise SystemExit


#Hash mechanism
def c_files(file1, file2):
        with open(file1, "rb") as f1, open(file2, "rb") as f2:
            return hashlib.md5(f1.read()).hexdigest() == hashlib.md5(f2.read()).hexdigest()


#File syncronization mechanism
def date_2():
    os.chdir(source_folder)
    s_items = sorted(filter(os.path.isfile, os.listdir(source_folder)), key=os.path.getmtime)
    s_dir = sorted(filter(os.path.isdir, os.listdir(source_folder)), key=os.path.getmtime)
    [s_items.append(i) for i in s_dir]
    os.chdir(replica_folder)
    r_items = sorted(filter(os.path.isfile, os.listdir(replica_folder)), key=os.path.getmtime)
    r_dir = sorted(filter(os.path.isdir, os.listdir(replica_folder)), key=os.path.getmtime)
    [r_items.append(i) for i in r_dir]
    for files in s_items:
        source_file_path = os.path.join(source_folder, files)
        replica_file_path = os.path.join(replica_folder, files)
        if files not in r_items:
            shutil.copytree(source_folder, replica_folder, dirs_exist_ok=True)
            log_mes = f'Name: {files}: File has been Copied.'
            logging.info(log_mes)
            print(log_mes)
        else:
            try:
                c_files(source_file_path, replica_file_path)
                log_mes = f'Name: {files}: File is up to date. '
                logging.info(log_mes)
                print(log_mes)
            except IsADirectoryError:
                log_mes = f'Name: {files}: File is up to date. '
                logging.info(log_mes)
                print(log_mes)
    for files in r_items:
        if files not in s_items:
            log_mes = f'Name: {files}: File has been deleted.'
            try:
                shutil.rmtree(files)
            except NotADirectoryError:
                os.remove(files)
            logging.info(log_mes)
            print(log_mes)

#Logs Mechanism 
def log():
    if not log_file:
        logging.basicConfig(filename=log_file, format=f'%(asctime)s %(message)s\n', filemode='w')
    else:
        logging.basicConfig(filename=log_file, format=f'%(asctime)s %(message)s\n', filemode='a')

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logging.info(f"Start with parameters:\nsource:{source_folder}\nreplica:{replica_folder}\nlog:{log_file}\ntime_interval:{time_interval}\n")

log()
sync()
















