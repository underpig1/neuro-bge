# NeuroBGE
![NeuroBGE Storefront](images/storefront.png)
#### A node-based Blender game engine and logic editor addon for Blender
##
![NeuroBGE Example](images/untitled.png)
##
Create games using a node-based logic editor and other incorporated features and functionalities
## Installation
Clone or [download](https://github.com/underpig1/neuro-bge/archive/master.zip) this repository and install the addon in Blender with `Preferences > Addons > Install` and enable the addon.
## Functionalities
- Logic editor
- Scripting capabilities
- Game engine
- Build functions for supported platforms (Mac OSX*; Windows; Linux*)
- Over forty-five nodes to develop stable games
## Build
***Notice:*** *building in Blender 2.8 requires Python 3.8 to be installed*

Build your game with the build functionality. Press build in either menu, and select your platform and directory to build your game. The game will become a shell script or executable.

*Building for Linux returns a SH file, which is suitable for both Mac OSX and Linux, if desirable.*

[BAT to EXE for Windows](https://superuser.com/questions/868340/how-can-i-convert-a-windows-batch-script-to-a-exe)

[SH to APP for Mac OSX and Linux](https://gist.github.com/mathiasbynens/674099)
## Use
#### *Keymap and Interface*
The node utility menu can be found in the Logic Editor interface, and includes such functions as Assign Script and Run. The menu found in the header of the Viewport can be triggered by pressing E while in Object Mode.
Functionality | Operation
------------ | -------------
Assign Script | The selected object is assigned to the selected node. This can be useful if you would like a node to apply only to a certain object. All Output nodes require an assigned object. Found in the node utility menu.
Run | Runs all.
Stop | Stops all.
Build | [Builds](https://github.com/underpig1/neuro-bge#build) game to selected platform.
Create Variable | Creates a variable, used in the Logic nodes: Set Variable and Variable. Found in the node utility menu.
#### *Events*
#### *Controllers*
## TODO
- [x] Build support
- [ ] XR support
  - [ ] XR build support

*Untested
