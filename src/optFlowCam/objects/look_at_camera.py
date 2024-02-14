import bpy
from mathutils import Vector

from .camera import add_camera_object

# ------------------------------------------------------------------------------

class OFC_OT_CreateLookAtCamera(bpy.types.Operator):
    
    #custom ID
    bl_idname = "ofc.create_look_at_camera"
    bl_label = "Create Look-At Camera"
    bl_options = {'INTERNAL'}

    def __add_collection(self, context):
        collection = bpy.context.blend_data.collections.new(name='LookAtCamera')
        bpy.context.collection.children.link(collection)

        return collection

    def __add_camera(self, context, collection):
        cam = add_camera_object(collection.name, camera_name="LA_Camera")
        cam.location = context.scene.cursor.location + \
                       (cam.matrix_world@Vector([0, 0, 1, 0])).xyz
        return cam

    def __add_target(self, context, collection):
        bpy.ops.object.empty_add(type='PLAIN_AXES',radius=0.2)
        target = context.active_object
        target.name = "LA_Target"
        target.location = context.scene.cursor.location

        # move target to collection
        for coll in target.users_collection:
            # Unlink the object
            coll.objects.unlink(target)
        collection.objects.link(target)

        return target

    def __add_constraints(self, camera, target):
        '''
        Add constraints to the camera object so that it always looks at
        the target point (an empty object) and scales according to the distance
        of camera to target.
        '''

        # add track_to constraint to camera
        track_to_const = camera.constraints.new('TRACK_TO')
        
        # set empty as track object
        track_to_const.target = target
        track_to_const.track_axis = 'TRACK_NEGATIVE_Z'
        track_to_const.up_axis = 'UP_Y'

        # add driver to camera scale
        for i in range(3):
            d = camera.driver_add("scale", i).driver
            d.type = 'SCRIPTED'
            d.use_self = True

            v_dist = d.variables.new()
            v_dist.name          = "dist"
            v_dist.type          = 'LOC_DIFF'
            v_dist.targets[0].id = camera
            v_dist.targets[1].id = target

            d.expression = "dist*self.data.sensor_width/self.data.lens"

    def execute(self, context):

        # add new collection to have the camera and target bundled
        collection = self.__add_collection(context)

        cam = self.__add_camera(context, collection)
        target = self.__add_target(context, collection)
        self.__add_constraints(cam, target)

        # select new objects
        bpy.ops.object.select_all(action='DESELECT')
        for obj in (cam, target):
            obj.select_set(True)

        return {'FINISHED'}

# ------------------------------------------------------------------------------

classes = [OFC_OT_CreateLookAtCamera]

def create_lookat_camera_button(self, context):
    self.layout.operator(OFC_OT_CreateLookAtCamera.bl_idname, 
                         text="LookAt Camera", icon='OUTLINER_DATA_CAMERA')

def register():
    for cl in classes:
        bpy.utils.register_class(cl)

    bpy.types.VIEW3D_MT_add.append(create_lookat_camera_button)

def unregister():
    bpy.types.VIEW3D_MT_add.remove(create_lookat_camera_button)

    for cl in classes:
        bpy.utils.unregister_class(cl)