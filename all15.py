import glob
print('set -e')
for vid in glob.glob('./*h264'):
    print('ffmpeg -y -r 15 -i ' + vid[2:] + ' -c copy ' + vid[2:-5] + ".mp4")
    print('rm ' + vid[2:])
