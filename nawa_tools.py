import json, os, random, struct, shutil
import yamm_data.fileporters.newdat_unpacker as newdattUn
import yamm_data.fileporters.bxmToXml as bxm2xml
import yamm_data.fileporters.mcd as mcd

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
defaultWPConf = {
"weaponname": "Mysterious Weapon",
"weapondescshort": "Descended upon the world\\nfrom a different one",
"weapondesclong": "Descended upon the world from a different one",
"weapontype": "0",
"lvl1dmgl": "160",
"lvl1dmgr": "190",
"lvl1cmbl": "5",
"lvl1cmbr": "3",
"lvl1spd": "100",
"lvl1end": "100",
"lvl1stun": "100",
"lvl1crit": "0",
"lvl2dmgl": "320",
"lvl2dmgr": "380",
"lvl2cmbl": "5",
"lvl2cmbr": "3",
"lvl2spd": "110",
"lvl2end": "100",
"lvl2stun": "100",
"lvl2crit": "0",
"lvl3dmgl": "448",
"lvl3dmgr": "532",
"lvl3cmbl": "6",
"lvl3cmbr": "3",
"lvl3spd": "115",
"lvl3end": "100",
"lvl3stun": "100",
"lvl3crit": "0",
"lvl4dmgl": "608",
"lvl4dmgr": "722",
"lvl4cmbl": "7",
"lvl4cmbr": "3",
"lvl4spd": "120",
"lvl4end": "100",
"lvl4stun": "100",
"lvl4crit": "0",
"priPerk": "0003",
"secPerk": "1003"
}

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
            print(f"[...{newuId}...]")
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
                return "wp" + newuId, "1" + newuId[1:]
        else:
            indexStart +=1

def write_last_wp():
    global logDelList
    with open("configs/lastWP.txt", "w") as f:
        for str in logDelList:
            f.write("%s\n" % str)



#cleans the deploy folder, cleaning good pog
def cleanDeploy():
    regenBlacklists()
    for filename in os.scandir("yamm_data/deploy/"):
        subFName = filename
        for filename in os.scandir(subFName):
            toRM = "yamm_data/deploy/" + str(subFName)[11:][:-2] + "/" + str(filename)[11:][:-2]
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

def translateSpecial(sId): #not used. will leave in if ever needed
    with open("configs/weaponspecials.json", "r") as specialA:
        specialAs = specialA.read()
    jsonSpecials = json.loads(specialAs)
    toReSid = jsonSpecials[sId]
    return toReSid

def resetConfig(cfDir): #resets a weapons config file to the default version... not a good way todo so but it works lmao
    with open(cfDir, 'w') as f:
        json.dump(defaultWPConf, f)
    print("config reset")

def readwpConfig(cfDir): #reads the weapon config cfDir and returns it as a list of strings (dont judge me)
    if not os.path.isfile(cfDir):
        with open(cfDir, 'w') as f:
            json.dump(defaultWPConf, f)
            print("no config found, adding default config")

    with open(cfDir, "r") as file:
        wpconf = file.read()
    wpconfJson = json.loads(wpconf)
    wpName = wpconfJson['weaponname']
    wpDescS = wpconfJson['weapondescshort']
    wpDescL = wpconfJson['weapondesclong']
    wpType = wpconfJson['weapontype']
    lvl1dmgl = wpconfJson["lvl1dmgl"]
    lvl1dmgr = wpconfJson["lvl1dmgr"]
    lvl1cmbl = wpconfJson["lvl1cmbl"]
    lvl1cmbr = wpconfJson["lvl1cmbr"]
    lvl1spd = wpconfJson["lvl1spd"]
    lvl1end = wpconfJson["lvl1end"]
    lvl1stun = wpconfJson["lvl1stun"]
    lvl1crit = wpconfJson["lvl1crit"]
    lvl2dmgl = wpconfJson["lvl2dmgl"]
    lvl2dmgr = wpconfJson["lvl2dmgr"]
    lvl2cmbl = wpconfJson["lvl2cmbl"]
    lvl2cmbr = wpconfJson["lvl2cmbr"]
    lvl2spd = wpconfJson["lvl2spd"]
    lvl2end = wpconfJson["lvl2end"]
    lvl2stun = wpconfJson["lvl2stun"]
    lvl2crit = wpconfJson["lvl2crit"]
    lvl3dmgl = wpconfJson["lvl3dmgl"]
    lvl3dmgr = wpconfJson["lvl3dmgr"]
    lvl3cmbl = wpconfJson["lvl3cmbl"]
    lvl3cmbr = wpconfJson["lvl3cmbr"]
    lvl3spd = wpconfJson["lvl3spd"]
    lvl3end = wpconfJson["lvl3end"]
    lvl3stun = wpconfJson["lvl3stun"]
    lvl3crit = wpconfJson["lvl3crit"]
    lvl4dmgl = wpconfJson["lvl4dmgl"]
    lvl4dmgr = wpconfJson["lvl4dmgr"]
    lvl4cmbl = wpconfJson["lvl4cmbl"]
    lvl4cmbr = wpconfJson["lvl4cmbr"]
    lvl4spd = wpconfJson["lvl4spd"]
    lvl4end = wpconfJson["lvl4end"]
    lvl4stun = wpconfJson["lvl4stun"]
    lvl4crit = wpconfJson["lvl4crit"]

    return wpName, wpDescS, wpDescL, wpType, wpconfJson, lvl1dmgl, lvl1dmgr, lvl1cmbl, lvl1cmbr, lvl1spd, lvl1end, lvl1stun, lvl1crit, lvl2dmgl, lvl2dmgr, lvl2cmbl, lvl2cmbr, lvl2spd, lvl2end, lvl2stun, lvl2crit, lvl3dmgl, lvl3dmgr, lvl3cmbl, lvl3cmbr, lvl3spd, lvl3end, lvl3stun, lvl3crit, lvl4dmgl, lvl4dmgr, lvl4cmbl, lvl4cmbr, lvl4spd, lvl4end, lvl4stun, lvl4crit



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

