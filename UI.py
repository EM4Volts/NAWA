import shutil
from pathlib import Path
import os, tkinter.messagebox
from tkinter import *
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, filedialog
from tkinter.colorchooser import askcolor
import lib_nawa as jout
import nawa, save, json




OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")

new=""
modList = []

conDir= ""

def check_names(path):
    if os.path.exists(os.path.dirname(path)):
        return True

if not os.path.isfile("configs/config.ini"):
    with open("configs/config.ini", "x"):
        print("config remade")
    with open(r'configs/config.ini', 'w') as cfg:
        cfg.write("%s\n" % str)
        cfg.write("%s\n" % str)

cfgFile = open("configs/config.ini", "r")
data = cfgFile.read()
config = data.split("\n")
cfgFile.close()
nierDatDir= config[0]
nierModsDir= config[1]
save_file = config[2]
cfgStruct = [nierDatDir, nierModsDir, save_file]


#DEAR READER, DONT EVEN READ FURTHER THEN THIS, THIS FILE IS A MESS. DO NOT ATTEMPT TO READ MORE THEN JUST A BIT HERE

def generateConfig():
    with open(r'configs/config.ini', 'w') as cfg:
        for str in cfgStruct:
            cfg.write("%s\n" % str)

def selectNierDataDir():
    global nierDatDir, nierModsDir, save_file
    global cfgStruct
    folder_selected = filedialog.askdirectory()
    nierDatDir = folder_selected
    cfgStruct = [nierDatDir, nierModsDir, save_file]
    generateConfig()
    return folder_selected + "/"


def select_save_file():
    global nierDatDir, nierModsDir, save_file
    global cfgStruct
    folder_selected = filedialog.askopenfile()
    save_file = folder_selected.name
    cfgStruct = [nierDatDir, nierModsDir, save_file]
    generateConfig()
    print(save_file)
    return folder_selected


def selectNierModsDir():
    global nierModsDir, nierDatDir, save_file
    global cfgStruct
    folder_selected = filedialog.askdirectory()
    nierModsDir = folder_selected
    cfgStruct = [nierDatDir, nierModsDir, save_file]
    return folder_selected + "/"

def genPathList(folder):
    mDir = os.listdir(folder)
    mDir2 = []
    for str in mDir:
        entry = str
        mDir2.append(entry)
    return mDir2

def buildModList():
    global modList
    modList = genPathList(nierModsDir)
    return modList

if check_names(nierModsDir):
    buildModList()

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

window = Tk()

window.geometry("1143x734")
window.configure(bg = "#3A7FF6")

def alertBox(str):
    tkinter.messagebox.showinfo("NAWA", str)

canvas = Canvas(
    window,
    bg = "#3A7FF6",
    height = 734,
    width = 1143,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
canvas.create_rectangle(
    0.0,
    0.0,
    1206.0,
    734.0,
    fill="#595959",
    outline="")
def key(event):
    global new, conDir
    try:
        new= lb.get(lb.curselection())
    except:
        pass
    conDir = nierModsDir + "/" + new + "/config.json"
    updateConfigWindow(conDir)

lb=Listbox(window,bg="#383838", height=22,width=93, foreground="white")
lb.place(x=0, y=0)
lb.bind('<<ListboxSelect>>',key)
def modListUpdate():
    lb.delete(0,END)
    buildModList()
    for str in modList:
        str2 = str
        lb.insert(0, str2)
if check_names(nierModsDir):
    modListUpdate()
canvas.create_rectangle(
    557.0,
    0.0,
    570.0,
    368.0,
    fill="#83796A",
    outline="")

canvas.create_rectangle(
    561.0,
    0.0,
    1143.0,
    387.0,
    fill="#464646",
    outline="")

canvas.create_rectangle(
    0.0,
    355.0,
    1143.0,
    410.0,
    fill="#83796A",
    outline="")


configU=Label(window, bg="#474747", fg='white', font=("RobotoRoman CondensedRegular", 36 * -1))
configU.place(x=571.0, y=15.0)
configU.config(text = "Select a Weapon to start")
canvas.create_rectangle(
    0.0,
    362.0,
    1143.0,
    678.0,
    fill="#383838",
    outline="")

canvas.create_rectangle(
    0.0,
    668.0,
    1143.0,
    728.0,
    fill="#83796A",
    outline="")

canvas.create_rectangle(
    0.0,
    672.0,
    1143.0,
    734.0,
    fill="#2E2E2E",
    outline="")

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0, fg="white", justify='center',
    command=lambda: updateConfigFile(),
    relief="flat"
)


