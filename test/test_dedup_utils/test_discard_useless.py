import pytest

from bw_dedup.dedup_utils.data_types import BWEntryType
from bw_dedup.dedup_utils.data_types import LoginInfo
from bw_dedup.dedup_utils.data_types import make_item_data
from bw_dedup.dedup_utils.data_types import PrunedEntry


@pytest.mark.parametrize(
    "test_data,expected",
    [
        (
            [
                {"id": "nothing", "name": "here"},
                {"id": "or", "name": "here"},
            ],
            [
                PrunedEntry(
                    BWEntryType.UNKNOWN, data={"id": "nothing", "name": "here"}
                ),
                PrunedEntry(BWEntryType.UNKNOWN, data={"id": "or", "name": "here"}),
            ],
        ),
        (
            [
                {"id": "nothing", "name": "here", "type": 1},
                {"id": "or", "name": "here", "type": 2},
            ],
            [
                PrunedEntry(
                    BWEntryType.UNKNOWN, data={"id": "or", "name": "here", "type": 2}
                ),
            ],
        ),
        (
            [
                {
                    "id": "nothing",
                    "name": "here",
                    "type": 1,
                    "login": {"username": "foo", "password": ""},
                },
                {
                    "id": "or",
                    "name": "here",
                    "type": 2,
                    "login": {"username": "", "password": "foo"},
                },
            ],
            [
                LoginInfo(
                    BWEntryType.UNAME_PW,
                    data={
                        "id": "nothing",
                        "login": {"password": "", "username": "foo"},
                        "name": "here",
                        "type": 1,
                    },
                    username="foo",
                    password="",
                    hex_digest=None,
                    uris=None,
                ),
                PrunedEntry(
                    BWEntryType.UNKNOWN,
                    data={
                        "id": "or",
                        "login": {"password": "foo", "username": ""},
                        "name": "here",
                        "type": 2,
                    },
                ),
            ],
        ),
    ],
)
def test_prep_duplicate_folders(test_data, expected):
    assert make_item_data(test_data) == expected
