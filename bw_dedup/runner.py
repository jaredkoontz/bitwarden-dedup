import argparse
import json
import logging
import sys
from pathlib import Path
from typing import Sequence

from bw_dedup.dedup_utils import fix_entries_in_items
from bw_dedup.dedup_utils import prune_duplicate_dirs
from bw_dedup.dedup_utils.data_types import BWDataMap
from bw_dedup.dedup_utils.data_types import BWDataMapJSONEncoder
from bw_dedup.dedup_utils.data_types import make_bw_data_map_from_json


def _read_args(command_line: Sequence[str] | None = None):
    parser = argparse.ArgumentParser(description="Bitwarden exported json path.")
    parser.add_argument(
        "file_path",
        type=Path,
        help="Path to the input file",
    )
    args = parser.parse_args(command_line)

    if not args.file_path.is_file():
        parser.error(f"The file {args.file_path} does not exist or is not a file.")

    return args.file_path


def _write_json(merged: BWDataMap, json_file: Path):
    new_file = json_file.with_name(f"{json_file.stem}_verified{json_file.suffix}")
    # write JSON files:
    with new_file.open("w", encoding="UTF-8") as target:
        json.dump(merged, target, cls=BWDataMapJSONEncoder)


def main(command_line: Sequence[str] | None = None) -> int:
    logging.basicConfig(level="INFO")

    json_file = _read_args(command_line)
    bw_data = make_bw_data_map_from_json(json_file)

    folder_id_map, pruned_dirs = prune_duplicate_dirs(bw_data.folders)
    entry_data = fix_entries_in_items(bw_data.items, folder_id_map)

    bw_data.items = entry_data
    bw_data.folders = pruned_dirs
    _write_json(bw_data, json_file)

    return 0


if __name__ == "__main__":
    sys.exit(main())
