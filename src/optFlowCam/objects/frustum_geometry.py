import bpy
from mathutils import Vector

from ..math import make_lookAt_matrix

def add_frustum_object(collection_name, object_name='Frustum'):
    '''
    Add a new cube to the scene which represents the simplified
    view frustum. Returns the object.
    '''

    bpy.ops.mesh.primitive_cube_add()
    cube = bpy.context.active_object

    # display properties
    cube.display_type = 'WIRE'
    cube.hide_render = True
    cube.name = object_name

    bpy.context.collection.objects.unlink(cube)
    bpy.data.collections[collection_name].objects.link(cube)

    return cube

def update_frustum(sample, cube):
    '''
    Updates the view frustum according to the given camera sample.
    '''

    pos = Vector(sample['position'])
    up = Vector(sample['up'])
    forw = Vector(sample['view'])
    
    focal_length = float(sample['focal'])
    scale = float(sample['frustum_scale'])

    pos = pos + scale*focal_length*forw

    world = make_lookAt_matrix(pos, forw, up)
    scale = Vector((scale/2, scale/2, scale/2))

    cube.matrix_world = world
    cube.scale = scale

def animate_frustum(opt_coords, cube, start_frame=0):
    '''
    Adds a keyframe to the frustum object for every frame beginning at
    the start frame.
    '''

    n = len(opt_coords)

    for frame in range(start_frame, start_frame+n):
        update_frustum(opt_coords[frame], cube)
        cube.keyframe_insert("location", frame=frame)
        cube.keyframe_insert("rotation_euler", frame=frame)
        cube.keyframe_insert("scale", frame=frame)

