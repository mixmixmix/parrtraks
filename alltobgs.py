import glob
for vid in glob.glob('./*mp4'):
    print('python3 parrtrak.py -f ' + vid[2:] + ' -o ' + vid[2:-5] + ".yml")
