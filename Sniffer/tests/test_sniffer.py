import os
import csv
import pandas as pd
from Sniffer import sniffer
import glob


def test_change_filename():
   # Verify change_filename appends _good to the filename
    sniffer_app = sniffer.SnifferClass()
    sorted_dir = os.getcwd() + os.sep + "test_dir"
    old_filename = "old_filename.jpg"
    sort_type = "good"
    new_filename_loc = sniffer_app.change_filename(old_filename, sort_type, sorted_dir)
    assert new_filename_loc == sorted_dir + os.sep + "old_filename_good.jpg"


def test_create_csv(get_temp_empty_csv_dir):
    # Verify that create_csv will create a csv when a csv_filename is given
    sniffer_app = sniffer.SnifferClass()
    csv_filename = "test.csv"
    result_path = sniffer_app.create_csv(get_temp_empty_csv_dir, csv_filename)
    expected_path = get_temp_empty_csv_dir + os.sep + csv_filename
    assert expected_path == result_path
    csv_filename = "test"
    result_path = sniffer_app.create_csv(get_temp_empty_csv_dir, csv_filename)
    expected_path = get_temp_empty_csv_dir + os.sep + csv_filename+".csv"
    assert expected_path == result_path


def test_create_csv_without_name(get_temp_empty_csv_dir):
    # Verify that create_csv will create a csv when a csv_filename is not given
    sniffer_app = sniffer.SnifferClass()
    result_path = sniffer_app.create_csv(csv_path=get_temp_empty_csv_dir)
    assert os.path.exists(result_path)


def test_delete_filename_from_csv_invalid_csv_file(get_temp_empty_csv_dir):
    # Verify that delete_filename_from_csv will not raise an error when the csv_file doesn't exist
    sniffer_app = sniffer.SnifferClass()
    sniffer_app.delete_filename_from_csv("fakefile.jpg", "fake_location")


def test_create_thumbnails(get_temp_thumbnails_images_dir, get_temp_populated_images_dir):
    """Verify thumnails get created for in the images directory"""
    sniffer_app = sniffer.SnifferClass()
    sniffer_app.thumbnails_path =str( get_temp_thumbnails_images_dir)
    images_list = glob.glob1(get_temp_populated_images_dir + os.sep, "*jpg")
    sniffer_app.create_thumbnails(str(get_temp_populated_images_dir),images_list)
    for photo in images_list:
        expected_thumbnail=sniffer_app.thumbnails_path+os.sep+photo
        assert os.path.exists(expected_thumbnail)


def test_create_thumbnails_dir_not_exist(get_temp_populated_images_dir):
    """Verify thumbnails get created for in the images directory when the thumbanils dir doesn't exist"""
    sniffer_app = sniffer.SnifferClass()
    sniffer_app.thumbnails_path =str(os.getcwd()+os.sep+"tmpthumbnail")
    images_list = glob.glob1(get_temp_populated_images_dir + os.sep, "*jpg")
    sniffer_app.create_thumbnails(str(get_temp_populated_images_dir),images_list)
    for photo in images_list:
        expected_thumbnail=sniffer_app.thumbnails_path+os.sep+photo
        assert os.path.exists(expected_thumbnail)     
    # Remove the directories once we are done testing
    if os.path.exists(sniffer_app.thumbnails_path):
          for file in glob.glob(sniffer_app.thumbnails_path + os.sep + "*jpg"):
                os.remove(file)
          os.rmdir(sniffer_app.thumbnails_path)
    
    


def test_delete_filename_from_csv(get_temp_csv):
    # Verify that delete_filename_from_csv will not raise an error when the csv_file doesn't exist
    sniffer_app = sniffer.SnifferClass()
    sniffer_app.delete_filename_from_csv("testfile.jpg", get_temp_csv)
    assert(os.path.exists(get_temp_csv))
    # delete_filename_from_csv should have deleted the 1st entry from the csv. The new 1st entry should be testfile2.jpg
    df = pd.read_csv(get_temp_csv)
    assert df.iloc[0]['Filename'] == 'testfile2.jpg'


