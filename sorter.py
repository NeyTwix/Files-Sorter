import os, shutil, sys
import colorama as col
from pathlib import Path
from datetime import datetime

if os.name != 'nt':
    print(f"{col.Fore.WHITE}{col.Back.RED}[!] This script is intended to run on Windows.{col.Style.RESET_ALL}")
    sys.exit(1)

col.init()

print(f"{col.Fore.WHITE}{col.Style.BRIGHT}Nesquik Sorter{col.Style.RESET_ALL}")
print(f"{col.Fore.WHITE}{col.Style.BRIGHT}Version: 1.0{col.Style.RESET_ALL}")
print(f"{col.Fore.WHITE}{col.Style.BRIGHT}Author: Nesquik{col.Style.RESET_ALL}")
print(f"{col.Fore.WHITE}{col.Style.BRIGHT}Github: https://github.com/NeyTwix{col.Style.RESET_ALL}")
print(f"{col.Fore.WHITE}{col.Style.BRIGHT}Discord: ney_twix{col.Style.RESET_ALL}")
print()
print(f"{col.Fore.WHITE}[?] Checking for config file..{col.Style.RESET_ALL}")

APPDATA_PATH = os.getenv('APPDATA')
if not APPDATA_PATH:
    print(f"{col.Fore.WHITE}{col.Back.RED}[!] APPDATA environment variable not found."+col.Style.RESET_ALL)
    sys.exit(1)

os.makedirs(os.path.join(APPDATA_PATH, "Nesquik"), exist_ok=True)

if not os.path.exists(os.path.join(APPDATA_PATH, "Nesquik", "config_sort.nsk")):
    DL_PATH = input(f"""{col.Fore.YELLOW}[?] Config file not found.
    Enter 'd' or 'default' to use the default Downloads folder.
    Or enter a custom path to sort: {col.Style.RESET_ALL}""")
    if not DL_PATH:
        print(f"{col.Fore.WHITE}{col.Back.RED}[!] No path specified."+col.Style.RESET_ALL)
        sys.exit(1)
    if DL_PATH.lower() == "d" or DL_PATH.lower() == "default":
        DL_PATH = os.path.join(str(Path.home()), "Downloads") + '\\'
    if DL_PATH[-1] != '\\':
        DL_PATH += '\\'
    if not os.path.exists(DL_PATH):
        print(f"{col.Fore.WHITE}{col.Back.RED}[!] Path {DL_PATH} does not exist.{col.Style.RESET_ALL}")
        sys.exit(1)
    else:
        with open(os.path.join(APPDATA_PATH, "Nesquik", "config_sort.nsk"), 'w') as config_file:
            config_file.write(f"DL_PATH:{DL_PATH}")
else:
    with open(os.path.join(APPDATA_PATH, "Nesquik", "config_sort.nsk"), 'r') as config_file:
        line = config_file.readline().strip()
        if not line or ":" not in line:
            print(f"{col.Fore.WHITE}{col.Back.RED}[!] Invalid config file format.{col.Style.RESET_ALL}")
            sys.exit(1)
        DL_PATH = line.split(":", 1)[1]
        if not DL_PATH:
            print(f"{col.Fore.WHITE}{col.Back.RED}[!] No path specified in config file.")
            sys.exit(1)
        if not os.path.exists(DL_PATH):
            print(f"{col.Fore.WHITE}{col.Back.RED}[!] Path {DL_PATH} from config file does not exist.{col.Style.RESET_ALL}")
            sys.exit(1)

log_dir = os.path.join(APPDATA_PATH, "Nesquik", "logs")
os.makedirs(log_dir, exist_ok=True)
log_file = open(os.path.join(log_dir, f"sorter_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.nsklog"), 'w')

