import bpy

# https://sinestesia.co/blog/tutorials/using-uilists-in-blender/
# https://sinestesia.co/blog/tutorials/amazing-uilists-in-blender/

def sort_keyframe_list(_, context):
    '''
    Sorts the list with camera keyframes according
    to the frame number.
    '''

    props = context.scene.OFC.init_props

    # bubble sort because we are only allowed to swap
    # items and are not allowed to use sorted or sort
    # (at least I didn't find anything)
    # We can usually assume the list to be nearly sorted
    # when this is called, so the complexity should be closer
    # to O(n) than O(n^2)
    n = len(props.keyframes)
    while True:
        swapped = False
        for i in range(n-1):
            if props.keyframes[i].frame > props.keyframes[i+1].frame:
                props.keyframes.move(i, i+1)
                swapped = True

        if not swapped:
            break

# ------------------------------------------------------------------------------

class OFC_OT_NewKeyframeItem(bpy.types.Operator):
    '''
    Operator to add a new item to the keyframe list.
    '''

    bl_idname = "ofc.new_keyframe"
    bl_label = "Add a new keyframe"

    def execute(self, context):
        props = context.scene.OFC.init_props
        props.keyframes.add()

        if len(props.keyframes) > 1:
            props.keyframes[-1].frame = props.keyframes[-2].frame+1

        return {'FINISHED'}

# ------------------------------------------------------------------------------

class OFC_OT_DeleteKeyframeItem(bpy.types.Operator):
    '''
    Operator to delete the selected item from the keyframe list.
    '''

    bl_idname = "ofc.delete_keyframe"
    bl_label = "Delete selected keyframe"

    target : bpy.props.IntProperty(
        name="Target Keyframe Index",
        options={'HIDDEN'})

    @classmethod
    def poll(cls, context):
        return context.scene.OFC.init_props.keyframes

    def execute(self, context):
        props = context.scene.OFC.init_props

        my_list = props.keyframes
        my_list.remove(self.target)

        props.curr_keyframe_index = min(max(0, props.curr_keyframe_index), len(my_list) - 1)

        return {'FINISHED'}

# ------------------------------------------------------------------------------

class OFC_OT_MoveKeyframeItemOperator(bpy.types.Operator):
    '''
    Operator to move the item in the keyframe list
    '''

    bl_idname = "ofc.move_keyframe"
    bl_label = "Move selected keyframe"

    target : bpy.props.IntProperty(
        name="Target Item Index")

    direction : bpy.props.EnumProperty(
        name="Direction", 
        items=[("UP", "Up", "", 1), ("DOWN", "Down", "", 2)])

    def clamp(self, n, length):
        return max(min(length, n), 0)

    def swap_frame(self, item1, item2):
        tmp_frame = item1.frame
        item1.frame = item2.frame
        item2.frame = tmp_frame

    def execute(self, context):
        props = context.scene.OFC.init_props
        keyframes = props.keyframes

        target_item = keyframes[self.target]

        newindex = self.target
        if self.direction == "UP":
            newindex = self.clamp(self.target - 1, len(keyframes))
        if self.direction == "DOWN":
            newindex = self.clamp(self.target + 1 , len(keyframes))


        self.swap_frame(target_item, keyframes[newindex])
        keyframes.move(self.target, newindex)

        return {'FINISHED'}

# ------------------------------------------------------------------------------

class OFC_PG_KeyframeItem(bpy.types.PropertyGroup):
    '''
    Class that defines an item in the keyframe list.
    '''

    bl_idname="OFC_PG_KeyframeItem"

    def camera_poll(self, object):
        return object.type == 'CAMERA'

    cam: bpy.props.PointerProperty(
        name="Camera",
        description="The camera keyframe.",
        type=bpy.types.Object,
        poll=camera_poll)
    
    frame: bpy.props.IntProperty(
        name="Frame",
        description="The frame value of the keyframe.",
        default=0,
        update=sort_keyframe_list)

# ------------------------------------------------------------------------------

class OFC_UL_KeyframeList(bpy.types.UIList):
    '''
    Class that defines the UI for the keyframe list.
    '''

    bl_idname="OFC_UL_KeyframeList"

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):

        layout_col = layout.column()

        # add column description
        if index == 0:
            desc_r = layout_col.row(align=True)
            desc_r.label(text="Camera")
            frame_row = desc_r.row()
            frame_row.scale_x = 0.6
            frame_row.label(text="Frame")
            desc_r.enabled = False

        u = layout_col.row()

        # add a little bit of horizontal spacing
        c = u.column()
        c.scale_x = 0.2

        # camera selector
        r = u.row(align=True)
        r.prop(item, "cam", text="")

        # frame number
        frame_row = r.row()
        frame_row.scale_x = 0.6
        frame_row.prop(item, "frame", text="")

        # delete keyframe operator
        op = r.operator("ofc.delete_keyframe", text="", icon="TRASH", emboss=False)
        op.target=index

    def draw_filter(self, context, layout):
        pass

# ------------------------------------------------------------------------------

classes = [OFC_PG_KeyframeItem, OFC_UL_KeyframeList,
           OFC_OT_NewKeyframeItem, OFC_OT_DeleteKeyframeItem,
           OFC_OT_MoveKeyframeItemOperator]

def register():
    for cl in classes:
        bpy.utils.register_class(cl)
        print(cl)

def unregister():
    for cl in classes:
        bpy.utils.unregister_class(cl)