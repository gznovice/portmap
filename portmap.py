import asyncio
import socket
import os
from data_encode import base_encode
#import base_host_selector don't need
#test only, test finished
###from no_data_encode import no_data_encode
###from xor_data_encode import xor_data_encode
###XOR_KEY=int(os.getenv("XOR_KEY")).to_bytes(1, byteorder='big')


###TEST_SERVER=os.getenv("TEST_SERVER")
###TEST_PORT=int(os.getenv("TEST_PORT"))
#test only end
BYTES_PER_READ = 4096
RUBBISH_DATA_LEN = 4096
RUBBISH_DATA = b'A'*RUBBISH_DATA_LEN
DATA_END_FLAG = b'ZZQ_WXJ_K_END'

class portmap:

    def __init__(self, listen_port, remote_host, remote_port, encoder, mode=0, host_selector = None):
        self.listen_port=listen_port
        self.remote_host=remote_host
        self.remote_port=remote_port
        self.server_socket=None
        self.encoder=encoder
        self.mode=mode    #now we have 0, 1, 2 mode
        self.host_selector=host_selector
        #the following is for mode 2 
        self.remote_reader_byte_received=0
        self.remote_writer_byte_sent=0
    
    def __refresh_host(self):
        self.remote_host, self.remote_port = self.host_selector.get_host()

    #handle connection    
    #1)connect to target address
    #2)relay read write
    #3)should handle encode/decode later
    async def handle_connect(self, reader, writer):
        try:  
            self.__refresh_host()

            remote_reader, remote_writer = await asyncio.open_connection(self.remote_host, self.remote_port)
            

            async def normal_relay(_reader, _writer, remote_to_local = False):
                try:                    
                    while True:
                        data = await _reader.read(BYTES_PER_READ)
                        if not data:
                            break
                        if remote_to_local:
                            self.remote_reader_byte_received += len(data)
                            
                        data = self.encoder.encode(data)
                        _writer.write(data)
                        await _writer.drain()
                except ConnectionResetError as e:
                    print(f"ConnectionResetError occurred: {e}")
                except asyncio.CancelledError:
                    pass
                except Exception as e:
                    print(f"exception occurred: {e}")
                    

            async def rubbish_handle_relay(_reader, _writer):
                try:                    
                    buffer = b''
                    while True:
                        data = await _reader.read(BYTES_PER_READ)
                        if not data:
                            break        

                        
                        buffer += data
                        if buffer.startswith(RUBBISH_DATA):
                            buffer = buffer[RUBBISH_DATA_LEN:]   
                            #print("rubbish found")                         
                            continue

                        if DATA_END_FLAG in buffer:
                            #Split the data at "end"
                            useful_data, buffer = buffer.split(DATA_END_FLAG, 1)
                            data = self.encoder.encode(useful_data)
                        else:
                            continue
                            
                        _writer.write(data)
                        await _writer.drain()                        

                except ConnectionResetError as e:
                    print(f"ConnectionResetError occurred: {e}")
                except asyncio.CancelledError:
                    pass
                except Exception as e:
                    print(f"exception occurred: {e}")

            async def rubbish_creator_relay(_reader, _writer):
                try:
                    async def send_rubbish(__write, diff):                        
                        cnt = diff/2
                        while cnt > 0:                            
                            __write.write(RUBBISH_DATA)
                            cnt -= RUBBISH_DATA_LEN
                            await __write.drain()
                        self.remote_writer_byte_sent += diff
                
                  
                    while True:
                        data = await _reader.read(BYTES_PER_READ)
                        if not data:
                            break 

                        data = self.encoder.encode(data) +  DATA_END_FLAG
                        _writer.write(data)
                        #await _writer.drain()
                        
                        await send_rubbish(_writer, self.remote_reader_byte_received - self.remote_writer_byte_sent)
                except ConnectionResetError as e:
                    print(f"ConnectionResetError occurred: {e}")
                except asyncio.CancelledError:
                    pass
                except Exception as e:
                    print(f"exception occurred: {e}")                    

            if self.mode == 0:                
                local_to_remote = asyncio.create_task(normal_relay(reader, remote_writer, False))
                remote_to_local = asyncio.create_task(normal_relay(remote_reader, writer, True))
            elif self.mode == 1:                
                local_to_remote = asyncio.create_task(rubbish_handle_relay(reader, remote_writer))
                remote_to_local = asyncio.create_task(normal_relay(remote_reader, writer, True))
            elif self.mode == 2:                
                local_to_remote = asyncio.create_task(rubbish_creator_relay(reader, remote_writer))
                remote_to_local = asyncio.create_task(normal_relay(remote_reader, writer, True))
            
            
            done, pending = await asyncio.wait([local_to_remote, remote_to_local],
                                               return_when=asyncio.FIRST_COMPLETED)
            for task in pending:
                task.cancel()
            print("all task finished")

        
        except OSError as e:
            print(f"see OSError:{e}") 
        except asyncio.TimeoutError as e:
            print(f"timed out when connecting remote server:{e}")            


    #create server socket and listen to client connection
    async def start(self):
        try:            
            # #host='', bind to all the adapter           
            host=''
            server = await asyncio.start_server(self.handle_connect, host, self.listen_port)    
                        

            async with server:
                await server.serve_forever()
            
            # #non-blocking server socket
            # self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            # self.server_socket.setblocking(False)

            # #host='', bind to all the adapter
            # host=''
            # self.server_socket.bind(host, self.listen_port)
            # self.server_socket.listen()
            # print(f"listening on port {self.listen_port}")

            # #handle connect
            # conn, addr = self.server_socket.accept()
            # ret = await self.handle_connect(self, conn)
            # return ret
        except socket.error as e:
            print(f"Socket error: {e}")
            return False
        except Exception as e:
            print(f"Other error: {e}")
            return False




async def main():
    # Your main code here
    print("Hello, World!")
    #test only, test finished
    #portmap_server = portmap(4320, TEST_SERVER, TEST_PORT, no_data_encode(), 0)
    ###portmap_server = portmap(4320, TEST_SERVER, TEST_PORT, xor_data_encode(XOR_KEY), 1)
    ###portmap_server2 = portmap(4321, "127.0.0.1", 4320, xor_data_encode(XOR_KEY), 2)

    ###async def startSever(server):
    ###    await server.start()    
    
   

    ###server1 = asyncio.create_task(startSever(portmap_server))
    ###server2 = asyncio.create_task(startSever(portmap_server2))

    # # Run both servers concurrently
    ###await asyncio.gather(server1, server2)


    #portmap_server = portmap(4321, TEST_SERVER, TEST_PORT, no_data_encode())
   # await portmap_server.start()    

if __name__ == "__main__":
    asyncio.run(main())