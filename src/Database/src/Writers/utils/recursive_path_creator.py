import os


def recursive_folder_creator(path: str):
    if path[-1] == '/':
        path = path[0:-1]
    if os.path.exists(path):
        return True
    split_path = path.split('/')[:-1:]
    if len(split_path) == 1:
        os.mkdir(split_path[0])
    recursive_folder_creator('/'.join(split_path))
    os.mkdir(path)
