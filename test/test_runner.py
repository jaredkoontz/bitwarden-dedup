import json
from pathlib import Path

import pytest

from bw_dedup.runner import main
from test.test_data import happy_path_test_data


@pytest.fixture(scope="session")
def password_data(tmp_path_factory) -> Path:
    pw_data = happy_path_test_data
    file_path = tmp_path_factory.mktemp("data") / "tests.json"
    file_path.write_text(json.dumps(pw_data))
    return file_path


def test_happy_path(password_data):
    main([str(password_data.absolute())])
    new_data_path = password_data.with_name(
        f"{password_data.stem}_verified{password_data.suffix}"
    )
    assert new_data_path.exists()
    new_data = json.loads(new_data_path.read_text())
    assert len(new_data["folders"]) == 1
    assert len(new_data["items"]) == 5


def test_no_file():
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        main(["🐧🐬"])

    assert pytest_wrapped_e.type is SystemExit
    assert pytest_wrapped_e.value.code == 2
