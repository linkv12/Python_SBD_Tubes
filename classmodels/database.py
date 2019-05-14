class database (object) :

    def __init__(self, file_name):
        import formatting.script as script

        # open file yg namanya file_name
        file_temp = open(file_name, 'r')

        # iterasi file temp per baris sampe akhir
        for line in file_temp :
            line_list = line[:-1]   # hilangin character '\n'
            break                   # berhenti pada baris pertama


        # pisahin di tanda #
        important_data = line_list.split(';')

        for i in range(0, important_data.__len__()) :
            important_data[i] = script.cleanString(important_data[i])


        self._pointersize = int(important_data[0].split(' ')[1])
        self._blocksize = int(important_data[1].split(' ')[1])

        #print(important_data)
        #print("p_size : %d" % self._pointersize)
        #print("b_size : %d" % self._blocksize)

    def getPointerSize(self):
        return self._pointersize

    def getBlockSize(self):
        return self._blocksize