import subprocess


class ScreenReader():

    def shot(self):
        """
        Gets the screenshot from the connected android using
        adb shell command
        """
        # Generate a file identifier
        filename = "dsfsfsd"

        # Execute the screenshot command and save it in temp
        subprocess.run([f'adb exec-out screencap -p > temp/{filename}.png'])

        self.filename = filename


    def read(self):
        """ From the filename, read the question and the answers """

        # Raise exception when the file is not defined
        if self.filename is None:
            raise ValueError('Filename value is empty')

        # Obtain the answer
        # TODO

    def search(self):
        """ Search in google the results """
        pass

    def show(self):
        """ Print the results """

        print(f'Question: {self.question}')
        print(f'Answer1: {self.results[0]}')
        print(f'Answer2: {self.results[1]}')
        print(f'Answer3: {self.results[2]}')


def run():
    screen = ScreenReader()

    # take a screenshot
    screen.shot()

    # read the question and answers
    screen.read()

    # Get the results of the search
    screen.search()

    # Print the results to console
    screen.show()

