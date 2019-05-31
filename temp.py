import glob
import os

path = os.getcwd()

files = [f for f in glob.glob(path + "**/*.*", recursive=True)]

print(len(files))