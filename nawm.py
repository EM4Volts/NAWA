import os, random, shutil, string
import yamm_data.fileporters.mcd as mcd
import yamm_data.fileporters.export_dat as dattExpo
import journey_tools as jout
import yamm_data.fileporters.xmlToBxm as xml2Bxm
import yamm_data.fileporters.newexport_dat as newdattExpo
import yamm_data.fileporters.newdat_unpacker as newdattUn
import yamm_data.fileporters.tmd as tmd

def newpackDatt(dattDir, name):
    dct = jout.genPathList(dattDir)
    newdattExpo.main(name, dct)

def copyFold(source,dest): #stolen from stackvoerflow lol
    os.mkdir(dest)
    dest_dir = os.path.join(dest,os.path.basename(source))
    shutil.copytree(source,dest_dir)

def main():
    #list of all xml files to convert
    xmlList = ["yamm_data/coregm/WeaponInfoTable.xml",
               "yamm_data/coregm/ItemInfoTable.xml",
               "yamm_data/coregm/ShopInfoTable.xml",
               "yamm_data/coregm/ShopInfoTable.xml",
               "yamm_data/coregm/WeaponStrengthenTable.xml",
               "yamm_data/core/WeaponStrengthenTable.xml"
               ]

    #read the cfg file for directories
    cfgFile = open("configs/config.ini", "r")
    data = cfgFile.read()
    config = data.split("\n")
    cfgFile.close()
    print(cfgFile)
    nierDatDir= config[0]
    nierModsDir= config[1]

    #Copy vanilla xml and json files to the work folders
    shutil.copyfile("yamm_data/xml2Merge/txt_pause_add_us/txt_pause_add.json", "yamm_data/txt_pause_add_us/txt_pause_add.json")
    shutil.copyfile("yamm_data/xml2Merge/core/WeaponStrengthenTable.xml", "yamm_data/core/WeaponStrengthenTable.xml")
    shutil.copyfile("yamm_data/xml2Merge/core/WeaponParam.csv", "yamm_data/core/WeaponParam.csv")
    shutil.copyfile("yamm_data/xml2Merge/txt_core_add_us/txt_core_add.json", "yamm_data/txt_core_add_us/txt_core_add.json")
    shutil.copyfile("yamm_data/xml2Merge/ui_core_us/messcore.json", "yamm_data/ui_core_us/messcore.json")
    for filename in os.listdir("yamm_data/xml2Merge/coregm"):
        shutil.copyfile("yamm_data/xml2Merge/coregm/" + filename, "yamm_data/coregm/" + filename)
    curWhitelist = ["file_order.metadata", "hash_data.metadata","dat_info.json"]
    jout.cleanDeploy()
    for filename in os.scandir(nierModsDir):
        wkDir = str(filename.path)
        wpCFGdata = jout.readwpConfig(wkDir + "/config.json")
        newWpName = jout.getWPfileName(wpCFGdata[3])
        print(newWpName)
        internalWeaponID = 'weapon_' + ''.join(random.choice(string.ascii_lowercase) for _ in range(11))
        uniqueID = jout.getUniqueID()
        print("[Writing all Tables using config: " + internalWeaponID, uniqueID, newWpName, wpCFGdata[0], wpCFGdata[1], wpCFGdata[2], wpCFGdata[3], wpCFGdata[5], wpCFGdata[6], wpCFGdata[7], wpCFGdata[8] + "]")
        jout.WriteAllTables(internalWeaponID, uniqueID, newWpName, wpCFGdata[0], wpCFGdata[1], wpCFGdata[2], wpCFGdata[3], wpCFGdata[5], wpCFGdata[6], wpCFGdata[7], wpCFGdata[8])
        for filename in os.scandir(wkDir + "/wp"):
            eFile = str(filename)[11:][:-2]
            print(eFile)
            if eFile.endswith(".dat"):
                shutil.copyfile(wkDir + "/wp/" + eFile, 'deploy/wp/' + newWpName + ".dat")
                newdattUn.main('deploy/wp/' + newWpName + ".dat",'deploy/wp/' + newWpName + "_dat")
                for filename in os.scandir("deploy/wp/" + newWpName + "_dat"):
                    try:
                        shutil.copyfile("deploy/wp/" + newWpName + "_dat/" + str(filename)[11:][:-2], "deploy/wp/" + newWpName + "_dat/" + newWpName + str(filename)[17:][:-2])
                    except shutil.SameFileError:
                        pass
                    curStr= str(filename)[11:][:-2]
                    if not curStr.startswith(newWpName):
                        delString = "deploy/wp/" + newWpName + "_dat/" + str(filename)[11:][:-2]
                        os.remove(delString)
            if eFile.endswith(".dtt"):
                shutil.copyfile(wkDir + "/wp/" + eFile, 'deploy/wp/' + newWpName + ".dtt")
                newdattUn.main('deploy/wp/' + newWpName + ".dtt",'deploy/wp/' + newWpName + "_dtt")
                for filename in os.scandir("deploy/wp/" + newWpName + "_dtt"):
                    try:
                        shutil.copyfile("deploy/wp/" + newWpName + "_dtt/" + str(filename)[11:][:-2], "deploy/wp/" + newWpName + "_dtt/" + newWpName + str(filename)[17:][:-2])
                    except shutil.SameFileError:
                        pass
                    curStr= str(filename)[11:][:-2]
                    if not curStr.startswith(newWpName):
                        delString = "deploy/wp/" + newWpName + "_dtt/" + str(filename)[11:][:-2]
                        os.remove(delString)
                jout.shuffleIdentifierWta( "deploy/wp/" + newWpName + "_dat/" + newWpName + ".wta", "deploy/wp/" + newWpName + "_dtt/" + newWpName + ".wmb")
                newpackDatt("deploy/wp/" + newWpName + "_dat/", "deploy/wp/" + newWpName + ".dat")
                newpackDatt("deploy/wp/" + newWpName + "_dtt/", "deploy/wp/" + newWpName + ".dtt")
    print("[Converting new XML...]")
    xml2Bxm.main(xmlList)
    print("[Building TMD...]")
    tmd.json_to_tmd("yamm_data/txt_core_add_us/txt_core_add.json")
    tmd.json_to_tmd("yamm_data/txt_pause_add_us/txt_pause_add.json")
    print("[Building MCD...]")
    mcd.json_to_mcd("yamm_data/ui_core_us/messcore.json", "yamm_data/ui_core_us/messcore.mcd")

    print("[Packing essential .dat's...]")
    newpackDatt("yamm_data/core/", "deploy/core/core.dat")
    newpackDatt("yamm_data/coregm/", "deploy/core/coregm.dat")
    dattExpo.main("yamm_data/ui_core_us/", "deploy/ui/ui_core_us.dat")
    dattExpo.main("yamm_data/txt_core_add_us/", "deploy/txtmess/txt_core_add_us.dat")
    dattExpo.main("yamm_data/txt_pause_add_us/", "deploy/txtmess/txt_pause_add_us.dat")