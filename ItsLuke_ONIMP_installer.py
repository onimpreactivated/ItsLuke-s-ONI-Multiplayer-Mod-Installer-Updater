import requests
import customtkinter as ctk
import os
import ctypes.wintypes

def getfolder(folder_path):
    CSIDL_PERSONAL = 5       # My Documents
    SHGFP_TYPE_CURRENT = 0   # Get current, not default value

    buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
    ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_PERSONAL, None, SHGFP_TYPE_CURRENT, buf)
    global folder
    folder = ctk.filedialog.askdirectory(initialdir=buf.value)
    if folder != "":
        folder_path.set(folder)
        os.chdir(folder)

def getcredential(credential_path, install_button):
    global filec
    filec = ctk.filedialog.askopenfilename()
    if filec != "":
        credential_path.set(filec)
        install_button.pack(pady=5)

def install(app):
    filelist = ["Google.Apis.Auth.dll","Google.Apis.Core.dll","Google.Apis.dll","Google.Apis.Drive.v3.dll","mod_info.yaml", "mod.yaml","multiplayer_settings.json","Newtonsoft.Json.dll","ONI_MP.dll"]
    localmoddir = f"{folder}/Klei/OxygenNotIncluded/mods/local/oni_mp/"
    os.makedirs(localmoddir,exist_ok=True)
    for file in filelist:
        raw_url = f"https://raw.githubusercontent.com/onimpreactivated/ItsLuke-s-ONI-Multiplayer-Mod-Installer-Updater/oni_mp/{file}"
        response = requests.get(raw_url)
        try:
            with open(f"{localmoddir}{file}", "wb") as f:
                f.write(response.content)
            f.close()
            print(f"{localmoddir}{file}  downloaded/updated")
        except Exception as e:
            print(f"{localmoddir}{file} wasn't successfully saved. Close the game if it's running and check your antivirus! Error: {e}")
    if filec == "credentials.json.json":
        os.rename(filec,filec[0:-21]+"credentials.json")
    os.replace(f"{filec}",f"{localmoddir}/credentials.json")
def main():
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    app = ctk.CTk()
    
    app.title("ItsLuke's ONI multiplayer mod installer/updater")
    
    folder_path = ctk.StringVar(app)
    credential_path = ctk.StringVar(app)
    crfmlbl = ctk.CTkLabel(app,text="This installer was made by: magicnothief").pack()
    clbl = ctk.CTkLabel(app,text="You can see debug text in the console window.").pack()
    flbl= ctk.CTkLabel(app,text="1. Select your main documents folder (e.g. c:/Users/username/Documents)!").pack(pady=5)
    folder_button = ctk.CTkButton(app,command=lambda:getfolder(folder_path), text="Select documents").pack(pady=0)
    lbl1 = ctk.CTkLabel(master=app,textvariable=folder_path).pack(pady=5)
    clbl= ctk.CTkLabel(app,text="2. Select your credential file (credentials.json").pack(pady=5)
    credential_button = ctk.CTkButton(app,command=lambda:getcredential(credential_path,install_button), text="Select credentials.json").pack(pady=0)
    clbl1 = ctk.CTkLabel(master=app,textvariable=credential_path).pack(pady=5)
    install_button = ctk.CTkButton(app,command=lambda:install(app),text="Install/Update")
    
    #Set installer default  size
    app.geometry("800x480")

    #Start application
    app.mainloop()
    
if __name__ == "__main__":
    main()