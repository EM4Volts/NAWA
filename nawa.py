import os, random, shutil, string, datetime, json, binascii
import nawa_data.fileporters.newdat_unpacker as dat_unpacker
import nawa_data.fileporters.dat as dat_packer
import nawa_data.fileporters.xmlToBxm as xml2Bxm
import nawa_data.fileporters.mcd as mcd
import lib_nawa, save



cfgFile = open("configs/config.ini", "r") #loads filePath configs for mods and data dir
data = cfgFile.read()
config = data.split("\n")
cfgFile.close()
nierDatDir= config[0]
nierModsDir= config[1]
save_file= config[2]


default_weapon_config = {
    "weapon_name":          "Mysterious Weapon", 
    "short_description":    "How did this get here?", 
    "long_description":     "How did this get here?", 
    "weapon_type":          "0",
    "config_version" :      "1",
    "level_1_left_damage":  "160", 
    "level_1_right_damage": "190", 
    "level_1_left_combo":   "5", 
    "level_1_right_combo":  "3", 
    "level_1_speed":        "100", 
    "level_1_endurance":    "69", 
    "level_1_stun":         "100", 
    "level_1_crit":         "0", 
    "level_2_left_damage":  "320", 
    "level_2_right_damage": "380", 
    "level_2_left_combo":   "5", 
    "level_2_right_combo":  "3", 
    "level_2_speed":        "110", 
    "level_2_endurance":    "100", 
    "level_2_stun":         "100", 
    "level_2_crit":         "0", 
    "level_3_left_damage":  "448", 
    "level_3_right_damage": "532", 
    "level_3_left_combo":   "6", 
    "level_3_right_combo":  "3", 
    "level_3_speed":        "115", 
    "level_3_endurance":    "100", 
    "level_3_stun":         "100", 
    "level_3_crit":         "0",
    "level_4_left_damage":  "608", 
    "level_4_right_damage": "722", 
    "level_4_left_combo":   "7", 
    "level_4_right_combo":  "3", 
    "level_4_speed":        "120", 
    "level_4_endurance":    "100", 
    "level_4_stun":         "100", 
    "level_4_crit":         "0"
    }   

def file_crc32(filename):   #calculates the crc32 hash of a file, in the future used for calculating wether files changed to not have weapons redeploy to save a couple seconds on deploy
    file_buffer = open(filename,'rb').read()
    file_buffer = (binascii.crc32(file_buffer) & 0xFFFFFFFF)
    return "%08X" % file_buffer

