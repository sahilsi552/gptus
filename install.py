#Install requirements.txt using python..

import os
def install():
 file = open("requirements.txt","r")
 lines = file.read()
 file.close()
 print()
 if lines:
  for module in lines.split("\n"):
   try:
    os.system("pip3 install " + module)
   except Exception as e:
    print(e)
    continue
 else:
  print("requirements.txt file not found unable to install requirements")
install()
