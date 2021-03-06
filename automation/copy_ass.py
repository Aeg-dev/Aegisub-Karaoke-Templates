import os
import shutil


target_dir = r'F:\subt\Aegisub-Karaoke-Templates\_big_aeg'
dir_list = [
    ('kf-481', r'F:\subt\aeg 特效模板\[Kara Effector]\Aegisub Karaoke Effect 481 Templates'),
    # ('', r''),
]

dir_name, path = None, None
for dir_name, path in dir_list:
    # traverse root directory, and list directories as dirs and files as files
    for root, dirs, files in os.walk(path):
        print(f'walk in {os.path.basename(root)} --------------------')
        print('starting copying files...')
        for file in files:
            _, ext = os.path.splitext(file)
            # print(f'{root}, {ext}')
            if ext != '.ass':
                continue

            fname = dir_name + '—'  + file
            src = os.path.join(root, file)
            desc = os.path.join(target_dir, fname)
            # print(f'{src} -> {desc}')
            shutil.copyfile(src, desc)
        print('finished copying files -------------------------')