log_file.write(f"Log created on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
log_file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Checking for config file..\n")
log_file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Config file found.\n")
log_file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Download Path: {DL_PATH}\n")

print(f"{col.Fore.WHITE}[?] Download Path: {col.Fore.MAGENTA}{DL_PATH}{col.Style.RESET_ALL}")
if not os.path.exists(DL_PATH):
    print(f"{col.Fore.WHITE}{col.Back.RED}[!] Path {DL_PATH} does not exist.{col.Style.RESET_ALL}")
    sys.exit(1)

fold_names=["Images","Docs","Videos","Audio","Archives","Apps", "Dev"]
app_ext_list = ["exe", "msi", "lnk"]
img_ext_list = ["png", "bmp", "jpg", "jpeg", "gif", "mdc", "tiff", "webp", "webm", "tif", "thumb", "jpe", "jfif", "ico", "heif", "heic"]
vid_ext_list = ["mp4", "avi", "mkv", "mp4v", "mov", "m4v", "asf"]
song_ext_list = ["mp3","flac","ogg","m3u","m3u8","m4a","tts","wav"]
docs_ext_list = ["pdf", "odt", "doc", "txt", "gdoc", "xls", "xlxs", "pptx", "docx"]
arch_ext_list = ["gz", "rar", "zip", "7z", "jar", "iso"]
dev_ext_list = ["py", "js", "json", "java", "lua", "ini", "sk"]

os.chdir(DL_PATH)
os.makedirs(fold_names[0], 511, True)
os.makedirs(fold_names[1], 511, True)
os.makedirs(fold_names[2], 511, True)
os.makedirs(fold_names[3], 511, True)
os.makedirs(fold_names[4], 511, True)
os.makedirs(fold_names[5], 511, True)
os.makedirs(fold_names[6], 511, True)
os.makedirs("SubFolders", 511, True,)

print(f"{col.Fore.WHITE}[?] Starting..{col.Style.RESET_ALL}")
log_file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Starting..\n")
found_list = os.listdir()
for elem in found_list:
    log_file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Found {elem}\n")
    try:
        if elem in fold_names or elem == "SubFolders" or elem == "desktop.ini":
            log_file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Skipping {elem}\n")
            continue
        if elem.split(".")[-1].lower() in img_ext_list and os.path.exists(DL_PATH+elem):
            shutil.move(DL_PATH+elem,DL_PATH+fold_names[0]+"/")
            print(f"{col.Fore.GREEN}[+] File {col.Fore.MAGENTA}{elem} moved in {fold_names[0]}{col.Style.RESET_ALL}")
            log_file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Moved {elem} in {fold_names[0]}\n")
        elif elem.split(".")[-1].lower() in docs_ext_list and os.path.exists(DL_PATH+elem):
            shutil.move(DL_PATH+elem,DL_PATH+fold_names[1]+"/")
            print(f"{col.Fore.GREEN}[+] File {col.Fore.MAGENTA}{elem} moved in {fold_names[1]}{col.Style.RESET_ALL}")
            log_file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Moved {elem} in {fold_names[1]}\n")
        elif elem.split(".")[-1].lower() in vid_ext_list and os.path.exists(DL_PATH+elem):
            shutil.move(DL_PATH+elem,DL_PATH+fold_names[2]+"/")
            print(f"{col.Fore.GREEN}[+] File {col.Fore.MAGENTA}{elem} moved in {fold_names[2]}{col.Style.RESET_ALL}")
            log_file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Moved {elem} in {fold_names[2]}\n")
        elif elem.split(".")[-1].lower() in song_ext_list and os.path.exists(DL_PATH+elem):
            shutil.move(DL_PATH+elem,DL_PATH+fold_names[3]+"/")
            print(f"{col.Fore.GREEN}[+] File {col.Fore.MAGENTA}{elem} moved in {fold_names[3]}{col.Style.RESET_ALL}")
            log_file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Moved {elem} in {fold_names[3]}\n")
        elif elem.split(".")[-1].lower() in arch_ext_list and os.path.exists(DL_PATH+elem):
            shutil.move(DL_PATH+elem,DL_PATH+fold_names[4]+"/")
            print(f"{col.Fore.GREEN}[+] File {col.Fore.MAGENTA}{elem} moved in {fold_names[4]}{col.Style.RESET_ALL}")
            log_file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Moved {elem} in {fold_names[4]}\n")
        elif elem.split(".")[-1].lower() in app_ext_list and os.path.exists(DL_PATH+elem):
            shutil.move(DL_PATH+elem,DL_PATH+fold_names[5]+"/")
            print(f"{col.Fore.GREEN}[+] File {col.Fore.MAGENTA}{elem} moved in {fold_names[5]}{col.Style.RESET_ALL}")
            log_file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Moved {elem} in {fold_names[5]}\n")
        elif elem.split(".")[-1].lower() in dev_ext_list and os.path.exists(DL_PATH+elem):
            shutil.move(DL_PATH+elem,DL_PATH+fold_names[6]+"/")
            print(f"{col.Fore.GREEN}[+] File {col.Fore.MAGENTA}{elem} moved in {fold_names[6]}{col.Style.RESET_ALL}")
            log_file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Moved {elem} in {fold_names[6]}\n")
        elif os.path.isdir(DL_PATH+elem) and os.path.exists(DL_PATH+elem):
            shutil.move(DL_PATH+elem,DL_PATH+"SubFolders/")
            print(f"{col.Fore.GREEN}[+] Folder {col.Fore.MAGENTA}{elem} moved in SubFolders{col.Style.RESET_ALL}")
            log_file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Moved {elem} in SubFolders\n")
        elif elem.split(".")[-1].lower() == "crdownload":
            print(f"{col.Fore.RED}[~] File {col.Fore.MAGENTA}{elem} not moved.{col.Style.RESET_ALL}")
            log_file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - File {elem} not moved.\n")
        else:
            print(f"{col.Fore.RED}[~] File {col.Fore.MAGENTA}{elem} not moved.{col.Style.RESET_ALL}")
            log_file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - File {elem} not moved.\n")
    except Exception as e:
        print(f"{col.Fore.WHITE}{col.Back.RED}[!] An error as Occured with file {col.Fore.MAGENTA}{elem} : {e}{col.Style.RESET_ALL}")
        log_file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - An error as Occured with file {elem} : {e}\n")
print(f"{col.Fore.GREEN}[O] Done ! :){col.Style.RESET_ALL}")
log_file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Done ! :)\n")
log_file.close()
sys.exit(0)