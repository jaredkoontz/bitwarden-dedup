import validators

from .data_types import BWEntryType
from .data_types import LoginInfo
from .data_types import PrunedEntry


def fix_entries_in_items(
    entry_data: list[PrunedEntry], folder_id_map: dict[str, str]
) -> list[PrunedEntry]:
    def _fix_and_verify(entry: PrunedEntry) -> PrunedEntry | None:
        if entry.type != BWEntryType.UNAME_PW:
            # this is not a username / password entry skip it
            return entry
        assert isinstance(entry, LoginInfo)
        login_entry: LoginInfo = entry
        name = login_entry.data.get("name")
        if not name:
            print(f"INVALID NAME: {entry}")

        if not login_entry.uris:
            print(f"NO URI: {entry}")
            return None
        else:
            url = login_entry.uris[0]["uri"]
            if not validators.url(url):
                print(f"INVALID URL: {entry}")

        if not login_entry.username:
            print(f"NO USERNAME: {entry}")
        if not login_entry.password:
            print(f"NO PW: {entry}")

        if login_entry.hex_digest in all_pws:
            pass
            # print(f"duplicate PW on {entry}")
        else:
            all_pws.add(login_entry.hex_digest)
        cred_tuple = (login_entry.username, login_entry.hex_digest)
        if credential_map.get(url):
            if cred_tuple in credential_map[url]:
                print(f"DUPLICATE {entry}")
                return None
            else:
                credential_map[url].add(cred_tuple)
        else:
            credential_map[url] = {cred_tuple}

        # if we made it this far, we have a unique entry, with a password and username
        if entry.data.get("folderId"):
            new_id = folder_id_map.get(entry.data["folderId"])
            if new_id:
                entry.data["folderId"] = new_id

        return entry

    all_pws = set()
    credential_map = {}
    verified = []
    for cred_data in entry_data:
        fixed_and_verified = _fix_and_verify(cred_data)
        if fixed_and_verified:
            verified.append(fixed_and_verified)
    return verified
