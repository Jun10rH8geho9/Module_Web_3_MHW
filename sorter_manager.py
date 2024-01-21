import shutil
import re
from pathlib import Path
from rich.console import Console
from concurrent.futures import ThreadPoolExecutor

console = Console()

class FolderOrganizer:
    def __init__(self, folder_path=None):
        self.folder_path = folder_path

        # Транслітерація
        self.CYRILLIC_SYMBOLS = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ'
        self.TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
                           "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "u", "ja", "je", "ji", "g")

        self.TRANS = dict()

        for cyrillic, latin in zip(self.CYRILLIC_SYMBOLS, self.TRANSLATION):
            self.TRANS[ord(cyrillic)] = latin
            self.TRANS[ord(cyrillic.upper())] = latin.upper()
        
        # Доступні розширення
        self.KNOWN_EXTENSIONS = {
            'Images': {'JPEG', 'JPG', 'PNG', 'SVG'},
            'Video': {'AVI', 'MP4', 'MOV', 'MKV'},
            'Documents': {'DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'},
            'Audio': {'MP3', 'OGG', 'WAV', 'AMR'},
            'Archives': {'ZIP', 'GZ', 'TAR'},
        }

    # Перетворення кирилиці на латиницю
    def normalize(self, name: str) -> str:
        translate_name = re.sub(r'[^a-zA-Z0-9.]', '_', name.translate(self.TRANS))
        return translate_name

    def get_extension(self, name: str) -> str:
        return Path(name).suffix[1:].upper()

    def handle_file(self, file_name: Path, target_folder: Path):
        extension = self.get_extension(file_name)
        normalized_name = self.normalize(file_name.name)

        if extension in {ext for exts in self.KNOWN_EXTENSIONS.values() for ext in exts}:
            target_folder = target_folder / extension
        else:
            target_folder = target_folder / 'MY_OTHER'

        # Якщо файл знаходиться в підпапці, перемістіть його в основну папку
        if target_folder.name != self.folder_path.name:
            target_folder = self.folder_path / extension

        target_folder.mkdir(exist_ok=True, parents=True)
        target_path = target_folder / f"{Path(normalized_name).stem}_{Path(normalized_name).suffix}"

        if target_path.exists():
            target_path = target_folder / f"{Path(normalized_name).stem}_{Path(normalized_name).suffix}"

        shutil.move(str(file_name), str(target_path))

    def process_files_in_folder(self, folder_path):
        with ThreadPoolExecutor() as executor:
            futures = []
            for item in folder_path.iterdir():
                if item.is_file():
                    future = executor.submit(self.handle_file, item, folder_path)
                    futures.append(future)
                elif item.is_dir():
                    # Рекурсивно обробляємо файли в підпапці
                    self.process_files_in_folder(item)
                    # Видаляємо підпапку після того, як файли були оброблені
                    shutil.rmtree(item)

        # Чекаємо завершення всіх завдань
        for future in futures:
            future.result()
    
    def organize_folder(self):   
        while True:
            local_path = input('Введіть шлях до папки для сортування (або натисніть "enter", для виходу): ')
            if local_path == '':
                break

            self.folder_path = Path(local_path).resolve()
            
            if not self.folder_path.exists() or not self.folder_path.is_dir():
                console.print(f'[red]Папка "{self.folder_path}" не існує.[/red]')
            else:
                self.process_files_in_folder(self.folder_path)
                console.print(f'[green]Файли в папці "{self.folder_path.name}" відсортовані.[/green]')

if __name__ == "__main__":
    organizer = FolderOrganizer()
    organizer.organize_folder()