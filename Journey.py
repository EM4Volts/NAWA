import os
from tkinter import *
from tkinter import filedialog
import journey_tools as jout

new=""
modList = []
cfgFile = open("configs/config.ini", "r")
data = cfgFile.read()
config = data.split("\n")
cfgFile.close()
nierDatDir= config[0]
nierModsDir= config[1]
cfgStruct = [nierDatDir, nierModsDir]
creditStr = "Huge thanks to:\n\n@Woeful_Wolf\n@RaiderB\n@grojdg\n\nfor their amazing\nwork on basically\neverything Automata!"

def generateConfig():
    with open(r'/configs/config.ini', 'w') as cfg:
        for str in cfgStruct:
            cfg.write("%s\n" % str)

def selectNierDataDir():
    global nierDatDir
    global cfgStruct
    folder_selected = filedialog.askdirectory()
    nierDatDir = folder_selected
    cfgStruct = [nierDatDir, nierModsDir]
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







buildModList()

class MyWindow:
    def __init__(self, win):
        global modList
        lblndselect=Label(window, text=nierDatDir,bg="#474747", fg='white', font=("Helvetica", 10))
        lblndselect.place(x=140, y=522)


        btn=Button(window,width=15, height=15, text="DEPLOY",bg="grey", fg='white', command=lambda : os.system("YAMM.py"))
        btn.place(x=10, y=5)



        btn=Button(window,width=15, text="SELECT DATA DIR ",bg="grey", fg='white', command=lambda : [selectNierDataDir(),lblndselect.config(text = nierDatDir), generateConfig()])
        btn.place(x=10, y=520)

        lblnmcredit=Label(window, text=creditStr,bg="#474747", fg='white', font=("Helvetica", 10))
        lblnmcredit.place(x=1, y=250)

        lblnmdselect=Label(window, text=nierModsDir,bg="#474747", fg='white', font=("Helvetica", 10))
        lblnmdselect.place(x=140, y=562)


        def key(event):
            global new
            new= lb.get(lb.curselection())
            conDir = "mods/" + new + "/config.json"
            updateConfigWindow(conDir)
        lb=Listbox(window,bg="#737373", height=31,width=50)
        lb.place(x=130, y=5)
        lb.bind('<<ListboxSelect>>',key)

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
        def updateConfigFile(dir):
            global new
            conDir = "mods/" + new + "/config.json"
            conData = getConfigEntry()
            jout.writewpConfig(conDir,conData[0], conData[1], conData[2], jout.conWeaponType(variable.get()), conData[3], conData[4], conData[5], conData[6])


        configU=Label(window, bg="#474747", fg='white', font=("Helvetica", 14))
        configU.place(x=438, y=3)

        lblnmname=Label(window, text="Name",bg="#474747", fg='white', font=("Helvetica", 10))
        lblnmname.place(x=438, y=40)

        config1 = Entry(window, width=33)
        config1.place(x=440, y=60)

        lblnmshortDest=Label(window, text="Short Description",bg="#474747", fg='white', font=("Helvetica", 10))
        lblnmshortDest.place(x=438, y=100)

        config2 = Entry(window, width=33)
        config2.place(x=440, y=120)

        lblnmlongdesc=Label(window, text="Long Description",bg="#474747", fg='white', font=("Helvetica", 10))
        lblnmlongdesc.place(x=438, y=160)

        config3 = Entry(window, width=33)
        config3.place(x=440, y=180)

        variable = StringVar(window)
        variable.set("Small Sword") # default value

        config4 = OptionMenu(window,variable, "Large Sword", "Spear", "Small Sword", "Combat Bracers")
        config4.place(x=440, y=220)

        btn=Button(window, width=27,height=4,  text="Save Config", bg="grey", fg='white', command=lambda : [updateConfigFile(dir)])
        btn.place(x=442, y=435)

        lblnmlongatk1=Label(window, text="Level 1 ATK",bg="#474747", fg='white', font=("Helvetica", 10))
        lblnmlongatk1.place(x=438, y=280)

        config5 = Entry(window, width=19)
        config5.place(x=525, y=280)

        lblnmlongatk1=Label(window, text="Level 2 ATK",bg="#474747", fg='white', font=("Helvetica", 10))
        lblnmlongatk1.place(x=438, y=310)

        config6 = Entry(window, width=19)
        config6.place(x=525, y=310)

        lblnmlongatk1=Label(window, text="Level 3 ATK",bg="#474747", fg='white', font=("Helvetica", 10))
        lblnmlongatk1.place(x=438, y=340)

        config7 = Entry(window, width=19)
        config7.place(x=525, y=340)

        lblnmlongatk1=Label(window, text="Level 4 ATK",bg="#474747", fg='white', font=("Helvetica", 10))
        lblnmlongatk1.place(x=438, y=370)

        config8 = Entry(window, width=19)
        config8.place(x=525, y=370)






        def getConfigEntry():
            kName = config1.get()
            kName2 = config2.get()
            kName3 = config3.get()
            kName4 = config5.get()
            kName5 = config6.get()
            kName6 = config7.get()
            kName7 = config8.get()


            return kName, kName2, kName3, kName4, kName5, kName6, kName7
        def modListUpdate():
            lb.delete(0,END)
            buildModList()
            for str in modList:
                str2 = str
                lb.insert(0, str2)

        btn=Button(window, width=15,  text="SELECT MODS DIR", bg="grey", fg='white', command=lambda : [selectNierModsDir(),lblnmdselect.config(text = nierModsDir), modListUpdate(), generateConfig()])
        btn.place(x=10, y=560)
        modListUpdate()


buildModList()
window=Tk()
mywin=MyWindow(window)
window.resizable(False, False)
window.iconbitmap("yamm_data/namc.ico")
window.title('NAWM')
window.configure(bg='#474747')
window.geometry("647x600+100+200")
window.mainloop()








