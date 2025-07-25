# gui.py
import flet as ft
import json
from sorter import sort_files, load_config, save_config
from Test_files import lazy_files

CONFIG_PATH = "config.json"

def main(page: ft.Page):
    page.title = "File Sorter UI"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20

    config = load_config()
    langs = config["langs"]
    download_path = config.get("download_path", "")

    path_input = ft.TextField(label="Dossier à trier", value=download_path, adaptive=True)
    log_box = ft.ListView(
        controls=[],
        expand=True,
        auto_scroll=True,
    )
    log_container = ft.Container(
        content=log_box,
        height=410,
        bgcolor=ft.Colors.with_opacity(0.08, ft.Colors.ON_SURFACE),  # fond sombre doux
        border_radius=10,
        padding=10
    )

    language_dropdown = ft.Dropdown(
        label="Langue",
        options=[ft.dropdown.Option(l["code"], l["name"]) for l in langs.values()],
        value=next(k for k, v in langs.items() if v["selected"])
    )

    def enregistrer_config():
        selected_lang = language_dropdown.value
        path = path_input.value.strip() # type: ignore
        if not path:
            raise ValueError("Le chemin du dossier ne peut pas être vide.")
        for lang in langs.values():
            lang["selected"] = lang["code"] == selected_lang

        config["download_path"] = path
        save_config(config)

    def lancer_tri(e):
        enregistrer_config()
        log_box.controls.clear()
        log_box.controls.append(ft.Text("⏳ Lancement du tri..."))
        page.update()

        try:
            logs = sort_files()
            for line in logs:
                log_box.controls.append(ft.Text(line))
        except Exception as err:
            log_box.controls.append(ft.Text(f"[ERREUR] {err}", color=ft.Colors.RED))

        page.update()

    def generer_fichiers(e):
        log_box.controls.clear()
        log_box.controls.append(ft.Text("⏳ Génération des fichiers de test..."))
        page.update()

        try:
            logs = lazy_files()
            for line in logs:
                log_box.controls.append(ft.Text(line))
        except Exception as err:
            log_box.controls.append(ft.Text(f"[ERREUR] {err}", color=ft.Colors.RED))
        page.update()

    page.add(
        ft.Text("Interface de tri de fichiers", size=22, weight=ft.FontWeight.BOLD),
        path_input,
        language_dropdown,
        ft.Row(
            [
                ft.ElevatedButton("Lancer le tri", on_click=lancer_tri),
                ft.ElevatedButton("Générer des fichiers de test", on_click=generer_fichiers)
            ],
            alignment=ft.MainAxisAlignment.START
        ),
        ft.Text("Logs :", size=16, weight=ft.FontWeight.BOLD),
        log_container
    )

ft.app(target=main)
