import requests

BASE_URL = "https://blockchain.info"

class APIRequestError(Exception):
    """Custom exception for API request failures."""
    def __init__(self, status_code, message, url):
        super().__init__(f"Error {status_code} for {url}: {message}")
        self.status_code = status_code
        self.message = message
        self.url = url

def make_request(endpoint, method="GET", params=None, data=None, json_data=None, headers=None):
    url = f"{BASE_URL}{endpoint}"
    
    response = requests.request(
        method=method,
        url=url,
        params=params,
        data=data,
        json=json_data,
        headers=headers
    )

    # Raise an exception if the request failed
    if not response.ok:
        raise APIRequestError(response.status_code, response.text, url)
    
    return response.json()

def addresses_balance(addresses=[]):
    addresses_param="|".join(addresses)
    try:
        balance_data = make_request("/balance", params={"active": addresses_param})  # GET request
        print(balance_data)
        return balance_data
    except APIRequestError as e:
        print(f"API call failed: {e}")


def addresses_rawaddr(address,limit=50,offset=0):
    try:
        addr_data = make_request(f"/rawaddr/{address}",params={"limit":limit,"offset":offset})  # GET request
        return addr_data
    except APIRequestError as e:
        print(f"API call failed: {e}")
