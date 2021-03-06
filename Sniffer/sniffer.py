import shutil
import os
import glob
from datetime import datetime
from PIL import Image
import csv
import pandas as pd
import panel as pn
import param


class SnifferClass(param.Parameterized):
    image_index = param.Integer(0)

    # Widgets
    thumbnail_button = pn.widgets.Button(name='THUMBNAIL', button_type='success', width=30, margin=(5, 50))
    image_button = pn.widgets.Button(name='IMAGE', button_type='success', width=30, margin=(5, 50))
    yes_button = pn.widgets.Button(name='YES', button_type='success', width=50, margin=(10, 20))
    no_button = pn.widgets.Button(name='NO', button_type='danger', width=50, margin=(10, 20))
    undo_button = pn.widgets.Button(name='UNDO', button_type='warning', width=35, margin=(10, 20))
    # Mode selector
    radio_group = pn.widgets.RadioButtonGroup(
        name='Radio Button Group', options=['CSV Mode', 'File Mode'], margin=(40, 1))
    # Informational text
    text = pn.widgets.StaticText(margin=(5, 120))
    image_index_text = pn.widgets.StaticText(margin=(5, 120))

    def __init__(self, **params):
        super().__init__(**params)
        # initialize the photo index to -1 to indicate no thumbnails have been loaded yet
        self.image_index = -1
        # Disable Thumbnail mode by default and use original images
        self.thumbnail_mode = False
        # Variables for images
        self.csv_file_location = ""
        self.images_path = os.getcwd() + os.sep + "images"
        # fix issues with the file extensions by converting to lowercase .jpg
        self.replace_ext(["JPG", "jpeg"], ".jpg")
        self.images_list = glob.glob1(self.images_path, "*jpg")
        # Location of the thumbnails directory
        self.thumbnails_path = os.getcwd() + os.sep + "thumbnails"
        self.last_index_images_list = len(self.images_list) - 1
        self.good_images_path = os.getcwd() + os.sep + "good_images"
        self.bad_images_path = os.getcwd() + os.sep + "bad_images"
        # initial_photo will be the first image from the user dataset to be display in the jpg panel
        if self.quality_control(
                self.images_path,
                self.images_list,
                self.bad_images_path,
                self.good_images_path) == False:
            raise FileNotFoundError(f"{self.images_path} contains no jpgs")

        # Disable all buttons except thumbnail and image buttons
        self.modify_buttons_state(True)
        self.text.value = "Click THUMBNAIL to create thumbnails for all images or IMAGE to use the original images.\
        \n WARNING: If you choose IMAGE and your images are too large switching images may take longer. "
        self.loading_jpg = os.getcwd() + os.sep + "assets" + os.sep + "new_loading_sniffer.jpg"
        self.jpg_panel = pn.pane.JPG(self.loading_jpg, width=450, height=450, sizing_mode='fixed', margin=(0, 25))
        self.thumbnail_button.on_click(self.thumbnail_button_clicked)
        self.image_button.on_click(self.image_button_clicked)
        self.yes_button.on_click(self.yes_button_clicked)
        self.no_button.on_click(self.no_button_clicked)
        self.undo_button.on_click(self.undo_button_clicked)

    def replace_ext(self, old_exts: list, new_ext: str, images_path=os.getcwd() + os.sep + "images"):
        """ Converts all images of the old ext(short for extension) to the new ext(extension) in the images_path \

        Args:
            old_ext (str): the old file extension to be replaced
            new_ext (str): the new file extension that replaces the old file extension

        Example:
            replace_ext(".JPG",".jpg")
                replaces all files with the .JPG extension with the .jpg extension

        """
        ext_list = []
        for ext in old_exts:
            searchable_path = str(images_path) + os.sep + "*." + ext
            ext_list.extend(glob.glob(searchable_path))
        for JPG in ext_list:
            src = JPG
            dest = os.path.splitext(JPG)[:-1]
            # convert the tuple to a string
            new_dest = "".join(map(str, dest))
            # append the new file extension to the new filename
            new_dest = new_dest + new_ext
            os.rename(src, new_dest)

    def create_thumbnails(self, images_path: str, images_list: list):
        """Create thumbnails of size 500x500 for each photo at the images_path
            in images_list. Save the thumbnails to the thumbnails directory.

        Args:
            images_path (str): location of the images directory
            images_list (list): list of photo names
        """
        if not os.path.exists(self.thumbnails_path):
            os.mkdir(self.thumbnails_path)
        elif os.path.exists(self.thumbnails_path):
            # remove old files in thumbnail directory
            for file in os.listdir(self.thumbnails_path):
                os.remove(os.path.join(self.thumbnails_path, file))
        # Create thumbnails for each photo in photos list
        for photo in images_list:
            photo_loc = images_path + os.sep + photo
            # resize the thumbnails and save them to thumbnails directory
            im = Image.open(photo_loc)
            MAX_SIZE = (500, 500)
            im.thumbnail(MAX_SIZE)
            thumbnail_loc = self.thumbnails_path + os.sep + photo
            im.save(thumbnail_loc)

    def get_jpg_panel(self):
        """Return a jpg panel with the current jpg depending on the image_index.

        Returns Sniffer complete jpg if the image_index is greater than the last_index_images_list.
        Returns Sniffer loading jpg if teh index is -1 or -2.
        Returns the jpg at the location of the image_index if the image_index is <= last_index_images_list.

        Returns:
            panel.pane.image.JPG: self.jpg_panel
        """
        # Index = -1 means Sniffer just loaded
        if self.image_index == -1:
            self.jpg_panel = pn.pane.JPG(self.loading_jpg, width=450, height=450, sizing_mode='fixed', margin=(0, 25))
        elif self.image_index == -2:
            # Index = -2 it means the THUMBNAIL button was pressed
            self.jpg_panel = pn.pane.JPG(self.loading_jpg, width=450, height=450, sizing_mode='fixed', margin=(0, 25))
            self.jpg_panel.loading = True
        elif self.image_index <= self.last_index_images_list:
            self.jpg_panel.loading = False
            self.undo_button.disabled = False
            if self.thumbnail_mode:
                new_photo = self.thumbnails_path + os.sep + self.thumbnails_list[self.image_index]
            elif self.thumbnail_mode == False:
                new_photo = self.images_path + os.sep + self.images_list[self.image_index]

            self.jpg_panel.object = new_photo
        elif self.image_index > self.last_index_images_list:
            last_jpg = os.getcwd() + os.sep + "assets" + os.sep + "new_sniffer_done.jpg"
            self.jpg_panel.object = last_jpg
        return self.jpg_panel

    def get_image_index_text(self):
        if self.image_index >= 0:
            self.image_index_text.value = f"Current Index: # {self.image_index}"
            return self.image_index_text

    def get_progress_bar(self):
        """Returns the progress bar that shows how far the image_index is through the images_list
        Returns:
            panel.widgets.indicators.Progress: self.progress_bar
        """
        if self.image_index < 0:
            self.progress_bar = pn.indicators.Progress(
                name='Progress Bar',
                margin=(
                    10,
                    120),
                value=0,
                active=True,
                max=self.last_index_images_list,
                bar_color='info',
                width=200)
        elif self.image_index <= self.last_index_images_list:
            self.progress_bar.value = self.image_index
            self.progress_bar.bar_color = 'info'
        elif self.image_index > self.last_index_images_list:
            self.progress_bar.value = self.last_index_images_list
            self.progress_bar.bar_color = 'success'
        return self.progress_bar

    def handle_all_images_processed(self):
        """ Disables the Yes and No buttons and displays all images have been processed"""
        self.text.value = "All images have been processed."
        self.yes_button.disabled = True
        self.no_button.disabled = True

    def quality_control_failure(self):
        """ Quality control has failed disable all buttons and display error message """
        self.modify_buttons_state(True)
        self.text.value = f"ERROR: There are no images in\n{self.images_path}"

    def quality_control(self, images_path: str, images_list: list, bad_images_path: str, good_images_path: str):
        """Checks if the images_path exists and that it contains .jpgs. Returns false if either check fails

        Args:
            images_path (str): Images directory containing images to be sorted
            images_list (list): List of image names to be sorted

        Returns:
            True: images_path contained only .jpgs
            False: images_path contained files other than .jpgs
        """
        if not os.path.isdir(images_path):
            return False
        if not os.path.exists(bad_images_path):
            os.mkdir(bad_images_path)
        if not os.path.exists(good_images_path):
            os.mkdir(good_images_path)
        if len(images_list) == 0:
            return False
    #         If neither of these return false it means quality control passed
        return True

    def create_csv(self, csv_path: str = os.getcwd(), csv_filename: str = None):
        """ Creates a CSV file in the location in csv_path called csv_filename if is given or Sniffer_Output_{current time}.csv.
        Args:
            csv_filename (str): name of the csv file generated instead of the default name Sniffer_Output_{current time}.csv
            csv_path (str): Directory where Sniffer_Output_{current time}.csv will be generated.
                            By Default it is the current working directory

        Returns:
            str: Path to the csv file in the current working directory
        """
        today = datetime.now()
        if csv_filename is not None:
            if not csv_filename.endswith(".csv"):
                csv_filename += ".csv"
            csv_path = csv_path + os.sep + csv_filename
        elif csv_filename is None:
            d1 = today.strftime("%d_%m_%Y_hr_%H_%M")
            filename = f"Sniffer_Output_" + d1 + ".csv"
            csv_path = csv_path + os.sep + filename
        with open(csv_path, 'w', newline='') as outcsv:
            writer = csv.writer(outcsv)
            writer.writerow(["Filename", "Sorted", "index"])
        return csv_path

    def delete_filename_from_csv(self, filename: str, csv_file: str):
        """Removes the filename from the csv file"""
        if not os.path.exists(csv_file):
            return
        df = pd.read_csv(csv_file)
        # Get the index in the csv where the filename to be removed is located
        index = df.loc[df["Filename"] == filename].index.values
        df.drop(index, axis=0, inplace=True)
        # Delete the old csv file
        os.remove(csv_file)
        # Create a new csv file
        df.to_csv(csv_file, index=False)

    def delete_image(self, filename: str, bad_images_path: str, good_images_path: str):
        """Deletes the file called filename from either the good_images or bad_images directory"""
        locations = [str(bad_images_path), str(good_images_path)]
        # Check if the file exists in either of the directories
        for location in locations:
            image_location = self.find_image(location, filename)
            if image_location is not None:
                os.remove(image_location)
                return  # If the file cannot be found then it proceeds normally

    def find_image(self, file_path: str, filename: str) -> str:
        """Looks for the filename in the file_path and returns the location of the file.Otherwise it returns None """
        # Remove the extension from the filename
        filename = os.path.splitext(filename)[0]
        # Check if the directory already exists if it doesn't then don't search it
        if os.path.isdir(file_path):
            # See if the filename exists in the directory and return the extact location
            for file in os.listdir(file_path):
                if filename in file:
                    return (file_path + os.sep + file)
            return None

    def save_sorted_image(self, photo_loc: str, sort_type: str):
        """Copies the photo at photo_loc to the good or bad directory depending on whether sort_type = "good" or "bad"
         with the sort_type appended to the filename"""
        # Copy the images into the good or bad directories depending on the sort_type
        if "bad" in sort_type:
            sorted_images_path = self.bad_images_path
        elif "good" in sort_type:
            sorted_images_path = self.good_images_path
        # Check if the sorted dir exists if it doesn't create it
        if not os.path.isdir(sorted_images_path):
            os.mkdir(sorted_images_path)
        # Change the filename of the photo_loc
        print(f"\n sorted_images_path : {sorted_images_path}")
        new_filename = self.change_filename(os.path.basename(photo_loc), sort_type, sorted_images_path)
        # Move the image from images into sorted_images

        shutil.copyfile(photo_loc, new_filename)

    def change_filename(self, old_filename: str, sort_type: str, sorted_dir: str):
        """Appends sort_type to the end of the filename. Returns the location of the file in the sorted_dir"""
        new_filename = os.path.splitext(old_filename)
        new_filename = new_filename[0] + "_" + str(sort_type) + new_filename[1]
        new_photo_loc = str(sorted_dir) + os.sep + new_filename
        print(f"\n new_photo_loc: {new_photo_loc}")
        return new_photo_loc

    def handle_file_choice(self, sort_type: str):
        """Sorts the current file into a good or bad directory depending on the yes/no choice
           when file mode is active

        Arguments:
        -----------
        sort_type: str
            -"good": sort the image as a good image
            -"bad": sort the image as a bad image
        """
        quality_control_passed = self.quality_control(
            self.images_path,
            self.images_list,
            self.bad_images_path,
            self.good_images_path)
        if not quality_control_passed:
            self.quality_control_failure()
        elif quality_control_passed:
            self.modify_buttons_state(True)
            self.text.value = f'Saving image #{self.image_index} / {self.last_index_images_list} as {sort_type}'
            # Save the sorted image
            photo_loc = self.images_path + os.sep + self.images_list[self.image_index]
            self.save_sorted_image(photo_loc, sort_type)
            self.image_index += 1
            # Check if all images have been processed, if so display the done image
            if self.image_index > self.last_index_images_list:
                self.handle_all_images_processed()
                self.undo_button.disabled = False
            # Still more jpgs to check
            elif self.image_index <= self.last_index_images_list:
                self.text.value = f'Saved image # {self.image_index-1} / {self.last_index_images_list} as {sort_type}'
                self.modify_buttons_state(False)

    def handle_csv_choice(self, sort_type: str):
        """Sorts the current file as a good or bad type in the csv file depending on the yes/no choice
           when csv mode is active

        Arguments:
        -----------
        sort_type: str
            -"good": sort the image as a good image
            -"bad": sort the image as a bad image
        """
        if not os.path.exists(self.csv_file_location):
            self.csv_file_location = self.create_csv()
        # Save the image filename to the csv file and the type of sort as good
        with open(self.csv_file_location, 'a', newline='') as outcsv:
            writer = csv.writer(outcsv)
            writer.writerow([self.images_list[self.image_index], sort_type, self.image_index])
        self.image_index += 1
        # Check if all images have been processed, if so display the done image
        if self.image_index > self.last_index_images_list:
            self.handle_all_images_processed()
            self.undo_button.disabled = False
        # Still more jpgs to check
        elif self.image_index <= self.last_index_images_list:
            self.text.value = f"Saved image # {self.image_index-1} / {self.last_index_images_list}  as {sort_type}"
            self.modify_buttons_state(False)

    def thumbnail_button_clicked(self, event):
        """ Generate thumbnails for all the jpgs in the images folder. While the thumbnails are
            being generated a loading icon is displayed and all the buttons are disabled.
        """
        if (event.obj.name == "THUMBNAIL"):
            self.text.value = "THUMBNAIL button clicked! Creating Thumbnails."
            # Sniffer variable indicating it will display thumbnails in the jpg panel
            self.thumbnail_mode = True
            # Setting image_index =-2 forces JPG Panel to display loading spinner
            self.image_index = -2
            # Set the jpg panel to loading while the thumbnails are created
            self.jpg_panel.loading = True
            if self.image_index < 0:
                # Create the thumbnails in the thumbnails directory
                self.create_thumbnails(self.images_path, self.images_list)
                thumbnail_jpgs = glob.glob(self.images_path + os.sep + "*jpg")
                self.thumbnails_list = map(lambda x: os.path.basename(x), thumbnail_jpgs)
                self.thumbnails_list = list(self.thumbnails_list)
                self.image_index = 0
                self.jpg_panel.loading = False
                self.modify_buttons_state(False)
                self.text.value = "Click YES or NO to begin!"

    def image_button_clicked(self, event):
        if (event.obj.name == "IMAGE"):
            # Sniffer variable indicating it will display the original jpgs in the jpg panel
            self.thumbnail_mode = False
            self.image_index = 0
            self.text.value = f"IMAGE button clicked!{self.image_index}"
            self.modify_buttons_state(False)
            self.text.value = f"Click YES or NO to begin!"

    def yes_button_clicked(self, event):
        if (event.obj.name == "YES" and self.radio_group.value == "File Mode"):
            self.handle_file_choice("good")
        elif (event.obj.name == "YES" and self.radio_group.value == "CSV Mode"):
            self.handle_csv_choice("good")

    def yes_hotkey(self):
        if self.image_index > self.last_index_images_list:
            self.handle_all_images_processed()
        else:  # valid file index
            if (self.radio_group.value == "File Mode"):
                self.handle_file_choice("good")
            elif (self.radio_group.value == "CSV Mode"):
                self.handle_csv_choice("good")

    def no_hotkey(self):
        if self.image_index > self.last_index_images_list:
            self.handle_all_images_processed()
        else:  # valid file index
            if(self.radio_group.value == "File Mode"):
                self.handle_file_choice("bad")
            elif (self.radio_group.value == "CSV Mode"):
                self.handle_csv_choice("bad")

    def no_button_clicked(self, event):
        if(self.radio_group.value == "File Mode"):
            self.handle_file_choice("bad")
        elif (self.radio_group.value == "CSV Mode"):
            self.handle_csv_choice("bad")

    def handle_undo(self):
        """ Handles the undo button or hotkey """
        if self.image_index <= 0:
            self.image_index = 0
            self.text.value = f'Cannot undo image. None Left'
            self.undo_button.disabled = True
            self.yes_button.disabled = False
            self.no_button.disabled = False
        elif self.image_index > 0 and self.image_index <= self.last_index_images_list + 1:
            if (self.radio_group.value == "File Mode"):
                quality_control_passed = self.quality_control(
                    self.images_path, self.images_list, self.bad_images_path, self.good_images_path)
                if not quality_control_passed:
                    self.quality_control_failure()
            # Decrease the photo's index so it goes back one
            self.image_index -= 1
            if self.radio_group.value == "File Mode":
                self.delete_image(self.images_list[self.image_index], self.bad_images_path, self.good_images_path)
            elif self.radio_group.value == "CSV Mode":
                self.delete_filename_from_csv(self.images_list[self.image_index], self.csv_file_location)
                self.delete_image(self.images_list[self.image_index], self.bad_images_path, self.good_images_path)
            self.text.value = f'Undo completed image #{self.image_index} / {self.last_index_images_list}'
            self.modify_buttons_state(False)

    def undo_hotkey(self):
        self.handle_undo()

    def undo_button_clicked(self, event):
        if event.obj.name == "UNDO":
            self.handle_undo()

    def modify_buttons_state(self, is_clickable: bool):
        """If given True disables all the buttons"""
        self.yes_button.disabled = is_clickable
        self.no_button.disabled = is_clickable
        self.undo_button.disabled = is_clickable
        return
