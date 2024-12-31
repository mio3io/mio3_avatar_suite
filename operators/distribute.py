import bpy
from bpy.types import Operator
from bpy.props import BoolProperty
from ..utils import split_bone_chains


def select_current_selection(armature):
    current_selection = [
        (bone.name, bone.select_head, bone.select_tail) for bone in armature.edit_bones if bone.select
    ]
    if armature.use_mirror_x:
        bpy.ops.armature.select_mirror(extend=True)
    return current_selection


def restore_current_selection(armature, current_selection):
    if armature.use_mirror_x:
        bpy.ops.armature.select_all(action="DESELECT")
        for bone_name, select_head, select_tail in current_selection:
            bone = armature.edit_bones[bone_name]
            bone.select = True
            bone.select_head = select_head
            bone.select_tail = select_tail


class MIO3BONE_OT_bone_evenly(Operator):
    bl_idname = "armature.mio3_bone_evenly"
    bl_label = "Evenly Bones"
    bl_description = "ボーンの長さを均等にする"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        bpy.ops.object.mode_set(mode="OBJECT")
        bpy.ops.object.mode_set(mode="EDIT")

        armature = context.active_object.data
        current_selection = select_current_selection(armature)

        selected_bones = context.selected_bones
        if selected_bones:
            bone_chains = split_bone_chains(selected_bones)
            for chain in bone_chains:
                self.evenly(chain)

        restore_current_selection(armature, current_selection)
        return {"FINISHED"}

    # 反復して調整
    def evenly(self, chain, iterations=3):
        original_positions = [(bone.head.copy(), bone.tail.copy()) for bone in chain]
        for _ in range(iterations):
            total_length = sum((tail - head).length for head, tail in original_positions)
            equal_length = total_length / len(chain)

            sum_distances = [0.0]
            for head, tail in original_positions:
                sum_distances.append(sum_distances[-1] + (tail - head).length)

            target_distances = [i * equal_length for i in range(1, len(chain) + 1)]

            def interpolate_position(distance):
                for i in range(len(sum_distances) - 1):
                    if sum_distances[i] <= distance <= sum_distances[i + 1]:
                        t = (distance - sum_distances[i]) / (sum_distances[i + 1] - sum_distances[i])
                        return original_positions[i][0].lerp(original_positions[i][1], t)
                return original_positions[-1][1]

            chain[0].head = original_positions[0][0]
            for i in range(1, len(chain)):
                chain[i - 1].tail = interpolate_position(target_distances[i - 1])
                chain[i].head = chain[i - 1].tail
            chain[-1].tail = original_positions[-1][1]


class MIO3BONE_OT_bone_align(Operator):
    bl_idname = "armature.mio3_bone_align"
    bl_label = "Align Bones (child)"
    bl_description = "ボーンを整列する（先頭と末端のボーンを基準）"
    bl_options = {"REGISTER", "UNDO"}

    roll: BoolProperty(name="Unify roles", default=False)
    preserve_length: BoolProperty(name="Preserve Length Bone", default=False)

    def execute(self, context):
        bpy.ops.object.mode_set(mode="OBJECT")
        bpy.ops.object.mode_set(mode="EDIT")

        armature = context.active_object.data
        current_selection = select_current_selection(armature)

        selected_bones = context.selected_bones
        if selected_bones:
            bone_chains = split_bone_chains(selected_bones)
            for chain in bone_chains:
                self.seiretu(chain)

        restore_current_selection(armature, current_selection)
        return {"FINISHED"}

    def seiretu(self, chain):
        head = chain[0].head
        tail = chain[-1].tail
        direction = (tail - head).normalized()
        roll = chain[0].roll
        total_distance = (tail - head).length

        if self.preserve_length:
            positions = [head]
            for bone in chain:
                positions.append(positions[-1] + direction * bone.length)
            for i, bone in enumerate(chain):
                bone.head = positions[i]
                bone.tail = positions[i + 1]
        else:
            length_ratios = [bone.length / sum(bone.length for bone in chain) for bone in chain]
            current_length = 0
            for i, bone in enumerate(chain):
                bone_length = total_distance * length_ratios[i]
                bone.head = head + direction * current_length
                current_length += bone_length
                bone.tail = head + direction * current_length

        if self.roll:
            for bone in chain:
                bone.roll = roll


classes = [
    MIO3BONE_OT_bone_evenly,
    MIO3BONE_OT_bone_align,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
