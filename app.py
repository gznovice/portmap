from config_reader import read_conf
from data_encode import base_encode
from portmap import portmap
import asyncio

#file content should be changed when deploying
CONFIG_FILE="config.json"

async def main():
    # Your main code here
    print("Hello, World!")
        
    config = read_conf(CONFIG_FILE)

    # add mode parameter, when mode = 0, no rubbish data send or recv, when mode = 1, will receive
    # rubbish data from local server port, should handle it, when mode = 2, will send rubbish data using remote socket
    # mode 1 and mode 2 should be paird, mode 0 and mode 0 should be paired
    portmap_server = portmap(config["port"], config["target_addr"], config["target_port"], base_encode.generate(config["algo"]), config.get("mode", 0))
    await portmap_server.start()
   

if __name__ == "__main__":
     asyncio.run(main())