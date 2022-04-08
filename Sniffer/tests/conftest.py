import pytest
import shutil
import csv
import pandas as pd
import os


@pytest.fixture(scope="function")
def get_temp_images_dir(tmpdir_factory):
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
def get_temp_thumbnails_images_dir(tmpdir_factory):
    test_images_dir="./Sniffer/tests/test_data/good_images"
    temp_dir = tmpdir_factory.mktemp("thumbnails")
    for img in os.listdir(test_images_dir):
        temp_dest_path=temp_dir
        temp_dest_path = temp_dir.join(f"{img}")
        src_path=test_images_dir+os.sep+img
        shutil.copy(src_path,temp_dest_path)
    return temp_dir

@pytest.fixture(scope="function")
def get_temp_good_images_dir(tmpdir_factory):
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
def get_temp_empty_csv_dir(tmpdir_factory):
    temp_dir = tmpdir_factory.mktemp("csv")
    return temp_dir

@pytest.fixture(scope="session")
def get_temp_csv(tmpdir_factory):
    # dataframe = pd.DataFrame()
    temp_dir = tmpdir_factory.mktemp("csv").join("data.csv")
    with open(temp_dir, 'w', newline='') as outcsv:
            writer = csv.writer(outcsv)
            writer.writerow(["Filename", "Sorted", "index"])
            writer.writerow(["testfile.jpg", "good", "0"])
            writer.writerow(["testfile2.jpg", "bad", "1"])
    # dataframe.to_csv(temp_dir)
    return temp_dir

# @pytest.fixture(scope='session')
# def csv_file(tmpdir_factory):
#     N = 10
#     index = range(N)
#     even = [(n % 2 == 0) for n in range(N)]
#     dataframe = pd.DataFrame({'even': even}, index=index) 
#     filename = str(tmpdir_factory.mktemp('data').join('data.csv'))
#     dataframe.to_csv(filename)
#     return filename