bl_info = {
    "name": "NeuroBGE",
    "author": "Underpig",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "description": "Neural node-based game engine",
    "location": "Logic Editor > Game Engine",
    "wiki_url": "",
    "category": "Object",
}

import bpy
import neurobge

def register():
    neurobge.register()

def unregister():
    neurobge.unregister()

if __name__ == "__main__":
    register()