def test_find_image(get_temp_images_mixed_exts_dir):
    sniffer_app = sniffer.SnifferClass()
    # Verify that find_image will not raise an error when the file doesn't exist
    assert sniffer_app.find_image(get_temp_images_mixed_exts_dir, "fake.jpg") is None
    # Verify that find_image will not raise an error when the file doesn't exist
    assert sniffer_app.find_image(get_temp_images_mixed_exts_dir, "fake") is None
    # Verify that find_image will not raise an error when the file_path doesn't exist
    sniffer_app.find_image("fakedir", "fake")
    # Verify that find_image will return the correct location when the image does exist
    expected_output = get_temp_images_mixed_exts_dir + os.sep + "img1.JPG"
    result = sniffer_app.find_image(get_temp_images_mixed_exts_dir, "img1.JPG")
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


def test_save_sorted_image_good(get_temp_valid_images_dir, get_temp_empty_good_images_dir):
    sniffer_app = sniffer.SnifferClass()
    # Set the good_images directory to the empty temp "good_images" directory for testing
    sniffer_app.good_images_path=str(get_temp_empty_good_images_dir)
    # Use conftest fixture to get a temporary directory called images with valid .jpgs
    jpg_list = glob.glob1(get_temp_valid_images_dir + os.sep, "*jpg")
    photo_loc =  str(get_temp_valid_images_dir)+ os.sep + jpg_list[0]
    sniffer_app.save_sorted_image(photo_loc,"good")
    new_jpg_name=os.path.splitext(jpg_list[0])[0] + "_good.jpg"
    expected_photo_loc=sniffer_app.good_images_path+ os.sep + new_jpg_name
    images_path_glob=str(sniffer_app.good_images_path) + os.sep +"*jpg"
    resulting_jpg_list= glob.glob(images_path_glob)
    actual_photo_loc=resulting_jpg_list[0]
    assert actual_photo_loc == expected_photo_loc

    
def test_save_sorted_image_bad(get_temp_valid_images_dir,get_temp_empty_bad_images_dir):    
    # Verify it saves to bad_images directory when sort_type="bad"
    sniffer_app = sniffer.SnifferClass()
    # Set the bad_images directory to the empty temp "bad_images" directory for testing
    sniffer_app.bad_images_path=str(get_temp_empty_bad_images_dir)
    # Use conftest fixture to get a temporary directory called images with valid .jpgs
    jpg_list = glob.glob1(get_temp_valid_images_dir + os.sep, "*jpg")
    photo_loc =  str(get_temp_valid_images_dir)+ os.sep + jpg_list[0]
    sniffer_app.save_sorted_image(photo_loc,"bad")
    new_jpg_name=os.path.splitext(jpg_list[0])[0] + "_bad.jpg"
    expected_photo_loc=sniffer_app.bad_images_path+ os.sep + new_jpg_name
    images_path_glob=str(sniffer_app.bad_images_path) + os.sep +"*jpg"
    resulting_jpg_list= glob.glob(images_path_glob)
    actual_photo_loc=resulting_jpg_list[0]
    assert actual_photo_loc == expected_photo_loc

def test_save_sorted_image_bad_dir_not_exist(get_temp_valid_images_dir):
    """Verify it creates to bad_images directory when it doesn't exist"""
    sniffer_app = sniffer.SnifferClass()
    bad_path=os.getcwd()+os.sep+"tmpbad"
    sniffer_app.bad_images_path=bad_path
     # Use conftest fixture to get a temporary images directory with valid .jpgs
    jpg_list = glob.glob1(get_temp_valid_images_dir + os.sep, "*jpg")
    photo_loc =  str(get_temp_valid_images_dir)+ os.sep + jpg_list[0]
    sniffer_app.save_sorted_image(photo_loc,"bad")
    new_jpg_name=os.path.splitext(jpg_list[0])[0] + "_bad.jpg"
    expected_photo_loc=sniffer_app.bad_images_path+ os.sep + new_jpg_name
    images_path_glob=str(sniffer_app.bad_images_path) + os.sep +"*jpg"
    resulting_jpg_list= glob.glob(images_path_glob)
    actual_photo_loc=resulting_jpg_list[0]
    assert actual_photo_loc == expected_photo_loc
    assert os.path.exists(bad_path)
    # Remove the directories once we are done testing
    if os.path.exists(bad_path):
          os.remove(actual_photo_loc)
          os.rmdir(bad_path)

