import requests
from dotenv import load_dotenv
import os

load_dotenv()
API_key = os.getenv("minter_key")

def mint_on_polygon(file_url, extension, name, description, address):
    query_params = {
        "chain": "goerli",
        "name": name,
        "description": description,
        "mint_to_address": address
    }

    file = open(name+'.'+extension, 'wb')
    file.write(requests.get(file_url).content)
    file.close()
    file = open(name + '.' + extension, 'rb')

    response = requests.post(
        "https://api.nftport.xyz/v0/mints/easy/files",
        headers={"Authorization": API_key},
        params=query_params,
        files={"file": file}
    )

    file.close()
    os.remove(name+'.'+extension)



    print(response.text)


mint_on_polygon("https://images.all-free-download.com/footage_preview/mp4/wild_butterfly_in_nature_6891914.mp4",
                "mp4","mp4_nft_test_1",
                "This is the first video NFT test",
                "0xB61DE5AF42F08a32e49cA72c46E21731D20a8FB4")