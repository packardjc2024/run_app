"""
This module first checks to see if there is a new export ZIP file. If so it
opens and extracts the new export XML file and replaces the old XML file in the
program directory. It will get the most recently modified ZIP folder if there
are multiple files in the directory.
"""
import configparser
from zipfile import ZipFile
import shutil
from pathlib import Path


class GetNewXML:
    def __init__(self, config_file, new_file=False):
        self.new_file = new_file
        self.config_file = config_file

    def get_file_names(self):
        self.config = configparser.ConfigParser()
        self.config.read(self.config_file)
        self.zip_file = Path(self.config.get('directory_info', 'zip_file'))
        self.old_xml_file = Path(self.config.get('directory_info', 'old_xml_file'))
        self.downloads_folder = Path(self.config.get('directory_info', 'downloads_directory'))
        self.unzipped_file = Path(self.config.get('directory_info', 'unzipped_file'))
        self.unzipped_folder = Path(self.config.get('directory_info', 'unzipped_folder'))

    def check_for_file(self):
        """
        The program first goes to the downloads folder and checks for an
        export.zip file. If there is no file it returns False.
        """
        self.get_file_names()
        if Path.exists(self.zip_file):
            self.check_for_multiple_files()
            # Delete the old xml file from the clean old data folder
            if Path.exists(self.old_xml_file):
                self.old_xml_file.unlink()
            self.unzip_file()

    def unzip_file(self):
        """
        Unzips the export file. This will result in multiple files and a
        'Apple Health Export' folder where the export XML file is located.
        """
        with ZipFile(self.zip_file, 'r') as zip_object:
            zip_object.extractall(self.downloads_folder)
        zip_object.close()
        self.move_file()

    def move_file(self):
        """
        Once the zip file has been extracted the 'Apple Health Export'
        directory is searched for the export.xml file. If it exists it is
        moved to the program directory
        """
        if Path.exists(self.unzipped_file):
            self.unzipped_file.rename(self.old_xml_file)
            self.delete_files()

    def delete_files(self):
        """
        It is first verified that the new export.xml file has been moved to
        the program directory. If so, all the zip and extracted files are
        deleted from the downloads folder to free up space.
        """
        if Path.exists(self.old_xml_file):
            # Delete the export files from the downloads folder
            shutil.rmtree(self.unzipped_folder)
            self.zip_file.unlink()
            self.new_file = True

    def check_for_multiple_files(self):
        """
        Checks if there are multiple export files in the downloads folder.
        If so the most recently created file is used.
        """
        files = [(file, file.stat().st_mtime) for file in self.downloads_folder.glob('export*.zip')]
        if len(files) > 1:
            creation_time = 0
            for file, time in files:
                if time > creation_time:
                    creation_time = time
                    self.zip_file = file


