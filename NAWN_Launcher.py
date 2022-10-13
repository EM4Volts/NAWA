from pathlib import Path
import os
from tkinter import *
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, filedialog
import journey_tools as jout
import nawm
nawmversion = "NAWM version 1.0.5"

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")

new=""
modList = []


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
cfgStruct = [nierDatDir, nierModsDir]
def generateConfig():
    with open(r'configs/config.ini', 'w') as cfg:
        for str in cfgStruct:
            cfg.write("%s\n" % str)



def selectNierDataDir():
    global nierDatDir
    global cfgStruct
    folder_selected = filedialog.askdirectory()
    nierDatDir = folder_selected
    cfgStruct = [nierDatDir, nierModsDir]
    generateConfig()
    return folder_selected + "/"

def selectNierModsDir():
    global nierModsDir
    global cfgStruct
    folder_selected = filedialog.askdirectory()
    nierModsDir = folder_selected
    cfgStruct = [nierDatDir, nierModsDir]
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
    global new
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
configU.place(x=577.0, y=15.0)

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
    command=lambda: updateConfigFile(dir),
    relief="flat"
)
variable = StringVar(window)
variable.set("Small Sword") # default value

config4 = OptionMenu(window,variable, "Large Sword", "Spear", "Small Sword", "Combat Bracers")
config4.place(x=742, y=278)
button_1.place(
    x=732.0,
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
    command=lambda: nawm.main(),
    relief="flat"
)
button_2.place(
    x=941.0,
    y=686.0,
    width=190.0,
    height=35.0
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0, fg="white", justify='center',
    command=lambda: [selectNierDataDir(), generateConfig()],
    relief="flat"
)
button_3.place(
    x=12.0,
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
    command=lambda: [selectNierModsDir(), modListUpdate()],
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
    338.0,
    anchor="nw",
    text="If you do not know what a value means leave it at its default.",
    fill="#FFFFFF",
    font=("RobotoItalic Condensed", 16 * -1)
)

canvas.create_text(
    485.0,
    709.0,
    anchor="nw",
    text=nawmversion,
    fill="#353535",
    font=("RobotoRoman CondensedMedium", 16 * -1)
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
    config_data = jout.readwpConfig(dir)
    config1.delete(0, END)
    config1.insert(END, config_data[0])
    config2.delete(0, END)
    config2.insert(END, config_data[1])
    config3.delete(0, END)
    config3.insert(END, config_data[2])

    configU.config(text = new[:20] + "...")
    jout.conWeaponType(config_data[3])
    variable.set(jout.conWeaponType(config_data[3]))
    
    config5.delete(0, END)
    config5.insert(END, config_data[5])
    config6.delete(0, END)
    config6.insert(END, config_data[6])
    config7.delete(0, END)
    config7.insert(END, config_data[7])
    config8.delete(0, END)
    config8.insert(END, config_data[8])
    config9.delete(0, END)
    config9.insert(END, config_data[9])
    config10.delete(0, END)
    config10.insert(END, config_data[10])
    config11.delete(0, END)
    config11.insert(END, config_data[11])
    config12.delete(0, END)
    config12.insert(END, config_data[12])
    config13.delete(0, END)
    config13.insert(END, config_data[13])
    config14.delete(0, END)
    config14.insert(END, config_data[14])
    config15.delete(0, END)
    config15.insert(END, config_data[15])
    config16.delete(0, END)
    config16.insert(END, config_data[16])
    config17.delete(0, END)
    config17.insert(END, config_data[17])
    config18.delete(0, END)
    config18.insert(END, config_data[18])
    config19.delete(0, END)
    config19.insert(END, config_data[19])
    config20.delete(0, END)
    config20.insert(END, config_data[20])
    config21.delete(0, END)
    config21.insert(END, config_data[21])
    config22.delete(0, END)
    config22.insert(END, config_data[22])
    config23.delete(0, END)
    config23.insert(END, config_data[23])
    config24.delete(0, END)
    config24.insert(END, config_data[24])
    config25.delete(0, END)
    config25.insert(END, config_data[25])
    config26.delete(0, END)
    config26.insert(END, config_data[26])
    config27.delete(0, END)
    config27.insert(END, config_data[27])
    config28.delete(0, END)
    config28.insert(END, config_data[28])
    config29.delete(0, END)
    config29.insert(END, config_data[29])
    config30.delete(0, END)
    config30.insert(END, config_data[30])
    config31.delete(0, END)
    config31.insert(END, config_data[31])
    config32.delete(0, END)
    config32.insert(END, config_data[32])
    config33.delete(0, END)
    config33.insert(END, config_data[33])
    config34.delete(0, END)
    config34.insert(END, config_data[34])
    config35.delete(0, END)
    config35.insert(END, config_data[35])
    config36.delete(0, END)
    config36.insert(END, config_data[36])
def getConfigEntry():
    kName = config1.get()
    kName2 = config2.get()
    kName3 = config3.get()
    kName4 = config5.get()
    kName5 = config6.get()
    kName6 = config7.get()
    kName7 = config8.get()
    kName8 = config9.get()
    kName9 = config10.get()
    kName10 = config11.get()
    kName11 = config12.get()
    kName12 = config13.get()
    kName13 = config14.get()
    kName14 = config15.get()
    kName15 = config16.get()
    kName16 = config17.get()
    kName17 = config18.get()
    kName18 = config19.get()
    kName19 = config20.get()
    kName20 = config21.get()
    kName21 = config22.get()
    kName22 = config23.get()
    kName23 = config24.get()
    kName24 = config25.get()
    kName25 = config26.get()
    kName26 = config27.get()
    kName27 = config28.get()
    kName28 = config29.get()
    kName29 = config30.get()
    kName30 = config31.get()
    kName31 = config32.get()
    kName32 = config33.get()
    kName33 = config34.get()
    kName34 = config35.get()
    kName35 = config36.get()

    return kName, kName2, kName3, kName4, kName5, kName6, kName7, kName8, kName9, kName10, kName11, kName12, kName13, kName14, kName15, kName16, kName17, kName18, kName19, kName20, kName21, kName22, kName23, kName24, kName25, kName26, kName27, kName28, kName29, kName30, kName31, kName32, kName33, kName34, kName35
def updateConfigFile(dir):
    global new
    conDir = nierModsDir + "/" + new + "/config.json"
    conData = getConfigEntry()
    jout.writewpConfig(conDir,conData[0], conData[1], conData[2], jout.conWeaponType(variable.get()),conData[3], conData[4], conData[5], conData[6], conData[7], conData[8], conData[9], conData[10], conData[11], conData[12], conData[13], conData[14], conData[15], conData[16], conData[17], conData[18], conData[19], conData[20], conData[21], conData[22], conData[23], conData[24], conData[25], conData[26], conData[27], conData[28], conData[29], conData[30], conData[31], conData[32], conData[33], conData[34])

if check_names(nierModsDir):
    buildModList()
window.resizable(False, False)
window.iconbitmap("yamm_data/namc.ico")
window.title('NAWM NieR: Automata Weapon Manager')
window.mainloop()
