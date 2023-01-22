from nawa_data.fileporters.ioUtils import *
import datetime, random
from shutil import copy

class INVENTORY_WEAPON:
    def __init__(self,f):
        self.weapon_id = read_int32(f)
        self.weapon_level = read_int32(f)
        self.weapon_is_new = read_int32(f)
        self.weapon_new_story = read_int32(f)
        self.weapon_enemies_defeated = read_int32(f)
    
    def write_weapon(self, f):
        write_Int32(f, self.weapon_id)
        write_Int32(f, self.weapon_level)
        write_Int32(f, self.weapon_is_new)
        write_Int32(f, self.weapon_new_story)
        write_Int32(f, self.weapon_enemies_defeated)

cus = [123,12313,241,324]
class SAVE_FILE:
    def __init__(self, slot_data, custom_weapons = []):
        self.save_file = open(slot_data, "r+b")
        copy(slot_data, f"slot_data_backup{random.randrange(0, 12031231)}.dat")

        self.save_file_path = slot_data
        self.save_file_part1 = self.save_file.read(204144) #read everything before weapons struct
        self.vanilla_weapons = []  #read weapon saves 
        for i in range(80):
            weapon = INVENTORY_WEAPON(self.save_file)
            self.vanilla_weapons.append(weapon)

        if len(custom_weapons) > 0:
            self.save_file.seek(204944)
            custom_weapon_index = 0
            weapon_modifcation_index = 40
            for i in range(len(custom_weapons)):
                weapon = self.vanilla_weapons[weapon_modifcation_index]
                weapon.weapon_id = custom_weapons[custom_weapon_index]
                weapon.weapon_level = 3
                custom_weapon_index +=1
                weapon_modifcation_index += 1


        self.save_file.seek(205744)
        self.save_file_part2 = self.save_file.read()

    def write_save_file(self):
        with open(self.save_file_path, "w+b")as save_file:
            save_file.write(self.save_file_part1)
            for i in self.vanilla_weapons:
                i.write_weapon(save_file)
            save_file.write(self.save_file_part2)


