import requests


def query_api(id, question):
    base_url = "http://localhost:5000/api/response/get"
    url = f"{base_url}/{id}"
    params = {'question': question}
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        print("Response from API:", response.text)
    else:
        print("Failed to get response from API, status code:", response.status_code)


## REPLACE WITH THE ID OF BOT
ID_TEST = 'fedfd51a-5aad-4f2a-8393-90edc3d91ea4'
query_api(ID_TEST, "Recommend me a blog")