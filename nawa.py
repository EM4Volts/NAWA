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

renameblacklist = ["file_order.metadata", "hash_data.metadata"]
cfgFile = open("configs/config.ini", "r")
data = cfgFile.read()
config = data.split("\n")
cfgFile.close()
nierDatDir= config[0]
nierModsDir= config[1]

def wpStaging():
    for filename in os.scandir(nierModsDir):
        wp_Files_Folder = nierModsDir + "/" + filename.name + "/wp"
        wpCFGdata = jout.readwpConfig(nierModsDir + "/" + filename.name + "/config.json")
        print("_____DEBUG_____")
        uniqueID = jout.getUniqueID()
        internalWeaponID = 'weapon_' + ''.join(random.choice(string.ascii_lowercase) for _ in range(11))
        new_wp_name = jout.getWPfileName(wpCFGdata[3])
        print(wpCFGdata[0])
        jout.WriteAllTables(internalWeaponID, uniqueID, new_wp_name, wpCFGdata[0], wpCFGdata[1], wpCFGdata[2], wpCFGdata[3], wpCFGdata[5], wpCFGdata[6], wpCFGdata[7], wpCFGdata[8], wpCFGdata[9], wpCFGdata[10], wpCFGdata[11], wpCFGdata[12], wpCFGdata[13], wpCFGdata[14], wpCFGdata[15], wpCFGdata[16], wpCFGdata[17], wpCFGdata[18], wpCFGdata[19], wpCFGdata[20], wpCFGdata[21], wpCFGdata[22], wpCFGdata[23], wpCFGdata[24], wpCFGdata[25], wpCFGdata[26], wpCFGdata[27], wpCFGdata[28], wpCFGdata[29], wpCFGdata[30], wpCFGdata[31], wpCFGdata[32], wpCFGdata[33], wpCFGdata[34], wpCFGdata[35], wpCFGdata[36])
        for filename in os.scandir(wp_Files_Folder):
            wp_Path = wp_Files_Folder + "/" + filename.name
            old_wp_name =  filename.name[:-4]

            if wp_Path.endswith(".dat"):
                new_dat_path = "deploy/wp/" + new_wp_name + ".dat"
                unpack_dat_path = "deploy/wp/" + new_wp_name + "_dat"
                shutil.copyfile(wp_Path, new_dat_path)
                newdattUn.main(new_dat_path, unpack_dat_path)
                for filename in os.scandir(unpack_dat_path):
                    if not filename.name in renameblacklist:
                        fn_rename_name = filename.name
                        new_fn_name = fn_rename_name.replace(old_wp_name, new_wp_name)
                        os.rename(unpack_dat_path + "/" + fn_rename_name, unpack_dat_path + "/"  + new_fn_name)
                    else:
                        os.remove(unpack_dat_path + "/" + filename.name)

            if wp_Path.endswith(".dtt"):
                new_dtt_path = "deploy/wp/" + new_wp_name + ".dtt"
                unpack_dtt_path = "deploy/wp/" + new_wp_name + "_dtt"
                shutil.copyfile(wp_Path, new_dtt_path)
                newdattUn.main(new_dtt_path, unpack_dtt_path)
                for filename in os.scandir(unpack_dtt_path):
                    if not filename.name in renameblacklist:#
                        fn_rename_name = filename.name
                        new_fn_name = fn_rename_name.replace(old_wp_name, new_wp_name)
                        os.rename(unpack_dtt_path + "/" + fn_rename_name, unpack_dtt_path + "/"  + new_fn_name)
                    else:
                        os.remove(unpack_dtt_path + "/" + filename.name)
                jout.shuffleIdentifierWta(unpack_dat_path + "/" + new_wp_name + ".wta", unpack_dtt_path + "/" +  new_wp_name + ".wmb")
                newpackDatt(unpack_dat_path + "/", new_dat_path)
                newpackDatt(unpack_dtt_path + "/", new_dtt_path)
                shutil.rmtree(unpack_dat_path)
                shutil.rmtree(unpack_dtt_path)

def deploy():
    if not os.path.isdir("deploy"):
        os.makedirs("deploy/wp", 0o666)
        os.makedirs("deploy/core", 0o666)
        os.makedirs("deploy/ui", 0o666)
    xmlList = ["yamm_data/coregm/WeaponInfoTable.xml",
               "yamm_data/coregm/ItemInfoTable.xml",
               "yamm_data/coregm/ShopInfoTable.xml",
               "yamm_data/coregm/ShopInfoTable.xml",
               "yamm_data/coregm/WeaponStrengthenTable.xml",
               "yamm_data/core/WeaponStrengthenTable.xml"
               ]

    #Copy vanilla xml and json files to the work folders
    shutil.copyfile("yamm_data/xml2Merge/core/WeaponStrengthenTable.xml", "yamm_data/core/WeaponStrengthenTable.xml")
    shutil.copyfile("yamm_data/xml2Merge/core/WeaponParam.csv", "yamm_data/core/WeaponParam.csv")
    shutil.copyfile("yamm_data/xml2Merge/ui_core_us/messcore.json", "yamm_data/ui_core_us/messcore.json")
    for filename in os.listdir("yamm_data/xml2Merge/coregm"):
        shutil.copyfile("yamm_data/xml2Merge/coregm/" + filename, "yamm_data/coregm/" + filename)
    #read the cfg file for directories
    cfgFile = open("configs/config.ini", "r")
    data = cfgFile.read()
    config = data.split("\n")
    cfgFile.close()
    global nierModsDir, nierDatDir
    nierDatDir= config[0]
    nierModsDir= config[1]
    jout.cleanDeploy()
    wpStaging()
    print("[Converting new XML...]")
    xml2Bxm.main(xmlList)
    print("[Building MCD...]")
    mcd.json_to_mcd("yamm_data/ui_core_us/messcore.json", "yamm_data/ui_core_us/messcore.mcd")
    print("[Packing essential .dat's...]")
    newpackDatt("yamm_data/core/", "deploy/core/core.dat")
    newpackDatt("yamm_data/coregm/", "deploy/core/coregm.dat")
    dattExpo.main("yamm_data/ui_core_us/", "deploy/ui/ui_core_us.dat")
    shutil.copytree("deploy/", nierDatDir, copy_function=shutil.copy, dirs_exist_ok=True)
    print("[Mods successfuly deployed!]")

    jout.cleanDeploy()