variable = StringVar(window)
variable.set("Small Sword") # default value

config4 = OptionMenu(window,variable, "Large Sword", "Spear", "Small Sword", "Combat Bracers")
config4.configure(font=('RobotoRoman CondensedRegular',13), bg="#464646")
config4.place(x=742, y=275)
button_1.place(
    x=682.0,
    y=686.0,
    width=190.0,
    height=35.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0, fg="white", justify='center',
    command=lambda: [check_ifCfg(True)],
    relief="flat"
)
button_2.place(
    x=891.0,
    y=686.0,
    width=190.0,
    height=35.0
)

def del_wp():
    global save_file
    delList = open("configs/lastWP.txt", "r")
    data = delList.read()
    kewlWPIDDELLIST = data.split("\n")
    delList.close()
    if save_file.endswith(".dat"):          #check for valid save file, if yes remove weapons from it
        none_weapon_list = []
        for i in range(40):
            none_weapon_list.append(-1)                                   
        save_file_class = save.SAVE_FILE(save_file, none_weapon_list)
        save_file_class.write_save_file()

    for str in kewlWPIDDELLIST:
        try:
            print(f"removing {str}")
            os.remove(f"{nierDatDir}/wp/wp{str}.dat")
            os.remove(f"{nierDatDir}/wp/wp{str}.dtt")
            os.remove(f"{nierDatDir}/misctex/misctex_wp{str}.dat")
            os.remove(f"{nierDatDir}/misctex/misctex_wp{str}.dtt")
            os.remove(f"{nierDatDir}/effect/wp{str}.eff")
        except:
            print("skipping file")
    try:
        os.remove(f"{nierDatDir}/core/core.dat")
        os.remove(f"{nierDatDir}/core/coregm.dat")
        os.remove(f"{nierDatDir}/ui/ui_core_us.dat")
    except:
        print(" ")

def delConfirm():
    msg_box = tkinter.messagebox.askquestion('Remove NAWA', 'Are you sure you want to remove all mods added by NAWA from the game?',
                                        icon='warning')
    if msg_box == 'yes':
        del_wp()
        tkinter.messagebox.showinfo('Done!', 'All mods removed')
    else:
        print("Abort removal")


button_image_del = PhotoImage(
    file=relative_to_assets("delete.png"))
button_del = Button(
    image=button_image_del,
    borderwidth=0,
    highlightthickness=0, fg="white", justify='center',
    command=lambda: [delConfirm()],
    relief="flat"
)
button_del.place(
    x=1098.0,
    y=686.0,
    width=35.0,
    height=35.0
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0, fg="white", justify='center',
    command=lambda: [selectNierDataDir(), generateConfig(), check_ifCfg(False)],
    relief="flat"
)

button_3.place(
    x=12.0,
    y=686.0,
    width=190.0,
    height=35.0
)




button_image_save = PhotoImage(
    file=relative_to_assets("button_save.png"))
button_save = Button(
    image=button_image_save,
    borderwidth=0,
    highlightthickness=0, fg="white", justify='center',
    command=lambda: [select_save_file(), generateConfig(), check_ifCfg(False)],
    relief="flat"
)

button_save.place(
    x=450.0,
    y=686.0,
    width=190.0,
    height=35.0
)


button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0, fg="white", justify='center',
    command=lambda: [selectNierModsDir(),generateConfig(), modListUpdate(), check_ifCfg(False)],
    relief="flat"
)
button_4.place(
    x=221.0,
    y=686.0,
    width=190.0,
    height=35.0
)

canvas.create_text(
    19.0,
    615.0,
    anchor="nw",
    text="Level 4",
    fill="#FFFFFF",
    font=("RobotoRoman CondensedMedium", 16 * -1)
)

canvas.create_text(
    19.0,
    552.0,
    anchor="nw",
    text="Level 3",
    fill="#FFFFFF",
    font=("RobotoRoman CondensedMedium", 16 * -1)
)

