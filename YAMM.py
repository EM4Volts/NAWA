import os, random, shutil, string
import yamm_data.fileporters.mcd as mcd
import yamm_data.fileporters.export_dat as dattExpo
import yamm_data.fileporters.dat_unpacker as dattUn
import journey_tools as jout
import yamm_data.fileporters.xmlToBxm as xml2Bxm
import yamm_data.fileporters.newexport_dat as newdattExpo
import yamm_data.fileporters.newdat_unpacker as newdattUn
import yamm_data.fileporters.tmd as tmd

xmlList = ["yamm_data/coregm/WeaponInfoTable.xml",
           "yamm_data/coregm/ItemInfoTable.xml",
           "yamm_data/coregm/ShopInfoTable.xml",
           "yamm_data/coregm/ShopInfoTable.xml",
           "yamm_data/coregm/WeaponStrengthenTable.xml",
           "yamm_data/core/WeaponStrengthenTable.xml"
           ]

itenInfoTablecrispList = []
messCorecrispList = []
secondweaponstrenghttablecrispList = []
shopInfoTablecrispList = []
weaponInfoTablecrispList = []
crispList = []

dir_path = os.path.dirname(os.path.realpath(__file__))
directory = 'mods'

newUid = 1003
mXMLn = 1

idBlacklistFile = open("configs/wpids.xml", "r")
data = idBlacklistFile.read()
idBlacklist = data.split("\n")
idBlacklistFile.close()

cfgFile = open("configs/config.ini", "r")
data = cfgFile.read()
config = data.split("\n")
cfgFile.close()
nierDatDir= config[0]
nierModsDir= config[1]


def newunpackDatt(datt, datt2):
    newdattUn.main(datt, datt2)

def newpackDatt(dattDir, name):
    dct = jout.genPathList(dattDir)
    newdattExpo.main(name, dct)

def unpackDatt(datt, datt2):
    dattUn.main(datt, datt2)


def wpunpackDatt(datt, datt2):
    wpdattUn.main(datt, datt2)


def packDatt(dattDir, name):
    dattExpo.main(dattDir, name)

def getUniqueID():
    global newUid
    newUidFound = False
    while not newUidFound:
        uId = str(newUid)
        newUid += 1
        if uId in idBlacklist:
            print("[UNIQUEID : " + uId + " in Use, retrying...]")
        if uId not in idBlacklist:
            if uId == "1000":
                print("delete some wp mods.... how do you even have this many?")
                exit()
            else:
                return uId

shutil.copyfile("yamm_data/xml2Merge/txt_pause_add_us/txt_pause_add.json", "yamm_data/txt_pause_add_us/txt_pause_add.json")
shutil.copyfile("yamm_data/xml2Merge/core/WeaponStrengthenTable.xml", "yamm_data/core/WeaponStrengthenTable.xml")
shutil.copyfile("yamm_data/xml2Merge/core/WeaponParam.csv", "yamm_data/core/WeaponParam.csv")
shutil.copyfile("yamm_data/xml2Merge/txt_core_add_us/txt_core_add.json", "yamm_data/txt_core_add_us/txt_core_add.json")
shutil.copyfile("yamm_data/xml2Merge/ui_core_us/messcore.json", "yamm_data/ui_core_us/messcore.json")
for filename in os.listdir("yamm_data/xml2Merge/coregm"):
    shutil.copyfile("yamm_data/xml2Merge/coregm/" + filename, "yamm_data/coregm/" + filename)
curWhitelist = ["file_order.metadata", "hash_data.metadata","dat_info.json"]


