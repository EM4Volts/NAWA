import os, random, shutil, string
import yamm_data.fileporters.mcd as mcd
import journey_tools as jout
import yamm_data.fileporters.xmlToBxm as xml2Bxm
import yamm_data.fileporters.newexport_dat as newdattExpo
import yamm_data.fileporters.newdat_unpacker as newdattUn
import yamm_data.fileporters.dat as oneTrueDatPacker

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
        misctex_files_folder = nierModsDir + "/" + filename.name + "/misctex"
        wpCFGdata = jout.readwpConfig(nierModsDir + "/" + filename.name + "/config.json")
        print("_____DEBUG_____")
        internalWeaponID = 'weapon_' + ''.join(random.choice(string.ascii_lowercase) for _ in range(11))
        wpId = jout.getWPfileName(wpCFGdata[3])
        new_wp_name = wpId[0]
        uniqueID = wpId[1]
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
                oneTrueDatPacker.main(unpack_dat_path + "/", new_dat_path)
                oneTrueDatPacker.main(unpack_dtt_path + "/", new_dtt_path)
                shutil.rmtree(unpack_dat_path)
                shutil.rmtree(unpack_dtt_path)


        if os.path.isdir(misctex_files_folder):
            print(filename.name, "has misctex")
            for filename in os.scandir(misctex_files_folder):
                mt_Path = misctex_files_folder + "/" + filename.name
                if mt_Path.endswith(".dat"):
                    shutil.copyfile(mt_Path, "deploy/misctex/misctex_" + new_wp_name + ".dat")
                if mt_Path.endswith(".dtt"):
                    shutil.copyfile(mt_Path, "deploy/misctex/misctex_" + new_wp_name + ".dtt")
        else:
            if wpCFGdata[3] == "0":
                mTexSName = "misctex_smallsword"
            if wpCFGdata[3] == "1":
                mTexSName = "misctex_largesword"
            if wpCFGdata[3] == "2":
                mTexSName = "misctex_spear"
            if wpCFGdata[3] == "3":
                mTexSName = "misctex_bracers"
            shutil.copyfile("yamm_data\configTemplates/" + mTexSName + ".dat", "deploy/misctex/misctex_" + new_wp_name + ".dat")
            shutil.copyfile("yamm_data\configTemplates/" + mTexSName + ".dtt", "deploy/misctex/misctex_" + new_wp_name + ".dtt")


def finishMisctex():
    for filename in os.scandir("deploy/misctex"):
        mt_Path = "deploy/misctex/" + filename.name
        old_wp_name =  filename.name[:-4][8:]
        if mt_Path.endswith(".dat"):
            mt_dat_un = mt_Path + "_dat"
            newdattUn.main(mt_Path, mt_dat_un)
            for filename in os.scandir(mt_dat_un):
                if not filename.name in renameblacklist:
                    fn_rename_name = filename.name
                    fn_ext = fn_rename_name[-4:]
                    os.rename(mt_dat_un + "/" + fn_rename_name, mt_dat_un + "/misctex_"  + old_wp_name +fn_ext)
                else:
                    os.remove(mt_dat_un + "/" + filename.name)

        if mt_Path.endswith(".dtt"):
            mt_dtt_un = mt_Path + "_dtt"
            newdattUn.main(mt_Path, mt_dtt_un)
            for filename in os.scandir(mt_dtt_un):
                if not filename.name in renameblacklist:
                    fn_rename_name = filename.name
                    fn_ext = fn_rename_name[-4:]
                    os.rename(mt_dtt_un + "/" + fn_rename_name, mt_dtt_un + "/misctex_"  + old_wp_name +fn_ext)
                else:
                    os.remove(mt_dtt_un + "/" + filename.name)

            jout.shuffleIdentifierMisctex(mt_dat_un + "/" + "misctex_" + old_wp_name + ".wta")
            oneTrueDatPacker.main(mt_dtt_un + "/", "deploy/misctex/misctex_"  + old_wp_name + ".dtt")
            oneTrueDatPacker.main(mt_dat_un + "/", "deploy/misctex/misctex_"  + old_wp_name + ".dat")
            shutil.rmtree(mt_dtt_un)
            shutil.rmtree(mt_dat_un)


def deploy():
    cfgFile = open("configs/config.ini", "r")
    data = cfgFile.read()
    config = data.split("\n")
    cfgFile.close()
    global nierModsDir, nierDatDir
    nierDatDir= config[0]
    nierModsDir= config[1]
    jout.prepareDatFiles()

    if not os.path.isdir("deploy"):
        os.makedirs("deploy/wp", 0o666)
        os.makedirs("deploy/core", 0o666)
        os.makedirs("deploy/ui", 0o666)
        os.makedirs("deploy/misctex", 0o666)
    xmlList = ["yamm_data/dat_files/coregm.dat/WeaponInfoTable.xml",
               "yamm_data/dat_files/coregm.dat/ItemInfoTable.xml",
               "yamm_data/dat_files/coregm.dat/ShopInfoTable.xml",
               "yamm_data/dat_files/coregm.dat/WeaponStrengthenTable.xml",
               "yamm_data/dat_files/core.dat/WeaponStrengthenTable.xml"
               ]
    jout.cleanDeploy()
    wpStaging()
    finishMisctex()
    print("[Converting new XML...]")
    xml2Bxm.main(xmlList)
    print("[Building MCD...]")
    mcd.json_to_mcd("yamm_data/dat_files/ui_core_us.dat/messcore.json", "yamm_data/dat_files/ui_core_us.dat/messcore.mcd")
    print("[Packing essential .dat's...]")
    oneTrueDatPacker.main("yamm_data/dat_files/core.dat/", "deploy/core/core.dat")
    oneTrueDatPacker.main("yamm_data/dat_files/coregm.dat/", "deploy/core/coregm.dat")
    oneTrueDatPacker.main("yamm_data/dat_files/ui_core_us.dat/", "deploy/ui/ui_core_us.dat")
    shutil.copytree("deploy/", nierDatDir, copy_function=shutil.copy, dirs_exist_ok=True)
    print("[Mods successfuly deployed!]")

    jout.cleanDeploy()
