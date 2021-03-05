

## 生成空白视频

```
ffmpeg -f lavfi -i color=c=Gray:s=1920x1080:rate=30:duration=4 gary-1080p-4s.mp4
```

ref:
+ [ffmpeg create blank screen with text video - Stack Overflow]( https://stackoverflow.com/questions/22710099/ffmpeg-create-blank-screen-with-text-video )
+ [Libav documentation : Libavfilter]( https://libav.org/documentation/libavfilter.html#buffer )
+ [FFmpeg Devices Documentation]( https://ffmpeg.org/ffmpeg-devices.html#lavfi )


## 准备特效字幕

使用模板的样式和测试文字
生成 `fx-raw.ass`

使用 `fx-apply.cmd` 应用特效

## 压制视频

运行 `encode.bat`
