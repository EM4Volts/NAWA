import json, os, random, struct, shutil
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

identifierBlackList = open("configs/ddslist.xml", "r")
data = identifierBlackList.read()
idBlackList = data.split("\n")
identifierBlackList.close()

wpidBlacklistFile = open("configs/allwpids.xml", "r")
data = wpidBlacklistFile.read()
wpidBlacklist = data.split("\n")
wpidBlacklistFile.close()

idBlacklistFile = open("configs/wpids.xml", "r")
data = idBlacklistFile.read()
idBlacklist = data.split("\n")
idBlacklistFile.close()
newUid = 1003
defaultWPConf = {"weaponname": "NAMC Weapon", "weapondescshort": "", "weapondesclong": "", "weapontype": "0", "lv1": "150", "lv2": "270", "lv3": "440", "lv4": "570"}

def getWPfileName(wpC):
    if wpC == "0":
        cName = "Small Sword"
        indexStart = 1
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
    wpidnotFound = True
    while wpidnotFound:
        nWpn = indexStart
        if len(str(nWpn)) == 1:
            newuId = "000" + str(nWpn)
        if len(str(nWpn)) == 2:
            newuId = "00" + str(nWpn)
        if len(str(nWpn)) == 3:
            newuId = "0" + str(nWpn)
        if newuId in wpidBlacklist:
            print("[WPNAME : " + str(newuId) + " in Use, retrying...]")
        if newuId == indexEnd:
            print("[WPNAME ERROR: YOU RAN OUT OF SPACE IN THE " + cName + " CATEGORY, REMOVE A MOD FROM THE CATEGORY, THIS WEAPON WILL NOT BE EXPORTED")
            wpidnotFound = False
            return "Skip"
        if newuId not in wpidBlacklist:
                wpidBlacklist.append(newuId)
                wpidnotFound = False
                return "wp" + newuId
        else:
            indexStart +=1

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

def cleanDeploy():
    for filename in os.scandir("deploy/"):
        subFName = filename
        for filename in os.scandir(subFName):
            toRM = "deploy/" + str(subFName)[11:][:-2] + "/" + str(filename)[11:][:-2]
            if os.path.isdir(toRM):
                shutil.rmtree(toRM)
            else:
                os.remove(toRM)


def genNierIdentifier():
    random_ID = ''.join(random.choice('0123456789ABCDEF') for n in range(8))
    while random_ID in idBlackList:
        print("Dupe found")
        random_ID = ''.join(random.choice('0123456789ABCDEF') for n in range(8))
        quit()
    idBlackList.append(random_ID)
    return random_ID


def conWeaponType(re):
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

def readwpConfig(cfDir):
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
    lv1 = wpconfJson['lv1']
    lv2 = wpconfJson['lv2']
    lv3 = wpconfJson['lv3']
    lv4 = wpconfJson['lv4']

    return wpName, wpDescS, wpDescL, wpType, wpconfJson, lv1, lv2, lv3, lv4


def writewpConfig(cfDir, wpName, wpDescS, wpDescL, wpType, lv1, lv2, lv3, lv4):

    if not os.path.isfile(cfDir):
        with open(cfDir, 'w') as f:
            json.dump(defaultWPConf, f)
            print("no config found, adding default config")
    with open(cfDir, 'r') as file:
        wpconf = file.read()
    newCfg = json.loads(wpconf)
    newCfg["weaponname"] = wpName
    newCfg["weapondescshort"] = wpDescS
    newCfg["weapondesclong"] = wpDescL
    newCfg["weapontype"] = wpType
    newCfg["lv1"] = lv1
    newCfg["lv2"] = lv2
    newCfg["lv3"] = lv3
    newCfg["lv4"] = lv4
    with open(cfDir, 'w') as file:
        json.dump(newCfg, file)

def genPathList(folder):
    mDir = os.listdir(folder)
    mDir2 = []
    for str in mDir:
        entry = folder + str
        mDir2.append(entry)
    return mDir2

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
with open("yamm_data/configTemplates/txtcoreadd.txt", 'r') as file:
    txtcoreaddCrisp = file.read()
with open("yamm_data/configTemplates/txtpauseadd.txt", 'r') as file:
    txtpauseaddCrisp = file.read()
with open("yamm_data/configTemplates/coreweaponParam.txt", 'r') as file:
    weaponParamCrisp = file.read()
