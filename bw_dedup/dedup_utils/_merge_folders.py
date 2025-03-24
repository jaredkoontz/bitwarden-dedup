"""
My bitwarden was full of duplicate folders. The submodule only worries about the folder section.
We take a folder name, and then create a map for all collisions to this name so we can clean them
up later. See tests for examples.
"""


def _create_id_map_and_prune_folders(new_folders) -> tuple[dict[str, str], list[dict]]:
    id_map = {}
    pruned_folders = []
    for key, entry in new_folders.items():
        new_entry = {"id": entry["id"], "name": entry["name"]}
        pruned_folders.append(new_entry)
        if entry.get("dupes"):
            for dupe in entry["dupes"]:
                id_map[dupe] = entry["id"]
    return id_map, pruned_folders


def prep_duplicate_folders(
    folder_data: list[dict],
) -> tuple[dict[str, str], list[dict]] | tuple[None, None]:
    new_folders = {}
    if not folder_data:
        return None, None
    for x in folder_data:
        if not new_folders.get(x["name"]):
            new_folders[x["name"]] = x
        else:
            entry = new_folders[x["name"]]
            if not entry.get("dupes"):
                entry.setdefault("dupes", [])
            entry["dupes"].append(x["id"])
    return _create_id_map_and_prune_folders(new_folders)
