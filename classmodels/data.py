import classmodels.table as table


class data (object):
    # constructor
    def __init__(self, folder_name):
        import classmodels.database as database
        self.folder_name = folder_name + '/'
        self.db = database.database(self.folder_name + "data_dict.txt")
        self.tb = table.createTablefromFile(self.folder_name + "data_dict.txt")


        # cek dalam constructor
        #self.getTable(self.tb, 'Mahasiswa')

    ################# NO 1
    def calcFanout(self, tbl: table):
        # harus diisi rumusnya
        from math import floor

        return floor(self.db.getBlockSize() / (tbl.key_size + self.db.getTidSize()))

    def calcBfr(self, tbl: table):
        # harus diisi rumusnya
        from math import floor
        return (floor(self.db.getBlockSize() / tbl.record_size))

#############################

################### NO 2
    # ini hitung jumlah blok yg dipake tbl -> table
    def calcJmlBlok(self, tbl: table):
        from math import ceil
        return (ceil(tbl.record_num / self.calcBfr(tbl)))

    # ini hitung jumlah blok yg dipake indeks dari tbl -> table
    def calcIndeksBlock(self, tbl : table):
        from math import ceil, floor
        # rumus udah bener
        return  (ceil(tbl.record_num/self.calcFanout(tbl)))

 ##########################


################ NO 3
    # ini search menggunakan indeks
    # no 3 di cli
    def searchIndeks(self, table_name : str, record_loc : int):
        import math
        # langkahnya
        fanout = self.calcFanout(self.getTable(self.tb, table_name))
        # rumusnya record_loc / fanout ratio
        result = math.ceil(record_loc / fanout)
        return result

    # ini search tanpa indeks
    # no 3 di cli
    # pke BFR
    def searchNoIndeks(self, table_name : str, record_loc : int):
        import math

        # harus diisi rumusnya

        bfr = self.calcBfr(self.getTable(self.tb, table_name))

        # rumus = ceil(record_loc/bfr)
        result = math.ceil(record_loc/bfr)
        return result
##################################