#writes the weapons config to a file... dont judge me again
def writewpConfig(cfDir, wpName, wpDescS, wpDescL, wpType, lvl1dmgl, lvl1dmgr, lvl1cmbl, lvl1cmbr, lvl1spd, lvl1end, lvl1stun, lvl1crit, lvl2dmgl, lvl2dmgr, lvl2cmbl, lvl2cmbr, lvl2spd, lvl2end, lvl2stun, lvl2crit, lvl3dmgl, lvl3dmgr, lvl3cmbl, lvl3cmbr, lvl3spd, lvl3end, lvl3stun, lvl3crit, lvl4dmgl, lvl4dmgr, lvl4cmbl, lvl4cmbr, lvl4spd, lvl4end, lvl4stun, lvl4crit):
    if not os.path.isfile(cfDir):
        with open(cfDir, 'w') as f:
            json.dump(defaultWPConf, f)
            print("no config found, adding default config")
    with open(cfDir, 'r') as file:
        wpconf = file.read()
    newCfg = json.loads(wpconf)
    dual_check_name = checkStringFont(wpName, 5)
    newCfg["weaponname"] = checkStringFont(dual_check_name, 36)
    newCfg["weapondescshort"] = checkStringFont(wpDescS, 36)
    newCfg["weapondesclong"] = checkStringFont(wpDescL, 36)
    newCfg["weapontype"] = wpType
    newCfg["lvl1dmgl"] = lvl1dmgl
    newCfg["lvl1dmgr"] = lvl1dmgr
    newCfg["lvl1cmbl"] = lvl1cmbl
    newCfg["lvl1cmbr"] = lvl1cmbr
    newCfg["lvl1spd"] = lvl1spd
    newCfg["lvl1end"] = lvl1end
    newCfg["lvl1stun"] = lvl1stun
    newCfg["lvl1crit"] = lvl1crit
    newCfg["lvl2dmgl"] = lvl2dmgl
    newCfg["lvl2dmgr"] = lvl2dmgr
    newCfg["lvl2cmbl"] = lvl2cmbl
    newCfg["lvl2cmbr"] = lvl2cmbr
    newCfg["lvl2spd"]  = lvl2spd
    newCfg["lvl2end"]  = lvl2end
    newCfg["lvl2stun"] = lvl2stun
    newCfg["lvl2crit"] = lvl2crit
    newCfg["lvl3dmgl"] = lvl3dmgl
    newCfg["lvl3dmgr"] = lvl3dmgr
    newCfg["lvl3cmbl"] = lvl3cmbl
    newCfg["lvl3cmbr"] = lvl3cmbr
    newCfg["lvl3spd"] = lvl3spd
    newCfg["lvl3end"] = lvl3end
    newCfg["lvl3stun"] = lvl3stun
    newCfg["lvl3crit"] = lvl3crit
    newCfg["lvl4dmgl"] = lvl4dmgl
    newCfg["lvl4dmgr"] = lvl4dmgr
    newCfg["lvl4cmbl"] = lvl4cmbl
    newCfg["lvl4cmbr"] = lvl4cmbr
    newCfg["lvl4spd"] = lvl4spd
    newCfg["lvl4end"] = lvl4end
    newCfg["lvl4stun"] = lvl4stun
    newCfg["lvl4crit"] = lvl4crit

    with open(cfDir, 'w') as file:
        json.dump(newCfg, file)

