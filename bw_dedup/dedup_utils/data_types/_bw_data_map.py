import dataclasses
import hashlib
import json
from enum import auto
from enum import Enum
from pathlib import Path


class BWEntryType(Enum):
    UNAME_PW = auto()
    UNKNOWN = auto()
    CARD = 36

    @classmethod
    def _missing_(cls, value):
        return cls.UNKNOWN


@dataclasses.dataclass
class PrunedEntry:
    type: BWEntryType
    data: dict


@dataclasses.dataclass
class BWDataMap:
    encrypted: bool
    folders: list[dict]
    items: list[PrunedEntry]


@dataclasses.dataclass
class LoginInfo(PrunedEntry):
    data: dict
    username: str = dataclasses.field(init=True, default=None)
    password: str = dataclasses.field(init=True, default=None)
    hex_digest: str = dataclasses.field(init=True, default=None)
    uris: list[dict[str]] = dataclasses.field(init=True, default=None)

    def __post_init__(self):
        login_info = self.data.get("login")
        if not login_info:
            return
        self.username = login_info.get("username")
        self.password = login_info.get("password")
        self.uris = login_info.get("uris")
        if self.password:
            encoded_string = self.password.encode("utf-8")  # Encode the string to bytes
            hash_object = hashlib.sha256(encoded_string)
            self.hex_digest = hash_object.hexdigest()


class BWDataMapJSONEncoder(json.JSONEncoder):
    def default(self, o):
        assert dataclasses.is_dataclass(o)
        return {
            "encrypted": o.encrypted,
            "folders": o.folders,
            "items": [x.data for x in o.items],
        }


def make_item_data(data_items: list[dict]) -> list[PrunedEntry]:
    verified = []
    for i, dict_info in enumerate(data_items):
        entry_type = dict_info.get("type")
        if entry_type == BWEntryType.CARD.value:
            entry = PrunedEntry(BWEntryType(entry_type), dict_info)
        elif entry_type == BWEntryType.UNAME_PW.value:
            entry = LoginInfo(BWEntryType(entry_type), dict_info)
            if not entry.password and not entry.username:
                print(f"USELESS {entry}")
                # skip this one completely
                continue
        else:
            # this might be malformed. For this sake of safety, just ignore it and add it back to the final
            # entry list
            entry = PrunedEntry(BWEntryType(entry_type), dict_info)
        verified.append(entry)
    return verified


def from_json(file_path: Path) -> BWDataMap:
    json_data = json.loads(file_path.read_text())
    return BWDataMap(
        json_data["encrypted"], json_data["folders"], make_item_data(json_data["items"])
    )
