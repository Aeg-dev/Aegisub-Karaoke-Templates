import os
import norm


input_dir = r'F:\subt\Aegisub-Karaoke-Templates\_big_aeg'
output_dir = r'F:\subt\Aegisub-Karaoke-Templates\_out'
for root, dirs, files in os.walk(input_dir):
    print(f'walk in {os.path.basename(root)} --------------------')
    print('starting norm files...')
    for file in files:
        _, ext = os.path.splitext(file)
        # print(f'{root}, {ext}')
        if ext != '.ass':
            continue
        
        src = os.path.join(root, file)
        dest = os.path.join(output_dir, file)
        print(f'{src} -> {dest}')
        norm.norm_ass(src, dest)
    print('finished norm files -------------------------')
