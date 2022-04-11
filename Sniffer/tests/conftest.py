import pytest
import shutil
import csv
import pandas as pd
import os
import glob
from Sniffer import sniffer

# Fixtures for the images directory (START)
# --------------------------------------------


@pytest.fixture(scope="function")
def tmp_fake_dir(tmpdir_factory):
    """Creates temp directory that doesn't exist"""
    temp_dir = tmpdir_factory.mktemp("images").join("fake_dir")
    return temp_dir


@pytest.fixture(scope="function")
def temp_images_mixed_extensions(tmpdir_factory):
    """Creates temp images directory with .jpg .jeg and .png files"""
    test_images_dir = "./Sniffer/tests/test_data/images"
    temp_dir = tmpdir_factory.mktemp("images")
    for img in os.listdir(test_images_dir):
        temp_dest_path = temp_dir
        temp_dest_path = temp_dir.join(f"{img}")
        src_path = test_images_dir + os.sep + img
        print(src_path)
        shutil.copy(src_path, temp_dest_path)
    return temp_dir


@pytest.fixture(scope="function")
def temp_images_from_good_images(tmpdir_factory):
    """Creates temp images directory with images from test_data/good_images """
    test_images_dir = "./Sniffer/tests/test_data/good_images"
    temp_dir = tmpdir_factory.mktemp("images")
    for img in os.listdir(test_images_dir):
        temp_dest_path = temp_dir
        temp_dest_path = temp_dir.join(f"{img}")
        src_path = test_images_dir + os.sep + img
        shutil.copy(src_path, temp_dest_path)
    return temp_dir


@pytest.fixture(scope="function")
def temp_populated_images(tmpdir_factory):
    """Creates temp images directory with images from test_data/bad_images """
    test_images_dir = "./Sniffer/tests/test_data/bad_images"
    temp_dir = tmpdir_factory.mktemp("images")
    for img in os.listdir(test_images_dir):
        temp_dest_path = temp_dir
        temp_dest_path = temp_dir.join(f"{img}")
        src_path = test_images_dir + os.sep + img
        shutil.copy(src_path, temp_dest_path)
    return temp_dir

# Fixtures for the images directory (END)
# --------------------------------------------

# Fixtures for the thumbnails directory (START)
# --------------------------------------------


@pytest.fixture(scope="function")
def empty_thumbnails_dir(tmpdir_factory):
    """Creates temp empty thumbnails directory"""
    temp_dir = tmpdir_factory.mktemp("thumbnails")
    return temp_dir


@pytest.fixture(scope="function")
def temp_good_thumbnails(tmpdir_factory):
    """Creates temp thumbnails directory from the test_data/good_images"""
    test_images_dir = "./Sniffer/tests/test_data/good_images"
    temp_dir = tmpdir_factory.mktemp("thumbnails")
    for img in os.listdir(test_images_dir):
        temp_dest_path = temp_dir
        temp_dest_path = temp_dir.join(f"{img}")
        src_path = test_images_dir + os.sep + img
        shutil.copy(src_path, temp_dest_path)
    return temp_dir

# Fixtures for the thumbnails directory (END)
# --------------------------------------------


# Fixtures for the good_images directory (START)
# --------------------------------------------

@pytest.fixture(scope="function")
def temp_empty_good_images(tmpdir_factory):
    temp_dir = tmpdir_factory.mktemp("good_images")
    return temp_dir


@pytest.fixture(scope="function")
def temp_good_images(tmpdir_factory):
    test_images_dir = "./Sniffer/tests/test_data/good_images"
    temp_dir = tmpdir_factory.mktemp("good_images")
    for img in os.listdir(test_images_dir):
        temp_dest_path = temp_dir
        temp_dest_path = temp_dir.join(f"{img}")
        src_path = test_images_dir + os.sep + img
        shutil.copy(src_path, temp_dest_path)
    return temp_dir


# Fixtures for the good_images directory (END)
# --------------------------------------------

# Fixtures for the bad_images directory (START)
# --------------------------------------------

@pytest.fixture(scope="function")
def temp_empty_bad_images(tmpdir_factory):
    temp_dir = tmpdir_factory.mktemp("bad_images")
    return temp_dir


@pytest.fixture(scope="function")
def temp_bad_images(tmpdir_factory):
    """Creates temp bad_images directory with images from test_data/bad_images"""
    test_images_dir = "./Sniffer/tests/test_data/bad_images"
    temp_dir = tmpdir_factory.mktemp("bad_images")
    for img in os.listdir(test_images_dir):
        temp_dest_path = temp_dir
        temp_dest_path = temp_dir.join(f"{img}")
        src_path = test_images_dir + os.sep + img
        shutil.copy(src_path, temp_dest_path)
    return temp_dir

# Fixtures for the bad_images directory (END)
# --------------------------------------------

# Fixtures for the CSV file location (START)
# --------------------------------------------


@pytest.fixture(scope="function")
def temp_empty_csv(tmpdir_factory):
    """ Creates an empty csv file with only the column names"""
    temp_dir = tmpdir_factory.mktemp("csv").join("data.csv")
    with open(temp_dir, 'w', newline='') as outcsv:
        writer = csv.writer(outcsv)
        writer.writerow(["Filename", "Sorted", "index"])
    return temp_dir


@pytest.fixture(scope="function")
def temp_populated_csv(tmpdir_factory, temp_populated_images):
    """ Creates  csv file with 1st image from test_data/good labeled as good """
    images_list = glob.glob1(temp_populated_images, "*jpg")
    temp_dir = tmpdir_factory.mktemp("csv").join("data.csv")
    with open(temp_dir, 'w', newline='') as outcsv:
        writer = csv.writer(outcsv)
        writer.writerow(["Filename", "Sorted", "index"])
        writer.writerow([images_list[0], "good", "0"])
    return temp_dir


@pytest.fixture(scope="session")
def temp_csv_multiple_entries(tmpdir_factory):
    """ Creates a csv file with multiple hardcoded entries"""
    temp_dir = tmpdir_factory.mktemp("csv").join("data.csv")
    with open(temp_dir, 'w', newline='') as outcsv:
        writer = csv.writer(outcsv)
        writer.writerow(["Filename", "Sorted", "index"])
        writer.writerow(["testfile.jpg", "good", "0"])
        writer.writerow(["testfile2.jpg", "bad", "1"])
    return temp_dir

# Fixtures for the CSV file location (END)
# --------------------------------------------
