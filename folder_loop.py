original_path = r"C:\Users\cc9wong\PycharmProjects\velocity_maker\Raw Data"

from os import walk
from os.path import splitext
from os.path import join
from test_code import *

barlist = list()

for root, dirs, files in walk(original_path):
  for f in files:
    if f[-13:]=="acc_index.txt" or ( f[-17:] == "acc_index.txt.txt" ):
      barlist.append(join(root, f))


print("barlist: ", barlist)

for x in barlist:
  print("x in barlist: ", x)
  velocity_maker(x)







