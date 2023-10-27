import bpy
from mathutils import Vector

from ..math import make_lookAt_matrix

def add_camera_object(collection_name, camera_name='OptimizedCamera'):
    # create camera data block
    cam = bpy.data.cameras.new(camera_name)

    # create the camera object
    cam_obj = bpy.data.objects.new(camera_name, cam)

    if collection_name == bpy.context.scene.collection.name:
        bpy.context.scene.collection.objects.link(cam_obj)
    else:
        bpy.data.collections[collection_name].objects.link(cam_obj)

    return cam_obj

def update_camera(sample, cam):
    '''
    Given a camera sample, update the given Blender camera object to represent
    the sample.
    '''

    pos = Vector(sample['position'])
    up = Vector(sample['up'])
    forw = Vector(sample['view'])
    focal_length = sample['focal']

    cam.data.lens = focal_length * cam.data.sensor_width
    cam_world = make_lookAt_matrix(pos, forw, up)
    cam.matrix_world = cam_world
    cam.scale = sample["frustum_scale"] * Vector((1,1,1))

def animate_camera(samples, cam, start_frame=0):
    '''
    Given a list of camera samples, add a keyframe to the camera for every
    sample in the list.
    '''

    n = len(samples)

    for i in range(0, n):
        frame = start_frame + i
        
        update_camera(samples[i], cam)
        
        cam.keyframe_insert("location", frame=frame)
        cam.keyframe_insert("rotation_euler", frame=frame)
        cam.data.keyframe_insert("lens", frame=frame)
        cam.keyframe_insert("scale", frame=frame)