import bpy
import fetch_file

member = bpy.props.EnumProperty(name = "Member", items = populate_members)
members = [("8 0 0 0", "Member", "Member", "USER")]

def populate_members(self, context):
    return members

def fetch():
    fetch_file.fetch_file(member, 8000, "C:\\Program Files\\Blender Foundation\\Collaboration\\" + bpy.path.basename(bpy.data.filepath), bpy.data.filepath)

def push():
    bpy.ops.wm.save_as_mainfile(filepath = "C:\\Program Files\\Blender Foundation\\Collaboration\\" + bpy.path.basename(bpy.data.filepath))
    fetch_file.init()

def get_host():
    import socket
    return socket.gethostbyname(socket.gethostname())
