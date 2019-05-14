import os
from classmodels.data import data

print(os.getcwd()+"/assets")
x = data(os.getcwd()+"/assets")

try :
    print(int('two'))
except Exception as e :
    print(e)
    print('2')