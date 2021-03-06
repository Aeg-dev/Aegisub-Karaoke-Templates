import os
import subprocess


input_dir = r'F:\subt\Aegisub-Karaoke-Templates\_fx_apply'
vpy_dir = r'F:\subt\Aegisub-Karaoke-Templates\_vpy'
v_dir = r'F:\subt\Aegisub-Karaoke-Templates\_fx_mp4'
gif_out_dir = r'F:\subt\Aegisub-Karaoke-Templates\_fx_gif'
for root, dirs, files in os.walk(input_dir):
    print(f'walk in {os.path.basename(root)} --------------------')
    print('starting exec cmd ...')
    for file in files:
        fname, ext = os.path.splitext(file)
        # print(f'{root}, {ext}')
        if ext != '.ass':
            continue

        ass_in = os.path.join(root, file)
        vpy_path = os.path.join(vpy_dir, fname + '.vpy')
        x264_path =  os.path.join(v_dir, 'x264', fname + '.raw')
        mp4_path = os.path.join(v_dir, fname + '.mp4')
        p540_path = os.path.join(v_dir, 'p540', fname + '.mp4')
        gif_path = os.path.join(gif_out_dir, fname + '.gif')


        v_out = r'F:\subt\Aegisub-Karaoke-Templates\automation\gary-1080p-4s.mp4'
        vpy = f"""
import vapoursynth as vs

v_fname = r"{v_out}"
ass_fname = r"{ass_in}"

core = vs.get_core()
src = core.lsmas.LWLibavSource(v_fname, threads=1)
src = core.vsfm.TextSubMod(src, ass_fname)
src.set_output()
"""
        with open(vpy_path, "w", encoding='utf_8_sig') as f:
            f.write(vpy)

        # print(f'{src} -> {dest}')
        cmd_vpy  = f'F:\\vTools\\VapourSynth64-Portable-R52\\VSPipe.exe --y4m {vpy_path} {x264_path}'
        cmd_mp4  = f'ffmpeg -y -i {x264_path} -preset slow -crf 18 {mp4_path}'
        cmd_p540 = f'ffmpeg -y -i {mp4_path}  -strict -2 -vf crop=960:540:480:270  {p540_path}'
        cmd_gif  = f'ffmpeg -y -i {p540_path} -f gif  -an -vf crop=960:270:0:135 -s 480:135 -loop 0  {gif_path}'
        print(cmd_vpy) 
        print(cmd_mp4)
        print(cmd_p540) 
        print(cmd_gif)
        ret = subprocess.run(cmd_vpy)
        if ret.returncode != 0:
            print(f'exec \n\t{cmd_vpy}\nfailed!')
            # exit(0) 
            continue
        ret = subprocess.run(cmd_mp4)
        if ret.returncode != 0:
            print(f'exec \n\t{cmd_mp4}\nfailed!')
            # exit(0) 
            continue
        ret = subprocess.run(cmd_p540)
        if ret.returncode != 0:
            print(f'exec \n\t{cmd_p540}\nfailed!')
            # exit(0) 
        ret = subprocess.run(cmd_gif)
        if ret.returncode != 0:
            print(f'exec \n\t{cmd_gif}\nfailed!')
            # exit(0) 
            continue
        # exit(0)
    print('finished exec cmd -------------------------')
