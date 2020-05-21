import bpy
import fetch_file

member = bpy.props.EnumProperty(name = "Member", items = populate_members)
members = [("8 0 0 0", "Member", "Member", "USER")]

def populate_members(self, context):
    return members

def fetch_file():
  fetch_file.fetch_file(member, 8000, "C:\\Program Files\\Blender Foundation\\Collaboration\\", bpy.data.filepath)
