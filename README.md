### README

AOV_rebuild is project to automate multipass EXR decomposition and recomposition in Nuke, it includes a python script (AOV_rebuild.py) that can be installed to perform an additive or subtractive AOV rebuild in Nuke when a multipass EXR read node is appended upstream.

This tool currently includes naming convention presets for render engines Arnold, Karma, RenderMan and V-Ray.

AOV_rebuild.py code is LLM assisted.

Also included are shelf tools (karma_albedo_raw_rebuild.nk), a Karma specific albedo rebuild template / example and (vray_raw_rebuild.nk) a V-Ray specific raw & filter rebuild template / example that are installed to the Channel menu in Nuke if the supplied .nuke package is used.



### v1.1 Updates

* Layout Change (AOV Management): Light, Material and Utility AOVs grouped to column 1 (aov_read) leaving only unassigned AOVs in column 02 (aov_unassigned_read) for a more intuitive user experience.

* Bug Fix: AOVs deleted from aov_read or moved to omit_list are now omitted from any rebuild.

* Bug Fix: User override moving Lights AOVs from column aov_read (previously named aov_lights_read) to additional_lighting column no longer breaks the rebuild.

* Tech Fix: Manually overriding the render engine setting while edit_read is toggled on now resets all columns in AOV Management to the newly selected engine default.

* Tech Fix: AOV names containing c, color or colour added to albedo (materials) skip list.

* Tech Fix: AOV names containing shadow added to skip list (materials & lightgroups).

* Tech Fix: Unpremult added to beauty compare switch to match unpremulted AOV rebuild.

* Tech Fix: For subtractive rebuild, AOV unpremult nodes removed from unassigned pipe.

* Tech Fix: For additive rebuild, AOV unpremult nodes removed.

* Optimisation: Cryptomatte remove group added before material and lightgroup rebuilds.



### Thanks

Thanks to Daniel Miller, Tony Lyons and Peter Arcara for their work upon which this project is based, and a special thanks to Todd Manus for beta testing and providing renders from RenderMan.

For any bug reports, feature requests or feedback hit me up on GitHub!