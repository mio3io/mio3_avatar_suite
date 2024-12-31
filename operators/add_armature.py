import bpy
import os
from bpy.types import Operator
from ..define import BLEND_DIR


class MIO3BONE_OT_add_humanoid(Operator):
    bl_idname = "armature.mio3_add_humanoid"
    bl_label = "VRChat Humanoid"
    bl_description = "Humanoid"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        blend_path = os.path.join(BLEND_DIR, "mio3_humanoid_base_chest_b4.blend")
        bpy.ops.wm.append(
            filename="Armature",
            directory=os.path.join(blend_path, "Object"),
            link=False,
        )
        obj = context.selected_objects[0]
        obj.select_set(True)
        context.view_layer.objects.active = obj
        obj.name = "Armature"
        return {"FINISHED"}


classes = [
    MIO3BONE_OT_add_humanoid,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
