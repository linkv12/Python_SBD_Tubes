import classmodels.table as table


class data (object):
    def __init__(self, folder_name):
        import classmodels.database as database
        self.folder_name = folder_name + '/'
        self.db = database.database(self.folder_name + "data_dict.txt")
        self.tb = table.createTablefromFile(self.folder_name + "data_dict.txt")



        self.getTable(self.tb, 'Mahasiswa')

    def calcFanout(self, tbl: table):
        # harus diisi rumusnya
        from math import floor

        return floor(self.db.getBlockSize() / (tbl.key_size + self.db.getTidSize()))

    def calcBfr(self, tbl: table):
        # harus diisi rumusnya
        from math import floor
        return (floor(self.db.getBlockSize() / tbl.record_size))

    def calcJmlBlok(self, tbl: table):
        from math import ceil
        return (ceil(tbl.record_num / self.calcBfr(tbl)))

    def calcIndeksBlock(self, tbl : table):
        from math import ceil, floor

        # rumus udah bener
        return  (ceil(tbl.record_num/self.calcFanout(tbl)))
        #return ceil(ceil(tbl.record_num/self.calcFanout(tbl))/floor(self.db.getBlockSize()/(tbl.key_size + self.db.getTidSize())))

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
        import math

        # harus diisi rumusnya
        # nilai fanout
        # langkahnya
        fanout = self.calcFanout(self.getTable(self.tb, table_name))
        # rumusnya record_loc / fanout ratio
        result = math.ceil(record_loc / fanout)
        return result

    def searchNoIndeks(self, table_name : str, record_loc : int):
        import math

        # harus diisi rumusnya

        bfr = self.calcBfr(self.getTable(self.tb, table_name))

        # rumus = ceil(record_loc/bfr)
        result = math.ceil(record_loc/bfr)
        return result


    #########NO4
    def countA1Key (self,b : float) :
        """
        Hitung A1 with key
        :param b: ini small b
        :return: nilai A1 with key
        """
        return float(b/2)


    def countA1NoKey(self,b : float):
        """
        Hitung A1 tanpa key
        :param b: ini small b
        :return:
        """
        return float(b)

    def countA2(self, b : float, block_size : int, v : int, P : int):
        """
        Hitung A2
        :param b: itu smallb -> ada func sendiri
        :param block_size: ini blocksize
        :param v: v -> yg terakhir di data_dict sebelum hastag
        :param P:pointer size dari data_dict
        :return: float yg udah dihitung
        """
        import math
        # b -> small b
        # block_size -> blockSize
        # v -> yg terakhir di data_dict sebelum hastag
        # P -> pointer size dari data_dict

        # rumus
        # ceil(log(b)/log(floor(block_size/(v+P)))) + 1
        # no comment cuma ikutin rumus
        part1 = math.log(b)
        part2 = math.log(math.floor(block_size /(v + P)))
        return math.ceil(part1/part2) + 1

    # n jumlah record
    def calcb(self,n : int, bfr : float ):
        """
        Hitung b -> ceil(n/bfr)
        :param n: record_num
        :param bfr: nilai bfr dari table tersebut
        :return: ceil(n/bfr)
        """
        # rumus untuk b -> ceil(n/bfr)
        import math
        return math.ceil(n/bfr)

    def countA3(self, b : float, block_size : int, v : int, P : int):
        """
        Hitung A3
        :param b: itu smallb -> ada func sendiri
        :param block_size: ini blocksize
        :param v: v -> yg terakhir di data_dict sebelum hastag
        :param P:pointer size dari data_dict
        :return: float yg udah dihitung
        """
        import math
        # rumus
        # ceil(log(b)/log(floor(block_size / (v+p))) + b
        part1 = math.log(b)
        part2 = math.log(math.floor(block_size / (v + P)))
        part3 = math.ceil(part1/part2)
        return part3 + b

