"""标准化 ASS 模板
便于无视频预览模板文件
固定
+ 空白视频
+ 字体样式
+ 测试歌词，带k (中日英)
"""
import ass

tass = None
with open("empty-template.ass", encoding='utf_8_sig') as f:
    tass = ass.parse(f)


def norm_ass(input_fpath, output_fpath):
    # input_fpath = r'../1.ass'
    # output_fpath = r'../_out/1.ass'
    iass = None
    with open(input_fpath, encoding='utf_8_sig') as f:
        iass = ass.parse(f)

    # 所有的样式名
    # iass_styles = [i.name for i in iass.styles]
    # iass_sections = [i for i in iass.sections]

    line_insert = 0
    line_jump = 0
    tass_events = []
    for e in iass.events:
        # 跳过非注释行
        if type(e) != ass.line.Comment:
            line_jump = line_jump + 1
            continue
        # 跳过歌词行
        if e.effect == 'karaoke':
            line_jump = line_jump + 1
            continue
        # 跳过空行
        if not e.text:
            line_jump = line_jump + 1
            continue

        # 插入模板
        e.style = 'Default'
        tass_events.append(e)
        line_insert = line_insert + 1

    tass_events.append(tass.events[0])
    tass.events.set_data(tass_events)
    print(f"total jumped {line_jump} lines")
    print(f"total insert {line_insert} lines")

    with open(output_fpath, "w", encoding='utf_8_sig') as f:
        tass.dump_file(f)
