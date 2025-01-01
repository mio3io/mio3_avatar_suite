import bpy
import re
from bpy.types import Operator, Panel


class MIO3BONE_OT_ConvertNames(Operator):
    bl_idname = "armature.convert_bone_names"
    bl_label = "ボーン名を変換"
    bl_description = "ポーズモードで表示されているボーンの名前を変換します"
    bl_options = {"REGISTER", "UNDO"}

    conventions = {
        "UpperArm_L": {
            "separator": "",
            "side_format": "_{}",
            "side_type": "suffix",
        },
        "Upper Arm_L": {
            "separator": " ",
            "side_format": "_{}",
            "side_type": "suffix",
        },
        "Upper_Arm_L": {
            "separator": "_",
            "side_format": "_{}",
            "side_type": "suffix",
        },
        "UpperArm.L": {
            "separator": "",
            "side_format": ".{}",
            "side_type": "suffix",
        },
        "Upper Arm.L": {
            "separator": " ",
            "side_format": ".{}",
            "side_type": "suffix",
        },
        "Upper_Arm.L": {
            "separator": "_",
            "side_format": ".{}",
            "side_type": "suffix",
        },
        "L_UpperArm": {
            "separator": "",
            "side_format": "{}_",
            "side_type": "prefix",
        },
        "Generic": {
            "separator": "",
            "side_format": "{}",
            "side_type": "none",
        },
    }

    patterns = (
        {  # _L とか
            "pattern": r"(.+)[._](L|R|Left|Right)([._]\d*(?:_end|\.end|end)?)?$",
            "side_type": "suffix",
        },
        {  # L_ とか
            "pattern": r"^(L|R|Left|Right)[._](.+)([._]\d*(?:_end|\.end|end)?)?$",
            "side_type": "prefix",
        },
        {  # UpperArmLeft とか
            "pattern": r"(.+)(Left|Right)([._]\d*(?:_end|\.end|end)?)?$",
            "side_type": "suffix",
        },
        {  # LeftUpperArm とか
            "pattern": r"^(Left|Right)([^a-z].*)([._]\d*(?:_end|\.end|end)?)?$",
            "side_type": "prefix",
        },
        {  # 左右なし
            "pattern": r"(.+?)([._]\d*(?:_end|\.end|end)?)?$",
            "side_type": "none",
        },
    )

    def detect_name_component(self, bone_name, prefix_list):
        prefix = ""
        base = bone_name
        for p in prefix_list:
            if bone_name.startswith(p):
                prefix = p
                base = bone_name[len(p) :]
        name, side, ext = self.detect_pattern(base)
        return prefix, name, side, ext

    def detect_pattern(self, name):
        for data in self.patterns:
            match = re.match(data["pattern"], name)
            if match:
                if data["side_type"] == "suffix":
                    return match.group(1), match.group(2), match.group(3) or ""
                elif data["side_type"] == "prefix":
                    return match.group(2), match.group(1), match.group(3) or ""
                else:
                    return match.group(1), "", match.group(2) or ""
        return name, "", ""

    def join_name_component(self, prefix, name, side, number, convert_type):
        conv_data = self.conventions[convert_type]
        if side == "":
            return "".join([prefix, name, number])
        elif self.conventions[convert_type]["side_type"] == "suffix":
            newstr = "".join([prefix, name, conv_data["side_format"].format(side), number])
        else:
            newstr = "".join([prefix, conv_data["side_format"].format(side), name, number])
        return newstr

    def convert_name(self, name, to_conv):
        if re.match(r"^[a-zA-Z0-9\s_.\-]+$", name):
            words = re.findall(r"[A-Z][a-z0-9]*|[a-z0-9]+", name)
        else:
            words = [name]
        separator = self.conventions[to_conv]["separator"]
        if self.conventions[to_conv]["separator"] == "":
            newstr = separator.join(word.capitalize() for word in words)
        else:
            newstr = separator.join(words)
        return newstr

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj is not None and obj.type == "ARMATURE"

    def execute(self, context):
        armature = context.active_object
        if armature.type != "ARMATURE":
            self.report({"ERROR"}, "アーマチュアを選択してください")
            return {"CANCELLED"}

        props = context.scene.mio3bone
        convert_type = props.convert_types
        prefix_list = [item.name for item in context.scene.mio3bone.prefix_list]

        for bone in armature.pose.bones:
            if not bone.bone.hide:
                prefix, name, side, ext = self.detect_name_component(bone.name, prefix_list)
                if context.scene.mio3bone.remove_prefix:
                    prefix = ""

                side = side[0] if side in ["Left", "Right"] else side

                name = self.convert_name(name, convert_type)
                new_name = self.join_name_component(prefix, name, side, ext, convert_type)
                if new_name != bone.name:
                    bone.name = new_name

        return {"FINISHED"}


class MIO3BONE_OT_PrefixAdd(bpy.types.Operator):
    bl_idname = "mio3bone.prefix_add"
    bl_label = "Add Item"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        mio3bone = context.scene.mio3bone

        prefix_list = mio3bone.prefix_list
        input_prefix = mio3bone.input_prefix
        new_item = prefix_list.add()
        new_item.name = input_prefix
        return {"FINISHED"}


class MIO3BONE_OT_PrefixRemove(bpy.types.Operator):
    bl_idname = "mio3bone.prefix_remove"
    bl_label = "Remove Item"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        mio3bone = context.scene.mio3bone

        prefix_list = mio3bone.prefix_list
        prefix_list.remove(mio3bone.prefix_active_index)
        mio3bone.prefix_active_index = min(max(0, mio3bone.prefix_active_index - 1), len(prefix_list) - 1)
        return {"FINISHED"}


class MIO3BONE_PT_Convert(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Mio3"
    bl_label = "フォーマット変換"
    bl_parent_id = "MIO3BONE_PT_Main"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        props = context.scene.mio3bone
        layout.prop(props, "convert_types")
        layout.operator("armature.convert_bone_names")

        box = layout.box()
        icon = "TRIA_DOWN" if props.show_prefix else "TRIA_RIGHT"
        row = box.row()
        row.alignment = "LEFT"
        row.prop(props, "show_prefix", toggle=True, emboss=False, icon=icon)

        if props.show_prefix:

            row = box.row(align=True)
            row.label(text="Prefix")
            row.scale_x = 2
            row.prop(context.scene.mio3bone, "input_prefix", text="")

            row = box.row()
            row.template_list(
                "MIO3BONE_UL_PrefixList",
                "prefix_list",
                context.scene.mio3bone,
                "prefix_list",
                context.scene.mio3bone,
                "prefix_active_index",
                rows=3,
            )

            col = row.column(align=True)
            col.operator("mio3bone.prefix_add", icon="ADD", text="")
            col.operator("mio3bone.prefix_remove", icon="REMOVE", text="")
            box.prop(context.scene.mio3bone, "remove_prefix")


class MIO3BONE_UL_PrefixList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        row = layout.row(align=True)
        row.prop(item, "name", icon="PINNED", text="", emboss=False)


classes = (
    MIO3BONE_OT_ConvertNames,
    MIO3BONE_OT_PrefixAdd,
    MIO3BONE_OT_PrefixRemove,
    MIO3BONE_UL_PrefixList,
    MIO3BONE_PT_Convert,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
