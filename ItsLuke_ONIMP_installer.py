import requests
import customtkinter as ctk
import os
import ctypes.wintypes

def getfolder(folder_path,install_button):
    CSIDL_PERSONAL = 5       # My Documents
    SHGFP_TYPE_CURRENT = 0   # Get current, not default value

    buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
    ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_PERSONAL, None, SHGFP_TYPE_CURRENT, buf)
    global folder
    folder = ctk.filedialog.askdirectory(initialdir=buf.value)
    if folder != "":
        folder_path.set(folder)
        install_button.pack(pady=5)
        os.chdir(folder)

def install(app):
    filelist = ["ONI_MP.dll","mod.yaml","mod_info.yaml"]
    localmoddir = f"{folder}/Klei/OxygenNotIncluded/mods/local/oni_mp/"
    os.makedirs(localmoddir,exist_ok=True)
    for file in filelist:
        raw_url = f"https://raw.githubusercontent.com/Lyraedan/Oxygen_Not_Included_Multiplayer/main/mod/oni_mp/{file}"
        response = requests.get(raw_url)
        try:
            with open(f"{localmoddir}{file}", "wb") as f:
                f.write(response.content)
            f.close()
            print(f"{localmoddir}{file}  downloaded/updated")
        except Exception as e:
            print(f"{localmoddir}{file} wasn't successfully saved. Close the game if it's running and check your antivirus! Error: {e}")
            
def main():
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    app = ctk.CTk()
    
    app.title("ItsLuke's ONI multiplayer mod installer/updater")
    
    folder_path = ctk.StringVar(app)
    crfmlbl = ctk.CTkLabel(app,text="This installer was made by: magicnothief").pack()
    clbl = ctk.CTkLabel(app,text="You can see debug text in the console window.").pack()
    flbl= ctk.CTkLabel(app,text="1. Select your main documents folder (e.g. c:/Users/username/Documents)!").pack(pady=5)
    folder_button = ctk.CTkButton(app,command=lambda:getfolder(folder_path,install_button), text="Select folder").pack(pady=0)
    lbl1 = ctk.CTkLabel(master=app,textvariable=folder_path).pack(pady=5)
    install_button = ctk.CTkButton(app,command=lambda:install(app),text="Install/Update")
    
    #Set installer default  size
    app.geometry("800x480")

    #Start application
    app.mainloop()
    
if __name__ == "__main__":
    main()