#########NO4
################ ini cli nya
    def calcQEPnCost(self, query: str):
        import formatting.script as script
        raw_query = query
        query = script.cleanString(query)

        # ini nested function karena cuma dipake sekali doang
        def isValidEnough(q_ery: str):
            if ('select' not in q_ery):
                return False
            else:
                if ('from' not in q_ery):
                    return False
                else:
                    if ('join' not in q_ery):
                        if ('using' in q_ery):
                            return False
                    else:
                        if ('using' not in q_ery):
                            return False

            return True

        # print(isValidEnough(query))

        if (isValidEnough(query)):
            if ("join" in query.lower()):
                print(">> Output:")
                join_info = self.parseJoinQuery(query.lower())
                print(join_info[0], join_info[1][0])
                print([join_info[-1]], join_info[1][1])
                part1 = self.isColumnValid(join_info[0], join_info[1][0])
                part2 = self.isColumnValid([join_info[-1]], join_info[1][1])
                tab1 = self.getTable(self.tb, join_info[1][0])
                tab2 = self.getTable(self.tb, join_info[1][1])

                bfr_left = self.calcBfr(tab1)  # table pertama ini setelah from
                smallb_left = self.calcb(tab1.record_num, bfr_left)  # table pertama ini setelah from
                bfr_right = self.calcBfr(tab2)  # table kedua ini setelah join
                smallb_right = self.calcb(tab2.record_num, bfr_right)  # table kedua ini setelah join

                # ini buat masukin ke shared_pool
                data_calc_qep = []
                print(str(part1) + " " + str(part2))
                if (part1 and part2):
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
                        temp_proj = 'PROJECTION '

                        for col in join_info[0]:
                            if (join_info[0][-1] == col):
                                print(col, end=' -- on the fly\n')
                                temp_proj = temp_proj + col + " -- on the fly"
                            else:
                                print(col, end=', ')
                                temp_proj = temp_proj + col + ", "

                        print("\t\tJOIN %s.%s = %s.%s -- BNLJ" % (
                            join_info[1][0], join_info[-1], join_info[1][1], join_info[-1]))
                        temp_join = ("\tJOIN %s.%s = %s.%s -- BNLJ" % (
                        join_info[1][0], join_info[-1], join_info[1][1], join_info[-1]))
                        temp_tab_name = ''
                        if i == 0:
                            print("\t%s\t\t%s" % (join_info[1][0], join_info[1][1]))
                            tab_name_temp = ("%s\t\t%s" % (join_info[1][0], join_info[1][1]))
                            qep_cost.append(self.countBNLJ(smallb_left, smallb_right))
                        else:
                            print("\t%s\t\t%s" % (join_info[1][1], join_info[1][0]))
                            tab_name_temp = ("%s\t\t%s" % (join_info[1][1], join_info[1][0]))
                            qep_cost.append(self.countBNLJ(smallb_right, smallb_left))
                        print("\tCost (worst case) : %d block" % qep_cost[i])  # 99 itu placeholder
                        data_calc_qep.append([temp_proj, temp_join, tab_name_temp, qep_cost[i]])

                    print(">> QEP optimal : QEP#%d" % (qep_cost.index(min(qep_cost)) + 1))
                    idxOptimal = qep_cost.index(min(qep_cost))
                    self.write_share_pool(raw_query, imp_data=data_calc_qep[idxOptimal])


                else:
                    print("Error query not valid")

            else:
                # ini bagian untuk where + selection
                # print("Bagian where")
                important_data = self.parseWhereQuery(query)
                # ambil nilai dari object table
                tab = self.getTable(self.tb, important_data.get('table_name'))
                col_valid = self.isColumnValid(important_data.get('projection'), important_data.get('table_name'))

                data_calc_qep = []
                if col_valid:
                    print("\tTabel(%d) : %s" % (1, tab.table_name))
                    print("\tList kolom : %s" % (str(tab.table_column)))
                    qep_cost = []
                    for i in range(0, 4):
                        print(">> QEP #%d" % (i + 1))
                        print("\tPROJECTION ", end='')
                        temp_proj = "PROJECTION "
                        for col in important_data.get('projection'):
                            if (important_data.get('projection')[-1] == col):
                                print(col, end=' -- on the fly\n')
                                temp_proj = temp_proj + col + " -- on the fly"
                            else:
                                print(col, end=', ')
                                temp_proj = temp_proj + col + ", "

                        reconstruct = ''
                        if important_data.get('condition') == None :
                            for part in important_data.get('condition'):
                                reconstruct = reconstruct + part + ' '
                            reconstruct = script.cleanString(reconstruct)
                        else :
                            reconstruct = None


                        smallb = self.calcb(tab.record_num, self.calcBfr(tab))
                        if (i == 0):
                            eq = 'A1 Key'
                            qep_cost.append(self.countA1Key(smallb))
                        elif i == 1:
                            eq = 'A1 No Key'
                            qep_cost.append(self.countA1NoKey(smallb))
                        elif i == 2:
                            eq = 'A2'
                            qep_cost.append(
                                self.countA2(smallb, self.db.getBlockSize(), tab.key_size, self.db.getTidSize()))
                        elif i == 3:
                            eq = 'A3'
                            qep_cost.append(
                                self.countA3(smallb, self.db.getBlockSize(), tab.key_size, self.db.getTidSize()))
                        print("\tSELECTION %s -- %s" % (reconstruct, eq))
                        print("\t%s" % important_data.get('table_name'))
                        print("\tCost (worst case) : %d block" % qep_cost[i])  # 99 itu placeholder

                        # temporary var untuk simpen bagian selection dari query
                        temp_sel = "SELECTION %s -- %s" % (str(reconstruct), eq)
                        # temporary var untuk pegang nilai bagian cost worstcase
                        temp_cost = "Cost (worst case) : %d block" % qep_cost[i]
                        data_calc_qep.append([temp_proj, temp_sel, tab.table_name, temp_cost])
                    print(">> QEP optimal : QEP#%d" % (qep_cost.index(min(qep_cost)) + 1))
                    idxOptimal = qep_cost.index(min(qep_cost))
                    self.write_share_pool(raw_query, imp_data=data_calc_qep[idxOptimal])
                else:
                    print("Error column not valid")



        else:
            print("Error query not valid")

######## ini function yg kepake
    def countA1Key (self,b : float) :
        """
        Hitung A1 with key
        :param b: ini small b
        :return: nilai A1 with key
        """
        return float(b/2)


