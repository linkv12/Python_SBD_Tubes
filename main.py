import os
from classmodels.data import data
from userinterface import mainCLI

if __name__ == "__main__" :
    import os
    mainCLI.mainCLI(data(os.getcwd()+"/assets"))