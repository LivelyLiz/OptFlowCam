import bpy

from ..interpolation import get_camera_distance
from ..utility import cam_to_sample

import numpy as np

# ------------------------------------------------------------------------------

class OFC_OT_RedistributeFrames(bpy.types.Operator):

    #custom ID
    bl_idname = "ofc.redistribute_frames"
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
        dists = np.array([get_camera_distance(cam_samples[i], cam_samples[i+1], focal, 
                                     props.metric, rho=props.rho)**alpha 
                    for i in range(len(keyframes)-1)])
        
        dists = dists/np.sum(dists)
        dists = np.insert(dists, 0, 0)
        new_frames = np.cumsum(dists)*(n_frames - 1) + keyframes[0].frame

        # store the original order of cameras
        # to circumvent the issue with automatic sorting 
        cams = [kf.cam for kf in keyframes]

        # need to precompute and assign after because
        # automatic sort shuffles keyframes
        # ideal would be to create and assign the new list without
        # any sort inbetween
        for i in range(len(new_frames)-1, 0, -1):
            while keyframes[i].frame != int(new_frames[i]):
                keyframes[i].frame = int(new_frames[i])
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