def test_save_sorted_image_good_dir_not_exist(get_temp_valid_images_dir):
    """Verify it creates to good_images directory when it doesn't exist"""
    sniffer_app = sniffer.SnifferClass()
    good_path=os.getcwd()+os.sep+"tmpgood"
    sniffer_app.good_images_path=good_path
     # Use conftest fixture to get a temporary images directory with valid .jpgs
    jpg_list = glob.glob1(get_temp_valid_images_dir + os.sep, "*jpg")
    photo_loc =  str(get_temp_valid_images_dir)+ os.sep + jpg_list[0]
    sniffer_app.save_sorted_image(photo_loc,"good")
    new_jpg_name=os.path.splitext(jpg_list[0])[0] + "_good.jpg"
    expected_photo_loc=sniffer_app.good_images_path+ os.sep + new_jpg_name
    images_path_glob=str(sniffer_app.good_images_path) + os.sep +"*jpg"
    resulting_jpg_list= glob.glob(images_path_glob)
    actual_photo_loc=resulting_jpg_list[0]
    assert actual_photo_loc == expected_photo_loc
    assert os.path.exists(good_path)
    # Remove the directories once we are done testing
    if os.path.exists(good_path):
          os.remove(actual_photo_loc)
          os.rmdir(good_path)

def setup_handle_csv_choice(images_path, images_list, csv_file_location):
    sniffer_app = sniffer.SnifferClass()
    sniffer_app.images_path = str(images_path)
    sniffer_app.images_list= images_list
    sniffer_app.csv_file_location=csv_file_location
    sniffer_app.last_index_images_list = len(sniffer_app.images_list) - 1
    return sniffer_app

def test_handle_csv_choice_good( get_temp_populated_images_dir, get_temp_empty_csv_file ):
    """Verify quality control failure is triggered when empty photo_list =[]"""
    images_list = glob.glob1(get_temp_populated_images_dir + os.sep, "*jpg")
    sniffer_app=setup_handle_csv_choice(get_temp_populated_images_dir, images_list,get_temp_empty_csv_file )
    initial_index=0
    sniffer_app.image_index=initial_index
    sort_type="good"
    sniffer_app.handle_csv_choice(sort_type)
    # Assert all the buttons are enabled since the 0<=index <= last_index
    assert sniffer_app.yes_button.disabled == False
    assert sniffer_app.no_button.disabled == False
    assert sniffer_app.undo_button.disabled == False   
    assert sniffer_app.image_index==initial_index+1
    # Assert the image is in the csv file
    new_jpg_name=os.path.splitext(images_list[initial_index])[0] + ".jpg"
    dataframe=pd.read_csv(sniffer_app.csv_file_location)
    assert  new_jpg_name in dataframe['Filename'].values
    
def test_handle_csv_choice_good_last_index( get_temp_populated_images_dir, get_temp_empty_csv_file ):
    """Verify quality control failure is triggered when empty photo_list =[]"""
    images_list = glob.glob1(get_temp_populated_images_dir + os.sep, "*jpg")
    sniffer_app=setup_handle_csv_choice(get_temp_populated_images_dir, images_list,get_temp_empty_csv_file )
    initial_index=sniffer_app.last_index_images_list
    sniffer_app.image_index=initial_index
    sort_type="good"
    sniffer_app.handle_csv_choice(sort_type)
    # Assert undo button  enabled, yes & no buttons disabled, since the 0<=index <= last_index
    assert sniffer_app.yes_button.disabled == True
    assert sniffer_app.no_button.disabled == True
    assert sniffer_app.undo_button.disabled == False   
    assert sniffer_app.image_index==initial_index+1
    # Assert the image is in the csv file
    new_jpg_name=os.path.splitext(images_list[initial_index])[0] + ".jpg"
    dataframe=pd.read_csv(sniffer_app.csv_file_location)
    index = dataframe.loc[dataframe["Filename"] == new_jpg_name].index.values
    assert  new_jpg_name in dataframe['Filename'].values
    assert dataframe["Sorted"].iloc[index].values[0] == sort_type
    
    
