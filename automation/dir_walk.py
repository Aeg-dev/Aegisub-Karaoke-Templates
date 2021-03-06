import logging
import os
import pathlib


def get_all_files_in_dir(root_dir, allow_ext=['.ass'], prefix=''):
    file_list = []
    for path_root, dirs, files in os.walk(root_dir):
        logging.info(f'walk in "{path_root}" ----')
        logging.debug(f'start looping...')
        for file in files:
            file_name, ext = os.path.splitext(file)
            logging.debug(f'{file_name},{ext}; ')

            # filter ext
            if ext not in allow_ext:
                continue
  
            # gen full path
            src = os.path.join(path_root, file)
            file_list.append((prefix, pathlib.Path(src)))
        logging.debug(f'end looping ----')
    return file_list


def get_all_files_in_dirs(root_dirs, allow_ext=['.ass']):
    all_files = []
    for dir_root in root_dirs:
        all_files += get_all_files_in_dir(dir_root, allow_ext)
    return all_files


def rename_all_files_in_dirs(root_dirs, allow_ext=['.ass']):
    src_files = []
    prefixes = []

    for dir_name, dir_root in root_dirs:
        src_files += get_all_files_in_dir(dir_root, allow_ext, dir_name + '——')

    return src_files
