### README ###

A project to automate AOV rebuild in Nuke, it includes a python script (AOV_rebuild.py) that can be installed to perform an additive or subtractive AOV rebuild in Nuke when a EXR read node is appended upstream. AOV_rebuild.py currently includes presets for render engines Arnold, Karma, RenderMan and V-Ray.

Also included are shelf tools (karma_albedo_raw_rebuild.nk), a Karma specific albedo rebuild template / example and (vray_raw_rebuild.nk) a V-Ray specific raw & filter rebuild template / example that are installed to the Channel menu in Nuke if the supplied .nuke package is used.



## Install ##



1. Copy .nuke folder to your desired directory

Linux = '/home/<your username>/.nuke'

Windows = 'C:\\Users\\<your username>\\.nuke'

Mac = '/Users/<your username>/.nuke'

Inside .nuke directory, edit menu.py <nukeCommonPath> to match your .nuke directory. That's it!



## Contents ##



1. AOV_rebuild.py

Is made following Daniel Millers course 'Dynamic Node Graphs with Python in Nuke' which rebuilds materials and lightgroups using a production approved method so users can grade both properties of their render in a safe manner which can be easy to break otherwise by adding and subtracting AOVs down the pipe. It also comes with an 'unassigned pipe', a great feature for QCing your lighters work by displaying unassigned AOVs.


2. karma_albedo_raw_rebuild.nk 

Is a template to demonstrate AOV rebuilding with albedo AOVs in Nuke. It won't work for every use case so you will need to rebuild depending on the albedo AOVs you have in your render. To work as a complete rebuild you will first need to use 

AOV_rebuild.py 

to breakout all AOVs, then delete out materials that you intend to rebuild with albedo and stitch both templates together manually.


3. vray_raw_rebuild.nk

Is a template to demonstrate AOV rebuilding with raw and filter AOVs in Nuke (as described in the Chaos Group V-Ray Docs, please see References). Again, to work as a complete rebuild you will first need to use 

AOV_rebuild.py 

to breakout all AOVs, then delete out materials that you intend to rebuild with raw / filter and stitch both templates together manually.


4. AOV_rebuild_karma_examples_v001.nk 

Was made for an earlier iteration of the project specific to Karma render engine and has been included as a dictionary / sandbox for users to test renders and rebuild AOVs from Karma. It includes EXRs rendered using Peter Arcara's Refining_Karma_Renders.hip from the tutorial series of the same name. These files are too large to upload to GitHub, so I've left a link below for those that want to use them..

https://drive.google.com/file/d/1fC_MgFowEWC1fEKMITLFggpaNTXeBvSy/view?usp=sharing

So far AOV_rebuild_karma_examples_v001.nk includes a key of all default and extra render vars available in Karma H21, and some (but not all) of the custom render vars shown in Refining_Karma_Renders and an albedo rebuild demonstrating the AOV_rebuild & karma_albedo_raw_rebuild.nk stitch.

AOV_rebuild_karma_examples_v001.nk uses Stamps for instancing and layout purposes so if you're not familiar with Stamps the link is at the bottom of the list of references so you can install it for Nuke.



## User Guide ##



A 'Features & Settings' instructional video can be found on the project page of my website

https://davidjthomasvfx.com/tools/aov-rebuild

Please refer to the 'Breakout Lightgroups, Materials and Utilities' panel tooltips within Nuke for guides on specific features.



## Features ##



AOV_rebuild.py

* Support for the default naming conventions from render engines Arnold, Karma, RenderMan, V-Ray and a Generic option as default.

* Additive or Subtractive rebuild modes.

* Regex to automate AOV management with user overrides taking priority when manual changes are needed.

* Layout options and simplified UI.

* QC option to check unassigned pipe for negative values (negative values will break the rebuild).



## Thanks ##



Thanks to Daniel Miller, Tony Lyons and Peter Arcara for their work upon which this project is based, and a special thanks to Todd Manus for sharing knowledge and providing renders from RenderMan. 

For any bug reports, feature requests or feedback hit me up on GitHub!



## References ##

https://www.fxphd.com/details/698/

https://github.com/areelillmind/BreakOutLightGroups

https://compositingmentor.com/category/cg-compositing-series/

https://help.autodesk.com/view/ARNOL/ENU/?guid=arnold_user_guide_ac_output_aovs_ac_aovs_html

https://www.sidefx.com/tutorials/refining-karma-renders/

https://www.sidefx.com/docs/houdini/solaris/support/lpe.html

https://www.sidefx.com/docs/houdini/news/21/karma.html#rendering-aovs

https://rmanwiki-27.pixar.com/space/REN27/542234274/Arbitrary+Output+Variables

https://rmanwiki-27.pixar.com/space/REN27/542234535/Light+Path+Expressions

https://rmanwiki-27.pixar.com/space/REN27/542232567/Denoiser+AOVs

https://rmanwiki-27.pixar.com/space/REN27/542234882/Using+LPE

https://www.youtube.com/watch?v=JDVQQTEVl50&t=20s

https://www.youtube.com/watch?v=zJ6d9UNdBlo&t=230s

https://www.youtube.com/watch?v=2V-O58fJ4bg&t=1s

https://documentation.chaos.com/space/VMAYA/111738952/Render+Elements

https://documentation.chaos.com/space/VMAYA/111739029/RGB_Color

https://github.com/adrianpueyo/Stamps