def test_handle_csv_choice_bad( get_temp_populated_images_dir, get_temp_empty_csv_file ):
    """Verify quality control failure is triggered when empty photo_list =[]"""
    images_list = glob.glob1(get_temp_populated_images_dir + os.sep, "*jpg")
    sniffer_app=setup_handle_csv_choice(get_temp_populated_images_dir, images_list,get_temp_empty_csv_file )
    initial_index=0
    sniffer_app.image_index=initial_index
    sort_type="bad"
    sniffer_app.handle_csv_choice(sort_type)
    # Assert all the buttons are enabled since the 0<=index <= last_index
    assert sniffer_app.yes_button.disabled == False
    assert sniffer_app.no_button.disabled == False
    assert sniffer_app.undo_button.disabled == False   
    assert sniffer_app.image_index==initial_index+1
    # Assert the image is in the csv file
    new_jpg_name=os.path.splitext(images_list[initial_index])[0] + ".jpg"
    dataframe=pd.read_csv(sniffer_app.csv_file_location)
    index = dataframe.loc[dataframe["Filename"] == new_jpg_name].index.values
    assert  new_jpg_name in dataframe['Filename'].values
    assert dataframe["Sorted"].iloc[index].values[0] == sort_type
    
def test_handle_csv_choice_bad_last_index( get_temp_populated_images_dir, get_temp_empty_csv_file ):
    """Verify quality control failure is triggered when empty photo_list =[]"""
    images_list = glob.glob1(get_temp_populated_images_dir + os.sep, "*jpg")
    sniffer_app=setup_handle_csv_choice(get_temp_populated_images_dir, images_list,get_temp_empty_csv_file )
    initial_index=sniffer_app.last_index_images_list
    sniffer_app.image_index=initial_index
    sort_type="bad"
    sniffer_app.handle_csv_choice(sort_type)
    # Assert undo button  enabled, yes & no buttons disabled, since the 0<=index <= last_index
    assert sniffer_app.yes_button.disabled == True
    assert sniffer_app.no_button.disabled == True
    assert sniffer_app.undo_button.disabled == False   
    assert sniffer_app.image_index==initial_index+1
    # Assert the image is in the csv file
    new_jpg_name=os.path.splitext(images_list[initial_index])[0] + ".jpg"
    dataframe=pd.read_csv(sniffer_app.csv_file_location)
    index = dataframe.loc[dataframe["Filename"] == new_jpg_name].index.values
    assert  new_jpg_name in dataframe['Filename'].values
    assert dataframe["Sorted"].iloc[index].values[0] == sort_type

    
def setup_handle_file_choice(bad_images_path,good_images_path,images_path,images_list):
    sniffer_app = sniffer.SnifferClass()
    sniffer_app.bad_images_path = str(bad_images_path)
    sniffer_app.good_images_path = str(good_images_path)
    sniffer_app.images_path = str(images_path)
    sniffer_app.images_list= images_list
    sniffer_app.last_index_images_list = len(sniffer_app.images_list) - 1
    return sniffer_app
    
def test_handle_file_choice_good( get_temp_populated_images_dir, get_temp_empty_good_images_dir,get_temp_empty_bad_images_dir ):
    """Verify quality control failure is triggered when empty photo_list =[]"""
    images_list = glob.glob1(get_temp_populated_images_dir + os.sep, "*jpg")
    sniffer_app=setup_handle_file_choice(get_temp_empty_bad_images_dir,get_temp_empty_good_images_dir,get_temp_populated_images_dir,images_list )
    initial_index=0
    sniffer_app.image_index=initial_index
    sniffer_app.handle_file_choice("good")
    # Assert all the buttons are enabled since the 0<=index <= last_index
    assert sniffer_app.yes_button.disabled == False
    assert sniffer_app.no_button.disabled == False
    assert sniffer_app.undo_button.disabled == False   
    assert sniffer_app.image_index==initial_index+1
    # Assert the image got put in the good images directory
    new_jpg_name=os.path.splitext(images_list[initial_index])[0] + "_good.jpg"
    expected_photo_loc=sniffer_app.good_images_path+ os.sep + new_jpg_name
    # Get the images in sniffer's good images directory.
    images_path_glob=str(sniffer_app.good_images_path) + os.sep +"*jpg"
    actual_jpg_list= glob.glob(images_path_glob)
    actual_photo_loc=actual_jpg_list[0]
    assert actual_photo_loc == expected_photo_loc

