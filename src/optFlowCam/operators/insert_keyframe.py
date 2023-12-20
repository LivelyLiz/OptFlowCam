import bpy
from mathutils import Vector

from ..ui.keyframe_list import sort_keyframe_list
from ..objects.camera import update_camera
from ..utility import cam_to_sample, get_look_at_point

# ------------------------------------------------------------------------------

class OFC_OT_Realize_Keyframe(bpy.types.Operator):
    #custom ID
    bl_idname = "ofc.realize_keyframe"
    bl_label = "Realize Keyframe"
    bl_options = {'INTERNAL'}

    bl_description = "Insert current frame as keyframe"

    @classmethod
    def poll(cls, context):
        op_props = context.scene.OFC.op_props

        try:
            context.scene.objects[op_props.temp_cam]
        except:
            return False

        return op_props.operator_running
    
    def execute(self, context):
        
        op_props = context.scene.OFC.op_props
        props = context.scene.OFC.init_props

        original_cam = context.scene.objects[op_props.temp_cam]
        original_cam_sample = cam_to_sample(original_cam)

        bpy.ops.ofc.create_look_at_camera()
        objs = context.selected_objects
        if objs[0].type == 'CAMERA':
            cam = objs[0]
            lookat = objs[1]
        else:
            cam = objs[1]
            lookat = objs[0]

        cam.name = "KeyframeCamera"
        lookat.name = "KeyframeLookAt"
        update_camera(original_cam_sample, cam)

        lookat.location = Vector(get_look_at_point(original_cam_sample).tolist())

        curr_frame = context.scene.frame_current

        props.keyframes.add()
        props.keyframes[-1].cam = cam
        props.keyframes[-1].frame = curr_frame

        sort_keyframe_list(None, context)

        return {"FINISHED"}

# ------------------------------------------------------------------------------

classes = [OFC_OT_Realize_Keyframe]

def register():
    for cl in classes:
        bpy.utils.register_class(cl)

def unregister():
    for cl in classes:
        bpy.utils.unregister_class(cl)