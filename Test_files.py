import os, random, json, shutil
from pathlib import Path

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")

def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def lazy_files():
    logs = []
    config = load_config()

    dl_path = config.get("download_path", "").strip()
    if not dl_path or not os.path.exists(dl_path):
        raise FileNotFoundError(f"Dossier de téléchargement invalide : {dl_path}")

    ext_to_folder = config.get("includes", {})
    if not ext_to_folder:
        raise ValueError("Aucun type de fichier configuré pour le tri.")

    logs.append(f"🗂️ Creation de fichiers dans : {dl_path}")


    # patch
    base_dir = dl_path

    # Create the base directory if it doesn't exist
    os.makedirs(base_dir, exist_ok=True)

    # Generate random files in the base directory
    for folder, extensions in ext_to_folder.items():
        for _ in range(15):  # Create 4 files per category
            file_name = f"file_{random.randint(1000, 9999)}.{random.choice(extensions)}"
            file_path = os.path.join(base_dir, file_name)
            with open(file_path, "w") as f:
                f.write("This is a test file.")
            logs.append(f"📄 Fichier créé : {file_name}")
    for _ in range(8):  # Create 4 files per category
        random_folder_name = f"folder_{random.randint(1000, 9999)}"
        folder_path = os.path.join(base_dir, random_folder_name)
        os.makedirs(folder_path, exist_ok=True)
        logs.append(f"📂 Dossier créé : {random_folder_name}")
    logs.append("✅ Fichiers générés avec succès.")
    return logs
