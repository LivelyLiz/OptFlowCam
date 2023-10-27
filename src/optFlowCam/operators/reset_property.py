import bpy

# ------------------------------------------------------------------------------

class OFC_OT_ResetPropertyOperator(bpy.types.Operator):

    #custom ID
    bl_idname = "ofc.reset_property"
    #bl_parent_id = "OBJECT_PT_optFlowPanel"
    #this variable is a label/name that is displayed to the user
    bl_label = "Reset Property"
    bl_options = {'INTERNAL'}

    bl_description = "Reset the property to its default value"

    target: bpy.props.StringProperty()

    def execute(self, context):
        context.scene.OFC.init_props.property_unset(self.target)
        return {'FINISHED'}

# ------------------------------------------------------------------------------

classes = [OFC_OT_ResetPropertyOperator]

def register():
    for cl in classes:
        bpy.utils.register_class(cl)

def unregister():
    for cl in classes:
        bpy.utils.unregister_class(cl)