
# NAWA

A NieR: Automata Weapon Assembler allowing to add completely custom weapons to the game




## Dependencies

You have to have Python 3.10 or higher installed


    
## How To Use:

**ON FIRST START:** 

Select your NieR: Automata install folders data folder and the folder you will put your weapon mods in using the buttons on the bottom left.


Your mods folder can be anywhere on your system.




**HOW TO ADD WEAPONS:**

Inside your mods folder make an folder for each weapon, name the folder in a way so you will recognize the weapon.

inside the weapons folder put an folder called "wp" and put the weapons .dat and .dtt files in.

Repeat this for each weapon. Do not put multiple dat or dtt files in a weapons folder.

If the weapon you wanna put in came with a misctex file or folder delete them, currently the tool does not support adding custom misctex (soon added)

If you have added a weapon folder white NAWA is running rechoose the mods folder to refresh the list (to be changed soon)


**HOW TO USE NAWA:**

Select the weapon you want to edit the Name, Stats and more in the list on the top right

Edit stuff and press the "Save config" button.

The config does not autosave, use the button before switching to another weapon!

Press the "Deploy mods" button to deploy all weapons to your game (make sure u your games data folder selected correctly)

Start the game, go to the resistance camp, open the weapon shop and enjoy!




## FAQ

#### Does this overwrite any vanilla weapons?

No! All vanilla weapons stay, and your new weapons are added as completely seperate ones.

#### Does this corrupt my savefile?

In my tests no. Only when u redeploy the weapon ids may change, so a weapon in your inventory may suddenly be another one.

#### How do i remove the weapoons?

Just delete the core, ui, txtmess and wp folders in your data folder.

#### Any problems ingame?

Sadly yes, currently the story and details tab of a weapon will softlock the game, dont press them. the details tab will be openable in
a future update, story is sadly hardcoded and will never be accesible



## Acknowledgements

 - [Woeful_Wolf](https://github.com/WoefulWolf) For the incredible work on Nier2Blender2Nier making this even possible
 - [RaiderB](https://github.com/ArthurHeitmann) Too, for the incredible work and tools making this possible
 - [grojdg](https://github.com/xxk-i) ...im repeating myself, for incredible tools


 

