import os
import random

ext_to_folder = {
    "Images": ["png", "bmp", "jpg", "jpeg", "gif", "mdc", "tiff", "webp", "webm", "tif", "thumb", "jpe", "jfif", "ico", "heif", "heic", "svg", "raw", "indd", "ai", "eps", "psd", "xcf", "cdr", "emf", "wmf"],
    "Docs": ["pdf", "odt", "doc", "txt", "gdoc", "xls", "xlsx", "pptx", "docx", "dotx", "dotm", "dot", "docm", "rtf", "wps", "wpd", "csv", "tsv", "epub", "mobi", "tex", "bib", "ppt", "odp", "ods"],
    "Videos": ["mp4", "avi", "mkv", "mp4v", "mov", "m4v", "asf", "wmv", "flv", "webm", "3gp", "3g2", "m2ts", "mts", "ts", "vob", "ogv", "rm", "rmvb", "divx", "xvid"],
    "Audio": ["mp3", "flac", "ogg", "m3u", "m3u8", "m4a", "tts", "wav", "wma", "aac", "opus", "aiff", "aif", "au", "snd", "cda", "alac", "amr", "mid", "midi"],
    "Archives": ["gz", "rar", "zip", "7z", "jar", "iso", "tar", "tar.gz", "tar.bz2", "tar.xz", "tar.lz", "tar.lzo", "tar.zst", "tar.lz4", "xz", "z", "cab", "arj", "bz2"],
    "Apps": ["exe", "msi", "lnk", "bat", "cmd", "com", "scr", "pif", "cpl", "msp", "reg", "dll", "sys", "drv", "ocx", "vxd", "cpl", "msc", "mspx", "apk", "app", "dmg", "deb", "rpm"],
    "Dev": ["py", "js", "json", "java", "lua", "ini", "sk", "jar", "cpp", "c", "h", "hpp", "cs", "html", "css", "php", "sql", "xml", "yaml", "yml", "ts", "tsx", "jsx", "sh", "bat", "md", "go", "rs", "swift", "kt", "dart", "rb", "pl", "r", "ipynb"],
    "Fonts": ["ttf", "otf", "woff", "woff2", "eot"],
    "3D": ["obj", "fbx", "stl", "dae", "blend", "gltf", "glb"],
    "Design": ["fig", "sketch", "xd", "psd", "ai"],
}
# Base directory to create files and folders
base_dir = "E:\\Telechargement"

# Create the base directory if it doesn't exist
os.makedirs(base_dir, exist_ok=True)

# Generate random files in the base directory
for folder, extensions in ext_to_folder.items():
    for _ in range(15):  # Create 4 files per category
        file_name = f"file_{random.randint(1000, 9999)}.{random.choice(extensions)}"
        file_path = os.path.join(base_dir, file_name)
        with open(file_path, "w") as f:
            f.write("This is a test file.")
for _ in range(8):  # Create 4 files per category
    random_folder_name = f"folder_{random.randint(1000, 9999)}"
    folder_path = os.path.join(base_dir, random_folder_name)
    os.makedirs(folder_path, exist_ok=True)
        
