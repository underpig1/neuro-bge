import bpy

bpy.ops.screen.userpref_show("INVOKE_DEFAULT")
area = bpy.context.window_manager.windows[-1].screen.areas[0]
area.type = "VIEW_3D"
bpy.context.scene.frame_end = 1048574
bpy.ops.screen.animation_play()
bpy.ops.object.select_all(action = "DESELECT")
area.spaces[0].region_3d.view_perspective = "CAMERA"
area.spaces[0].region_3d.view_camera_zoom = 31.112701416015625
area.spaces[0].overlay.show_overlays = False
area.spaces[0].show_gizmo = False
area.spaces[0].show_region_header = False
area.spaces[0].shading.type = "RENDERED"
bpy.ops.wm.window_fullscreen_toggle()