class WEAPON_CONFIG:        #reads a weapon config, made into a class for easier usablility
    def __init__(self, config_path):


        if not os.path.isfile(config_path):
            self.regen_config()

        with open(config_path, "r") as file:
            wpconf = file.read()
        
        self.config_path = config_path

        wpconfJson                  =   json.loads(wpconf)
        if "level_1_right_damage" in wpconfJson:
            self.weapon_name            =   wpconfJson['weapon_name']
            self.short_description      =   wpconfJson['short_description']
            self.long_description       =   wpconfJson['long_description']
            self.weapon_type            =   wpconfJson['weapon_type']  
            self.level_1_left_damage    =   wpconfJson["level_1_left_damage"]
            self.level_1_right_damage   =   wpconfJson["level_1_right_damage"]
            self.level_1_left_combo     =   wpconfJson["level_1_left_combo"]
            self.level_1_right_combo    =   wpconfJson["level_1_right_combo"]
            self.level_1_speed          =   wpconfJson["level_1_speed"]
            self.level_1_endurance      =   wpconfJson["level_1_endurance"]
            self.level_1_stun           =   wpconfJson["level_1_stun"]
            self.level_1_crit           =   wpconfJson["level_1_crit"]
            self.level_2_left_damage    =   wpconfJson["level_2_left_damage"]
            self.level_2_right_damage   =   wpconfJson["level_2_right_damage"]
            self.level_2_left_combo     =   wpconfJson["level_2_left_combo"]
            self.level_2_right_combo    =   wpconfJson["level_2_right_combo"]
            self.level_2_speed          =   wpconfJson["level_2_speed"]
            self.level_2_endurance      =   wpconfJson["level_2_endurance"]
            self.level_2_stun           =   wpconfJson["level_2_stun"]
            self.level_2_crit           =   wpconfJson["level_2_crit"]
            self.level_3_left_damage    =   wpconfJson["level_3_left_damage"]
            self.level_3_right_damage   =   wpconfJson["level_3_right_damage"]
            self.level_3_left_combo     =   wpconfJson["level_3_left_combo"]
            self.level_3_right_combo    =   wpconfJson["level_3_right_combo"]
            self.level_3_speed          =   wpconfJson["level_3_speed"]
            self.level_3_endurance      =   wpconfJson["level_3_endurance"]
            self.level_3_stun           =   wpconfJson["level_3_stun"]
            self.level_3_crit           =   wpconfJson["level_3_crit"] 
            self.level_4_left_damage    =   wpconfJson["level_4_left_damage"]
            self.level_4_right_damage   =   wpconfJson["level_4_right_damage"]
            self.level_4_left_combo     =   wpconfJson["level_4_left_combo"]
            self.level_4_right_combo    =   wpconfJson["level_4_right_combo"]
            self.level_4_speed          =   wpconfJson["level_4_speed"]
            self.level_4_endurance      =   wpconfJson["level_4_endurance"]
            self.level_4_stun           =   wpconfJson["level_4_stun"]
            self.level_4_crit           =   wpconfJson["level_4_crit"]             
        else:
            self.weapon_name            =   wpconfJson["weaponname"]
            self.short_description      =   wpconfJson["weapondescshort"]
            self.long_description       =   wpconfJson["weapondesclong"]
            self.weapon_type            =   wpconfJson["weapontype"]
            self.level_1_left_damage    =   wpconfJson["lvl1dmgl"]
            self.level_1_right_damage   =   wpconfJson["lvl1dmgr"]
            self.level_1_left_combo     =   wpconfJson["lvl1cmbl"]
            self.level_1_right_combo    =   wpconfJson["lvl1cmbr"]
            self.level_1_speed          =   wpconfJson["lvl1spd"]
            self.level_1_endurance      =   wpconfJson["lvl1end"]
            self.level_1_stun           =   wpconfJson["lvl1stun"]
            self.level_1_crit           =   wpconfJson["lvl1crit"]
            self.level_2_left_damage    =   wpconfJson["lvl2dmgl"]
            self.level_2_right_damage   =   wpconfJson["lvl2dmgr"]
            self.level_2_left_combo     =   wpconfJson["lvl2cmbl"]
            self.level_2_right_combo    =   wpconfJson["lvl2cmbr"]
            self.level_2_speed          =   wpconfJson["lvl2spd"]
            self.level_2_endurance      =   wpconfJson["lvl2end"]
            self.level_2_stun           =   wpconfJson["lvl2stun"]
            self.level_2_crit           =   wpconfJson["lvl2crit"]
            self.level_3_left_damage    =   wpconfJson["lvl3dmgl"]
            self.level_3_right_damage   =   wpconfJson["lvl3dmgr"]
            self.level_3_left_combo     =   wpconfJson["lvl3cmbl"]
            self.level_3_right_combo    =   wpconfJson["lvl3cmbr"]
            self.level_3_speed          =   wpconfJson["lvl3spd"]
            self.level_3_endurance      =   wpconfJson["lvl3end"]
            self.level_3_stun           =   wpconfJson["lvl3stun"]
            self.level_3_crit           =   wpconfJson["lvl3crit"]
            self.level_4_left_damage    =   wpconfJson["lvl4dmgl"]
            self.level_4_right_damage   =   wpconfJson["lvl4dmgr"]
            self.level_4_left_combo     =   wpconfJson["lvl4cmbl"]
            self.level_4_right_combo    =   wpconfJson["lvl4cmbr"]
            self.level_4_speed          =   wpconfJson["lvl4spd"]
            self.level_4_endurance      =   wpconfJson["lvl4end"]
            self.level_4_stun           =   wpconfJson["lvl4stun"]
            self.level_4_crit           =   wpconfJson["lvl4crit"]

    def regen_config(self):
         with open(self.config_path, 'w') as f:
                json.dump(default_weapon_config, f, ensure_ascii=False, indent=4)
                print("[Generating config]")
    def save(self):
        with open(self.config_path, 'w') as file:
            dict_data = self.__dict__
            del dict_data['config_path']
            json.dump(dict_data, file, ensure_ascii=False, indent=4)
    
    def return_weapon_stats(self): #returns the first part of the string used for the weaponParam.csv
        stat_dict = self.__dict__
        del stat_dict['config_path'], stat_dict['weapon_name'], stat_dict['short_description'], stat_dict['long_description'], stat_dict['weapon_type'] 
        stat_csv_string = ""
        for v in stat_dict.values():
            stat_csv_string = stat_csv_string + f"{v},"
        return "6," + stat_csv_string + ",,,,,,"

