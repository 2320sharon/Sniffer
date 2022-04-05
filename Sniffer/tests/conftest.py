import pytest
import shutil
import os

# @pytest.fixture
# def get_sample_images():
#     test_images_dir="./Sniffer/tests/test_data"
#     return test_images_dir


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