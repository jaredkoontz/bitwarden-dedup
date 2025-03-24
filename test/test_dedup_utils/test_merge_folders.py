import pytest

from bw_dedup.dedup_utils import prep_duplicate_folders


@pytest.mark.parametrize(
    "test_data,expected_map,expected_folders",
    [
        (
            [
                {"id": "S0M31D", "name": "shared"},
                {"id": "4N07H3R", "name": "shared"},
            ],
            {"4N07H3R": "S0M31D"},
            [{"id": "S0M31D", "name": "shared"}],
        ),
        (
            [
                {"id": "4N07H3R", "name": "shared"},
            ],
            {},
            [
                {"id": "4N07H3R", "name": "shared"},
            ],
        ),
        ([], None, None),
    ],
)
def test_prep_duplicate_folders(test_data, expected_map, expected_folders):
    prepped = prep_duplicate_folders(test_data)
    assert len(prepped) == 2
    assert prepped[0] == expected_map
    assert prepped[1] == expected_folders
