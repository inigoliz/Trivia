from subprocess import run
import sys
from datetime import datetime
import os
from shutil import rmtree, copy
from PIL import Image
import pytesseract as pys  # OCR

directory = '.screenshots'
sample_directory = 'samples'


class ScreenManager():
    """
    The ScreenManager class is in charge of doing the screenshots from
    the connected Android device and managing where to store them.
    They are stored in '.screenshots', and deleted when the app is closed.
    """

    def __init__(self):
        self.filepath = None
        self.filename = None

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

class Reader():
    def __init__(self, filepath=None, lang='eng'):

        self.width = 900

        # add some values as defaukts
        self.set_question_box(410,1040)
        self.set_a1_box(1280,1340)
        self.set_a2_box(1465, 1525)
        self.set_a3_box(1650, 1710)

        self.lang = lang
    
    def set_question_box(self, top, bottom):
        self.question_box = (0, top, self.width, bottom)
    
    def set_a1_box(self, top, bottom):
        self.a1_box = (0, top, self.width, bottom)

    def set_a2_box(self, top, bottom):
        self.a2_box = (0, top, self.width, bottom)

    def set_a3_box(self, top, bottom):
        self.a3_box = (0, top, self.width, bottom)
    
    def read(self, filepath):
        self.image = Image.open(filepath)

        results = {}
        results['q'] = self.read_box(self.question_box)
        results['a1'] = self.read_box(self.a1_box)
        results['a2'] = self.read_box(self.a2_box)
        results['a3'] = self.read_box(self.a3_box)
    
        self.results = results
        return results

    def read_box(self, section):
        return pys.image_to_string(self.image.crop(section), lang=self.lang)

    def set_language(self, lang):
        self.lang = lang

    def get_results(self):
        if hasattr(self, 'results'):
            return self.results

def read(self):
    """
    Executes OCR on the screenshot just taken. So far, boxes are adjusted manually.
    """
    image = Image.open(self.filepath)
    box_q = (130, 410, 950, 1040)
    q = image.crop(box_q)
    box_a1 = (210, 1280, 900, 1340)
    a1 = image.crop(box_a1)
    box_a2 = (210, 1465, 900, 1525)
    a2 = image.crop(box_a2)
    box_a3 = (210, 1650, 900, 1710)
    a3 = image.crop(box_a3)

    Q = pys.image_to_string(q, lang='eng')
    A1 = pys.image_to_string(a1, lang='eng')
    A2 = pys.image_to_string(a2, lang='eng')
    A3 = pys.image_to_string(a3, lang='eng')

    return {'q': Q, 'a1': A1, 'a2': A2, 'a3': A3}