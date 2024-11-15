
import http.client; 
import json; 

api_url = "api.cloudflare.com"
auth = "Bearer AYN-4DzJ-9aDD3VsqLeujprnlSqz73-jxeVc8NYT"

request = ""

zone_name = ".1009theeagle.com"

zone_identifier = "178c758c1e27bd10302d41ca5c536370"
base_url_get_records = f"/client/v4/zones/{zone_identifier}/dns_records"

get_record_name = f"em._domainkey999999999999{zone_name}"
get_record_id = ""
base_url_delete_record = f"/client/v4/zones/{zone_identifier}/dns_records/{get_record_id}"

content_type = "application/json"
content = "dkim.emailcampaigns.net9999"
name = "em._domainkey999999999999"
proxied = False
type = "CNAME"
comment = "Campaigner DKIM99999"
ttl = 3600

conn = http.client.HTTPSConnection(api_url)

headers = {
    'Content-Type': content_type,
    'Authorization': auth
    }

payload = {
    "content":content,
    "name":name,
    "proxied":proxied,
    "type":type,
    "comment":comment,
    "ttl":ttl
    }
           
payload_json = json.dumps(payload)

error_code = 0
error_text = ""

#conn.request("POST", "/client/v4/zones/{zone_identifier}/dns_records", payload_json, headers); 
#conn.request("DELETE", base_url_delete_record, headers=headers)
conn.request("GET", base_url_get_records, headers=headers)

response_text = conn.getresponse().read(); 
response_data = json.loads(response_text.decode()); 

# Find the specific record to update
record_id = None
result_array = response_data['result']
for record in result_array:
    if record['name'] == get_record_name:
        record_id = (record['id']) 
#for record in result_array:
#    if record['content'] == "v=spf1 -all": print(record['id']) 
#if response_data['result'][0]['content'] == "v=spf1 -all": print(record['id']) 

if response_data["errors"]:
    error_code = response_data["errors"][0]["code"]
if error_code:
    error_text = error_code_map.get(error_code, "Unknown Error")
        
if request != "GET" and response_data["success"]:
    result = (
        f"\n\n"
        f"****Success!****\n"
        f"The following {response_data["result"]["type"]} record was added...\n"
        f"Domain: {response_data["result"]["zone_name"]}\n"
        f"Name: {response_data["result"]["name"]}\n"
        f"Value: {response_data["result"]["content"]}\n"
        f"Comment: {response_data["result"]["comment"]}\n"
        f"****************"
        f"\n\n"
        ) 

else:
    result = (
        f"\n\n"
        f"!!!!Operation failed!!!!  "
        f"Error: {error_code} - {error_text}"
        f"\n\n"
        )

# print(payload_json)
#print(response_data["success"])
#print(result)
#print(response_text)
#print(base_url)
#print(result)
#print(result_array)
#print("Error:", error_text)
#print(error_code)
