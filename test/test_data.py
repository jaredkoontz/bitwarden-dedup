from bw_dedup.dedup_utils.data_types import BWEntryType

happy_path_test_data = {
    "encrypted": False,
    "folders": [
        {"id": "S0M31D", "name": "shared"},
        {"id": "4N07H3R", "name": "shared"},
    ],
    "items": [
        {
            "id": "4N07H3R",
            "folderId": "4N07H3R",
            "name": "",
            "type": BWEntryType.UNAME_PW.value,
            "login": {
                "username": "",
                "password": "info",
                "uris": [{"uri": ""}],
            },
        },
        {
            "id": "S0M31D",
            "folderId": "4N07H3R",
            "name": "here",
            "type": BWEntryType.UNAME_PW.value,
            "login": {
                "username": "foo",
                "password": "",
                "uris": [{"uri": "https://google.com"}],
            },
        },
        {
            "id": "dupe",
            "folderId": "4N07H3R",
            "name": "dupe",
            "type": BWEntryType.UNAME_PW.value,
            "login": {
                "username": "dupe",
                "password": "dupe",
                "uris": [{"uri": "https://google.com"}],
            },
        },
        {
            "id": "dupe",
            "folderId": "4N07H3R",
            "name": "dupe",
            "type": BWEntryType.UNAME_PW.value,
            "login": {
                "username": "dupe",
                "password": "dupe",
                "uris": [{"uri": "https://google.com"}],
            },
        },
        {
            "id": "or",
            "name": "here",
            "type": BWEntryType.UNKNOWN.value,
            "login": {"username": "", "password": ""},
        },
        {
            "id": "or",
            "name": "here",
            "type": BWEntryType.CARD.value,
            "login": {"username": "", "password": ""},
        },
    ],
}
