import glob
for vid in glob.glob('./*h264'):
    print('ffmpeg -y -r 15 -i ' + vid[2:] + ' -c copy ' + vid[2:-5] + ".mp4")
