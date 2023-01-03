import sys, socket, psycopg2, logging, datetime
from _thread import start_new_thread

# HOST = "127.0.0.1" --> sys.argv[1]
# PORT = 65430 --> sys.argv[2]
class Server:

    db_cursor = None
    list_of_clients = []
    
    def __init__(self, host, port ) -> None:
        # self.connect_to_postgresql()
        self.connect_server(host, port)

    def client_thread(self, conn,addr):

        logging.basicConfig(filename="logging/log_file.log", filemode="a", level=logging.DEBUG)  

        with conn:
            # tidak masalah pembuatan komponen label koneksi disini
            # karena kalaupun koneksi gagal maka statusnya bisa dicek ama looping cek koneksi pada program client_service
            # lagipula disini sudah ada append list utk ip client

            # yg memebdakan satu client dengan client yg lain adalah ip ny
            # sementara pada penamaan komponen label harus ada hubungan/integrasi antara client yg konek dengan name 
            # komponent tersebut

            self.list_of_clients.append(addr)
            print(f"Connected by {addr}")
            
            # create label component

            try:
                while True:
                    data = conn.recv(1024)
                    msg = data.decode("utf-8")
                    # print(data.decode("utf-8"))
                    
                    if(msg==''):
                        print(f"client{addr} disconnected at {datetime.datetime.now()}")
                        logging.warning(f"client{addr} disconnected at {datetime.datetime.now()}")
                    elif(msg!=''):
                        print(data.decode("utf-8"))
                    
                    if not data:
                        break
            except:
                print(f"client{addr} disconnected at {datetime.datetime.now()}")
                logging.warning(f"client{addr} disconnected at {datetime.datetime.now()}")


    def connect_server(self, h, p):
        
        # while true -> fro server socket always stanby, event after client connection break/fail
        while True:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.bind((h, p))
                s.listen()
                conn, addr = s.accept()
                
                t = start_new_thread(self.client_thread, (conn, addr))
                
                # with conn:
                #     print(f"Connected by {addr}")
                    


                #     while True:
                #     #     data_send = ""
                #         data = conn.recv(1024)
                #         print(data.decode("utf-8"))
                #         if not data:
                #             break
                        
                    #     byte_len = len(data)
                    #     start_index = len(data) - 6
                    #     flag = data[start_index:byte_len]

                    #     # self.write_image(data, byte_len)
                       
                    #     # if has image flag --> write image file in server
                    #     # if( flag==b'\x0fimage' ):
                    #         # print("ok")
                    #         # self.write_image(data, byte_len)

                    #     # print(data[start_index:byte_len])

                    #     # server bridge here( bytes decode to string ) 
                    #     data_to_str = data.decode("utf-8")
                    #     dt_split = data_to_str.split("#")

                    #     # # filter data based on flag
                    #     if(dt_split[1] == "rfid"):
                    #         # if rfid --> check to DB
                    #         query = "select count(*) as jum from pegawai where rfid_pegawai='"+dt_split[0]+"';"
                    #         fetch_res = self.exec_and_fetch( query )

                    #         print(query)
                    #         print(fetch_res)

                    #         if fetch_res[0]==1:
                    #             data_send='true' 
                    #         else: 
                    #             data_send='false'

                    #     # sen data back to client
                    #     conn.sendall( bytes(data_send, 'utf-8') )
                    #     # conn.sendall( bytes("berhasil", 'utf-8') )
                        
    def connect_to_postgresql(self):
        conn = psycopg2.connect(
            database="parkir", user='Admin', password='', host='127.0.0.1', port= '5432'
        )
        self.db_cursor = conn.cursor()

    
    def exec_and_fetch(self, query):
        self.db_cursor.execute(query)
        data = self.db_cursor.fetchone()

        return data

    def write_image(self, img_bytes, byte_length):
        # clear flag
        # clear_size = byte_length - 6
        # print(img_bytes)
        # print(f"cs: {clear_size}") 
        w = open("tes_img.png", "wb")
        w.write(img_bytes)
        # w.write(img_bytes[:clear_size])

# run server
Server(sys.argv[1], int(sys.argv[2]))            