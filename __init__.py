bl_info = {
    "name": "NeuroBGE",
    "author": "Underpig",
    "version": (1, 0, 0),
    "description": "Neural node-based game engine",
    "location": "Logic Editor > Game Engine",
    "wiki_url": "https://github.com/underpig1/neuro-bge",
    "warning": "Save your work before run; do not modify during run",
    "category": "Object",
}

import bpy
from . import neurobge

def register():
    neurobge.register()

def unregister():
    neurobge.unregister()

if __name__ == "__main__":
    register()