def test_handle_file_choice_bad( get_temp_populated_images_dir, get_temp_empty_bad_images_dir,get_temp_empty_good_images_dir ):
    """Verify quality control failure is triggered when empty photo_list =[]"""
    images_list = glob.glob1(get_temp_populated_images_dir + os.sep, "*jpg")
    sniffer_app=setup_handle_file_choice(get_temp_empty_bad_images_dir,get_temp_empty_good_images_dir,get_temp_populated_images_dir,images_list )
    initial_index=0
    sniffer_app.image_index=initial_index
    sniffer_app.handle_file_choice("bad")
    # Assert all the buttons are enabled since the 0<=index <= last_index
    assert sniffer_app.yes_button.disabled == False
    assert sniffer_app.no_button.disabled == False
    assert sniffer_app.undo_button.disabled == False   
    assert sniffer_app.image_index==initial_index+1
    # Assert the image got put in the bad images directory
    new_jpg_name=os.path.splitext(images_list[initial_index])[0] + "_bad.jpg"
    expected_photo_loc=sniffer_app.bad_images_path+ os.sep + new_jpg_name
    # Get the images in sniffer's bad images directory.
    images_path_glob=str(sniffer_app.bad_images_path) + os.sep +"*jpg"
    actual_jpg_list= glob.glob(images_path_glob)
    actual_photo_loc=actual_jpg_list[0]
    assert actual_photo_loc == expected_photo_loc
    
def test_handle_file_choice_bad_last_index( get_temp_populated_images_dir, get_temp_empty_bad_images_dir,get_temp_empty_good_images_dir ):
    """Verify quality control failure is triggered when empty photo_list =[]"""
    images_list = glob.glob1(get_temp_populated_images_dir + os.sep, "*jpg")
    sniffer_app=setup_handle_file_choice(get_temp_empty_bad_images_dir,get_temp_empty_good_images_dir,get_temp_populated_images_dir,images_list )
    initial_index=sniffer_app.last_index_images_list
    sniffer_app.image_index=initial_index
    sniffer_app.handle_file_choice("bad")
    # Assert undo button  enabled, yes & no buttons disabled, since the 0<=index <= last_index
    assert sniffer_app.yes_button.disabled == True
    assert sniffer_app.no_button.disabled == True
    assert sniffer_app.undo_button.disabled == False   
    assert sniffer_app.image_index==initial_index+1
    # Assert the image got put in the bad images directory
    new_jpg_name=os.path.splitext(images_list[initial_index])[0] + "_bad.jpg"
    expected_photo_loc=sniffer_app.bad_images_path+ os.sep + new_jpg_name
    # Get the images in sniffer's bad images directory.
    images_path_glob=str(sniffer_app.bad_images_path) + os.sep +new_jpg_name
    actual_jpg_list= glob.glob(images_path_glob)
    actual_photo_loc=actual_jpg_list[0]
    assert actual_photo_loc == expected_photo_loc
    
