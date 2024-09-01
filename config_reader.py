import json

def main():
    # Your main code here
    print("Hello, World!")

"""
config_data is a dict 
{
    "listen_port":443,
    "algo":0,
    "dest_addr":"google.com",
    "dest_port":443
}
"""
def read_conf(file_name):
    try:
        with open(file_name, 'r') as file:            
            content = file.read()
            config = json.loads(content)
            return config
    except FileNotFoundError:
        print(f"Error: The file {file_name} does not exist.")
    except json.JSONDecodeError:
        print(f"Error: The file {file_name} is not a valid JSON.")
    except Exception as e:
        print(f"Other exception is found: {e}.")
    
def main():
    read_conf("config.json")


if __name__ == "__main__":
    main()