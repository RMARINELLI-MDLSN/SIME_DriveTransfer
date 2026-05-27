import json
import tkinter as tk
from tkinter import filedialog, messagebox

from drive_client import GoogleDriveClient

CONFIG_FILE = "config.json"


class App:

    def __init__(self, root):

        self.root = root
        self.root.title("Google Drive Sync")

        self.load_config()

        # ==========================================
        # FILE LOCALE
        # ==========================================

        tk.Label(
            root,
            text="File Locale"
        ).grid(
            row=0,
            column=0,
            padx=10,
            pady=10
        )

        self.local_file_var = tk.StringVar(
            value=self.config.get("local_file", "")
        )

        tk.Entry(
            root,
            textvariable=self.local_file_var,
            width=60
        ).grid(
            row=0,
            column=1
        )

        tk.Button(
            root,
            text="Sfoglia",
            command=self.select_file
        ).grid(
            row=0,
            column=2,
            padx=10
        )

        # ==========================================
        # GOOGLE DRIVE FOLDER ID
        # ==========================================

        tk.Label(
            root,
            text="Google Drive Folder ID"
        ).grid(
            row=1,
            column=0,
            padx=10,
            pady=10
        )

        self.folder_var = tk.StringVar(
            value=self.config.get("drive_folder_id", "")
        )

        tk.Entry(
            root,
            textvariable=self.folder_var,
            width=60
        ).grid(
            row=1,
            column=1
        )

        # ==========================================
        # OVERWRITE
        # ==========================================

        self.overwrite_var = tk.BooleanVar(
            value=self.config.get("overwrite", True)
        )

        tk.Checkbutton(
            root,
            text="Sovrascrivi file esistente",
            variable=self.overwrite_var
        ).grid(
            row=2,
            column=1,
            pady=10
        )

        # ==========================================
        # BOTTONE TEST AUTH
        # ==========================================

        tk.Button(
            root,
            text="Test Autenticazione",
            bg="orange",
            fg="black",
            width=20,
            command=self.test_auth
        ).grid(
            row=3,
            column=0,
            pady=20
        )

        # ==========================================
        # BOTTONE SYNC
        # ==========================================

        tk.Button(
            root,
            text="Sincronizza",
            bg="green",
            fg="white",
            width=20,
            command=self.sync
        ).grid(
            row=3,
            column=1,
            pady=20
        )

    # ==========================================
    # SELEZIONE FILE
    # ==========================================

    def select_file(self):

        filename = filedialog.askopenfilename()

        self.local_file_var.set(filename)

    # ==========================================
    # LOAD CONFIG
    # ==========================================

    def load_config(self):

        try:

            with open(CONFIG_FILE, "r") as file:
                self.config = json.load(file)

        except:
            self.config = {}

    # ==========================================
    # SAVE CONFIG
    # ==========================================

    def save_config(self):

        self.config["local_file"] = self.local_file_var.get()
        self.config["drive_folder_id"] = self.folder_var.get()
        self.config["overwrite"] = self.overwrite_var.get()

        with open(CONFIG_FILE, "w") as file:
            json.dump(self.config, file, indent=4)

    # ==========================================
    # TEST AUTENTICAZIONE
    # ==========================================

    def test_auth(self):

        try:

            client = GoogleDriveClient()

            messagebox.showinfo(
                "Autenticazione OK",
                "Login Google completato e token creato correttamente!"
            )

        except Exception as e:

            messagebox.showerror(
                "Errore autenticazione",
                str(e)
            )

    # ==========================================
    # SINCRONIZZAZIONE FILE
    # ==========================================

    def sync(self):

        try:

            self.save_config()

            client = GoogleDriveClient()

            client.upload_file(
                local_file=self.local_file_var.get(),
                folder_id=self.folder_var.get(),
                overwrite=self.overwrite_var.get()
            )

            messagebox.showinfo(
                "Successo",
                "Upload completato!"
            )

        except Exception as e:

            messagebox.showerror(
                "Errore",
                str(e)
            )


# ==========================================
# AVVIO APP
# ==========================================

root = tk.Tk()

root.geometry("850x250")

app = App(root)

root.mainloop()