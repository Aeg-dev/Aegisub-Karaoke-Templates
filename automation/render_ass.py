"""渲染 ASS 特效模板到视频文件

## 依赖工具
+ python: 脚本驱动
+ aegisub-cli: 命令行应用模板
+ VapourSynth64: 字幕压制自动化
+ ffmpeg: x264 压制、gif、webp 输出

## 输入要求
+ 
"""
import logging
from pathlib import Path
from dir_walk import get_all_files_in_dir, get_all_files_in_dirs, rename_all_files_in_dirs
from norm import norm_ass
import subprocess


dir_list = [
    ('52fx-duoi', r'F:\subt\aeg 特效模板\[Kara Effector]\52fx duoi'),
    ('55', r'F:\subt\aeg 特效模板\[Kara Effector]\55'),
    ('55-tren', r'F:\subt\aeg 特效模板\[Kara Effector]\55 tren'),
    ('kf+1-54', r'F:\subt\aeg 特效模板\[Kara Effector]\Aegisub Effect 搬运 by darinjie\Kara Effect 1-54'),
    ('kf-tran+1-6', r'F:\subt\aeg 特效模板\[Kara Effector]\Aegisub Effect 搬运 by darinjie\Kara+Trans Effect 1-6'),
    ('kf-tran+1-10', r'F:\subt\aeg 特效模板\[Kara Effector]\Aegisub Effect 搬运 by darinjie\Trans Effect 1-10'),
    ('kf-481', r'F:\subt\aeg 特效模板\[Kara Effector]\Aegisub Karaoke Effect 481 Templates'),
    ('kf-ht', r'F:\subt\aeg 特效模板\[Kara Effector]\Aegisub Karaoke Effects Tong Hop'),
    ('fx-nice', r'F:\subt\aeg 特效模板\[Kara Effector]\Effect-Aegisub-Nice\Effect Nice'),
    ('fx', r'F:\subt\aeg 特效模板\[Kara Effector]\Fx'),
    # ('', r''),
]
ass__dir = Path('../_ass_in').resolve()
temp_dir = Path('../_tmp').resolve()
vout_dir = Path('../_vout').resolve()
aegisub_cli_exec = Path('F:\\subt\\Aegisub\\aegisub-cli.exe')
template_vin = Path(r'F:\subt\Aegisub-Karaoke-Templates\automation\gary-1080p-4s.mp4')
vspipe_exec = Path('F:\\vTools\\VapourSynth64-Portable-R52\\VSPipe.exe')


def get_all_io_path(ass_path, prefix=''):
    full_name = ass_path.name
    fname, ext = ass_path.stem, ass_path.suffix
    if prefix:
        fname = prefix + fname

    # in
    fx = ass__dir.joinpath(fname + '.ass')
    # temp
    fx_ = temp_dir.joinpath(fname + '_applyed.ass')
    vpy = temp_dir.joinpath(fname + '.vpy')
    raw = temp_dir.joinpath(fname + '.raw')
    p540 = temp_dir.joinpath(fname + '.mp4')
    bat = temp_dir.joinpath(fname + '.bat')
    # out
    mp4 = vout_dir.joinpath(fname + '.mp4')
    gif = vout_dir.joinpath(fname + '.gif')
    webp = vout_dir.joinpath(fname + '.webp')

    return fx, fx_, vpy, raw, mp4, bat, p540, gif, webp


def run_cmd_err(cmd, on_err_exit=False):
    logging.debug(cmd)

    ret = subprocess.run(cmd)
    if ret.returncode != 0:
        print(f'exec \n\t{cmd}\nfailed!\n')
        if on_err_exit:
            exit(0)
    
    return ret.returncode


## TODO:  多文件夹复制 ASS
##  产生文件列表
# 少量文件测试
dir_list = [
    # ('kf-ht', r'F:\subt\aeg 特效模板\[Kara Effector]\Aegisub Karaoke Effects Tong Hop'),
    ('kf-tran+1-6', r'F:\subt\aeg 特效模板\[Kara Effector]\Aegisub Effect 搬运 by darinjie\Kara+Trans Effect 1-6'),
]
ass_files = rename_all_files_in_dirs(dir_list)

# 小文件测试
# ass_files = [
#     # ('', Path('F:\\subt\\Aegisub-Karaoke-Templates\\1.ass')),
#     ('kf-ht', Path(r'F:\subt\aeg 特效模板\[Kara Effector]\52fx duoi\1.ass')),
#     ('kf-ht', Path(r'F:\subt\aeg 特效模板\[Kara Effector]\52fx duoi\2.ass')),
#     ('kf-ht', Path(r'F:\subt\aeg 特效模板\[Kara Effector]\52fx duoi\3.ass')),
# ]
## 处理一个文件
for prefix, ass in ass_files:
    run_err = False
    fname = ass.name
    fx, fx_, vpy, raw, mp4, bat, p540, gif, webp = get_all_io_path(ass, prefix)


    # 1. 正规化模板
    norm_ass(ass, fx)

    # 2. 应用模板
    
    apply_cmd = f'{aegisub_cli_exec}  --automation kara-templater.lua  "{fx}" "{fx_}"  "Apply karaoke template"'
    logging.debug(apply_cmd)
    ret = subprocess.run(apply_cmd)
    if ret.returncode != 0:
        print(f'apply "{fname}" failed!\n')
        continue
    
    #3. vs 渲染
    vpy_str = f"""
import vapoursynth as vs

v_fname = r"{template_vin}"
ass_fname = r"{fx_}"

core = vs.get_core()
src = core.lsmas.LWLibavSource(v_fname, threads=1)
src = core.vsfm.TextSubMod(src, ass_fname)
src.set_output()
"""
    with open(vpy, "w", encoding='utf_8_sig') as f:
        f.write(vpy_str)

    #             VSPipe.exe  --y4m add-ass.vpy - | ffmpeg -y -i - -preset slow -crf 18 fx.mp4
    bat_str = f"""{vspipe_exec} --y4m "{vpy}" - | ffmpeg -y -i - -preset slow -crf 18 "{mp4}" """
    with open(bat, "w", encoding='utf_8_sig') as f:
        f.write(bat_str)

    # 命令行处理
    cmd_list = [
        f'"{bat}"',
        # # 3. ass 渲染
        # f'{vspipe_exec} --y4m "{vpy}" "{raw}"',
        # # 4. 压制
        # f'ffmpeg -y -i "{raw}" -preset slow -crf 18 "{mp4}"',

        # 5. 其他输出
        f'ffmpeg -y -i "{mp4}"  -strict -2 -vf crop=960:540:480:270  "{p540}"',
        f'ffmpeg -y -i "{p540}" -f gif -an -vf crop=960:270:0:135 -s 480:135 -loop 0  "{gif}"',
        f'ffmpeg -y -i "{p540}" -an -vcodec libwebp -vf crop=960:270:0:135 -s 480:135  -lossless 1 -loop 0 -preset text  "{webp}"',
    ]

    for cmd in cmd_list:
        if run_cmd_err(cmd):
            run_err = True
            break
    
    if run_err:
        continue
