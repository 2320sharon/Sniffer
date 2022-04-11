import pytest
import shutil
import csv
import pandas as pd
import os
import glob
from Sniffer import sniffer

@pytest.fixture(scope="function")
def get_temp_images_mixed_exts_dir(tmpdir_factory):
    test_images_dir="./Sniffer/tests/test_data/images"
    temp_dir = tmpdir_factory.mktemp("images")
    for img in os.listdir(test_images_dir):
        temp_dest_path=temp_dir
        temp_dest_path = temp_dir.join(f"{img}")
        src_path=test_images_dir+os.sep+img
        print(src_path)
        shutil.copy(src_path,temp_dest_path)
    return temp_dir

@pytest.fixture(scope="function")
def get_temp_populated_images_dir(tmpdir_factory):
    test_images_dir="./Sniffer/tests/test_data/bad_images"
    temp_dir = tmpdir_factory.mktemp("images")
    for img in os.listdir(test_images_dir):
        temp_dest_path=temp_dir
        temp_dest_path = temp_dir.join(f"{img}")
        src_path=test_images_dir+os.sep+img
        shutil.copy(src_path,temp_dest_path)
    return temp_dir


@pytest.fixture(scope="function")
def get_temp_good_populated_images_dir(tmpdir_factory):
    test_images_dir="./Sniffer/tests/test_data/good_images"
    temp_dir = tmpdir_factory.mktemp("images")
    for img in os.listdir(test_images_dir):
        temp_dest_path=temp_dir
        temp_dest_path = temp_dir.join(f"{img}")
        src_path=test_images_dir+os.sep+img
        shutil.copy(src_path,temp_dest_path)
    return temp_dir

@pytest.fixture(scope="function")
def empty_thumbnails_dir(tmpdir_factory):
    temp_dir = tmpdir_factory.mktemp("thumbnails")
    return temp_dir

@pytest.fixture(scope="function")
def temp_good_thumbnails(tmpdir_factory):
    test_images_dir="./Sniffer/tests/test_data/good_images"
    temp_dir = tmpdir_factory.mktemp("thumbnails")
    for img in os.listdir(test_images_dir):
        temp_dest_path=temp_dir
        temp_dest_path = temp_dir.join(f"{img}")
        src_path=test_images_dir+os.sep+img
        shutil.copy(src_path,temp_dest_path)
    return temp_dir

@pytest.fixture(scope="function")
def temp_good_images(tmpdir_factory):
    test_images_dir="./Sniffer/tests/test_data/good_images"
    temp_dir = tmpdir_factory.mktemp("good_images")
    for img in os.listdir(test_images_dir):
        temp_dest_path=temp_dir
        temp_dest_path = temp_dir.join(f"{img}")
        src_path=test_images_dir+os.sep+img
        shutil.copy(src_path,temp_dest_path)
    return temp_dir

@pytest.fixture(scope="function")
def get_temp_valid_images_dir(tmpdir_factory):
    test_images_dir="./Sniffer/tests/test_data/good_images"
    temp_dir = tmpdir_factory.mktemp("images")
    for img in os.listdir(test_images_dir):
        temp_dest_path=temp_dir
        temp_dest_path = temp_dir.join(f"{img}")
        src_path=test_images_dir+os.sep+img
        shutil.copy(src_path,temp_dest_path)
    return temp_dir


@pytest.fixture(scope="function")
def get_temp_empty_good_images_dir(tmpdir_factory):
    temp_dir = tmpdir_factory.mktemp("good_images")
    return temp_dir

@pytest.fixture(scope="function")
def get_temp_empty_bad_images_dir(tmpdir_factory):
    temp_dir = tmpdir_factory.mktemp("bad_images")
    return temp_dir

@pytest.fixture(scope="function")
def get_temp_bad_images_dir(tmpdir_factory):
    test_images_dir="./Sniffer/tests/test_data/bad_images"
    temp_dir = tmpdir_factory.mktemp("bad_images")
    for img in os.listdir(test_images_dir):
        temp_dest_path=temp_dir
        temp_dest_path = temp_dir.join(f"{img}")
        src_path=test_images_dir+os.sep+img
        shutil.copy(src_path,temp_dest_path)
    return temp_dir


@pytest.fixture(scope="function")
def temp_empty_csv(tmpdir_factory):
    temp_dir = tmpdir_factory.mktemp("csv").join("data.csv")
    with open(temp_dir, 'w', newline='') as outcsv:
        writer = csv.writer(outcsv)
        writer.writerow(["Filename", "Sorted", "index"])
    return temp_dir

@pytest.fixture(scope="function")
def temp_populated_csv(tmpdir_factory,get_temp_populated_images_dir):
    # 1st element in temp_populated_images_dir written to temp csv as "good"
    images_list = glob.glob1(get_temp_populated_images_dir, "*jpg")
    temp_dir = tmpdir_factory.mktemp("csv").join("data.csv")
    with open(temp_dir, 'w', newline='') as outcsv:
            writer = csv.writer(outcsv)
            writer.writerow(["Filename", "Sorted", "index"])
            writer.writerow([images_list[0], "good", "0"])
    return temp_dir

@pytest.fixture(scope="session")
def get_temp_csv(tmpdir_factory):
    temp_dir = tmpdir_factory.mktemp("csv").join("data.csv")
    with open(temp_dir, 'w', newline='') as outcsv:
            writer = csv.writer(outcsv)
            writer.writerow(["Filename", "Sorted", "index"])
            writer.writerow(["testfile.jpg", "good", "0"])
            writer.writerow(["testfile2.jpg", "bad", "1"])
    return temp_dir