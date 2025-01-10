import requests
import json

ip = ''
urls = [
    f"https://ipinfo.io/{ip}?token=KEY",
    f"https://ipwho.is/{ip}",
    f"https://get.geojs.io/v1/ip/geo/{ip}.json",
    f"https://api.theipapi.com/v1/ip/{ip}?api_key=KEY",
    f"http://proxycheck.io/v2/{ip}?key=KEY&vpn=1&asn=1&node=1&time=1&inf=1&risk=2&port=1&seen=1",
]

def fetch_ip_info(urls):
    all_info = []

    for url in urls:
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            # print(f"Data from {url}: {json.dumps(data, indent=2)}")
            all_info.append(data)
        except requests.RequestException as e:
            print(f"Error fetching data from {url}: {e}")
        except json.JSONDecodeError:
            print(f"Error decoding JSON response from {url}")

    return all_info
def merge_ip_data(data_list):
    merged_data = {}
    
    for data in data_list:
        for key, value in data.items():
            if key in ['organization', 'org', 'organization_name']:
                key = 'organization'

            if key in ['country_code3', 'country_code']:
                key = 'country_code'

            if key not in merged_data:
                merged_data[key] = value
            elif isinstance(value, dict) and isinstance(merged_data[key], dict):
                merged_data[key].update(value)
            elif isinstance(value, list) and isinstance(merged_data[key], list):
                merged_data[key].extend(x for x in value if x not in merged_data[key])
            elif isinstance(value, str) and key == 'organization':
                if value not in merged_data[key]:
                    merged_data[key] += f", {value}"
            else:
                merged_data[key] = value

    return merged_data


ip_info = fetch_ip_info(urls)
merged_info = merge_ip_data(ip_info)
with open("merged_ip_info.json", "w") as json_file:
    json.dump(merged_info, json_file, indent=4)
print("\nMerged IP Information saved to 'merged_ip_info.json':\n")
print(json.dumps(merged_info, indent=4))
