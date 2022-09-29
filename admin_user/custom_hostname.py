import json
from urllib import response
import requests
from django.conf import settings


# Create Custom Hostname "Ex : 'https://api.cloudflare.com/client/v4/zones/023e105f4ecef8ad9ca31a8372d0c353/custom_hostnames'"
def create_custom_hostname(whitelabeldomian):

    header = {
        'content-type': 'application/json',
        'X-Auth-Email': settings.CLOUDFLARE_ACCOUNT_EMAIL,
        'X-Auth-Key': settings.CLOUDFLARE_ACCOUNT_TOKEN
    }
    # print(whitelabeldomian, "**********")
    payload = {
        "hostname": str(whitelabeldomian),
        "ssl": {
            "method": "http",
            "type": "dv",
            "settings": {
                "min_tls_version": "1.0"
            }
        }
    }

    url = f'{settings.CLOUDFLARE_API_URL}zones/{settings.CLOUDFLARE_ZONE_ID}/custom_hostnames'
    # url = "https://api.cloudflare.com/client/v4/zones/8b3ecd66cf4b713a7aa021d24610dae0/custom_hostnames"
    # response = requests.get(url, headers=header, data=payload)
    response = requests.post(url, headers=header, data=json.dumps(payload))

    json_response = response.json()

    return json_response


# Delete Custom Hostname "Ex : 'https://api.cloudflare.com/client/v4/zones/023e105f4ecef8ad9ca31a8372d0c353/custom_hostnames/0d89c70d-ad9f-4843-b99f-6cc0252067e9'"
def delete_custom_hostname(id):
    header = {
        'content-type': 'application/json',
        'X-Auth-Email': settings.CLOUDFLARE_ACCOUNT_EMAIL,
        'X-Auth-Key': settings.CLOUDFLARE_ACCOUNT_TOKEN
    }

    payload = {
        'id': id
    }

    url = f'{settings.CLOUDFLARE_API_URL}zones/{settings.CLOUDFLARE_ZONE_ID}/custom_hostnames/{id}'

    response = requests.delete(url, headers=header, data=json.dumps(payload))
    json_response = response.json()
    # print(json_response)
    # print(json_response['status'])
    return json_response

def custom_hostname_detail(id):
    header = {
        'content-type': 'application/json',
        'X-Auth-Email': settings.CLOUDFLARE_ACCOUNT_EMAIL,
        'X-Auth-Key': settings.CLOUDFLARE_ACCOUNT_TOKEN
    }

    payload = {
        'id': id
    }

    url = f'{settings.CLOUDFLARE_API_URL}zones/{settings.CLOUDFLARE_ZONE_ID}/custom_hostnames/{id}'

    response = requests.get(url, headers=header, data=json.dumps(payload))
    json_response = response.json()
    # print(json_response)
    # print(json_response['status'])
    return json_response