#make kewl list from folderidoo
def genPathList(folder):
    mDir = os.listdir(folder)
    mDir2 = []
    for str in mDir:
        entry = folder + str
        mDir2.append(entry)
    return mDir2


#open all the templates and load into mem to use later on, done on import.
with open("yamm_data/configTemplates/coregmItemInfoTable.txt", 'r') as file:
    coregmItemInfoTableCrisp = file.read()
with open("yamm_data/configTemplates/coregmShopInfoTable.txt", 'r') as file:
    coregmShopInfoTableCrisp = file.read()
with open("yamm_data/configTemplates/coregmWeaponInfoTable.txt", 'r') as file:
    coregmWeaponInfoTableCrisp = file.read()
with open("yamm_data/configTemplates/coregmWeaponStrenghtTable.txt", 'r') as file:
    coregmWeaponStrenghtenTableCrisp = file.read()
with open("yamm_data/configTemplates/coreWeaponStrenghtTable.txt", 'r') as file:
    coreWeaponStrenghtTableCrisp = file.read()
with open("yamm_data/configTemplates/messcore.txt", 'r') as file:
    uimesscoreCrisp = file.read()
with open("yamm_data/configTemplates/coreweaponParam.txt", 'r') as file:
    weaponParamCrisp = file.read()

#replaces a string inside of ta binary thingeridoo...
def kewlDatt(ptf, kewlName, newName):
    with open(ptf, "rb") as f:
        contents = f.read()
    ff=contents.replace(kewlName.encode("ascii"), newName.encode("ascii"))
    with open(ptf, "wb") as f:
        f.write(ff)

