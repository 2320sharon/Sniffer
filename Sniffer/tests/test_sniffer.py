import os
import pandas as pd
from Sniffer import sniffer


def test_change_filename():
   # Verify change_filename appends _good to the filename
    sniffer_app = sniffer.SnifferClass()
    sorted_dir = os.getcwd() + os.sep + "test_dir"
    old_filename = "old_filename.jpg"
    sort_type = "good"
    new_filename_loc = sniffer_app.change_filename(old_filename, sort_type, sorted_dir)
    assert new_filename_loc == sorted_dir + os.sep + "old_filename_good.jpg"


def test_create_csv(get_temp_dir):
    # Verify that create_csv will create a csv when a csv_filename is given
    sniffer_app = sniffer.SnifferClass()
    csv_filename = "test.csv"
    result_path = sniffer_app.create_csv(csv_path=get_temp_dir, csv_filename="test.csv")
    expected_path = get_temp_dir + os.sep + csv_filename
    assert expected_path == result_path


def test_create_csv_without_name(get_temp_dir):
    # Verify that create_csv will create a csv when a csv_filename is not given
    sniffer_app = sniffer.SnifferClass()
    result_path = sniffer_app.create_csv(csv_path=get_temp_dir)
    assert os.path.exists(result_path)


def test_delete_filename_from_csv_invalid_csv_file(get_temp_dir):
    # Verify that delete_filename_from_csv will not raise an error when the csv_file doesn't exist
    sniffer_app = sniffer.SnifferClass()
    sniffer_app.delete_filename_from_csv("fakefile.jpg", "fake_location")


def test_delete_filename_from_csv(get_temp_csv):
    # Verify that delete_filename_from_csv will not raise an error when the csv_file doesn't exist
    sniffer_app = sniffer.SnifferClass()
    sniffer_app.delete_filename_from_csv("testfile.jpg", get_temp_csv)
    assert(os.path.exists(get_temp_csv))
    # delete_filename_from_csv should have deleted the 1st entry from the csv. The new 1st entry should be testfile2.jpg
    df = pd.read_csv(get_temp_csv)
    assert df.iloc[0]['Filename'] == 'testfile2.jpg'


def test_find_image(get_temp_images_dir):
    sniffer_app = sniffer.SnifferClass()
    # Verify that find_image will not raise an error when the file doesn't exist
    assert sniffer_app.find_image(get_temp_images_dir, "fake.jpg") is None
    # Verify that find_image will not raise an error when the file doesn't exist
    assert sniffer_app.find_image(get_temp_images_dir, "fake") is None
    # Verify that find_image will not raise an error when the file_path doesn't exist
    sniffer_app.find_image("fakedir", "fake")
    # Verify that find_image will return the correct location when the image does exist
    expected_output = get_temp_images_dir + os.sep + "img1.JPG"
    result = sniffer_app.find_image(get_temp_images_dir, "img1.JPG")
    assert expected_output == result
    

def test_delete_image(get_temp_bad_images_dir,get_temp_good_images_dir):
      sniffer_app = sniffer.SnifferClass()
      # Verify delete_image won't raise an error when an invalid file is given
      sniffer_app.delete_image("invalid.jpg",get_temp_bad_images_dir,get_temp_good_images_dir)
      
      # Verify delete_image deletes a img2.jpg from the good_images directory
      sniffer_app.delete_image("img2.jpg",get_temp_bad_images_dir,get_temp_good_images_dir)
      deleted_file_loc=get_temp_good_images_dir+os.sep+"img2.jpg"
      
      # Verify delete_image deletes a img1.jpg from the bad_images directory
      sniffer_app.delete_image("img1.jpg",get_temp_bad_images_dir,get_temp_good_images_dir)
      deleted_file_loc=get_temp_good_images_dir+os.sep+"img1.jpg"
      assert not os.path.exists(deleted_file_loc)
      
       


def test_replace_ext(get_temp_images_dir):
    # Verify the extensions .JPG .jpeg get replaced by jpg
    sniffer_app = sniffer.SnifferClass()
    old_ext = ["JPG", "jpeg"]
    new_ext = ".jpg"
    sniffer_app.replace_ext(old_ext, new_ext, images_path=get_temp_images_dir)
    for file in os.listdir(get_temp_images_dir):
        if os.path.splitext(file)[1] != ".png":
            assert os.path.splitext(file)[1] == ".jpg"


def test_sniffer_initial_button_state():
    # Verify yes, no and undo buttons should be disabled when Sniffer starts
    sniffer_app = sniffer.SnifferClass()
    assert sniffer_app.yes_button.disabled
    assert sniffer_app.no_button.disabled
    assert sniffer_app.undo_button.disabled


def test_quality_control_failure():
    # When sniffer starts yes,no and undo are disabled, enable them, and
    # verify they are disabled by quality_control_failure()
    sniffer_app = sniffer.SnifferClass()
    sniffer_app.yes_button.disabled = False
    sniffer_app.no_button.disabled = False
    sniffer_app.undo_button.disabled = False
    sniffer_app.quality_control_failure()
    assert sniffer_app.yes_button.disabled
    assert sniffer_app.no_button.disabled
    assert sniffer_app.undo_button.disabled


def test_handle_all_images_processed():
    # Enable yes and no buttons and verify they are disabled by handle_all_images_processed()
    sniffer_app = sniffer.SnifferClass()
    sniffer_app.yes_button.disabled = False
    sniffer_app.no_button.disabled = False
    sniffer_app.handle_all_images_processed()
    assert sniffer_app.yes_button.disabled
    assert sniffer_app.no_button.disabled


def test_get_photo_index_text():
    # get_photo_index_text() returns StaticText access the value and verify it == photo index
    sniffer_app = sniffer.SnifferClass()
    sniffer_app.photo_index = 2
    assert sniffer_app.get_photo_index_text().value == "Current Index: # 2"


def test_modify_buttons_state():
    # yes, no and undo buttons should be enabled when False is passed modify_buttons_state
    sniffer_app = sniffer.SnifferClass()
    sniffer_app.modify_buttons_state(False)
    assert sniffer_app.yes_button.disabled == False
    assert sniffer_app.no_button.disabled == False
    assert sniffer_app.undo_button.disabled == False
    
def test_get_jpg_panel():
       
   sniffer_app = sniffer.SnifferClass()
   # Verify sniffer displays loading image when its loaded (index=-1)
   sniffer_app.photo_index = -1
   result_jpg_panel=sniffer_app.get_jpg_panel()
   loading_jpg = os.getcwd() + os.sep + "assets" + os.sep + "new_loading_sniffer.jpg"
   assert result_jpg_panel.object == loading_jpg
   # sniffer_app.photo_index = -2
   
