import pytest

from bw_dedup.dedup_utils import fix_entries_in_items
from bw_dedup.dedup_utils.data_types import make_item_data


@pytest.mark.parametrize(
    "test_data,folder_id_map,expected",
    [
        (
            [
                {"id": "nothing", "name": "here", "type": 1},
                {"id": "or", "name": "here", "type": 1},
            ],
            {"4N07H3R": "S0M31D"},
            [
                {"id": "nothing", "name": "here", "type": 1},
                {"id": "or", "name": "here", "type": 1},
            ],
        ),
        (
            [
                {"id": "nothing", "name": "here", "type": 1},
                {"id": "or", "name": "here", "type": 2},
            ],
            {"4N07H3R": "S0M31D"},
            [{"id": "or", "name": "here", "type": 2}],
        ),
        (
            [
                {
                    "id": "nothing",
                    "name": "here",
                    "type": 1,
                    "login": {"username": "", "password": ""},
                },
                {
                    "id": "or",
                    "name": "here",
                    "type": 2,
                    "login": {"username": "", "password": ""},
                },
            ],
            {"4N07H3R": "S0M31D"},
            [
                {
                    "id": "or",
                    "login": {"password": "", "username": ""},
                    "name": "here",
                    "type": 2,
                }
            ],
        ),
        (
            [
                {
                    "id": "nothing",
                    "name": "here",
                    "type": 1,
                    "login": {
                        "username": "foo",
                        "password": "bar",
                        "uris": [{"uri": "https://google.com"}],
                    },
                },
                {
                    "id": "or",
                    "name": "here",
                    "type": 2,
                    "login": {"username": "", "password": ""},
                },
            ],
            {"4N07H3R": "S0M31D"},
            [
                {
                    "id": "nothing",
                    "login": {
                        "password": "bar",
                        "uris": [{"uri": "https://google.com"}],
                        "username": "foo",
                    },
                    "name": "here",
                    "type": 1,
                },
                {
                    "id": "or",
                    "login": {"password": "", "username": ""},
                    "name": "here",
                    "type": 2,
                },
            ],
        ),
        (
            [
                {
                    "id": "4N07H3R",
                    "folderId": "4N07H3R",
                    "name": "here",
                    "type": 1,
                    "login": {
                        "username": "unique",
                        "password": "info",
                        "uris": [{"uri": "https://google.com"}],
                    },
                },
                {
                    "id": "S0M31D",
                    "folderId": "4N07H3R",
                    "name": "here",
                    "type": 1,
                    "login": {
                        "username": "foo",
                        "password": "bar",
                        "uris": [{"uri": "https://google.com"}],
                    },
                },
                {
                    "id": "or",
                    "name": "here",
                    "type": 2,
                    "login": {"username": "", "password": ""},
                },
            ],
            {"4N07H3R": "S0M31D"},
            [
                {
                    "folderId": "S0M31D",
                    "id": "4N07H3R",
                    "login": {
                        "password": "info",
                        "uris": [{"uri": "https://google.com"}],
                        "username": "unique",
                    },
                    "name": "here",
                    "type": 1,
                },
                {
                    "folderId": "S0M31D",
                    "id": "S0M31D",
                    "login": {
                        "password": "bar",
                        "uris": [{"uri": "https://google.com"}],
                        "username": "foo",
                    },
                    "name": "here",
                    "type": 1,
                },
                {
                    "id": "or",
                    "login": {"password": "", "username": ""},
                    "name": "here",
                    "type": 2,
                },
            ],
        ),
    ],
)
def test_merge_duplicate_entries(test_data, folder_id_map, expected):
    assert fix_entries_in_items(
        make_item_data(test_data), folder_id_map
    ) == make_item_data(expected)


@pytest.mark.parametrize(
    "test_data,folder_id_map,expected",
    [
        # different
        (
            [
                {
                    "id": "nothing",
                    "name": "here",
                    "type": 1,
                    "login": {
                        "username": "foo",
                        "password": "bar",
                        "uris": [{"uri": "https://google.com"}],
                    },
                },
                {
                    "id": "dupe",
                    "login": {
                        "username": "foo",
                        "password": "bar",
                        "uris": [{"uri": "https://google.com"}],
                    },
                    "name": "here",
                    "type": 1,
                },
                {
                    "id": "not_dupe",
                    "login": {
                        "username": "foo",
                        "password": "man",
                        "uris": [{"uri": "https://google.com"}],
                    },
                    "name": "here",
                    "type": 1,
                },
            ],
            {"4N07H3R": "S0M31D"},
            [
                {
                    "id": "nothing",
                    "login": {
                        "password": "bar",
                        "uris": [{"uri": "https://google.com"}],
                        "username": "foo",
                    },
                    "name": "here",
                    "type": 1,
                },
                {
                    "id": "not_dupe",
                    "login": {
                        "password": "man",
                        "uris": [{"uri": "https://google.com"}],
                        "username": "foo",
                    },
                    "name": "here",
                    "type": 1,
                },
            ],
        ),
        (
            [
                {
                    "id": "4N07H3R",
                    "folderId": "4N07H3R",
                    "name": "",
                    "type": 1,
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
                    "type": 1,
                    "login": {
                        "username": "foo",
                        "password": "",
                        "uris": [{"uri": "https://google.com"}],
                    },
                },
                {
                    "id": "or",
                    "name": "here",
                    "type": 2,
                    "login": {"username": "", "password": ""},
                },
            ],
            {"4N07H3R": "S0M31D"},
            [
                {
                    "folderId": "S0M31D",
                    "id": "4N07H3R",
                    "login": {
                        "password": "info",
                        "uris": [{"uri": ""}],
                        "username": "",
                    },
                    "name": "",
                    "type": 1,
                },
                {
                    "folderId": "S0M31D",
                    "id": "S0M31D",
                    "login": {
                        "password": "",
                        "uris": [{"uri": "https://google.com"}],
                        "username": "foo",
                    },
                    "name": "here",
                    "type": 1,
                },
                {
                    "id": "or",
                    "login": {"password": "", "username": ""},
                    "name": "here",
                    "type": 2,
                },
            ],
        ),
    ],
)
def test_corner_cases(test_data, folder_id_map, expected):
    assert fix_entries_in_items(
        make_item_data(test_data), folder_id_map
    ) == make_item_data(expected)
