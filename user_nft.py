import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_key = os.getenv("minter_key")

def user_nft(address, chain):
    query_params = {
        "chain": chain,
        "page_size": 50,
        "continuation": None,
        "include": "default"
    }

    headers = {
        "accept": "application/json",
        "Authorization": API_key
    }

    url = "https://api.nftport.xyz/v0/accounts/{}".format(address)

    response = requests.get(
        url,
        headers=headers,
        params=query_params,
    )

    print(response.text)

user_nft("0xde5F7152F7A0Ec65CDf8471CcfB468094f3875Dc", "goerli")