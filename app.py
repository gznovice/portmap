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

    portmap_server = portmap(config["port"], config["target_addr"], config["target_port"], base_encode.generate(config["algo"]))
    await portmap_server.start()
   

if __name__ == "__main__":
     asyncio.run(main())