import os
import subprocess


input_dir = r'F:\subt\Aegisub-Karaoke-Templates\_out'
output_dir = r'F:\subt\Aegisub-Karaoke-Templates\_fx_apply'
for root, dirs, files in os.walk(input_dir):
    print(f'walk in {os.path.basename(root)} --------------------')
    print('starting apply files...')
    for file in files:
        _, ext = os.path.splitext(file)
        # print(f'{root}, {ext}')
        if ext != '.ass':
            continue
        
        src = os.path.join(root, file)
        dest = os.path.join(output_dir, file)
        # print(f'{src} -> {dest}')
        cmd = f'F:\\subt\\Aegisub\\aegisub-cli  --automation kara-templater.lua  "{src}"  "{dest}"  "Apply karaoke template"'
        # print(cmd) 
        ret = subprocess.run(cmd)
        if ret.returncode != 0:
            print(f'apply {file} failed!')
            continue
    print('finished apply files -------------------------')




