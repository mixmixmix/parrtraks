import glob
for vid in glob.glob('./*h264'):
    print('ffmpeg -y -i ' + vid[2:] + ' -vf \"setpts=2.5*PTS\" -r 10 ' + vid[2:-5] + ".mp4")

