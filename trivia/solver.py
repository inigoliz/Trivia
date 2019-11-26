from subprocess import run
import sys
from datetime import datetime
import os
from shutil import rmtree, copy

directory = '.screenshots'
sample_directory = 'samples'


class ScreenManager():
    """
    The ScreenManager class is in charge of doing the screenshots from
    the connected Android device and managing where to store them.
    """
    def __init__(self):
        self.filepath = None

    def shot(self):
        """
        Gets the screenshot from the connected android using
        adb shell command
        """

        # Create the dir if it doesnt exist (or it was removed)
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Set a filename using the screenshot time
        self.filename = f'{datetime.now().strftime("%Y%m%d-%H%M%S")}.png'
        self.filepath = os.path.join(directory, self.filename)

        # Execute the screenshot command and save it in temp
        run(f"adb exec-out screencap -p > {self.filepath}", shell=True)

    def clear_screenshot_dir(self):
        """ Deletes the hidden .screenshot folder """
        if os.path.exists(directory):
            rmtree(directory)

    def save_to_samples(self):
        """
        Moves the current screenshot from the temporal
        directory to the persistent sample folder
        """
        if self.filepath is not None:
            new_path = os.path.join(sample_directory, self.filename)
            copy(self.filepath, new_path)

    