#writes to a table depending on which one was selected. different offsets for different ones. no i wont switch to proper json or xml stuff, not yet lol poggers
def writeToTable(crispSel, iName, UID, wpName, igName, igDescs, igDescl, wpCat, lvl1dmgl, lvl1dmgr, lvl1cmbl, lvl1cmbr, lvl1spd, lvl1end, lvl1stun, lvl1crit, lvl2dmgl, lvl2dmgr, lvl2cmbl, lvl2cmbr, lvl2spd, lvl2end, lvl2stun, lvl2crit, lvl3dmgl, lvl3dmgr, lvl3cmbl, lvl3cmbr, lvl3spd, lvl3end, lvl3stun, lvl3crit, lvl4dmgl, lvl4dmgr, lvl4cmbl, lvl4cmbr, lvl4spd, lvl4end, lvl4stun, lvl4crit):
    #SELECTS THE TABLE TO SET PATH, OFFSET AND TEMPLATE
    if crispSel == 1:
        crispPart = coregmItemInfoTableCrisp
        tablePath = "yamm_data/dat_files/coregm.dat/ItemInfoTable.xml"
        lineOffset = 8
    if crispSel == 2:
        crispPart = coregmShopInfoTableCrisp
        tablePath = "yamm_data/dat_files/coregm.dat/ShopInfoTable.xml"
        lineOffset = 3567
    if crispSel == 3:
        crispPart = coregmWeaponInfoTableCrisp
        tablePath = "yamm_data/dat_files/coregm.dat/weaponinfotable.xml"
        lineOffset = 10
    if crispSel == 4:
        crispPart = coregmWeaponStrenghtenTableCrisp
        tablePath = "yamm_data/dat_files/coregm.dat/WeaponStrengthenTable.xml"
        lineOffset = 3
    if crispSel == 5:
        crispPart = coreWeaponStrenghtTableCrisp
        tablePath = "yamm_data/dat_files/core.dat/WeaponStrengthenTable.xml"
        lineOffset = 3
    if crispSel == 6:
        crispPart = uimesscoreCrisp
        tablePath = "yamm_data/dat_files/ui_core_us.dat/messcore.json"
        lineOffset = 3
    if crispSel == 7:
        crispPart = weaponParamCrisp
        tablePath = "yamm_data/dat_files/core.dat/WeaponParam.csv"
        lineOffset = 40

    #REPLACE ALL PLACEHOLDER NAMES IN LOADED TEMPLATE TO GIVEN STRINGS
    crispPart = crispPart.replace("newWPid", wpName)
    if crispSel == 100:
        crispPart = crispPart.replace("newUid", str(int(UID) + 130000))
    crispPart = crispPart.replace("newUid", UID)
    crispPart = crispPart.replace("internalWPname", iName)
    crispPart = crispPart.replace("newIGname", igName)
    crispPart = crispPart.replace("newIGDescs", igDescs)
    crispPart = crispPart.replace("newIGDescl", igDescl)
    crispPart = crispPart.replace("newCat", wpCat)
    crispPart = crispPart.replace("lvl1dmgl", lvl1dmgl)
    crispPart = crispPart.replace("lvl1dmgr", lvl1dmgr)
    crispPart = crispPart.replace("lvl1cmbl", lvl1cmbl)
    crispPart = crispPart.replace("lvl1cmbr", lvl1cmbr)
    crispPart = crispPart.replace("lvl1spd", lvl1spd)
    crispPart = crispPart.replace("lvl1end", lvl1end)
    crispPart = crispPart.replace("lvl1stun", lvl1stun)
    crispPart = crispPart.replace("lvl1crit", lvl1crit)
    crispPart = crispPart.replace("lvl2dmgl", lvl2dmgl)
    crispPart = crispPart.replace("lvl2dmgr", lvl2dmgr)
    crispPart = crispPart.replace("lvl2cmbl", lvl2cmbl)
    crispPart = crispPart.replace("lvl2cmbr", lvl2cmbr)
    crispPart = crispPart.replace("lvl2spd", lvl2spd)
    crispPart = crispPart.replace("lvl2end", lvl2end)
    crispPart = crispPart.replace("lvl2stun", lvl2stun)
    crispPart = crispPart.replace("lvl2crit", lvl2crit)
    crispPart = crispPart.replace("lvl3dmgl", lvl3dmgl)
    crispPart = crispPart.replace("lvl3dmgr", lvl3dmgr)
    crispPart = crispPart.replace("lvl3cmbl", lvl3cmbl)
    crispPart = crispPart.replace("lvl3cmbr", lvl3cmbr)
    crispPart = crispPart.replace("lvl3spd", lvl3spd)
    crispPart = crispPart.replace("lvl3end", lvl3end)
    crispPart = crispPart.replace("lvl3stun", lvl3stun)
    crispPart = crispPart.replace("lvl3crit", lvl3crit)
    crispPart = crispPart.replace("lvl4dmgl", lvl4dmgl)
    crispPart = crispPart.replace("lvl4dmgr", lvl4dmgr)
    crispPart = crispPart.replace("lvl4cmbl", lvl4cmbl)
    crispPart = crispPart.replace("lvl4cmbr", lvl4cmbr)
    crispPart = crispPart.replace("lvl4spd", lvl4spd)
    crispPart = crispPart.replace("lvl4end", lvl4end)
    crispPart = crispPart.replace("lvl4stun", lvl4stun)
    crispPart = crispPart.replace("lvl4crit", lvl4crit)
    #crispPart = crispPart.replace("wpfamily")
    #OPEN TABLE AND LOAD INTO STRING
    with open(tablePath, "r") as f:
        tableContents = f.readlines()

    #INSERT CRISP INTO LOADED TABLE STRING
    tableContents.insert(lineOffset, crispPart)

    #WRITE TABLE STRING TO FILE
    with open(tablePath, "w") as f:
        tableContents = "".join(tableContents)
        f.write(tableContents)

#simplify writing to all tables by having kewl command (dont even try to judge me for this)
def WriteAllTables(a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z, a1, b1, c1, d1, e1, f1, g1, h1, i1, j1, k1, l1, m1):
    allTables = [1, 2, 3, 4, 5, 6, 7]
    #ecexutes the tablewrite on all currently accesible tables
    for int in allTables:
        writeToTable(int, a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z, a1, b1, c1, d1, e1, f1, g1, h1, i1, j1, k1, l1, m1)

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
    bxmList = ["yamm_data/dat_files/coregm.dat/WeaponInfoTable.bxm",
               "yamm_data/dat_files/coregm.dat/ItemInfoTable.bxm",
               "yamm_data/dat_files/coregm.dat/ShopInfoTable.bxm",
               "yamm_data/dat_files/coregm.dat/WeaponStrengthenTable.bxm",
               "yamm_data/dat_files/core.dat/WeaponStrengthenTable.bxm"
               ]
    for str in datList:
        if os.path.isfile(str):
            print(f"[Unpacking {str}]")
            newdattUn.main(str, "yamm_data/" + str)
        else:
            print("[ERROR: PLEASE PUT VALID DAT FILES IN THE DAT FILES DIRECTORY]\n")
            return False
    for str in bxmList:
        print(f"[Preparing XML File {str}]")
        bxm2xml.main(str)
    print("[Preparing MCD]")
    mcd.mcd_to_json("yamm_data/dat_files/ui_core_us.dat/messcore.mcd")