for filename in os.scandir(directory):
    workDir = str(filename.path) + "/wp"
    for filename in os.scandir(workDir):
        strFilename = str(filename)[11:][:-2]
        if strFilename.endswith('.dtt'):
            internalWeaponID = 'weapon_' + ''.join(random.choice(string.ascii_lowercase) for _ in range(11))
            shutil.copyfile(filename, 'deploy/wp/' + newWpName + ".dtt")
            uniqueID = getUniqueID()
            conDir = workDir + "/config.json"
            print(workDir)
            wpCFGdata = jout.readwpConfig("mods/" + workDir[5:][:-3] + "/config.json")
            print("[Writing all Tables using config: " + internalWeaponID, uniqueID, newWpName, wpCFGdata[0], wpCFGdata[1], wpCFGdata[2], wpCFGdata[3], wpCFGdata[5], wpCFGdata[6], wpCFGdata[7], wpCFGdata[8] + "]")
            jout.WriteAllTables(internalWeaponID, uniqueID, newWpName, wpCFGdata[0], wpCFGdata[1], wpCFGdata[2], wpCFGdata[3], wpCFGdata[5], wpCFGdata[6], wpCFGdata[7], wpCFGdata[8])
            newunpackDatt('deploy/wp/' + newWpName + ".dtt",'deploy/wp/' + newWpName + "_dtt")
            for filename in os.scandir("deploy/wp/" + newWpName + "_dtt"):
                fileToRenameStr= "deploy/wp/" + newWpName + "_dtt/" + str(filename)[11:][:-2]
                try:
                    shutil.copyfile("deploy/wp/" + newWpName + "_dtt/" + str(filename)[11:][:-2], "deploy/wp/" + newWpName + "_dtt/" + newWpName + str(filename)[17:][:-2])
                except shutil.SameFileError:
                    pass
                curStr= str(filename)[11:][:-2]
                if not curStr.startswith(newWpName):
                    delString = "deploy/wp/" + newWpName + "_dtt/" + str(filename)[11:][:-2]
                    os.remove(delString)

            mXMLn += 1
            print("[Packing " + workDir[5:][:-3] + " > " + newWpName + "_" + uniqueID + "]")
            jout.shuffleIdentifierWta( "deploy/wp/" + newWpName + "_dat/" + newWpName + ".wta", "deploy/wp/" + newWpName + "_dtt/" + newWpName + ".wmb")
            newpackDatt("deploy/wp/" + newWpName + "_dat/", "deploy/wp/" + newWpName + ".dat")
            newpackDatt("deploy/wp/" + newWpName + "_dtt/", "deploy/wp/" + newWpName + ".dtt")
        if strFilename.endswith('.dat'):
            newWpName = "wp" + str(getWPfileName())
            shutil.copyfile(filename, 'deploy/wp/' + newWpName + ".dat")
            newunpackDatt('deploy/wp/' + newWpName + ".dat",'deploy/wp/' + newWpName + "_dat")
            for filename in os.scandir("deploy/wp/" + newWpName + "_dat"):
                fileToRenameStr= "deploy/wp/" + newWpName + "_dat/" + str(filename)[11:][:-2]
                try:
                    shutil.copyfile("deploy/wp/" + newWpName + "_dat/" + str(filename)[11:][:-2], "deploy/wp/" + newWpName + "_dat/" + newWpName + str(filename)[17:][:-2])
                except shutil.SameFileError:
                    pass
                curStr= str(filename)[11:][:-2]
                if not curStr.startswith(newWpName):
                    delString = "deploy/wp/" + newWpName + "_dat/" + str(filename)[11:][:-2]
                    os.remove(delString)


print("[Converting new XML...]")
xml2Bxm.main(xmlList)
print("[Building TMD...]")
tmd.json_to_tmd("yamm_data/txt_core_add_us/txt_core_add.json")
tmd.json_to_tmd("yamm_data/txt_pause_add_us/txt_pause_add.json")
print("[Building MCD...]")
mcd.json_to_mcd("yamm_data/ui_core_us/messcore.json", "yamm_data/ui_core_us/messcore.mcd")

print("[Packing essential .dat's...]")
#packDatt("yamm_data/core/", "deploy/core/core.dat")
newpackDatt("yamm_data/core/", "deploy/core/core.dat")
newpackDatt("yamm_data/coregm/", "deploy/core/coregm.dat")
packDatt("yamm_data/ui_core_us/", "deploy/ui/ui_core_us.dat")
packDatt("yamm_data/txt_core_add_us/", "deploy/txtmess/txt_core_add_us.dat")
packDatt("yamm_data/txt_pause_add_us/", "deploy/txtmess/txt_pause_add_us.dat")

fourthVolt = open('yamm_data/shameless_plug.txt', 'r')
volt_contents = fourthVolt.read()
print (volt_contents)
fourthVolt.close()

exit()