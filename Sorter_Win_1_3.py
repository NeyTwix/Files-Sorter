import os, shutil, sys
import colorama as col
from pathlib import Path
from datetime import datetime
from pystyle import Center, Colors, Colorate

if os.name != 'nt':
    print(f"{col.Fore.WHITE}{col.Back.RED}[!] This script is intended to run on Windows.{col.Style.RESET_ALL}")
    sys.exit(1)

col.init()

print(Colorate.Horizontal(Colors.blue_to_green, f"""
      :::::::::: ::::::::::: :::        :::::::::: ::::::::          ::::::::   ::::::::  ::::::::: ::::::::::: :::::::::: ::::::::: 
     :+:            :+:     :+:        :+:       :+:    :+:        :+:    :+: :+:    :+: :+:    :+:    :+:     :+:        :+:    :+: 
    +:+            +:+     +:+        +:+       +:+               +:+        +:+    +:+ +:+    +:+    +:+     +:+        +:+    +:+  
   :#::+::#       +#+     +#+        +#++:++#  +#++:++#++        +#++:++#++ +#+    +:+ +#++:++#:     +#+     +#++:++#   +#++:++#:    
  +#+            +#+     +#+        +#+              +#+               +#+ +#+    +#+ +#+    +#+    +#+     +#+        +#+    +#+    
 #+#            #+#     #+#        #+#       #+#    #+#        #+#    #+# #+#    #+# #+#    #+#    #+#     #+#        #+#    #+#     
###        ########### ########## ########## ########          ########   ########  ###    ###    ###     ########## ###    ###      
                                                                                                                        by Nesquik""", 1))
print(Center.XCenter(Colorate.Horizontal(Colors.blue_to_green, f"Version: 1.3", 1)))
print(Center.XCenter(Colorate.Horizontal(Colors.blue_to_green,f"Github: https://github.com/NeyTwix", 1)))
print()
print(f"{col.Fore.WHITE}[?] Checking for config file..{col.Style.RESET_ALL}")

APPDATA_PATH = os.getenv('APPDATA')
if not APPDATA_PATH:
    print(f"{col.Fore.WHITE}{col.Back.RED}[!] APPDATA environment variable not found."+col.Style.RESET_ALL)
    sys.exit(1)

DATA_PATH = os.path.join(APPDATA_PATH, "Nesquik", "Files_Sorter")

os.makedirs(DATA_PATH, exist_ok=True)

if not os.path.exists(os.path.join(DATA_PATH, "config_sort.nsk")):
    while True:
        DL_PATH = input(f"""{col.Fore.YELLOW}[?] Config file not found.
        Enter 'd' or 'default' to use the default Downloads folder.
        Or enter a custom path to sort: {col.Style.RESET_ALL}""")
        if not DL_PATH:
            print(f"{col.Fore.WHITE}{col.Back.RED}[!] No path specified.{col.Style.RESET_ALL}")
        elif DL_PATH.lower() in ["d", "default"]:
            DL_PATH = os.path.join(str(Path.home()), "Downloads") + '\\'
            break
        elif not os.path.exists(DL_PATH):
            print(f"{col.Fore.WHITE}{col.Back.RED}[!] Path {DL_PATH} does not exist.{col.Style.RESET_ALL}")
        else:
            if DL_PATH[-1] != '\\':
                DL_PATH += '\\'
            break
    if not os.path.exists(DL_PATH):
        print(f"{col.Fore.WHITE}{col.Back.RED}[!] Path {DL_PATH} does not exist.{col.Style.RESET_ALL}")
        sys.exit(1)
    else:
        with open(os.path.join(DATA_PATH, "config_sort.nsk"), 'w') as config_file:
            config_file.write(f"DL_PATH:{DL_PATH}")
else:
    with open(os.path.join(DATA_PATH, "config_sort.nsk"), 'r') as config_file:
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

log_dir = os.path.join(DATA_PATH, "logs")
os.makedirs(log_dir, exist_ok=True)

