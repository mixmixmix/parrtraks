import yaml
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

with open('fish1.yml', 'r') as mfile:
    fish1 = yaml.safe_load(mfile)
print("Data read")
plt.plot(fish1)
plt.savefig('foo.pdf', bbox_inches='tight')
plt.show()
input("Press the <ENTER> key to continue...")