canvas.create_text(
    19.0,
    489.0,
    anchor="nw",
    text="Level 2",
    fill="#FFFFFF",
    font=("RobotoRoman CondensedMedium", 16 * -1)
)

canvas.create_text(
    19.0,
    426.0,
    anchor="nw",
    text="Level 1",
    fill="#FFFFFF",
    font=("RobotoRoman CondensedMedium", 16 * -1)
)

canvas.create_text(
    94.0,
    392.0,
    anchor="nw",
    text="Min Damage",
    fill="#FFFFFF",
    font=("RobotoRoman CondensedMedium", 16 * -1)
)

canvas.create_text(
    221.0,
    392.0,
    anchor="nw",
    text="Max Damage",
    fill="#FFFFFF",
    font=("RobotoRoman CondensedMedium", 16 * -1)
)

canvas.create_text(
    363.0,
    392.0,
    anchor="nw",
    text="Light Combo",
    fill="#FFFFFF",
    font=("RobotoRoman CondensedMedium", 16 * -1)
)

canvas.create_text(
    490.0,
    392.0,
    anchor="nw",
    text="Heavy Combo",
    fill="#FFFFFF",
    font=("RobotoRoman CondensedMedium", 16 * -1)
)

canvas.create_text(
    644.0,
    392.0,
    anchor="nw",
    text="Speed",
    fill="#FFFFFF",
    font=("RobotoRoman CondensedMedium", 16 * -1)
)

canvas.create_text(
    577.0,
    82.0,
    anchor="nw",
    text="Weapon Name",
    fill="#FFFFFF",
    font=("RobotoRoman CondensedRegular", 20 * -1)
)

canvas.create_text(
    577.0,
    149.0,
    anchor="nw",
    text="Description",
    fill="#FFFFFF",
    font=("RobotoRoman CondensedRegular", 20 * -1)
)

canvas.create_text(
    577.0,
    217.0,
    anchor="nw",
    text="Long Description",
    fill="#FFFFFF",
    font=("RobotoRoman CondensedRegular", 20 * -1)
)

canvas.create_text(
    577.0,
    285.0,
    anchor="nw",
    text="Weapon Type",
    fill="#FFFFFF",
    font=("RobotoRoman CondensedRegular", 20 * -1)
)

canvas.create_text(
    664.0,
    329.0,
    anchor="nw",
    text="If you do not know what a value means leave it at its default.",
    fill="#FFFFFF",
    font=("RobotoItalic Condensed", 16 * -1)
)



canvas.create_text(
    762.0,
    392.0,
    anchor="nw",
    text="Endurance",
    fill="#FFFFFF",
    font=("RobotoRoman CondensedMedium", 16 * -1)
)

canvas.create_text(
    922.0,
    392.0,
    anchor="nw",
    text="Stun",
    fill="#FFFFFF",
    font=("RobotoRoman CondensedMedium", 16 * -1)
)

