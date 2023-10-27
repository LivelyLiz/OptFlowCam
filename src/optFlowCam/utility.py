import bpy
from mathutils import Vector

from .math import get_orthonormal_basis

def get_focal_length(cam):
    return cam.data.lens/cam.data.sensor_width

def cam_to_sample(cam) -> dict:
    '''
    Convert a blender camera object to a more accessible format consisting
    of the eye point, orientation given by view and up vector, the focal length
    and the current "scale" of the frustum.
    '''

    mat = cam.matrix_world
    pos, rot, _ = mat.decompose()
    forw = rot @ Vector((0,0,-1))
    up = rot @ Vector((0,1,0))

    c = {
        'position': list(pos),
        'view' : list(forw),
        'up' : list(up),
        'focal' : get_focal_length(cam),
        'frustum_scale' : max(list(cam.scale))
    }

    return c

def get_look_at_point(cam: dict) -> list:
    pos, view, _, _, s = get_orthonormal_basis(cam)
    focal = cam["focal"]

    look = pos + s*focal*view
    return look

def lookat_path_from_camera_path(cam_path: list) -> list:

    lookats = [{"position": get_look_at_point(cam).tolist()} for cam in cam_path]

    return lookats