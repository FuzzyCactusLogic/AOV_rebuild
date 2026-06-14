#### IMPORT MODULES ####

import nuke
import AOV_rebuild

#### ASSIGNING NUKE PATH ####

nukeCommonPath = '/path/to/your/.nuke'

#### ASSIGNING NUKE PATH END ####



#### PYTHON MENU ####

python_menu = nuke.menu('Nodes').addMenu("Python", icon="python_icon.png")

python_menu.addCommand('AOV_rebuild', 'AOV_rebuild.custom_breakout_lightgroups_and_materials()','')

#### PYTHON MENU END ####



#### CHANNELS MENU ADDITIONS ####

channel_menu = nuke.menu("Nodes").menu("Channel")

channel_menu.addCommand("karma_albedo_raw_rebuild", 'nuke.nodePaste(nukeCommonPath + "/tools/Channel/karma_albedo_raw_rebuild.nk")', icon="ShuffleSplitRGB.png")
channel_menu.addCommand("vray_raw_rebuild", 'nuke.nodePaste(nukeCommonPath + "/tools/Channel/vray_raw_rebuild.nk")', icon="ShuffleSplitRGB.png")

#### CHANNELS MENU ADDITIONS END ####