canvas.create_text(
    1058.0,
    392.0,
    anchor="nw",
    text="Crit",
    fill="#FFFFFF",
    font=("RobotoRoman CondensedMedium", 16 * -1)
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry1.png"))
entry_bg_1 = canvas.create_image(
    1070.0,
    624.5,
    image=entry_image_1
)
config36 = Entry(
    bd=0,
    bg="#353434",
    highlightthickness=0, fg="white", justify='center'
)
config36.place(
    x=1009.0,
    y=607.0,
    width=122.0,
    height=33.0
)

entry_image_2 = PhotoImage(
    file=relative_to_assets("entry1.png"))
entry_bg_2 = canvas.create_image(
    937.0,
    624.5,
    image=entry_image_2
)
config35 = Entry(
    bd=0,
    bg="#353434",
    highlightthickness=0, fg="white", justify='center'
)
config35.place(
    x=876.0,
    y=607.0,
    width=122.0,
    height=33.0
)

entry_image_3 = PhotoImage(
    file=relative_to_assets("entry1.png"))
entry_bg_3 = canvas.create_image(
    804.0,
    624.5,
    image=entry_image_3
)
config34 = Entry(
    bd=0,
    bg="#353434",
    highlightthickness=0, fg="white", justify='center'
)
config34.place(
    x=743.0,
    y=607.0,
    width=122.0,
    height=33.0
)

entry_image_4 = PhotoImage(
    file=relative_to_assets("entry1.png"))
entry_bg_4 = canvas.create_image(
    671.0,
    624.5,
    image=entry_image_4
)
config33 = Entry(
    bd=0,
    bg="#353434",
    highlightthickness=0, fg="white", justify='center'
)
config33.place(
    x=610.0,
    y=607.0,
    width=122.0,
    height=33.0
)

entry_image_5 = PhotoImage(
    file=relative_to_assets("entry1.png"))
entry_bg_5 = canvas.create_image(
    538.0,
    624.5,
    image=entry_image_5
)
config32 = Entry(
    bd=0,
    bg="#353434",
    highlightthickness=0, fg="white", justify='center'
)
config32.place(
    x=477.0,
    y=607.0,
    width=122.0,
    height=33.0
)

entry_image_6 = PhotoImage(
    file=relative_to_assets("entry1.png"))
entry_bg_6 = canvas.create_image(
    405.0,
    624.5,
    image=entry_image_6
)
config31 = Entry(
    bd=0,
    bg="#353434",
    highlightthickness=0, fg="white", justify='center'
)
config31.place(
    x=344.0,
    y=607.0,
    width=122.0,
    height=33.0
)

entry_image_7 = PhotoImage(
    file=relative_to_assets("entry1.png"))
entry_bg_7 = canvas.create_image(
    272.0,
    624.5,
    image=entry_image_7
)
config30 = Entry(
    bd=0,
    bg="#353434",
    highlightthickness=0, fg="white", justify='center'
)
config30.place(
    x=211.0,
    y=607.0,
    width=122.0,
    height=33.0
)

entry_image_8 = PhotoImage(
    file=relative_to_assets("entry1.png"))
entry_bg_8 = canvas.create_image(
    139.0,
    624.5,
    image=entry_image_8
)
config29 = Entry(
    bd=0,
    bg="#353434",
    highlightthickness=0, fg="white", justify='center'
)
config29.place(
    x=78.0,
    y=607.0,
    width=122.0,
    height=33.0
)

entry_image_9 = PhotoImage(
    file=relative_to_assets("entry1.png"))
entry_bg_9 = canvas.create_image(
    1070.0,
    561.5,
    image=entry_image_9
)
config28 = Entry(
    bd=0,
    bg="#353434",
    highlightthickness=0, fg="white", justify='center'
)
config28.place(
    x=1009.0,
    y=544.0,
    width=122.0,
    height=33.0
)

entry_image_10 = PhotoImage(
    file=relative_to_assets("entry1.png"))
entry_bg_10 = canvas.create_image(
    937.0,
    561.5,
    image=entry_image_10
)
config27 = Entry(
    bd=0,
    bg="#353434",
    highlightthickness=0, fg="white", justify='center'
)
config27.place(
    x=876.0,
    y=544.0,
    width=122.0,
    height=33.0
)

entry_image_11 = PhotoImage(
    file=relative_to_assets("entry1.png"))
entry_bg_11 = canvas.create_image(
    804.0,
    561.5,
    image=entry_image_11
)
config26 = Entry(
    bd=0,
    bg="#353434",
    highlightthickness=0, fg="white", justify='center'
)
config26.place(
    x=743.0,
    y=544.0,
    width=122.0,
    height=33.0
)

entry_image_12 = PhotoImage(
    file=relative_to_assets("entry1.png"))
entry_bg_12 = canvas.create_image(
    671.0,
    561.5,
    image=entry_image_12
)
config25 = Entry(
    bd=0,
    bg="#353434",
    highlightthickness=0, fg="white", justify='center'
)
config25.place(
    x=610.0,
    y=544.0,
    width=122.0,
    height=33.0
)

entry_image_13 = PhotoImage(
    file=relative_to_assets("entry1.png"))
entry_bg_13 = canvas.create_image(
    538.0,
    561.5,
    image=entry_image_13
)

#DIDNT I TELL YOU TO STOP READING THIS?
config24 = Entry(
    bd=0,
    bg="#353434",
    highlightthickness=0, fg="white", justify='center'
)
config24.place(
    x=477.0,
    y=544.0,
    width=122.0,
    height=33.0
)

entry_image_14 = PhotoImage(
    file=relative_to_assets("entry1.png"))
entry_bg_14 = canvas.create_image(
    405.0,
    561.5,
    image=entry_image_14
)
config23 = Entry(
    bd=0,
    bg="#353434",
    highlightthickness=0, fg="white", justify='center'
)
config23.place(
    x=344.0,
    y=544.0,
    width=122.0,
    height=33.0
)

entry_image_15 = PhotoImage(
    file=relative_to_assets("entry1.png"))
entry_bg_15 = canvas.create_image(
    272.0,
    561.5,
    image=entry_image_15
)
config22 = Entry(
    bd=0,
    bg="#353434",
    highlightthickness=0, fg="white", justify='center'
)
config22.place(
    x=211.0,
    y=544.0,
    width=122.0,
    height=33.0
)

entry_image_16 = PhotoImage(
    file=relative_to_assets("entry1.png"))
entry_bg_16 = canvas.create_image(
    139.0,
    561.5,
    image=entry_image_16
)
config21 = Entry(
    bd=0,
    bg="#353434",
    highlightthickness=0, fg="white", justify='center'
)
config21.place(
    x=78.0,
    y=544.0,
    width=122.0,
    height=33.0
)

entry_image_17 = PhotoImage(
    file=relative_to_assets("entry1.png"))
entry_bg_17 = canvas.create_image(
    1070.0,
    498.5,
    image=entry_image_17
)
config20 = Entry(
    bd=0,
    bg="#353434",
    highlightthickness=0, fg="white", justify='center'
)
config20.place(
    x=1009.0,
    y=481.0,
    width=122.0,
    height=33.0
)

entry_image_18 = PhotoImage(
    file=relative_to_assets("entry1.png"))
entry_bg_18 = canvas.create_image(
    937.0,
    498.5,
    image=entry_image_18
)
config19 = Entry(
    bd=0,
    bg="#353434",
    highlightthickness=0, fg="white", justify='center'
)
config19.place(
    x=876.0,
    y=481.0,
    width=122.0,
    height=33.0
)

entry_image_19 = PhotoImage(
    file=relative_to_assets("entry1.png"))
entry_bg_19 = canvas.create_image(
    804.0,
    498.5,
    image=entry_image_19
)
config18 = Entry(
    bd=0,
    bg="#353434",
    highlightthickness=0, fg="white", justify='center'
)
config18.place(
    x=743.0,
    y=481.0,
    width=122.0,
    height=33.0
)

entry_image_20 = PhotoImage(
    file=relative_to_assets("entry1.png"))
entry_bg_20 = canvas.create_image(
    671.0,
    498.5,
    image=entry_image_20
)
config17 = Entry(
    bd=0,
    bg="#353434",
    highlightthickness=0, fg="white", justify='center'
)
config17.place(
    x=610.0,
    y=481.0,
    width=122.0,
    height=33.0
)

entry_image_21 = PhotoImage(
    file=relative_to_assets("entry1.png"))
entry_bg_21 = canvas.create_image(
    538.0,
    498.5,
    image=entry_image_21
)
config16 = Entry(
    bd=0,
    bg="#353434",
    highlightthickness=0, fg="white", justify='center'
)
config16.place(
    x=477.0,
    y=481.0,
    width=122.0,
    height=33.0
)

entry_image_22 = PhotoImage(
    file=relative_to_assets("entry1.png"))
entry_bg_22 = canvas.create_image(
    405.0,
    498.5,
    image=entry_image_22
)
config15 = Entry(
    bd=0,
    bg="#353434",
    highlightthickness=0, fg="white", justify='center'
)
config15.place(
    x=344.0,
    y=481.0,
    width=122.0,
    height=33.0
)

entry_image_23 = PhotoImage(
    file=relative_to_assets("entry1.png"))
entry_bg_23 = canvas.create_image(
    272.0,
    498.5,
    image=entry_image_23
)
config14 = Entry(
    bd=0,
    bg="#353434",
    highlightthickness=0, fg="white", justify='center'
)
config14.place(
    x=211.0,
    y=481.0,
    width=122.0,
    height=33.0
)

entry_image_24 = PhotoImage(
    file=relative_to_assets("entry1.png"))
entry_bg_24 = canvas.create_image(
    139.0,
    498.5,
    image=entry_image_24
)
config13 = Entry(
    bd=0,
    bg="#353434",
    highlightthickness=0, fg="white", justify='center'
)
config13.place(
    x=78.0,
    y=481.0,
    width=122.0,
    height=33.0
)

entry_image_25 = PhotoImage(
    file=relative_to_assets("entry1.png"))
entry_bg_25 = canvas.create_image(
    1070.0,
    435.5,
    image=entry_image_25
)
config12 = Entry(
    bd=0,
    bg="#353434",
    highlightthickness=0, fg="white", justify='center'
)
config12.place(
    x=1009.0,
    y=418.0,
    width=122.0,
    height=33.0
)

entry_image_26 = PhotoImage(
    file=relative_to_assets("entrybig.png"))
entry_bg_26 = canvas.create_image(
    936.0,
    228.5,
    image=entry_image_26
)
config3 = Entry(
    bd=0,
    bg="#353434",
    highlightthickness=0, fg="white", justify='center'
)
config3.place(
    x=742.0,
    y=211.0,
    width=388.0,
    height=33.0
)

entry_image_27 = PhotoImage(
    file=relative_to_assets("entrybig.png"))
entry_bg_27 = canvas.create_image(
    936.0,
    160.5,
    image=entry_image_27
)
config2 = Entry(
    bd=0,
    bg="#353434",
    highlightthickness=0, fg="white", justify='center'
)
config2.place(
    x=742.0,
    y=143.0,
    width=388.0,
    height=33.0
)

entry_image_28 = PhotoImage(
    file=relative_to_assets("entrybig.png"))
entry_bg_28 = canvas.create_image(
    936.0,
    93.5,
    image=entry_image_28
)



config1 = Entry(
    bd=0,
    bg="#353434",
    highlightthickness=0, fg="white", justify='center'
)
config1.place(
    x=742.0,
    y=76.0,
    width=388.0,
    height=33.0
)

entry_image_29 = PhotoImage(
    file=relative_to_assets("entry1.png"))
entry_bg_29 = canvas.create_image(
    937.0,
    435.5,
    image=entry_image_29
)
config11 = Entry(
    bd=0,
    bg="#353434",
    highlightthickness=0, fg="white", justify='center'
)
config11.place(
    x=876.0,
    y=418.0,
    width=122.0,
    height=33.0
)

entry_image_30 = PhotoImage(
    file=relative_to_assets("entry1.png"))
entry_bg_30 = canvas.create_image(
    804.0,
    435.5,
    image=entry_image_30
)
config10 = Entry(
    bd=0,
    bg="#353434",
    highlightthickness=0, fg="white", justify='center'
)
config10.place(
    x=743.0,
    y=418.0,
    width=122.0,
    height=33.0
)

entry_image_31 = PhotoImage(
    file=relative_to_assets("entry1.png"))
entry_bg_31 = canvas.create_image(
    671.0,
    435.5,
    image=entry_image_31
)
config9 = Entry(
    bd=0,
    bg="#353434",
    highlightthickness=0, fg="white", justify='center'
)
config9.place(
    x=610.0,
    y=418.0,
    width=122.0,
    height=33.0
)

entry_image_32 = PhotoImage(
    file=relative_to_assets("entry1.png"))
entry_bg_32 = canvas.create_image(
    538.0,
    435.5,
    image=entry_image_32
)
config8 = Entry(
    bd=0,
    bg="#353434",
    highlightthickness=0, fg="white", justify='center'
)
config8.place(
    x=477.0,
    y=418.0,
    width=122.0,
    height=33.0
)

entry_image_33 = PhotoImage(
    file=relative_to_assets("entry1.png"))
entry_bg_33 = canvas.create_image(
    405.0,
    435.5,
    image=entry_image_33
)
config7 = Entry(
    bd=0,
    bg="#353434",
    highlightthickness=0, fg="white", justify='center'
)
config7.place(
    x=344.0,
    y=418.0,
    width=122.0,
    height=33.0
)

entry_image_34 = PhotoImage(
    file=relative_to_assets("entry1.png"))
entry_bg_34 = canvas.create_image(
    272.0,
    435.5,
    image=entry_image_34
)
config6 = Entry(
    bd=0,
    bg="#353434",
    highlightthickness=0, fg="white", justify='center'
)
config6.place(
    x=211.0,
    y=418.0,
    width=122.0,
    height=33.0
)

entry_image_35 = PhotoImage(
    file=relative_to_assets("entry1.png"))
entry_bg_35 = canvas.create_image(
    139.0,
    435.5,
    image=entry_image_35
)
config5 = Entry(
    bd=0,
    bg="#353434",
    highlightthickness=0, fg="white", justify='center'
)
config5.place(
    x=78.0,
    y=418.0,
    width=122.0,
    height=33.0
)

def updateConfigWindow(dir):
    if not os.path.isfile(dir):
        with open(dir, 'w') as f:
            json.dump(nawa.default_weapon_config, f, ensure_ascii=False, indent=4)
    config_data = nawa.WEAPON_CONFIG(dir)
    config1.delete(0, END)
    config1.insert(END, config_data.weapon_name)
    config2.delete(0, END)
    config2.insert(END, config_data.short_description)
    config3.delete(0, END)
    config3.insert(END, config_data.long_description)
    configU.config(text = new[:32] + "...")
    jout.conWeaponType(config_data.weapon_type)
    variable.set(jout.conWeaponType(config_data.weapon_type))
    config5.delete(0, END)
    config5.insert(END, config_data.level_1_left_damage)
    config6.delete(0, END)
    config6.insert(END, config_data.level_1_right_damage)
    config7.delete(0, END)
    config7.insert(END, config_data.level_1_left_combo)
    config8.delete(0, END)
    config8.insert(END, config_data.level_1_right_combo)
    config9.delete(0, END)
    config9.insert(END, config_data.level_1_speed)
    config10.delete(0, END)
    config10.insert(END, config_data.level_1_endurance)
    config11.delete(0, END)
    config11.insert(END, config_data.level_1_stun)
    config12.delete(0, END)
    config12.insert(END, config_data.level_1_crit)
    config13.delete(0, END)
    config13.insert(END, config_data.level_2_left_damage)
    config14.delete(0, END)
    config14.insert(END, config_data.level_2_right_damage)
    config15.delete(0, END)
    config15.insert(END, config_data.level_2_left_combo)
    config16.delete(0, END)
    config16.insert(END, config_data.level_2_right_combo)
    config17.delete(0, END)
    config17.insert(END, config_data.level_2_speed)
    config18.delete(0, END)
    config18.insert(END, config_data.level_2_endurance)
    config19.delete(0, END)
    config19.insert(END, config_data.level_2_stun)
    config20.delete(0, END)
    config20.insert(END, config_data.level_2_crit)
    config21.delete(0, END)
    config21.insert(END, config_data.level_3_left_damage)
    config22.delete(0, END)
    config22.insert(END, config_data.level_3_right_damage)
    config23.delete(0, END)
    config23.insert(END, config_data.level_3_left_combo)
    config24.delete(0, END)
    config24.insert(END, config_data.level_3_right_combo)
    config25.delete(0, END)
    config25.insert(END, config_data.level_3_speed)
    config26.delete(0, END)
    config26.insert(END, config_data.level_3_endurance)
    config27.delete(0, END)
    config27.insert(END, config_data.level_3_stun)
    config28.delete(0, END)
    config28.insert(END, config_data.level_3_crit)
    config29.delete(0, END)
    config29.insert(END, config_data.level_4_left_damage)
    config30.delete(0, END)
    config30.insert(END, config_data.level_4_right_damage)
    config31.delete(0, END)
    config31.insert(END, config_data.level_4_left_combo)
    config32.delete(0, END)
    config32.insert(END, config_data.level_4_right_combo)
    config33.delete(0, END)
    config33.insert(END, config_data.level_4_speed)
    config34.delete(0, END)
    config34.insert(END, config_data.level_4_endurance)
    config35.delete(0, END)
    config35.insert(END, config_data.level_4_stun)
    config36.delete(0, END)
    config36.insert(END, config_data.level_4_crit)

def updateConfigFile():
    global new
    conDir = nierModsDir + "/" + new + "/config.json"
    if not os.path.isfile(conDir):
        with open(conDir, 'w') as f:
            json.dump(nawa.default_weapon_config, f, ensure_ascii=False, indent=4)
    config_data = nawa.WEAPON_CONFIG(conDir)
    config_data.weapon_name             = jout.checkStringFont(jout.checkStringFont(config1.get(), 5), 36)
    config_data.short_description       = jout.checkStringFont(jout.checkStringFont(config2.get(), 5), 36)
    config_data.long_description        = jout.checkStringFont(jout.checkStringFont(config3.get(), 5), 36)
    config_data.weapon_type             = jout.conWeaponType(variable.get())
    config_data.level_1_left_damage     = config5.get()
    config_data.level_1_right_damage    = config6.get()
    config_data.level_1_left_combo      = config7.get()
    config_data.level_1_right_combo     = config8.get()
    config_data.level_1_speed           = config9.get()
    config_data.level_1_endurance       = config10.get()
    config_data.level_1_stun            = config11.get()
    config_data.level_1_crit            = config12.get()
    config_data.level_2_left_damage     = config13.get()
    config_data.level_2_right_damage    = config14.get()
    config_data.level_2_left_combo      = config15.get()
    config_data.level_2_right_combo     = config16.get()
    config_data.level_2_speed           = config17.get()
    config_data.level_2_endurance       = config18.get()
    config_data.level_2_stun            = config19.get()
    config_data.level_2_crit            = config20.get()
    config_data.level_3_left_damage     = config21.get()
    config_data.level_3_right_damage    = config22.get()
    config_data.level_3_left_combo      = config23.get()
    config_data.level_3_right_combo     = config24.get()
    config_data.level_3_speed           = config25.get()
    config_data.level_3_endurance       = config26.get()
    config_data.level_3_stun            = config27.get()
    config_data.level_3_crit            = config28.get()
    config_data.level_4_left_damage     = config29.get()
    config_data.level_4_right_damage    = config30.get()
    config_data.level_4_left_combo      = config31.get()
    config_data.level_4_right_combo     = config32.get()
    config_data.level_4_speed           = config33.get()
    config_data.level_4_endurance       = config34.get()
    config_data.level_4_stun            = config35.get()
    config_data.level_4_crit            = config36.get()

    config_data.save()

if check_names(nierModsDir):
    buildModList()

button_image_reset = PhotoImage(
    file=relative_to_assets("button_reset.png"))
button_reset = Button(
    image=button_image_reset,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: [nawa.WEAPON_CONFIG(conDir).regen_config(), updateConfigWindow(conDir)],
    relief="flat"
)

button_reset.place(
    x=940.0,
    y=275.0,
    width=190.0,
    height=35.0
)
nierDataConfirm =Label(window, bg="#2E2E2E", font=("RobotoRoman CondensedRegular", 12 * -1))
nierDataConfirm.place(x=202.0, y=700.0)
modsDirConfirm =Label(window, bg="#2E2E2E", font=("RobotoRoman CondensedRegular", 12 * -1))
modsDirConfirm.place(x=414, y=700.0)

def check_ifCfg(startDeploy):
    internalSuccess = 1
    if not os.path.isdir(nierModsDir):
        alertBox("SELECT A VALID MODS FOLDER")
        internalSuccess = 0
        modsDirConfirm.config(text = "x", fg='red')
    if not os.path.isdir(nierDatDir):
        alertBox("SELECT A VALID DATA FOLDER")
        internalSuccess = 0
        nierDataConfirm.config(text = "x", fg='red')
    if internalSuccess == 1:
        modsDirConfirm.config(text = "✓", fg='green')
        nierDataConfirm.config(text = "✓", fg='green')
        if startDeploy:
            del_wp()
            if nawa.nawa_deploy() == True:
                shutil.rmtree("nawa_data/dat_files")
                alertBox("Mods successfully deployed!")
            else:
                alertBox("Error occured, refer to console window")

window.iconbitmap("nawa_data/namc.ico")
check_ifCfg(False)
window.resizable(False, False)
window.title('NAWA | NieR: Automata Weapon Assembly ver 3')
window.mainloop()