######### Bagian hitung cost
    # sesuai rumus
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
        :param v: -> yg terakhir di data_dict sebelum hastag
        :param P: pointer size dari data_dict
        :return: float yg udah dihitung
        """
        import math
        # rumus
        # ceil(log(b)/log(floor(block_size / (v+p))) + b
        part1 = math.log(b)
        part2 = math.log(math.floor(block_size / (v + P)))
        part3 = math.ceil(part1/part2)
        return part3 + b

    def countBNLJ(self, br : float, bs : float):
        return float(br*bs)+br

#########


    #################### function lain
    # cek apakah table dengan nama table_nama ada
    # di class data
    def isTableExist(self,table_name : str):
        import formatting.script as script
        found = False
        table_name = script.cleanString(table_name)
        for tab in self.tb :
            if (table_name == tab.table_name) :
                found = True

        return found
    # ini cek apakah inputan user
    # lebih kecil dari record num di tabel tersebut
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

    # ambil tabel dari list dabel yang dikasih
    # klo tablenya ada
    def getTable(self,tb : list, table_name : str) :
        for tabel in tb :
            if (tabel.table_name.lower() == table_name.lower()) :
                #print ('x')
                return tabel

        return None
    ####################################






    # ini parsing untuk query join
    # ini misahin string terus kembaliin bagian penting
    def parseWhereQuery(self, query):
        import formatting.script as script
        query_parse = query.split('from')

        # SELECT nim, nama FROM Mahasiswa WHERE nim = 190;

        # part 1 -> isinya SELECT nim, nama
        # ini ambil elemen pertama dari array query_parse
        # ini misahin string jadi list di 'select'
        # terus ambil elemen terakhir dari string yg dipisahin
        column_projection_raw = query_parse[0].split('select')[-1]

        # bersihin column_projection_raw
        # karena mungkin aja *
        column_projection_raw = script.cleanString(column_projection_raw)


        # part 1 -> indeks 0 isinya select sama colomn buat projection
        # SELECT nim, nama FROM Mahasiswa JOIN Registrasi using (nim);
        # Ambil bagian ini nim, nama
        column_projection = []

        # dilanjutin di part 1.5

        # part 2 -> isinya Mahasiswa JOIN Registrasi using (nim);
        # ini misahin string jadi list di 'join'
        # table_name_raw akan berisi
        # ['Mahasiswa', 'nim = 190;']
        if ('where' in query_parse[-1]) :
            table_name_raw = query_parse[-1].split('where')
            ##### klo ada condition
            ###################
            # condition -> nim = 190
            cond = []
            for isi in script.cleanString(table_name_raw[-1]).split(' '):
                cond.append(script.cleanString(isi))
        else :
            table_name_raw = list(script.cleanString(query_parse[-1]))
            ###################
            # condition -> nim = 190
            cond = None
        #print(table_name_raw)

        # table_name_clean = bagian pertama indeks ke 0
        table_name = script.cleanString(table_name_raw[0])
        #print(table_name_raw[-1])
        #print(table_name_raw[-1].split(' '))

        # part 1.5
        # ini lanjutannya klo * jaga jaga

        if (column_projection_raw.lower() == '*'):
            # ini ambil semua kolomnya langsung
            column_projection = self.getTable(self.tb, table_name).table_column
        else:
            if (',' not in column_projection_raw):
                column_projection.append(column_projection_raw)
            else:
                # ini klo ada comma
                for column_name in column_projection_raw.split(','):
                    column_projection.append(script.cleanString(column_name))


        #############

        temp = {'projection' : column_projection, 'table_name' : table_name, 'condition': cond }
        return (temp)
        ################

    # ini parsing untuk query where
    # ini misahin string terus kembaliin bagian penting
    def parseJoinQuery(self, query):

        # SELECT nim, nama FROM Mahasiswa JOIN Registrasi using (nim);
        import formatting.script as script
        query_parse = query.split('from')

        # part 1 -> isinya SELECT nim, nama
        # ini ambil elemen pertama dari array query_parse
        # ini misahin string jadi list di 'select'
        # terus ambil elemen terakhir dari string yg dipisahin
        column_projection_raw = query_parse[0].split('select')[-1]

        # bersihin column_projection_raw
        # karena mungkin aja *
        column_projection_raw = script.cleanString(column_projection_raw)


        # part 1 -> indeks 0 isinya select sama colomn buat projection
        # SELECT nim, nama FROM Mahasiswa JOIN Registrasi using (nim);
        # Ambil bagian ini nim, nama
        column_projection = []


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


        # part 1.5
        # ini lanjutannya klo * jaga jaga
        print(type(column_projection_raw))
        print(table_name)
        if (column_projection_raw == '*'):
            # ini ambil semua kolomnya langsung
            temp_tab = self.getTable(self.tb, table_name[0])
            column_projection = temp_tab.table_column
        else:
            if (',' not in column_projection_raw):
                column_projection.append(column_projection_raw)
            else:
                # ini klo ada comma
                for column_name in column_projection_raw.split(','):
                    column_projection.append(script.cleanString(column_name))

        print(column_projection)
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


    # ini cek apa kolom di query
    # sama untuk no 3 searching
    def isColumnValid(self, column : list, table_name : str):

        table_col = self.getTable(self.tb, table_name)


        inTabel = True


        for col in column :
            if (col.lower() not in table_col.table_column) :
                inTabel = False

        return inTabel


    ################## FIlE I/O
    ######### Write to file shared_pool.txt
    def write_share_pool(self, query : str, imp_data : list):
        import os
        with open(self.folder_name + "shared_pool.txt", 'a') as file :
            if (os.stat(self.folder_name + "shared_pool.txt").st_size != 0) :
                file.write('\n')
            file.write(query+'\n')
            for line in imp_data :
                file.write(str(line)+'\n')

    ######### ini read file shared_pool.txt
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







