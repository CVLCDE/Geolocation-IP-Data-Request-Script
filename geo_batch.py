import requests
import json
from time import sleep
ENDPOINT = "http://ip-api.com/batch"

def build_master_list(f):
    master_list = open(f).read().split()
    return master_list

def build_groups(m_list):
    for i in range(0, len(m_list), 10):
        print('<---------------------------------------->')
        print(f"Group {i} - {i+10} built -> passing to api post")
        group = m_list[i:i+10]
        post_to_api(group)
        print(f'<---------------------------------------->\n')

def post_to_api(group):
    jsonified_group = json.dumps(group)

    try:
        request = requests.post(url=ENDPOINT, data=jsonified_group)
        status_code = request.status_code
        headers = request.headers
    except:
        print("!!!ERROR!!! -> Something went wrong with the POST request")
        pass

    print(f"Status Code: {status_code}")
    if status_code == 200:
        print("Adding group to output file")
        geo_data = request.json()
        add_to_output_file(geo_data)
    elif status_code != 200:
        time_to_sleep = int(headers["X-Ttl"]) + 2
        print(f"SLEEPING for {time_to_sleep}")
        sleep(time_to_sleep)
        post_to_api(group)
        print(f"Trying this group again {group}")

def add_to_output_file(geo_data):
    output_file = open("geo_batch geolocation results.txt", "a")
    
    for obj in geo_data:
        status = obj["status"]
        query = obj["query"]
        try:
            if status == "success":    
                country = obj["country"]
                city = obj["city"]
                org = obj['org']
                region = obj["region"]
                desired_data = f"{query},{city},{region},{country},{org}\n"
            else:
                message = obj["message"]
                desired_data = f"{query},{message}\n"
            
            print("Writing to output file")
            output_file.write(desired_data)
        except:
            print("!!!ERROR!!! -> Could not find JSON attribute for obj")

    output_file.close()

def main():
    m_list = build_master_list("all.txt")
    build_groups(m_list)
    print("Output file complete, program is finished")

main()