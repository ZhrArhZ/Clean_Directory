import json
import shutil
from pathlib import Path
from loguru import logger
from src.Data import DATA_DIR
from collections import defaultdict


class CleanDirectory:

    def __init__(self, dir_path):

        """
        Initializes an instance of CleanDirectory.

        Args:
            dir_path (Union[str, Path]): The path to the directory to clean.
        """
        self.dir_path = dir_path
        if not self.dir_path.exists():
            raise FileNotFoundError(f"{self.dir_path} doesn't exist")
   
        with open(DATA_DIR / 'extensions.json') as ex:
            self.extension_categories = json.load(ex)

        self.dir_files = self._list_regular_files()
        self._categories = self._categorize_files()
        self._create_directories()

    def _list_regular_files(self):

        """
        List regular files (excluding hidden files) in the target directory.

        Returns:
            list: A list of pathlib.Path objects representing regular files.
        """

        dir_files = [p for p in self.dir_path.iterdir() if p.is_file()
                     and not str(p.name).startswith('.')]

        return dir_files

    def _categorize_files(self):
 
        """
        Categorize files based on their extensions.

        Returns:
            dict: A dictionary mapping file extensions to corresponding
            categories.
        """

        file_extensions = {p.suffix for p in self.dir_files}
        ext_dir = defaultdict(str)

        for ext in file_extensions:
            category = self.extension_categories.get(ext, 'Other Files')
            ext_dir[ext] = category

        return ext_dir

    def _create_directories(self):

        """
        Create directories for each file category if they don't exist.
        """

        cats = self._categories
        for value in cats.values():
            target_dir = DIR_PATH.joinpath(value)
            target_dir.mkdir(exist_ok=True)

    def organize_files(self):

        """
        Organize files into their corresponding directories based on their
        categories.
        """

        ext_dir = self._categories
        for file_path in self.dir_files:
            source_path = file_path
            destination_path = DIR_PATH.joinpath(ext_dir[file_path.suffix],
                                                 file_path.name)
            logger.info(f"Moving {source_path} to {destination_path} ...")
            shutil.move(source_path, destination_path)
       

if __name__ == "__main__":
    DIR_PATH = Path(input("What's the Directory Path intended to be clean? "))
    clean_dir = CleanDirectory(DIR_PATH)
    clean_dir.organize_files()