def test_handle_file_choice_good_last_index( get_temp_populated_images_dir, get_temp_empty_bad_images_dir,get_temp_empty_good_images_dir ):
    """Verify quality control failure is triggered when empty photo_list =[]"""
    images_list = glob.glob1(get_temp_populated_images_dir + os.sep, "*jpg")
    sniffer_app=setup_handle_file_choice(get_temp_empty_bad_images_dir,get_temp_empty_good_images_dir,get_temp_populated_images_dir,images_list )
    initial_index=sniffer_app.last_index_images_list
    sniffer_app.image_index=initial_index
    sniffer_app.handle_file_choice("good")
    # Assert undo button  enabled, yes & no buttons disabled, since the 0<=index <= last_index
    assert sniffer_app.yes_button.disabled == True
    assert sniffer_app.no_button.disabled == True
    assert sniffer_app.undo_button.disabled == False   
    assert sniffer_app.image_index==initial_index+1
    # Assert the image got put in the good images directory
    new_jpg_name=os.path.splitext(images_list[initial_index])[0] + "_good.jpg"
    expected_photo_loc=sniffer_app.good_images_path+ os.sep + new_jpg_name
    # Get the images in sniffer's good images directory.
    images_path_glob=str(sniffer_app.good_images_path) + os.sep +new_jpg_name
    actual_jpg_list= glob.glob(images_path_glob)
    actual_photo_loc=actual_jpg_list[0]
    assert actual_photo_loc == expected_photo_loc
    


def test_handle_file_choice_bad_input():
    """Verify quality control failure is triggered when empty photo_list =[]"""      
    sniffer_app = sniffer.SnifferClass()
    sniffer_app.images_list=[]
    sniffer_app.handle_file_choice("good")
    assert sniffer_app.yes_button.disabled == True
    assert sniffer_app.no_button.disabled == True
    assert sniffer_app.undo_button.disabled == True
    
       
def test_replace_ext(get_temp_images_mixed_exts_dir):
    # Verify the extensions .JPG .jpeg get replaced by jpg
    sniffer_app = sniffer.SnifferClass()
    old_ext = ["JPG", "jpeg"]
    new_ext = ".jpg"
    sniffer_app.replace_ext(old_ext, new_ext, images_path=get_temp_images_mixed_exts_dir)
    for file in os.listdir(get_temp_images_mixed_exts_dir):
        if os.path.splitext(file)[1] != ".png":
            assert os.path.splitext(file)[1] == ".jpg"


def test_sniffer_initial_button_state():
    # Verify yes, no and undo buttons should be disabled when Sniffer starts
    sniffer_app = sniffer.SnifferClass()
    assert sniffer_app.yes_button.disabled == True
    assert sniffer_app.no_button.disabled == True
    assert sniffer_app.undo_button.disabled == True


def test_quality_control_bad_directory():
   sniffer_app = sniffer.SnifferClass()
   # Verify quality_control returns False when a directory that doesn't exist is given
   result=sniffer_app.quality_control("fakedir",[],sniffer_app.bad_images_path,sniffer_app.good_images_path)
   assert result == False

def test_quality_control_missing_directories(get_temp_images_mixed_exts_dir):
   sniffer_app = sniffer.SnifferClass()
   # Verify quality_control creates good and bad directories when they don't exist
   good_path=os.getcwd() + os.sep +"tmpgood"
   bad_path=os.getcwd()+os.sep+"tmpbad"
   result=sniffer_app.quality_control(get_temp_images_mixed_exts_dir,[4,5],bad_path,good_path)
   assert os.path.exists(good_path)
   assert os.path.exists(bad_path)
   assert result ==True
   # Remove the directories once we are done testing
   if os.path.exists(good_path):
          os.rmdir(good_path)
   if os.path.exists(bad_path):
          os.rmdir(bad_path)
          
def test_quality_control_empty_images_list(get_temp_images_mixed_exts_dir,get_temp_bad_images_dir,get_temp_good_images_dir):
   sniffer_app = sniffer.SnifferClass()
   # Verify quality_control returns False when an empty photos list is given
   result=sniffer_app.quality_control(get_temp_images_mixed_exts_dir,[],get_temp_bad_images_dir,get_temp_good_images_dir)
   assert result ==False

def test_quality_control_valid_inputs(get_temp_images_mixed_exts_dir,get_temp_bad_images_dir,get_temp_good_images_dir):
   sniffer_app = sniffer.SnifferClass()
   # Verify quality_control returns true for valid inputs
   result=sniffer_app.quality_control(get_temp_images_mixed_exts_dir,[5,4],get_temp_bad_images_dir,get_temp_good_images_dir)
   assert result ==True
       

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


