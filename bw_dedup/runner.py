import argparse
import json
import sys
from pathlib import Path
from typing import Sequence

from bw_dedup.dedup_utils import fix_entries_in_items
from bw_dedup.dedup_utils import prep_duplicate_folders
from bw_dedup.dedup_utils.data_types import BWDataMap
from bw_dedup.dedup_utils.data_types import BWDataMapJSONEncoder
from bw_dedup.dedup_utils.data_types import from_json


def _read_args(command_line: Sequence[str] | None = None):
    parser = argparse.ArgumentParser(description="Bitwarden file path.")
    parser.add_argument(
        "file_path",
        type=Path,
        help="Path to the input file",
    )

    args = parser.parse_args(command_line)

    # Validate that the file exists
    if not args.file_path.is_file():
        parser.error(f"The file {args.file_path} does not exist or is not a file.")

    return args.file_path


def _read_json(json_file: Path) -> BWDataMap:
    return from_json(json_file)


def _write_json(merged: BWDataMap, json_file: Path):
    new_file = json_file.with_name(f"{json_file.stem}_verified{json_file.suffix}")
    # write JSON files:
    with new_file.open("w", encoding="UTF-8") as target:
        json.dump(merged, target, cls=BWDataMapJSONEncoder)


def main(command_line: Sequence[str] | None = None) -> int:
    json_file = _read_args(command_line)
    bw_data = _read_json(json_file)

    folder_id_map, pruned_folders = prep_duplicate_folders(bw_data.folders)
    entry_data = fix_entries_in_items(bw_data.items, folder_id_map)

    bw_data.items = entry_data
    bw_data.folders = pruned_folders
    _write_json(bw_data, json_file)

    return 0


if __name__ == "__main__":
    sys.exit(main())