class WEAPON_PACKAGE:           #A package of all contents of a weapons mod folder as a class
    def __init__(self, weapon_pack_root):

        self.weapon_model               =   f"{weapon_pack_root}/wp/"
        self.weapon_misctex             =   f"{weapon_pack_root}/misctex/"
        self.weapon_effect              =   f"{weapon_pack_root}/effect/"
        self.weapon_valid               =   False
        self.misctex_valid              =   False
        self.weapon_model_list          =   []
        self.weapon_misctex_list        =   []
        self.weapon_model_dat_count     =   0
        self.weapon_model_dtt_count     =   0
        self.weapon_misctex_dat_count   =   0
        self.weapon_misctex_dtt_count   =   0

        if os.path.isdir(self.weapon_model):    #adds all dtt and dat files from the wp directory to a list 
            for filename in os.scandir(self.weapon_model):
                if filename.name.endswith(".dat"):
                    self.weapon_model_dat_count += 1
                    self.weapon_model_list.append(self.weapon_model + filename.name)
                if filename.name.endswith(".dtt"):
                    self.weapon_model_dtt_count += 1 
                    self.weapon_model_list.append(self.weapon_model + filename.name)

        if os.path.isdir(self.weapon_misctex):    #adds all dtt and dat files from the misctex directory to a list 
            for filename in os.scandir(self.weapon_misctex):
                if filename.name.endswith(".dat"):
                    self.weapon_misctex_dat_count += 1
                    self.weapon_misctex_list.append(self.weapon_misctex + filename.name)
                if filename.name.endswith(".dtt"):
                    self.weapon_misctex_dtt_count += 1 
                    self.weapon_misctex_list.append(self.weapon_misctex + filename.name)

        if self.weapon_model_dat_count == 1 and self.weapon_model_dtt_count == 1: #checks if only 1 dat and dtt exists in the folder, if yes weapon is valid else it isnt
            self.weapon_valid = True
        if self.weapon_valid:   # if valid prepare config, aswell as get information for later usage in infotables
            if not os.path.isfile(f"{weapon_pack_root}/config.json"):
                with open(f"{weapon_pack_root}/config.json", 'w') as f:
                    json.dump(default_weapon_config, f, ensure_ascii=False, indent=4)
            self.weapon_config              =   WEAPON_CONFIG(f"{weapon_pack_root}/config.json")
            self.weapon_type                =   self.weapon_config.weapon_type
            self.ids                        =   lib_nawa.getWPfileName(self.weapon_config.weapon_type)
            self.weapon_id                  =   self.ids[0]
            self.unique_id                  =   self.ids[1]
            self.internal_weapon_name       =   'weapon_' + ''.join(random.choice(string.ascii_lowercase) for _ in range(11))
            self.ingame_weapon_name         =   self.weapon_config.weapon_name
            self.ingame_short_description   =   self.weapon_config.short_description
            self.ingame_long_description    =   self.weapon_config.long_description

        if self.weapon_misctex_dat_count == 1 and self.weapon_misctex_dtt_count == 1: #checks if only 1 dat and dtt exists in the folder, if yes misctex is valid else it isnt
            self.misctex_valid = True

    def rename_in_misctex_dat(self, list):
        for dat_file in list:
            dat_unpacker.main(dat_file, f"nawa_data/deploy/misctex/{self.weapon_id}_{dat_file[-3:]}")
            for filename in os.scandir(f"nawa_data/deploy/misctex/{self.weapon_id}_{dat_file[-3:]}"):
                filename_extension = filename.name[-4:]
                os.rename(f"nawa_data/deploy/misctex/{self.weapon_id}_{dat_file[-3:]}/{filename.name}", f"nawa_data/deploy/misctex/{self.weapon_id}_{dat_file[-3:]}/misctex_wp{self.weapon_id}{filename_extension}")
            for filename in os.scandir(f"nawa_data/deploy/misctex/{self.weapon_id}_dat"):
                if filename.name.endswith(".wta"):
                    lib_nawa.shuffleIdentifierMisctex(filename)
        dat_packer.main(f"nawa_data/deploy/misctex/{self.weapon_id}_dat", f"nawa_data/deploy/misctex/misctex_wp{self.weapon_id}.dat")
        dat_packer.main(f"nawa_data/deploy/misctex/{self.weapon_id}_dtt", f"nawa_data/deploy/misctex/misctex_wp{self.weapon_id}.dtt")
        shutil.rmtree(f"nawa_data/deploy/misctex/{self.weapon_id}_dat")
        shutil.rmtree(f"nawa_data/deploy/misctex/{self.weapon_id}_dtt")
            
    def build_deploy_package(self):                     #builds the new weapon package in the deploy folder for later deployment

        for dat_file in self.weapon_model_list:
            dat_unpacker.main(dat_file, f"nawa_data/deploy/wp/{self.weapon_id}_{dat_file[-3:]}")
            for filename in os.scandir(f"nawa_data/deploy/wp/{self.weapon_id}_{dat_file[-3:]}"):
                fn_rename_name = filename.name
                new_fn_name = fn_rename_name.replace(os.path.basename(dat_file)[:6], "wp" + self.weapon_id)
                os.rename(f"nawa_data/deploy/wp/{self.weapon_id}_{dat_file[-3:]}" + "/" + fn_rename_name, f"nawa_data/deploy/wp/{self.weapon_id}_{dat_file[-3:]}" + "/"  + new_fn_name)

        lib_nawa.shuffleIdentifierWta(f"nawa_data/deploy/wp/{self.weapon_id}_dat/wp{self.weapon_id}.wta", f"nawa_data/deploy/wp/{self.weapon_id}_dtt/wp{self.weapon_id}.wmb")
        dat_packer.main(f"nawa_data/deploy/wp/{self.weapon_id}_dat", f"nawa_data/deploy/wp/wp{self.weapon_id}.dat")
        dat_packer.main(f"nawa_data/deploy/wp/{self.weapon_id}_dtt", f"nawa_data/deploy/wp/wp{self.weapon_id}.dtt")
        shutil.rmtree(f"nawa_data/deploy/wp/{self.weapon_id}_dat")
        shutil.rmtree(f"nawa_data/deploy/wp/{self.weapon_id}_dtt")
        
    
        if self.misctex_valid:
            self.rename_in_misctex_dat(self.weapon_misctex_list)

        else:
            if self.weapon_type == "0":
                misctex_insert_list = ["nawa_data/configTemplates/misctex_smallsword.dat", "nawa_data/configTemplates/misctex_smallsword.dtt"]
            if self.weapon_type == "1":
                misctex_insert_list = ["nawa_data/configTemplates/misctex_largesword.dat", "nawa_data/configTemplates/misctex_largesword.dtt"]
            if self.weapon_type == "2":
                misctex_insert_list = ["nawa_data/configTemplates/misctex_spear.dat", "nawa_data/configTemplates/misctex_spear.dtt"]
            if self.weapon_type == "3":
                misctex_insert_list = ["nawa_data/configTemplates/misctex_bracers.dat", f"nawa_data/configTemplates/misctex_bracers.dtt"]
            self.rename_in_misctex_dat(misctex_insert_list)

        if os.path.isdir(self.weapon_effect): #Check if effect folder exists. copy over the eff file within if exists.
            for filename in os.scandir(self.weapon_effect):
                effect_Path = self.weapon_effect + "/" + filename.name
                if effect_Path.endswith(".eff"):
                    shutil.copyfile(effect_Path, f"nawa_data/deploy/effect/wp{self.weapon_id}.eff")