#currently in use for replacign binary strings
def kewlDatt(ptf, kewlName, newName):
    with open(ptf, "rb") as f:
        contents = f.read()
    ff=contents.replace(kewlName.encode("ascii"), newName.encode("ascii"))
    with open(ptf, "wb") as f:
        f.write(ff)

def writeToTable(crispSel, iName, UID, wpName, igName, igDescs, igDescl, wpCat, lv1, lv2, lv3, lv4):
    #SELECTS THE TABLE TO SET PATH, OFFSET AND TEMPLATE
    if crispSel == 1:
        crispPart = coregmItemInfoTableCrisp
        tablePath = "yamm_data/coregm/ItemInfoTable.xml"
        lineOffset = 827
    if crispSel == 2:
        crispPart = coregmShopInfoTableCrisp
        tablePath = "yamm_data/coregm/ShopInfoTable.xml"
        lineOffset = 3567
    if crispSel == 3:
        crispPart = coregmWeaponInfoTableCrisp
        tablePath = "yamm_data/coregm/weaponinfotable.xml"
        lineOffset = 1258
    if crispSel == 4:
        crispPart = coregmWeaponStrenghtenTableCrisp
        tablePath = "yamm_data/coregm/WeaponStrengthenTable.xml"
        lineOffset = 627
    if crispSel == 5:
        crispPart = coreWeaponStrenghtTableCrisp
        tablePath = "yamm_data/core/WeaponStrengthenTable.xml"
        lineOffset = 549
    if crispSel == 6:
        crispPart = uimesscoreCrisp
        tablePath = "yamm_data/ui_core_us/messcore.json"
        lineOffset = 13006
    if crispSel == 7:
        crispPart = txtcoreaddCrisp
        tablePath = "yamm_data/txt_core_add_us/txt_core_add.json"
        lineOffset = 1082
    if crispSel == 8:
        crispPart = txtpauseaddCrisp
        tablePath = "yamm_data/txt_pause_add_us/txt_pause_add.json"
        lineOffset = 143
    if crispSel == 9:
        crispPart = weaponParamCrisp
        tablePath = "yamm_data/core/WeaponParam.csv"
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
    crispPart = crispPart.replace("lv1a", lv1)
    crispPart = crispPart.replace("lv1b", str(int(lv1) + 20))
    crispPart = crispPart.replace("lv2a", lv2)
    crispPart = crispPart.replace("lv2b", str(int(lv2) + 20))
    crispPart = crispPart.replace("lv3a", lv3)
    crispPart = crispPart.replace("lv3b", str(int(lv3) + 20))
    crispPart = crispPart.replace("lv4a", lv4)
    crispPart = crispPart.replace("lv4b", str(int(lv4) + 20))
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

def WriteAllTables(a, b, c, d, e, f, g, h, i, j, k):
    allTables = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    #ecexutes the tablewrite on all currently accesible tables
    for int in allTables:
        writeToTable(int, a, b, c, d, e, f, g, h, i, j, k)




def genInsertableID(wtaFilePath):
    global wtaIdTable
    nierID = genNierIdentifier()
    retNierId = " ".join(nierID[i:i+2] for i in range(0, len(nierID), 2))
    return retNierId

def identifierTurn(str):
    revID = str[::-1]
    l1 = str[:-6]
    l2 = str[:-4][2:]
    l3 = str[:-2][4:]
    l4 = str[6:]
    binStr = l4 + l3 + l2 + l1

    return binStr

def replace_in_hex(file_to_manipulate, stringtoreplace, stringtoplace):
    g1 = bytes.fromhex(stringtoreplace)
    g2 = bytes.fromhex(stringtoplace)

    with open(file_to_manipulate, "rb") as file:
        content = file.read()
    rp = content.replace(g1, g2)
    with open(file_to_manipulate, "wb") as file:
        file.write(rp)


def shuffleIdentifierWta(wtaFilePath, wmbFilePath):
    with open(wtaFilePath, "rb") as wtab_fp:
        wtaIdTable = WTA(wtab_fp).wtaTextureIdentifier
    for str in wtaIdTable:
        newIDd=genInsertableID(wtaFilePath)
        revTurnTab= " ".join(identifierTurn(str)[i:i+2] for i in range(0, len(identifierTurn(str)), 2))
        replace_in_hex(wtaFilePath, revTurnTab, newIDd)
        replace_in_hex(wmbFilePath[:-4] + ".wmb", revTurnTab, newIDd)


