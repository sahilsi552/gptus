import os

file = open("requirements.txt","r")
lines = file.readlines()
file.close()

for module in lines[0].split():
 os.system(module)