log_file_path = os.path.join(log_dir, f"sorter_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.nsklog")
with open(log_file_path, 'w') as log_file:
    log_file.write(f"Log created on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    log_file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Checking for config file..\n")
    log_file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Config file found.\n")
    log_file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Download Path: {DL_PATH}\n")

    print(f"{col.Fore.WHITE}[?] Download Path: {col.Fore.MAGENTA}{DL_PATH}{col.Style.RESET_ALL}")
    if not os.path.exists(DL_PATH):
        print(f"{col.Fore.WHITE}{col.Back.RED}[!] Path {DL_PATH} does not exist.{col.Style.RESET_ALL}")
        sys.exit(1)



    print(f"{col.Fore.WHITE}[?] Starting..{col.Style.RESET_ALL}")
    log_file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Starting..\n")

    ext_to_folder = {
        "Images": ["png", "bmp", "jpg", "jpeg", "gif", "mdc", "tiff", "webp", "webm", "tif", "thumb", "jpe", "jfif", "ico", "heif", "heic", "svg", "raw", "indd", "ai", "eps", "psd", "xcf", "cdr", "emf", "wmf"],
        "Docs": ["pdf", "odt", "doc", "txt", "gdoc", "xls", "xlsx", "pptx", "docx", "dotx", "dotm", "dot", "docm", "rtf", "wps", "wpd", "csv", "tsv", "epub", "mobi", "tex", "bib", "ppt", "odp", "ods"],
        "Videos": ["mp4", "avi", "mkv", "mp4v", "mov", "m4v", "asf", "wmv", "flv", "webm", "3gp", "3g2", "m2ts", "mts", "ts", "vob", "ogv", "rm", "rmvb", "divx", "xvid"],
        "Audio": ["mp3", "flac", "ogg", "m3u", "m3u8", "m4a", "tts", "wav", "wma", "aac", "opus", "aiff", "aif", "au", "snd", "cda", "alac", "amr", "mid", "midi"],
        "Archives": ["gz", "rar", "zip", "7z", "jar", "iso", "tar", "gz", "bz2", "xz", "lz", "lzo", "zst", "lz4", "xz", "z", "cab", "arj", "bz2"],
        "Apps": ["exe", "msi", "lnk", "bat", "cmd", "com", "scr", "pif", "cpl", "msp", "reg", "dll", "sys", "drv", "ocx", "vxd", "cpl", "msc", "mspx", "apk", "app", "dmg", "deb", "rpm"],
        "Dev": ["py", "js", "json", "java", "lua", "ini", "sk", "jar", "cpp", "c", "h", "hpp", "cs", "html", "css", "php", "sql", "xml", "yaml", "yml", "ts", "tsx", "jsx", "sh", "bat", "md", "go", "rs", "swift", "kt", "dart", "rb", "pl", "r", "ipynb"],
        "Fonts": ["ttf", "otf", "woff", "woff2", "eot"],
        "3D": ["obj", "fbx", "stl", "dae", "blend", "gltf", "glb"],
        "Design": ["fig", "sketch", "xd", "psd", "ai"],
    }

    fold_names = [key for key in ext_to_folder.keys()] + ["SubFolders"]

    os.chdir(DL_PATH)
    found_list = os.listdir()

    # Vérifier les fichiers à déplacer avant de créer les dossiers
    folder_files_map = {folder: [] for folder in ext_to_folder.keys()}
    folder_files_map["SubFolders"] = []

    for elem in found_list:
        if elem in fold_names or elem == "desktop.ini":
            continue

        file_ext = elem.split(".")[-1].lower()
        moved = False

        for folder, ext_list in ext_to_folder.items():
            if file_ext in ext_list and os.path.exists(DL_PATH + elem):
                folder_files_map[folder].append(elem)
                moved = True
                break

        if not moved and os.path.isdir(DL_PATH + elem) and os.path.exists(DL_PATH + elem):
            folder_files_map["SubFolders"].append(elem)

    # Créer les dossiers uniquement s'il y a des fichiers à y déplacer
    for folder, files in folder_files_map.items():
        if files:
            if not os.path.exists(DL_PATH + folder):
                os.makedirs(folder, 511, True)
                log_file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Created folder {folder}\n")
            else:
                log_file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Folder {folder} already exists\n")

    # Déplacer les fichiers dans les dossiers correspondants
    for folder, files in folder_files_map.items():
        for elem in files:
            try:
                shutil.move(DL_PATH + elem, DL_PATH + folder + "/")
                print(f"{col.Fore.GREEN}[+] File {col.Fore.MAGENTA}{elem}{col.Fore.GREEN} moved in {col.Fore.MAGENTA}{folder}{col.Style.RESET_ALL}")
                log_file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Moved {elem} in {folder}\n")
            except Exception as e:
                print(f"{col.Fore.RED}[!] Error moving {col.Fore.MAGENTA}{elem}: {e}{col.Style.RESET_ALL}")
                log_file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Error moving {elem}: {e}\n")

    print(f"{col.Back.GREEN}{col.Fore.WHITE}[O] Done ! :){col.Style.RESET_ALL}")
    log_file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Done ! :)\n")
log_file.close()
sys.exit(0)