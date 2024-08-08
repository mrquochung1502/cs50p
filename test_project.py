import pytest
import json
from os import makedirs
from os.path import join, exists, isdir
from project import create_data_folder, get_target_positions, load_json, save_json


def test_get_target_positions():
    # A 500x300 screen for the test purpose, topleft at (225,125)
    expected_grid_topleft = (225, 125)
    expected_positions = [
        (225, 125), (275, 125),
        (225, 175), (275, 175)
    ]
    grid_topleft, positions = get_target_positions((500, 300), target_distance=50, grid_edge=2)
    assert grid_topleft == expected_grid_topleft
    assert positions == expected_positions


def test_create_data_folder(tmp_path):
    folder_path = join(tmp_path, "test_folder")
    assert not exists(folder_path)
    # Make sure the folder exists
    create_data_folder(folder_path)
    assert exists(folder_path)
    assert isdir(folder_path)
    # Make sure no exceptions raise if the folder already exists, all existing files inside remain intact
    test_data = {"test": "This is a test"}
    file_path = join(folder_path, "file_for_integrity_test.json")
    with open(file_path, 'w') as file:
        json.dump(test_data, file)
    create_data_folder(folder_path)  # recreate the folder (try to overwrite)
    loaded_data = load_json(join(folder_path, "file_for_integrity_test.json"))
    assert loaded_data == test_data


def test_load_json(tmp_path):
    test_data = {"test": "This is a test"}
    file_path = join(tmp_path, "test_file_for_loading.json")
    with open(file_path, 'w') as file:
        json.dump(test_data, file)

    loaded_data = load_json(file_path)
    assert loaded_data == test_data


def test_load_json_default(tmp_path):
    file_path = join(tmp_path, "non_exist_file_for_default_loading_test.json")
    default_data = {"test": "This is a test"}
    loaded_data = load_json(file_path, default=default_data)
    assert loaded_data == default_data


def test_save_json(tmp_path):
    test_data = {"test": "This is a test"}
    file_path = join(tmp_path, "test_file_for_saving.json")
    save_json(file_path, test_data)

    with open(file_path, 'r') as file:
        saved_data = json.load(file)
    assert saved_data == test_data
