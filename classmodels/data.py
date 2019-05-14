import classmodels.table as table


class data (object):
    def __init__(self, folder_name):
        import classmodels.database as database
        self.folder_name = folder_name + '/'
        self.db = database.database(self.folder_name + "data_dict.txt")
        self.tb = table.createTablefromFile(self.folder_name + "data_dict.txt")



        self.getTable(self.tb, 'Mahasiswa')


    def calcFanout(self,tbl : table):
        # harus diisi rumusnya

        return 1
    def calcBfr(self,tbl : table):
        # harus diisi rumusnya

        return 111

    def isTableExist(self,table_name : str):
        import formatting.script as script
        found = False
        table_name = script.cleanString(table_name)
        for tab in self.tb :
            if (table_name == tab.table_name) :
                found = True

        return found

    def validateRecordPosition(self,table_name : str ,record_num : int):
        temp_table = self.getTable(self.tb, table_name)
        print("LOL " + temp_table.record_num)
        if (temp_table != None) :
            if (record_num <= 0):
                return False
            elif (record_num > temp_table.record_num):
                return False
            else:
                return True
        else :
            return False

    def getTable(self,tb : list, table_name : str) :
        #print(tb)
        #print(table_name)
        #for i in tb :
        #    i.print_table()
        for tabel in tb :
            if (tabel.table_name.lower() == table_name.lower()) :
                #print ('x')
                return tabel

        return None


    def searchIndeks(self, table_name : str, record_loc : int):
        # harus diisi rumusnya

        return 134

    def searchNoIndeks(self, table_name : str, record_loc : int):
        # harus diisi rumusnya

        return 123



    def calcQEPnCost(self, query: str):
        import formatting.script as script
        query = script.cleanString(query)

        def isValidEnough(q_ery : str) :
            if ('select' not in q_ery) :
                return False
            else :
                if ('from' not in q_ery) :
                    return False
                else:
                    if ('join' not in q_ery) :
                        if ('using' in q_ery) :
                            return False
                    else :
                        if ('using' not in q_ery) :
                            return False

            return True

        print(isValidEnough(query))

        if (isValidEnough(query)) :
            if ("join" in query.lower()):
                print(">> Output:")
                join_info = self.parseJoinQuery(query.lower())
                # print(join_info[0])
                # print(join_info[1][0])
                part1 = self.isColumnValid(join_info[0], join_info[1][0])
                part2 = self.isColumnValid([join_info[-1]], join_info[1][1])

                if (part1 and part2):
                    valid = True
                    for i in range(1, 3):
                        print("\tTabel(%d) : %s" % (i, join_info[1][i - 1]))
                        if (i == 1):
                            print("\tList Kolom : %s" % str(self.getTable(self.tb, join_info[1][0]).table_column))
                        elif (i == 2):
                            print("\tList Kolom : %s" % str([join_info[-1]]))
                            # (str(self.getTable(self.tb,join_info[1][-1]).table_column))

                    qep_cost = []
                    for i in range(0, 2):
                        print(">> QEP #%d" % (i + 1))
                        print("\tPROJECTION ", end='')
                        for col in join_info[0]:
                            if (join_info[0][-1] == col):
                                print(col, end=' -- on the fly\n')
                            else:
                                print(col, end=', ')
                        print("\t\tJOIN %s.%s = %s.%s -- BNLJ" % (
                        join_info[1][0], join_info[-1], join_info[1][1], join_info[-1]))
                        if i == 0:
                            print("\t%s\t\t%s" % (join_info[1][0], join_info[1][1]))
                        else:
                            print("\t%s\t\t%s" % (join_info[1][1], join_info[1][0]))
                        qep_cost.append(99) # qep_cost.append(ini harus diisi formula hitung qep)
                        print("\tCost (worst case) : %d block" % qep_cost[i])  # 99 itu placeholder

                    print(">> QEP optimal : QEP#%d" % (qep_cost.index(min(qep_cost)) + 1))


                else:
                    print("Error query not valid")

            else:
                # ini bagian untuk where + selection
                print("Bagian where")
        else :
            print("Error query not valid")

   # def calcJoinQEPnCost(self, imp_data : list):



    def parseJoinQuery(self, query):

        # SELECT nim, nama FROM Mahasiswa JOIN Registrasi using (nim);
        import formatting.script as script
        valid = False
        query_parse = query.split('from')

        # part 1 -> isinya SELECT nim, nama
        # ini ambil elemen pertama dari array query_parse
        # ini misahin string jadi list di 'select'
        # terus ambil elemen terakhir dari string yg dipisahin
        column_projection_raw = query_parse[0].split('select')[-1]


        # part 1 -> indeks 0 isinya select sama colomn buat projection
        # SELECT nim, nama FROM Mahasiswa JOIN Registrasi using (nim);
        # Ambil bagian ini nim, nama
        column_projection = []
        for column_name in column_projection_raw.split(',') :
            column_projection.append(script.cleanString(column_name))

        # part 2 -> isinya Mahasiswa JOIN Registrasi using (nim);
        # ini misahin string jadi list di 'join'
        # table_name_raw akan berisi
        # ['Mahasiswa', 'Registrasi using (nim);']
        table_name_raw = query_parse[-1].split('join')


        # ini ambil elemen terakhir dari array table_name_raw
        # terus di pisahin pke split di bagian 'using' jadi list baru yg cuma ada di memory
        # selanjutnya ambil bagian pertama dari yang list sementara diatas
        table_name_raw[-1] = table_name_raw[-1].split('using')[0]

        # ini berisi table name yg bersih
        table_name = []
        for t_name in table_name_raw :
            table_name.append(script.cleanString(t_name))


        # part 3 -> ini bagian dimana isinya using
        # di join dimana
        # langkah langkahnya ->
        # 1 -> pisahin dibagian using
        # 2 -> di bersihin textnya
        # 3 -> done

        # ini string yg isinya bagian setelah using
        joined_on = query.split('using')[-1]

        joined_on = script.cleanString(joined_on)

        #print(column_projection)
        #print(table_name)
        #print(joined_on)

        return [column_projection, table_name, joined_on]

    def isColumnValid(self, column : list, table_name : str):

        table_col = self.getTable(self.tb, table_name)
        #print(self.getTable(self.tb, table_name))

        inTabel = True

        for col in column :
            if (col.lower() not in table_col.table_column) :
                inTabel = False

        return inTabel