
def split_bone_chains(selected_bones):
    bone_chains = []
    current_chain = []
    for bone in selected_bones:
        if not current_chain or current_chain[-1].tail == bone.head:
            current_chain.append(bone)
        else:
            bone_chains.append(current_chain)
            current_chain = [bone]

    if current_chain:
        bone_chains.append(current_chain)
    return bone_chains

def sort_bones(bone, sorted_bones, renamed_bones, selected_bones):
    if bone not in renamed_bones and bone in selected_bones:
        sorted_bones.append(bone)
        renamed_bones.add(bone)
        for child in bone.children:
            sort_bones(child, sorted_bones, renamed_bones, selected_bones)
