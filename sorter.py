# sorter.py
import os, shutil, json
from pathlib import Path

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")

def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_config(data):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def sort_files() -> list[str]:
    """Lance le tri des fichiers selon config.json et retourne une liste de logs texte."""
    logs = []
    config = load_config()

    dl_path = config.get("download_path", "").strip()
    if not dl_path or not os.path.exists(dl_path):
        raise FileNotFoundError(f"Dossier de téléchargement invalide : {dl_path}")

    ext_to_folder = config.get("includes", {})
    if not ext_to_folder:
        raise ValueError("Aucun type de fichier configuré pour le tri.")

    logs.append(f"🗂️ Tri des fichiers dans : {dl_path}")
    print(f"🗂️ Tri des fichiers dans : {dl_path}")
    os.chdir(dl_path)
    found_list = os.listdir()

    folder_files_map = {folder: [] for folder in ext_to_folder}
    folder_files_map["SubFolders"] = []

    for elem in found_list:
        full_path = os.path.join(dl_path, elem)
        file_ext = elem.split(".")[-1].lower() if "." in elem else ""
        moved = False

        for folder, ext_list in ext_to_folder.items():
            if file_ext in ext_list and os.path.isfile(full_path):
                folder_files_map[folder].append(elem)
                moved = True
                break

        # Ignore folders that have the same name as a destination folder
        if not moved and os.path.isdir(full_path) and elem not in ext_to_folder and elem != "SubFolders":
            folder_files_map["SubFolders"].append(elem)

    for folder, files in folder_files_map.items():
        if not files:
            continue
        folder_path = os.path.join(dl_path, folder)
        os.makedirs(folder_path, exist_ok=True)
        logs.append(f"📁 Dossier vérifié/créé : {folder}")
        print(f"📁 Dossier vérifié/créé : {folder}")

        for elem in files:
            try:
                shutil.move(os.path.join(dl_path, elem), folder_path)
                logs.append(f"✅ Fichier déplacé : {elem} → {folder}")
                print(f"✅ Fichier déplacé : {elem} → {folder}")
            except shutil.Error as e:
                if "already exists" in str(e):
                    base, ext = os.path.splitext(elem)
                    i = 1
                    new_elem = f"{base}_{i}{ext}"
                    while os.path.exists(os.path.join(folder_path, new_elem)):
                        i += 1
                        new_elem = f"{base}_{i}{ext}"
                    shutil.move(os.path.join(dl_path, elem), os.path.join(folder_path, new_elem))
                    logs.append(f"🔄 Fichier renommé et déplacé : {elem} → {new_elem} dans {folder}")
                    print(f"🔄 Fichier renommé et déplacé : {elem} → {new_elem} dans {folder}")
                else:
                    logs.append(f"❌ Erreur déplacement {elem} : {e}")
                    print(f"❌ Erreur déplacement {elem} : {e}")
            except Exception as e:
                logs.append(f"❌ Erreur déplacement {elem} : {e}")
                print(f"❌ Erreur déplacement {elem} : {e}")

    logs.append("🎉 Tri terminé.")
    print("🎉 Tri terminé.")
    return logs
