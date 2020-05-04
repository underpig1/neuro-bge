import bpy
import neurobge

def register():
    neurobge.register()

def unregister():
    neurobge.unregister()

if __name__ == "__main__":
    register()