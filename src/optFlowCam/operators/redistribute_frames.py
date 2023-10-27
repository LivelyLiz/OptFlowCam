import bpy

from ..interpolation import get_camera_distance
from ..utility import cam_to_sample

# ------------------------------------------------------------------------------

class OFC_OT_RedistributeFrames(bpy.types.Operator):

    #custom ID
    bl_idname = "ofc.redistribute_frames"
    #bl_parent_id = "OBJECT_PT_optFlowPanel"
    #this variable is a label/name that is displayed to the user
    bl_label = "Redistribute Frames"
    bl_options = {'INTERNAL'}

    @classmethod
    def poll(cls, context):
        props = context.scene.OFC.init_props

        if(len(props.keyframes) > 2 and 
           all([k.cam != None for k in props.keyframes])):
            return True

        return False

    def execute(self, context):
        props = context.scene.OFC.init_props

        keyframes = props.keyframes
        cam_samples = [cam_to_sample(k.cam) for k in keyframes]

        n_frames = keyframes[-1].frame - keyframes[0].frame + 1
        if n_frames == 1:
            return {'FINISHED'}

        alpha = None
        if props.parametrization == "Uniform":
            alpha = 0
        elif props.parametrization == "Centripetal":
            alpha = 1/2
        elif props.parametrization == "Chordal":
            alpha = 1
        else:
            raise ValueError(f"Unknown method: {props.parametrization}")

        focal = cam_samples[0]["focal"]
        
        dists = [get_camera_distance(cam_samples[i], cam_samples[i+1], focal, props.metric, rho=props.rho)**alpha for i in range(len(keyframes)-1)]
        total_dist = sum(dists)
        dists = [d/total_dist for d in dists]

        cams = [kf.cam for kf in keyframes]
        new_frames = [kf.frame for kf in keyframes]
        for i in range(len(new_frames)-2, 0, -1):
            new_frames[i] = new_frames[i+1] - int(dists[i]*n_frames)

        # need to precompute and assign after because
        # automatic sort shuffles keyframes
        # ideal would be to create and assign the new list without
        # any sort inbetween, but that seems not possible
        for i in range(len(new_frames)-1, 0, -1):
            while keyframes[i].frame != new_frames[i]:
                keyframes[i].frame = new_frames[i]
            keyframes[i].frame = new_frames[i]
            keyframes[i].cam = cams[i]

        return {'FINISHED'}
    
# ------------------------------------------------------------------------------

classes = [OFC_OT_RedistributeFrames]

def register():
    for cl in classes:
        bpy.utils.register_class(cl)

def unregister():
    for cl in classes:
        bpy.utils.unregister_class(cl)