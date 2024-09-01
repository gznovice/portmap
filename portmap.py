import asyncio
import socket
import os
from data_encode import base_encode
#test only, test finished
#from no_data_encode import no_data_encode
#from xor_data_encode import xor_data_encode
#XOR_KEY=int(os.getenv("XOR_KEY")).to_bytes(1, byteorder='big')
#test only end

TEST_SERVER=os.getenv("TEST_SERVER")
TEST_PORT=int(os.getenv("TEST_PORT"))

class portmap:
    def __init__(self, listen_port, remote_host, remote_port, encoder):
        self.listen_port=listen_port
        self.remote_host=remote_host
        self.remote_port=remote_port
        self.server_socket=None
        self.encoder=encoder

    #handle connection    
    #1)connect to target address
    #2)relay read write
    #3)should handle encode/decode later
    async def handle_connect(self, reader, writer):
        try:
            remote_reader, remote_writer = await asyncio.open_connection(self.remote_host, self.remote_port)

            async def relay(_reader, _writer):
                try:
                    while True:
                        data = await _reader.read(4096)
                        if not data:
                            break
                        data = self.encoder.encode(data)
                        _writer.write(data)
                        await _writer.drain()
                except ConnectionResetError as e:
                    print(f"ConnectionResetError occurred: {e}")
                except asyncio.CancelledError:
                    pass
                except Exception as e:
                    print(f"exception occurred: {e}")

            local_to_remote = asyncio.create_task(relay(reader, remote_writer))
            remote_to_local = asyncio.create_task(relay(remote_reader, writer))
            done, pending = await asyncio.wait([local_to_remote, remote_to_local],
                                               return_when=asyncio.FIRST_COMPLETED)
            for task in pending:
                task.cancel()
            print("all task finished")

        except OSError as e:
            print(f"OSError:{e}") 
        except TimeoutError as e:
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
    # portmap_server = portmap(4320, TEST_SERVER, TEST_PORT, xor_data_encode(XOR_KEY))
    # portmap_server2 = portmap(4321, "127.0.0.1", 4320, xor_data_encode(XOR_KEY))

    # async def startSever(server):
    #     await server.start()
    
    # print("see me??")
   

    # server1 = asyncio.create_task(startSever(portmap_server))
    # server2 = asyncio.create_task(startSever(portmap_server2))

    # # Run both servers concurrently
    # await asyncio.gather(server1, server2)


    #portmap_server = portmap(4321, TEST_SERVER, TEST_PORT, no_data_encode())
    #await portmap_server.start()
    print("see me2??")

if __name__ == "__main__":
    asyncio.run(main())