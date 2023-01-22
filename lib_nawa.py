import json, os, random, struct, shutil
import nawa_data.fileporters.newdat_unpacker as newdattUn
import nawa_data.fileporters.bxmToXml as bxm2xml
import nawa_data.fileporters.mcd as mcd

def read_uint32(file) -> int:
    entry = file.read(4)
    return struct.unpack('<I', entry)[0]

def to_uint(bs):
    return int.from_bytes(bs, byteorder='little', signed=False)

class WTA(object):
    def __init__(self, wta_fp):
        super(WTA, self).__init__()
        self.magicNumber = wta_fp.read(4)
        if self.magicNumber == b'WTB\x00':
            self.unknown04 = read_uint32(wta_fp)
            self.textureCount = read_uint32(wta_fp)
            self.textureOffsetArrayOffset = read_uint32(wta_fp)
            self.textureSizeArrayOffset = read_uint32(wta_fp)
            self.unknownArrayOffset1 = read_uint32(wta_fp)
            self.textureIdentifierArrayOffset = read_uint32(wta_fp)
            self.unknownArrayOffset2 = read_uint32(wta_fp)
            self.wtaTextureOffset = [0] * self.textureCount
            self.wtaTextureSize = [0] * self.textureCount
            self.wtaTextureIdentifier = [0] * self.textureCount
            self.unknownArray1 = [0] * self.textureCount
            self.unknownArray2 = []
            for i in range(self.textureCount):
                wta_fp.seek(self.textureOffsetArrayOffset + i * 4)
                self.wtaTextureOffset[i] = read_uint32(wta_fp)
                wta_fp.seek(self.textureSizeArrayOffset + i * 4)
                self.wtaTextureSize[i] =  read_uint32(wta_fp)
                wta_fp.seek(self.textureIdentifierArrayOffset + i * 4)
                self.wtaTextureIdentifier[i] = "%08x"%read_uint32(wta_fp)
                wta_fp.seek(self.unknownArrayOffset1 + i * 4)
                self.unknownArray1[i] = "%08x"%read_uint32(wta_fp)
            wta_fp.seek(self.unknownArrayOffset2 )
            unknownval =  (wta_fp.read(4))
            while unknownval:
                self.unknownArray2.append(to_uint(unknownval))
                unknownval =  (wta_fp.read(4))
            self.pointer2 = hex(wta_fp.tell())
    def getTextureByIndex(self, texture_index, texture_fp):
        texture_fp.seek(self.wtaTextureOffset[texture_index])
        texture = texture_fp.read(self.wtaTextureSize[texture_index])
        return texture

    def getTextureByIdentifier(self, textureIdentifier, texture_fp):
        for index in range(self.textureCount):
            if self.wtaTextureIdentifier[index] == textureIdentifier:
                return self.getTextureByIndex(index,texture_fp)
        return False

identifierBlackList = open("configs/ddslist.txt", "r")
data = identifierBlackList.read()
idBlackList = data.split("\n")
identifierBlackList.close()

wpidBlacklist = []
idBlacklist = []
def regenBlacklists():
    global wpidBlacklist, idBlacklist, newUid
    wpidBlacklistFile = open("configs/allwpids.txt", "r")
    data = wpidBlacklistFile.read()
    wpidBlacklist = data.split("\n")
    wpidBlacklistFile.close()

    idBlacklistFile = open("configs/wpids.txt", "r")
    data = idBlacklistFile.read()
    idBlacklist = data.split("\n")
    idBlacklistFile.close()
    newUid = 1003

regenBlacklists()



