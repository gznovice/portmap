from base_host_selector import base_host_selector

from typing import List
from typing import Tuple
import random
import json

#test only
import time
#test end

HOSTS_JSON = "hosts.json"



class host_selector(base_host_selector):

    def __readconfig(self) -> List:
        try:
            with open(HOSTS_JSON, 'r') as file:
                return json.load(file)
        except Exception as e:
            print(f"error when loading config:{e}")        
            return []

    def __init__(self) -> None:
        self.default_hosts = self.__readconfig()
        self.unselected_hosts = self.default_hosts.copy()     
    
    def get_host(self) -> Tuple[str, int]:

        if len(self.default_hosts) == 0:
            return None
        
        if len(self.unselected_hosts) == 0:
            self.unselected_hosts = self.default_hosts.copy()
        


        # Extract the weights
        weights = [host_item["weight"] for host_item in self.unselected_hosts]

        selected_item = random.choices(self.unselected_hosts, weights=weights, k=1)[0]

        print(f"after random:{selected_item}")

        self.unselected_hosts.remove(selected_item)

        return (selected_item["host"], selected_item["port"])

    

def main():
    # Your main code here
    print("Hello, World!")    
    one_selector = host_selector()
    while True:
        one_host = one_selector.get_host()
        print(f"current host:{one_host}")
        time.sleep(1)


if __name__ == "__main__":
    main()