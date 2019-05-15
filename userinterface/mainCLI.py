import classmodels.data as data


# ini main cli butuh object data untuk parameter
def mainCLI(dt : data.data) :
    shouldrun = True
    while (shouldrun) :
        print(
            """>> Menu Utama:
    [1]\tTampilkan BFR dan Fanout Ratio Setiap Tabel
    [2]\tTampilkan Total Blok Data + Blok Index Setiap Tabel
    [3]\tTampilkan Jumlah Blok yang Diakses Untuk Pencarian Rekord
    [4]\tTampilkan QEP dan Cost
    [5]\tTampilkan Isi File Shared Pool"""
        )
        # input user
        inp = input(">> Masukan Pilihan Anda: ")
        print('\n')
        if (inp == '1'):
            bfr_fanout_CLI(dt)
        elif (inp == '2'):
            blocking_CLI(dt)
        elif (inp == '3'):
            record_search_CLI(dt)
        elif (inp == '4'):
            print("QEP")
            qep_CLI(dt)
        elif (inp == '5'):
            print("Shared Pool")
            sharedpool_CLI(dt)
        elif (inp.lower() == 'exit'):
            print(">> Exitting")
            shouldrun = False
        else:
            print("Unknown")


# klo pilih 1
def bfr_fanout_CLI(dt : data.data) :
    print("Menu 1 : BFR dan Fan Out Ratio")
    for tbl in dt.tb :
        print("BFR %s \t: %d" % (tbl.table_name, dt.calcBfr(tbl)))
        print("Fan Out Ratio %s \t: %d" % (tbl.table_name, dt.calcFanout(tbl)))
    print('\n')
    input("Press Enter to continue ....")

# klo pilih 2
def blocking_CLI(dt : data.data) :
    print("Menu 2 : Jumlah Blok")
    for tbl in dt.tb :
        print("Tabel Data %s \t: %d \tblok" % (tbl.table_name, dt.calcJmlBlok(tbl)))
        print("Indeks %s \t\t: %d \tblok" % (tbl.table_name, dt.calcIndeksBlock(tbl)))
    print('\n')
    input("Press Enter to continue ....")


# klo pilih 3
def record_search_CLI(dt : data.data) :
    print("Menu 3 : Pencarian Rekord")
    print("Input:")

    # cobain
    try :
        # minta input
        # coba ubah ke type integer dari default typr string
        record_ke = int(input(">> Cari Rekord ke- : "))
    except Exception as e :
        # set data jadi None klo input bukan integer
        record_ke = None

    # cek apakah input valid -> isinya integer seharusnya
    if record_ke != None :
        # minta input
        # set data ke tbl_name
        tbl_name = input(">> Nama Tabel : ")

        # cek apakah table ada di data
        if dt.isTableExist(tbl_name) :
            # cek apakah table ada di data
            if (dt.validateRecordPosition(tbl_name,record_ke)) :
                print("Output:")
                print(">> Menggunakan indeks, jumlah blok yang diakses : %d blok" % dt.searchIndeks(tbl_name, record_ke))
                print(">> Tanpa indeks, jumlah blok yang diakses : %d blok" % dt.searchNoIndeks(tbl_name, record_ke) )

            # ini klo index gk sesuai
            else :
                # index kurang dari 0
                # index > record_num dari table
                print ("Index invalid")

            # ini pause biar teken enter dulu
            input("Press Enter to continue ....")

        # ini klo table gk ada
        else :
            # yup table gk ada
            print("Error Table not Found")
            input("Press Enter to continue ....")

    # ini klo isi record_ke -> isinya bukan integer
    else :
        # cetak invalid input
        print("Error invalid input")
        input("Press Enter to continue ....")

# klo pilih 4
def qep_CLI(dt : data.data) :
    print("Menu 4 :  QEP dan Cost")
    print("Input Query:")
    query = input(">> ").lower()
    dt.calcQEPnCost(query)
    input("Press Enter to continue ....")

# klo pilih 5
def sharedpool_CLI(dt : data.data) :
    print("Menu 5 :  Shared Pool")
    dt.print_shared_pool()
    input("Press Enter to continue ....")

