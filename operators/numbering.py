import bpy
from bpy.types import Operator
from bpy.props import BoolProperty, EnumProperty
from ..utils import split_bone_chains, sort_bones


class MIO3BONE_OT_bone_numbering(Operator):
    bl_idname = "armature.mio3_bone_numbering"
    bl_label = "Numbering Bones"
    bl_description = "Numbering Bone"
    bl_options = {"REGISTER", "UNDO"}

    delim: EnumProperty(
        name="Delim",
        default=".",
        items=[
            (".", "Dot (.)", ""),
            ("_", "Under Bar (_)", ""),
        ],
    )

    endbone: BoolProperty(name="EndBone", default=False)
    suffix: BoolProperty(name="Suffix L/R", default=False)

    def execute(self, context):
        bpy.ops.object.mode_set(mode="OBJECT")
        bpy.ops.object.mode_set(mode="EDIT")

        selected_bones = [bone for bone in context.selected_bones if bone.select]
        if selected_bones:
            bone_chains = split_bone_chains(selected_bones)
            for chain in bone_chains:
                self.rename_bone(chain)
        return {"FINISHED"}

    def rename_bone(self, chain):
        name = chain[0].name
        base_name = name
        suffix = ""
        if self.suffix and name.endswith(("_L", "_R", ".L", ".R")):
            suffix = name[-2:]
            base_name = name[:-2]

        sorted_bones = []
        renamed_bones = set()
        for bone in chain:
            if bone.parent not in chain:
                sort_bones(bone, sorted_bones, renamed_bones, set(chain))

        temp_names = {}
        for i, bone in enumerate(sorted_bones):
            temp_name = f"TEMP_mio3bones_{i:03d}_{bone.name}"
            temp_names[bone.name] = temp_name
            bone.name = temp_name

        for i, bone in enumerate(sorted_bones):
            original_name = list(temp_names.keys())[list(temp_names.values()).index(bone.name)]
            if original_name != name:
                if self.endbone and i == len(sorted_bones) - 1:
                    bone.name = f"{base_name}{self.delim}end{suffix}"
                else:
                    bone.name = f"{base_name}{self.delim}{i:03d}{suffix}"
            else:
                bone.name = name


classes = [
    MIO3BONE_OT_bone_numbering,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
