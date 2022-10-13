import os, random, shutil, string
import yamm_data.fileporters.mcd as mcd
import yamm_data.fileporters.export_dat as dattExpo
import journey_tools as jout
import yamm_data.fileporters.xmlToBxm as xml2Bxm
import yamm_data.fileporters.newexport_dat as newdattExpo
import yamm_data.fileporters.newdat_unpacker as newdattUn

def newpackDatt(dattDir, name):
    dct = jout.genPathList(dattDir)
    newdattExpo.main(name, dct)

def copyFold(source,dest): #stolen from stackvoerflow lol
    os.mkdir(dest)
    dest_dir = os.path.join(dest,os.path.basename(source))
    shutil.copytree(source,dest_dir)

def main():
    if not os.path.isdir("deploy"):
        os.makedirs("deploy/wp", 0o666)
        os.makedirs("deploy/core", 0o666)
        os.makedirs("deploy/ui", 0o666)
        os.makedirs("deploy/txtmess", 0o666)
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
    nierDatDir= config[0]
    nierModsDir= config[1]

    #Copy vanilla xml and json files to the work folders
    shutil.copyfile("yamm_data/xml2Merge/core/WeaponStrengthenTable.xml", "yamm_data/core/WeaponStrengthenTable.xml")
    shutil.copyfile("yamm_data/xml2Merge/core/WeaponParam.csv", "yamm_data/core/WeaponParam.csv")
    shutil.copyfile("yamm_data/xml2Merge/ui_core_us/messcore.json", "yamm_data/ui_core_us/messcore.json")
    for filename in os.listdir("yamm_data/xml2Merge/coregm"):
        shutil.copyfile("yamm_data/xml2Merge/coregm/" + filename, "yamm_data/coregm/" + filename)
    curWhitelist = ["file_order.metadata", "hash_data.metadata","dat_info.json"]
    jout.cleanDeploy()
    for filename in os.scandir(nierModsDir):
        wkDir = str(filename.path)
        wpCFGdata = jout.readwpConfig(wkDir + "/config.json")
        newWpName = jout.getWPfileName(wpCFGdata[3])
        internalWeaponID = 'weapon_' + ''.join(random.choice(string.ascii_lowercase) for _ in range(11))
        uniqueID = jout.getUniqueID()
        jout.WriteAllTables(internalWeaponID, uniqueID, newWpName, wpCFGdata[0], wpCFGdata[1], wpCFGdata[2], wpCFGdata[3], wpCFGdata[5], wpCFGdata[6], wpCFGdata[7], wpCFGdata[8], wpCFGdata[9], wpCFGdata[10], wpCFGdata[11], wpCFGdata[12], wpCFGdata[13], wpCFGdata[14], wpCFGdata[15], wpCFGdata[16], wpCFGdata[17], wpCFGdata[18], wpCFGdata[19], wpCFGdata[20], wpCFGdata[21], wpCFGdata[22], wpCFGdata[23], wpCFGdata[24], wpCFGdata[25], wpCFGdata[26], wpCFGdata[27], wpCFGdata[28], wpCFGdata[29], wpCFGdata[30], wpCFGdata[31], wpCFGdata[32], wpCFGdata[33], wpCFGdata[34], wpCFGdata[35], wpCFGdata[36])
        for filename in os.scandir(wkDir + "/wp"):
            eFile = str(filename)[11:][:-2]
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
                if os.path.isdir(wkDir + "/misctex"):
                    for filename in os.scandir(wkDir + "/misctex"):
                        misFile = str(filename)[11:][:-2]
                        print(misFile)
                        if eFile.endswith(".dat"):
                            shutil.copyfile(wkDir + "/misctex/" + misFile, 'deploy/misctex/' + "misctex_" + newWpName + ".dat")
                            newdattUn.main('deploy/misctex/' + "misctex_" + newWpName + ".dat",'deploy/misctex/' + "misctex_" + newWpName + "_dat")
                            for filename in os.scandir("deploy/misctex/" + "misctex_" + newWpName + "_dat"):
                                try:
                                    shutil.copyfile("deploy/misctex/" + "misctex_" + newWpName + "_dat/" + str(filename)[11:][:-2], "deploy/misctex/" + "misctex_" + newWpName + "_dat/" + "misctex_" + newWpName + str(filename)[25:][:-2])
                                except shutil.SameFileError:
                                    pass
                                curStr= str(filename)[11:][:-2]
                                if not curStr.startswith(newWpName):
                                    delString = "deploy/misctex/" + newWpName + "_dat/" + str(filename)[11:][:-2]
                                    try:
                                        os.remove(delString)
                                    except:
                                        pass
                            jout.shuffleIdentifierMisctex( "deploy/misctex/" + "misctex_" + newWpName + "_dat/" + "misctex_" +newWpName + ".wta")
                            newpackDatt("deploy/misctex/" + "misctex_" + newWpName + "_dat/", "deploy/misctex/" + "misctex_" +newWpName + ".dat")
                        if misFile.endswith(".dtt"):
                            shutil.copyfile(wkDir + "/misctex/" + misFile, 'deploy/misctex/' + "misctex_" + newWpName + ".dtt")
                            newdattUn.main('deploy/misctex/' + "misctex_" + newWpName + ".dtt",'deploy/misctex/' + "misctex_" + newWpName + "_dtt")
                            for filename in os.scandir("deploy/misctex/" + "misctex_" + newWpName + "_dtt"):
                                try:
                                    shutil.copyfile("deploy/misctex/" + "misctex_" + newWpName + "_dtt/" + str(filename)[11:][:-2], "deploy/misctex/" + "misctex_" + newWpName + "_dtt/" + "misctex_" + newWpName + str(filename)[25:][:-2])
                                except shutil.SameFileError:
                                    pass
                                curStr= str(filename)[11:][:-2]
                                if not curStr.startswith(newWpName):
                                    delString = "deploy/misctex/" + newWpName + "_dtt/" + str(filename)[11:][:-2]
                                    try:
                                        os.remove(delString)
                                    except:
                                        pass
                            newpackDatt("deploy/misctex/" + "misctex_" + newWpName + "_dtt/", "deploy/misctex/" + "misctex_" +newWpName + ".dtt")

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
                newpackDatt("deploy/misctex/" + "misctex_" + newWpName + "_dtt/", "deploy/misctex/" + "misctex_" +newWpName + ".dtt")

    print("[Converting new XML...]")
    xml2Bxm.main(xmlList)
    print("[Building MCD...]")
    mcd.json_to_mcd("yamm_data/ui_core_us/messcore.json", "yamm_data/ui_core_us/messcore.mcd")

    print("[Packing essential .dat's...]")
    newpackDatt("yamm_data/core/", "deploy/core/core.dat")
    newpackDatt("yamm_data/coregm/", "deploy/core/coregm.dat")
    dattExpo.main("yamm_data/ui_core_us/", "deploy/ui/ui_core_us.dat")
    shutil.copytree("deploy/", nierDatDir, copy_function=shutil.move, dirs_exist_ok=True)
    print("[Mods successfuly deployed!]")