class table (object) :

    def __init__(self, line):
        import formatting.script as script
        # pisahin di tanda #
        temp_data = line.split(';')

        # besihin data
        for i in range(0, temp_data.__len__()):
            temp_data[i] = script.cleanString(temp_data[i])

        self.table_name = temp_data[0]
        self.table_column = temp_data[1].split(',')

        # besihin data
        for i in range(0, self.table_column.__len__()):
            self.table_column[i] = script.cleanString(self.table_column[i])

        self.record_size = int(temp_data[2].split(' ')[-1])
        self.record_num = int(temp_data[3].split(' ')[-1])
        self.key_size = int(temp_data[-1].split(' ')[-1])


    def print_table(self):
        print("Table Name   \t: %s" % self.table_name)
        print("Table Column \t: %s" % str(self.table_column))
        print ("Record Size \t: %d" % self.record_size)
        print("Record num   \t: %d" % self.record_num)
        print("Tid Size     \t: %d" % self.tid_size)




def createTablefromFile(file_name) :

    # open file yg namanya file_name
    file_temp = open(file_name, 'r')

    table_raw = []
    # iterasi file temp per baris sampe akhir
    for line in file_temp:
        table_raw.append(line[:-1])  # hilangin character '\n'

    # hilangin baris pertama
    table_raw = table_raw[1:]

    # cleaned data
    table_clean = []

    for line in table_raw:
        table_clean.append(table(line))

    return table_clean