import os
def install():
 file = open("requirements.txt","r")
 lines = file.readlines()
 file.close()
 if lines:
  for module in lines[0].split():
   os.system(module)
 else:
  print("requirements.txt file not found unable to install requirements")