"""
    public double countA3(double b,int B, int v, int P){
         int x = B / (v+P) ;
         double y = Math.floor(x);
         double log = Math.log(b) / Math.log(y);
         double h1 = Math.ceil(log);
         double hasil = h1+b;
         return hasil ;
     }
"""
    #########


    def calcQEPnCost(self, query: str):
        import formatting.script as script
        raw_query = query
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

                    print("\tTabel(%d) : %s" % (i, join_info[1][i - 1]))
                    if (i == 1):
                        print("\tList Kolom : %s" % str(self.getTable(self.tb, join_info[1][0]).table_column))

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

                    qep_cost[1] = 10
                    print(">> QEP optimal : QEP#%d" % (qep_cost.index(min(qep_cost)) + 1))

                    ## ini cuma string formating
                    proj = "PROJECTION "
                    for col in join_info[0]:
                        if (join_info[0][-1] == col):
                            proj = proj + col + ' -- on the fly'
                        else:
                            proj = proj +" " + col + ', '
                    jn = "\t\tJOIN %s.%s = %s.%s -- BNLJ" % (
                        join_info[1][0], join_info[-1], join_info[1][1], join_info[-1])
                    if (qep_cost.index(min(qep_cost)) == 0) :
                        tbl_urutan = ("%s\t\t%s" % (join_info[1][0], join_info[1][1]))
                    else :
                        tbl_urutan = ("%s\t\t%s" % (join_info[1][1], join_info[1][0]))

                    cost_qep_formated = "Cost (worst case) : %d block" % min(qep_cost)
                    data_to_write =[raw_query, proj, jn, tbl_urutan, cost_qep_formated]
                    #for i in data_to_write:
                    #    print(i)

                else:
                    print("Error query not valid")

            else:
                # ini bagian untuk where + selection
                print("Bagian where")
                important_data = self.parseWhereQuery(query)
                # ambil nilai dari object table
                tab = self.getTable(important_data.get('table_name'))

                #print(type(important_data))
                col_valid = self.isColumnValid(important_data.get('projection'), important_data.get('table_name'))
                #print(important_data)
                #print(col_valid)
                if col_valid :
                    print("\tTabel(%d) : %s" % (1, tab.table_name))
                    print("\tList kolom : %s" % (str(tab.table_column)))
                    qep_cost = []
                    for i in range(0,4) :
                        print(">> QEP #%d" % (i + 1))
                        print("\tPROJECTION ", end='')
                        for col in important_data.get('projection'):
                            if (important_data.get('projection')[-1] == col):
                                print(col, end=' -- on the fly\n')
                            else:
                                print(col, end=', ')
                        reconstruct = ''
                        for part in important_data.get('condition') :
                            reconstruct = reconstruct + part + ' '

                        reconstruct = script.cleanString(reconstruct)
                        smallb = self.calcb(tab.record_num, self.calcBfr(tab))
                        if (i == 0) :
                            eq = 'A1 Key'
                            qep_cost.append(self.countA1Key(smallb))
                        elif i == 1 :
                            eq = 'A1 No Key'
                            qep_cost.append(self.countA1NoKey(smallb))
                        elif i == 2 :
                            eq ='A2'
                            qep_cost.append(self.countA2(smallb,self.db.getBlockSize(), tab.key_size, self.db.getTidSize()))
                        elif i == 3 :
                            eq = 'A3'
                            qep_cost.append()
                        print("\tSELECTION %s -- %s key" % (reconstruct, eq))

                        print("\t%s" % important_data.get('table_name'))
                        qep_cost.append(99)  # qep_cost.append(ini harus diisi formula hitung qep)
                        print("\tCost (worst case) : %d block" % qep_cost[i])  # 99 itu placeholder

                    print(">> QEP optimal : QEP#%d" % (qep_cost.index(min(qep_cost)) + 1))
                else :
                    print("Error column not valid")



        else :
            print("Error query not valid")

   # def calcJoinQEPnCost(self, imp_data : list):

    def parseWhereQuery(self, query):
        import formatting.script as script
        query_parse = query.split('from')

        # SELECT nim, nama FROM Mahasiswa WHERE nim = 190;

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
        # ['Mahasiswa', 'nim = 190;']
        table_name_raw = query_parse[-1].split('where')
        #print(table_name_raw)

        # table_name_clean = bagian pertama indeks ke 0
        table_name = script.cleanString(table_name_raw[0])
        #print(table_name_raw[-1])
        #print(table_name_raw[-1].split(' '))

        # condition -> nim = 190
        cond =  []
        for isi in script.cleanString(table_name_raw[-1]).split(' ') :
            cond.append(script.cleanString(isi))

        temp = {'projection' : column_projection, 'table_name' : table_name, 'condition': cond }
        return (temp)



    def parseJoinQuery(self, query):

        # SELECT nim, nama FROM Mahasiswa JOIN Registrasi using (nim);
        import formatting.script as script
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

    def print_shared_pool(self):
        # baca file shared pool
        text = open(self.folder_name + "shared_pool.txt", 'r')
        i = 1
        temp = []
        # ini for
        for line in text:
            if('\n' != line) :
                if('\n' == line[-1]) :
                    temp.append(line[:-1])
                else :
                    temp.append(line)
            elif ('\n' == line) :
                for j in range(0, temp.__len__()) :
                    if (j == 0) :
                        print('%d.\t%s' % (i, temp[j]))
                    else:
                        print("\t"+temp[j])

                print()
                i = i + 1
                if ('\n' == line[-1]):
                    temp = []

        # diluar for
        for j in range(0, temp.__len__()):
            if (j == 0):
                print('%d.\t%s' % (i, temp[j]))
            else:
                print("\t"+temp[j])

        print()


