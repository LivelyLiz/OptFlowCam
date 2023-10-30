import bpy

# ------------------------------------------------------------------------------

class OFC_PT_OptimalPathOperatorPanel(bpy.types.Panel):
    bl_idname = "OFC_PT_OptimalPathOperatorPanel"
    bl_label = "Optimal Path Operator"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = 'objectmode'
    bl_category = "OptFlowCam"
    
    def draw(self, context):
        layout = self.layout

        init_props = context.scene.OFC.init_props

        init_box = layout.row().box()

        init_box.label(text="Camera Keyframes")

        keyframe_col = init_box.column()
        keyframe_col.operator("ofc.new_keyframe", text="Add Keyframe", icon="KEY_HLT")
        keyframe_col.template_list(
            "OFC_UL_KeyframeList", "", 
            init_props, "keyframes", init_props, "curr_keyframe_index", 
            rows=len(init_props.keyframes) + 1, type="DEFAULT")

        reparam_row = keyframe_col.row()
        reparam_row.operator("ofc.redistribute_frames", text="Redistribute Frames", icon="CENTER_ONLY")
        reparam_row.prop(init_props, "parametrization", text="")

        layout.prop(init_props, "method")
        layout.prop(init_props, "metric")

        layout.separator()

        if context.scene.OFC.op_props.operator_running:
            keyframe_col.enabled = False
            r = layout.row()

            cmd_c = r.column()
            cmd_c.alignment = "RIGHT"
            desc_c = r.column()

            for cmd, description in [("SHIFT + SPACE", "to update"), 
                                     ("SHIFT + ENTER", "to make permanent"),
                                     ("ESC", "to cancel")]:
                cmd_c.label(text=cmd)
                desc_c.label(text=description)

            r.enabled = False

            layout.operator('ofc.realize_keyframe', text='Insert Current Frame')

        layout.operator('ofc.interpolate_camera', text='Interpolate Camera')

# ------------------------------------------------------------------------------

class OFC_PT_OptimalPathAdvancedOptionsPanel(bpy.types.Panel):
    bl_idname = "OFC_PT_OptimalPathAdvancedOptionsPanel"
    bl_parent_id = "OFC_PT_OptimalPathOperatorPanel"
    bl_label = "Advanced Options"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = 'objectmode'
    bl_category = "OptFlowCam"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout

        init_props = context.scene.OFC.init_props

        rho_row = layout.row()
        rho_row.prop(init_props, "rho")
        reset_rho_operator = rho_row.operator('ofc.reset_property', text="", icon="LOOP_BACK")
        reset_rho_operator.target = "rho"

        layout.prop(init_props, "make_path_permanent")
        layout.prop(init_props, "make_frustum_permanent")

# ------------------------------------------------------------------------------

classes = [OFC_PT_OptimalPathOperatorPanel,
           OFC_PT_OptimalPathAdvancedOptionsPanel]

def register():
    for cl in classes:
        bpy.utils.register_class(cl)
        print(cl)

def unregister():
    for cl in classes:
        bpy.utils.unregister_class(cl)