def checkStringFont(str, font):
    if font == 36:
        font_char_list = [" ", "#", "%", "&", "'", "(", ")", "*", "+", ",", "-", ".", "/", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ":", "?", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "[", "]", "_", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "!"]
    if font == 5:
        font_char_list = [" ", "%", "&", "'", "(", ")", "+", "-", ".", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ":", "A", "B", "C", "D", "E", "F", "G", "H", "I", "K", "L", "M", "N", "O", "P", "R", "S", "T", "U", "V", "W", "Y", "a", "b", "c", "d", "e", "f", "g", "h", "i", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
    newStr = ""
    invalidCharList = []
    for i in str:
        if i in font_char_list:
            newStr += i
        else:
            invalidCharList.append(i)
    print(f"[Removed invalid characters {invalidCharList}]")
    return 


logDelList = []
def getWPfileName(wpC):
    global logDelList
    #deciding on weapon name for weapon category based on WPC
    if wpC == "0":
        cName = "Small Sword"
        indexStart = 2
        indexEnd = 199
    if wpC == "1":
        cName = "Large Sword"
        indexStart = 201
        indexEnd = 399
    if wpC == "2":
        cName = "Spear"
        indexStart = 401
        indexEnd = 599
    if wpC == "3":
        cName = "Combat Bracer"
        indexStart = 601
        indexEnd = 799
    #setting wpidnotfound to True to iterate through the wpid list to make sure no dupe happens. < dupe id bad, we dont want this to happen lol
    wpidnotFound = True
    while wpidnotFound:
        nWpn = indexStart
        #checking if the index is shorter, to add some 0s thanks python for not allowing itegers to start with 0
        if len(str(nWpn)) == 1:
            newuId = "000" + str(nWpn)
        if len(str(nWpn)) == 2:
            newuId = "00" + str(nWpn)
        if len(str(nWpn)) == 3:
            newuId = "0" + str(nWpn)
        if newuId in wpidBlacklist:
            dummyVar = 0
        if newuId == indexEnd:
            #if newui hits indexend skip weapon, sadly only a limited ammount of weapons can be added
            print(f"[WPNAME ERROR: YOU RAN OUT OF SPACE IN THE {cName} CATEGORY, REMOVE A MOD FROM THE CATEGORY, THIS WEAPON WILL NOT BE EXPORTED]")
            wpidnotFound = False
            return "Skip"
        if newuId not in wpidBlacklist:
                #return new wp id for the weapon aswell as its uid counterpart with an 1 at the start
                logDelList.append(newuId)
                wpidBlacklist.append(newuId)
                wpidnotFound = False
                return newuId, "1" + newuId[1:]
        else:
            indexStart +=1

def write_last_wp():
    global logDelList
    with open("configs/lastWP.txt", "w") as f:
        write_list = []
        for str in logDelList:
            if not str in write_list:
                write_list.append
                f.write("%s\n" % str)

#cleans the deploy folder, cleaning good pog
def cleanDeploy():
    regenBlacklists()
    for filename in os.scandir("nawa_data/deploy/"):
        subFName = filename
        for filename in os.scandir(subFName):
            toRM = "nawa_data/deploy/" + str(subFName)[11:][:-2] + "/" + str(filename)[11:][:-2]
            if os.path.isdir(toRM):
                shutil.rmtree(toRM)
            else:
                os.remove(toRM)

def genNierIdentifier():
    # getting random hexstring to use as identifer
    random_ID = ''.join(random.choice('0123456789ABCDEF') for n in range(8))
    while random_ID in idBlackList: #compare new string against list of all known ingame identifiers to not have dupes
        print("Dupe found")
        random_ID = ''.join(random.choice('0123456789ABCDEF') for n in range(8))
        quit()
    idBlackList.append(random_ID)
    return random_ID

def conWeaponType(re):   #doing a bit of the skiddoodle to translate a name to a number and back for the configs
    if re == "0":
        return "Small Sword"
    if re == "1":
        return "Large Sword"
    if re == "2":
        return "Spear"
    if re == "3":
        return "Combat Bracers"
    if re == "Small Sword":
        return "0"
    if re == "Large Sword":
        return "1"
    if re == "Spear":
        return "2"
    if re == "Combat Bracers":
        return "3"


def checkStringFont(str, font):
    if font == 36:
        font_char_list = [" ", "#", "%", "&", "'", "(", ")", "*", "+", ",", "-", ".", "/", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ":", "?", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "[", "]", "_", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "!"]
    if font == 5:
        font_char_list = [" ", "%", "&", "'", "(", ")", "+", "-", ".", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ":", "A", "B", "C", "D", "E", "F", "G", "H", "I", "K", "L", "M", "N", "O", "P", "R", "S", "T", "U", "V", "W", "Y", "a", "b", "c", "d", "e", "f", "g", "h", "i", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
    newStr = ""
    invalidCharList = []
    for i in str:
        if i in font_char_list:
            newStr += i
        else:
            invalidCharList.append(i)
    print(f"[Removed invalid characters {invalidCharList}]")
    return newStr

#make kewl list from folderidoo
def genPathList(folder):
    mDir = os.listdir(folder)
    mDir2 = []
    for str in mDir:
        entry = folder + str
        mDir2.append(entry)
    return mDir2




#replaces a string inside of ta binary thingeridoo...
def kewlDatt(ptf, kewlName, newName):
    with open(ptf, "rb") as f:
        contents = f.read()
    ff=contents.replace(kewlName.encode("ascii"), newName.encode("ascii"))
    with open(ptf, "wb") as f:
        f.write(ff)


def genInsertableID(wtaFilePath): #if im honest i dont know what this does anymore. its needed. dont remove
    global wtaIdTable
    nierID = genNierIdentifier()
    retNierId = " ".join(nierID[i:i+2] for i in range(0, len(nierID), 2))
    return retNierId

def identifierTurn(str): #takes a kewl 8 char long string and make it be reverse.
    revID = str[::-1]
    l1 = str[:-6]
    l2 = str[:-4][2:]
    l3 = str[:-2][4:]
    l4 = str[6:]
    binStr = l4 + l3 + l2 + l1

    return binStr

def replace_in_hex(file_to_manipulate, stringtoreplace, stringtoplace): #replaces a string in a file via the kewl read and write binary shit lol
    g1 = bytes.fromhex(stringtoreplace)
    g2 = bytes.fromhex(stringtoplace)

    with open(file_to_manipulate, "rb") as file:
        content = file.read()
    rp = content.replace(g1, g2)
    with open(file_to_manipulate, "wb") as file:
        file.write(rp)

def shuffleIdentifierMisctex(wtaFilePath):
    with open(wtaFilePath, "rb") as wtab_fp:
        wtaIdTable = WTA(wtab_fp).wtaTextureIdentifier
    for str in wtaIdTable:
        newIDd=genInsertableID(wtaFilePath)
        revTurnTab= " ".join(identifierTurn(str)[i:i+2] for i in range(0, len(identifierTurn(str)), 2))
        replace_in_hex(wtaFilePath, revTurnTab, newIDd) #shuffles identifiers but for misctex only..

def shuffleIdentifierWta(wtaFilePath, wmbFilePath):
    with open(wtaFilePath, "rb") as wtab_fp:
        wtaIdTable = WTA(wtab_fp).wtaTextureIdentifier
    for str in wtaIdTable:
        newIDd=genInsertableID(wtaFilePath)
        revTurnTab= " ".join(identifierTurn(str)[i:i+2] for i in range(0, len(identifierTurn(str)), 2))
        replace_in_hex(wtaFilePath, revTurnTab, newIDd)
        replace_in_hex(wmbFilePath[:-4] + ".wmb", revTurnTab, newIDd)

def prepareDatFiles():      #init to make the dat files into usable folders for the main script to work on the xmls, no dmca infringement baby!
    datList = ["dat_files/core.dat",
               "dat_files/coregm.dat",
               "dat_files/ui_core_us.dat"
               ]
    bxmList = ["nawa_data/dat_files/coregm.dat/WeaponInfoTable.bxm",
               "nawa_data/dat_files/coregm.dat/ItemInfoTable.bxm",
               "nawa_data/dat_files/coregm.dat/ShopInfoTable.bxm",
               "nawa_data/dat_files/coregm.dat/WeaponStrengthenTable.bxm",
               "nawa_data/dat_files/core.dat/WeaponStrengthenTable.bxm"
               ]
    for str in datList:
        if os.path.isfile(str):
            print(f"[Unpacking {str}]")
            newdattUn.main(str, "nawa_data/" + str)
        else:
            print("[ERROR: PLEASE PUT VALID DAT FILES IN THE DAT FILES DIRECTORY]\n")
            return False
    for str in bxmList:
        print(f"[Preparing XML File {str}]")
        bxm2xml.main(str)
    print("[Preparing MCD]")
    mcd.mcd_to_json("nawa_data/dat_files/ui_core_us.dat/messcore.mcd")

with open("nawa_data/configTemplates/coregmItemInfoTable.xml", 'r') as file:
    coregmItemInfoTable_string = file.read()
with open("nawa_data/configTemplates/coregmShopInfoTable.xml", 'r') as file:
    coregmShopInfoTable_string = file.read()
with open("nawa_data/configTemplates/coregmWeaponInfoTable.xml", 'r') as file:
    coregmWeaponInfoTable_string = file.read()
with open("nawa_data/configTemplates/coregmWeaponStrenghtTable.xml", 'r') as file:
    coregmWeaponStrenghtenTable_string = file.read()
with open("nawa_data/configTemplates/coreWeaponStrenghtTable.xml", 'r') as file:
    coreWeaponStrenghtTable_string = file.read()
with open("nawa_data/configTemplates/messcore.json", 'r') as file:
    uimesscore_string = file.read()

def append_weapon_info_to_tables(weapon_pack): #append extracted dat tables with data of a weapon package.

    w_p = weapon_pack  #short variable to make the entire later format string a bit shorter

    table_starter_index = 1
    while not table_starter_index == 8:
        if table_starter_index == 1:
            temp_table_file = coregmItemInfoTable_string
            table_Path = "nawa_data/dat_files/coregm.dat/ItemInfoTable.xml"
            lineOffset = 8
        if table_starter_index == 2:
            temp_table_file = coregmShopInfoTable_string
            table_Path = "nawa_data/dat_files/coregm.dat/ShopInfoTable.xml"
            lineOffset = 3567
        if table_starter_index == 3:
            temp_table_file = coregmWeaponInfoTable_string
            table_Path = "nawa_data/dat_files/coregm.dat/weaponinfotable.xml"
            lineOffset = sum(1 for line in open(table_Path)) - 2
        if table_starter_index == 4:
            temp_table_file = coregmWeaponStrenghtenTable_string
            table_Path = "nawa_data/dat_files/coregm.dat/WeaponStrengthenTable.xml"
            lineOffset = sum(1 for line in open(table_Path)) - 2
        if table_starter_index == 5:
            temp_table_file = coreWeaponStrenghtTable_string
            table_Path = "nawa_data/dat_files/core.dat/WeaponStrengthenTable.xml"
            lineOffset = sum(1 for line in open(table_Path)) - 2
        if table_starter_index == 6:
            temp_table_file = uimesscore_string
            table_Path = "nawa_data/dat_files/ui_core_us.dat/messcore.json"
            lineOffset = 3
        if table_starter_index == 7:
            table_Path = "nawa_data/dat_files/core.dat/WeaponParam.csv"
            lineOffset = 40
            temp_table_file = f"wp{w_p.weapon_id}," + w_p.weapon_config.return_weapon_stats() + "\n"

        if table_starter_index == 6:
            temp_table_file = temp_table_file.replace("newUid", w_p.unique_id)
            temp_table_file = temp_table_file.replace("newIGDescs", w_p.ingame_short_description)
            temp_table_file = temp_table_file.replace("newIGDescl", w_p.ingame_long_description)
            temp_table_file = temp_table_file.replace("newIGname", w_p.ingame_weapon_name)

        else:
            temp_table_file = temp_table_file.format(internalWPname=w_p.internal_weapon_name, 
                                                    newWPid=w_p.weapon_id,
                                                    newUid=w_p.unique_id,
                                                    newCat=w_p.weapon_type)

        with open(table_Path, "r") as f:
            table_Contents = f.readlines()
        table_Contents.insert(lineOffset, temp_table_file)
        with open(table_Path, "w") as f:
            table_Contents = "".join(table_Contents)
            f.write(table_Contents)
        table_starter_index += 1