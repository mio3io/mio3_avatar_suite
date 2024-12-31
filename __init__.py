import bpy
from bpy.types import Panel, PropertyGroup
from bpy.props import (
    BoolProperty,
    IntProperty,
    StringProperty,
    EnumProperty,
    PointerProperty,
    CollectionProperty,
)
from .operators import convert
from .operators import convert_preset
from .operators import distribute
from .operators import numbering
from .operators import add_armature


bl_info = {
    "name": "Mio3 Avatar Tools",
    "author": "mio",
    "version": (1, 0),
    "blender": (4, 1, 0),
    "location": "View3D > Mio3",
    "description": "Avatar Setup support",
    "category": "Tools",
}

translation_dict = {
    "ja_JP": {
        ("*", "Suffix L/R"): "L/Rを接尾辞にする",
        ("*", "Delim"): "デリミタ",
        ("*", "EndBone"): "エンドボーン",
        ("Operator", "Evenly Bones"): "ボーンを均等",
        ("Operator", "Align Bones (child)"): "ボーンを整列（末端を基準）",
        ("Operator", "Numbering Bones"): "ボーンに通し番号をふる",
        ("Operator", "Unify roles"): "ロールを統一",
        ("*", "Preserve Length Bone"): "各ボーンの長さを維持",
        ("*", "After Format"): "変換後",
    }
}


def menu(self, context):
    menu_transform(self, context)
    menu_name(self, context)


def menu_transform(self, context):
    self.layout.separator()
    self.layout.operator("armature.mio3_bone_align")
    self.layout.operator("armature.mio3_bone_evenly")


def menu_name(self, context):
    self.layout.separator()
    self.layout.operator("armature.mio3_bone_numbering")


def menu_armature_add(self, context):
    self.layout.separator()
    self.layout.operator("armature.mio3_add_humanoid", icon="ARMATURE_DATA")


class MIO3BONE_PT_Main(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Mio3"
    bl_label = "Mio3 Avatar Tools"

    def draw(self, context):
        layout = self.layout


class MIO3BONE_PG_PrefixItem(PropertyGroup):
    name: StringProperty(name="Prefix")


class MIO3BONE_PG_Main(PropertyGroup):
    show_prefix: BoolProperty(name="カスタムプレフィックス")
    prefix_list: CollectionProperty(name="List", type=MIO3BONE_PG_PrefixItem)
    prefix_active_index: IntProperty()
    remove_prefix: BoolProperty(name="プレフィックスを削除", default=False)
    input_prefix: StringProperty(name="Prefix", default="Twist_")
    convert_types: EnumProperty(
        name="After Format",
        description="",
        items=[
            ("UpperArm_L", "UpperArm_L (推奨)", ""),
            ("UpperArm.L", "UpperArm.L", ""),
        ],
        default="UpperArm_L",
    )
    preset_reverse: BoolProperty(name="変換を反転")


classes = [
    MIO3BONE_PG_PrefixItem,
    MIO3BONE_PG_Main,
    MIO3BONE_PT_Main,
]

modules = [
    convert,
    convert_preset,
    distribute,
    numbering,
    add_armature,
]


def register():
    bpy.app.translations.register(__name__, translation_dict)
    for cls in classes:
        bpy.utils.register_class(cls)
    for module in modules:
        module.register()
    bpy.types.VIEW3D_MT_transform_armature.append(menu_transform)
    bpy.types.VIEW3D_MT_edit_armature_names.append(menu_name)
    bpy.types.VIEW3D_MT_armature_context_menu.append(menu)
    bpy.types.VIEW3D_MT_armature_add.append(menu_armature_add)
    bpy.types.Scene.mio3bone = PointerProperty(type=MIO3BONE_PG_Main)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    for module in reversed(modules):
        module.unregister()
    bpy.types.VIEW3D_MT_transform_armature.remove(menu_transform)
    bpy.types.VIEW3D_MT_edit_armature_names.remove(menu_name)
    bpy.types.VIEW3D_MT_armature_context_menu.remove(menu)
    bpy.types.VIEW3D_MT_armature_add.remove(menu_armature_add)
    del bpy.types.Scene.mio3bone
    bpy.app.translations.unregister(__name__)


if __name__ == "__main__":
    register()