def test_get_image_index_text():
    # get_image_index_text() returns StaticText access the value and verify it == photo index
    sniffer_app = sniffer.SnifferClass()
    sniffer_app.image_index = 2
    assert sniffer_app.get_image_index_text().value == "Current Index: # 2"


def test_modify_buttons_state():
    # yes, no and undo buttons should be enabled when False is passed modify_buttons_state
    sniffer_app = sniffer.SnifferClass()
    sniffer_app.modify_buttons_state(False)
    assert sniffer_app.yes_button.disabled == False
    assert sniffer_app.no_button.disabled == False
    assert sniffer_app.undo_button.disabled == False
    
def test_get_jpg_panel(get_temp_populated_images_dir):
   # @TODO need to test when 0<= image_index <= last_index
   sniffer_app = sniffer.SnifferClass()
   # Verify sniffer displays loading image when its loaded (index=-1)
   sniffer_app.image_index = -1
   result_jpg_panel=sniffer_app.get_jpg_panel()
   loading_jpg = os.getcwd() + os.sep + "assets" + os.sep + "new_loading_sniffer.jpg"
   assert result_jpg_panel.object == loading_jpg
   # Verify sniffer displays loading animation when index=-2
   sniffer_app.image_index = -2
   result_jpg_panel=sniffer_app.get_jpg_panel()
   assert result_jpg_panel.loading == True
   # Verify sniffer displays loading animation when index > last index
   sniffer_app.image_index = sniffer_app.last_index_images_list +5
   last_jpg = os.getcwd() + os.sep + "assets" + os.sep + "new_sniffer_done.jpg"
   result_jpg_panel=sniffer_app.get_jpg_panel()
   assert result_jpg_panel.object == last_jpg
   # Verify sniffer displays image[0] when index = 0
   sniffer_app.images_list=glob.glob1(get_temp_populated_images_dir + os.sep, "*jpg")
   initial_index=0
   sniffer_app.image_index=initial_index
   result_jpg_panel=sniffer_app.get_jpg_panel()
   new_jpg_name=sniffer_app.images_list[initial_index]
   print(f"new_jpg_name: {new_jpg_name}")
   expected_photo_loc=sniffer_app.images_path+ os.sep + new_jpg_name
   print(f"expected_photo_loc: {expected_photo_loc}")
   assert result_jpg_panel.object == expected_photo_loc
   # Verify sniffer displays last image when index = last_index
   sniffer_app.images_list=glob.glob1(get_temp_populated_images_dir + os.sep, "*jpg")
   sniffer_app.last_index_images_list=len(sniffer_app.images_list)-1
   initial_index=sniffer_app.last_index_images_list
   sniffer_app.image_index=sniffer_app.last_index_images_list
   result_jpg_panel=sniffer_app.get_jpg_panel()
   new_jpg_name=sniffer_app.images_list[initial_index]
   print(f"new_jpg_name: {new_jpg_name}")
   expected_photo_loc=sniffer_app.images_path+ os.sep + new_jpg_name
   print(f"expected_photo_loc: {expected_photo_loc}")
   assert result_jpg_panel.object == expected_photo_loc
   
def test_get_progress_bar():
   sniffer_app = sniffer.SnifferClass()
   # Verify progress bar's value =0 when sniffer loads (index =-1)
   sniffer_app.image_index = -1
   result_progress_bar=sniffer_app.get_progress_bar()
   assert result_progress_bar.value == 0
   # Verify progress bar's value = index  when index <= last index
   sniffer_app.image_index = 0
   result_progress_bar=sniffer_app.get_progress_bar()
   assert result_progress_bar.value == 0
   sniffer_app.image_index = 1
   result_progress_bar=sniffer_app.get_progress_bar()
   assert result_progress_bar.value == 1
   # Verify progress bar's value = last_index_images_list when index > last index
   sniffer_app.image_index = sniffer_app.last_index_images_list +5
   result_progress_bar=sniffer_app.get_progress_bar()
   assert result_progress_bar.value == sniffer_app.last_index_images_list