class WEAPON_MODS_FOLDER:       #Class for mods folder itself
    def __init__(self, mods_folder):

        self.valid_weapon_list = []
        self.invalid_weapon_list = []

        for filename in os.scandir(mods_folder):            #append all mods to one of two lists, either valid or invalid
            weapon = WEAPON_PACKAGE(f"{mods_folder}/{filename.name}")
            if weapon.weapon_valid:
                self.valid_weapon_list.append(weapon)
            else:
                self.invalid_weapon_list.append(weapon)
                

        print(f"[Found {len(self.valid_weapon_list)} valid Weapons]")
        if len(self.valid_weapon_list) > 40:
            print("ERROR, TOO MANY WEAPONS")

        print(f"[Found {len(self.invalid_weapon_list)} invalid Weapons]")



def nawa_deploy():
    global save_file
    print(f"[{datetime.datetime.now()}]")                                                   #print the starting time

    global nierModsDir, nierDatDir                                                          # get global config vars
    
    print("[Starting deployment]\n[Unpacking supplemental dat files]")

    if lib_nawa.prepareDatFiles() == False:                                                 #prepare the supplemental dat files, returns true if success. on false print an error and break.
        print("[ERROR: PLEASE PUT VALID DAT FILES IN THE DAT FILES DIRECTORY]\n")
    else:                                                                                   #if succsess deployment continues normally
        if not os.path.isdir("nawa_data/deploy"):                                           #make the deploy folders if not existing for any reason
            os.makedirs("nawa_data/deploy/wp", 0o666)
            os.makedirs("nawa_data/deploy/core", 0o666)
            os.makedirs("nawa_data/deploy/ui", 0o666)
            os.makedirs("nawa_data/deploy/misctex", 0o666)
            os.makedirs("nawa_data/deploy/effect", 0o666)

        xmlList = ["nawa_data/dat_files/coregm.dat/WeaponInfoTable.xml",                    #list of all xml files that will be needed to convert back to bxm later on
                   "nawa_data/dat_files/coregm.dat/ItemInfoTable.xml",
                   "nawa_data/dat_files/coregm.dat/ShopInfoTable.xml",
                   "nawa_data/dat_files/coregm.dat/WeaponStrengthenTable.xml",
                   "nawa_data/dat_files/core.dat/WeaponStrengthenTable.xml"
                   ]

        lib_nawa.cleanDeploy()                                                              #cleans the deploy folders if anything is in there

        weapon_id_list = []
        mod_folder = WEAPON_MODS_FOLDER(nierModsDir)                                        #start construction of all needed data of the mods folder.
        for weapon_mod in mod_folder.valid_weapon_list:
            weapon_mod.build_deploy_package()                                                #builds every valid weapon package into a deployment pack
            weapon_id_list.append(int(weapon_mod.unique_id))
        for i in mod_folder.valid_weapon_list:                                              #writes all the data tables for each weapon
            lib_nawa.append_weapon_info_to_tables(i)

        xml2Bxm.main(xmlList)                                                               #converts the newly appended xml files back to bxm                                                              

        mcd.json_to_mcd("nawa_data/dat_files/ui_core_us.dat/messcore.json",                 #convert the mcd files json back to mcd
                        "nawa_data/dat_files/ui_core_us.dat/messcore.mcd")

        dat_packer.main("nawa_data/dat_files/core.dat/", "nawa_data/deploy/core/core.dat")  #pack all the dat files
        dat_packer.main("nawa_data/dat_files/coregm.dat/", "nawa_data/deploy/core/coregm.dat")
        dat_packer.main("nawa_data/dat_files/ui_core_us.dat/", "nawa_data/deploy/ui/ui_core_us.dat")

        shutil.copytree("nawa_data/deploy/", nierDatDir, copy_function=shutil.move, dirs_exist_ok=True) #copy the deployment files to the actual game dir

        if save_file.endswith(".dat"):                                                      #check for valid save file, if yes adds the new weapons to save file
            save_file_class = save.SAVE_FILE(save_file, weapon_id_list)
            save_file_class.write_save_file()

        lib_nawa.write_last_wp()                                                            #write logfile of all weapon ids generated
        lib_nawa.cleanDeploy()                                                              #clean the deploy folders

        print(f"[{datetime.datetime.now()}]")                                               #print the finished time

        return True #AAAND its done... shorturl.at/fklQ4


