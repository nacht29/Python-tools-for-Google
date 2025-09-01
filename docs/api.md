# api.py

## Set up

1. Include the following:
	- OAuth2 client credentials 
	- Access token url
	- Base url for API endpoints, to easily combine with the API endpoint urls
2. Recommended: store the client credentials in the environment or use Secret Manager and access the secret using service account credentials.

```py
CLIENT_ID = 'E7F82A1B-CC34-4B21-A855-D3298BF751CD'
CLIENT_SECRET = '89D3E1F2-7B45-4C82-91A6-B8D72FAA34C7'
TOKEN_URL = 'https://school.isamshosting.cloud/auth/connect/token'
API_BASE_URL = 'https://school.isamshosting.cloud'
```

---

## gen_access_token

#### **Definition:**
```py
def gen_access_token(token_url:str, client_id:str, client_secret:str, api_base_url:str) -> str:
```

#### **Parameters:**
- `token_url`: The url used to generate access token using OAuth2 to send API requests.
- `client_id`: ID or username of the OAuth2 client.
- `client_secret`: Oauth2 client password.
- `api_base_url`: Base url for all API endpoints you are working with.

#### **Function call:**
```py
access_token = gen_access_token(
	token_url=TOKEN_URL,
	client_id=CLIENT_ID,
	client_secret=CLIENT_SECRET,
	api_base_url=API_BASE_URL
)
```

#### **Use case:**
Generate access token based on OAuth2 Client credentials. The token is used for authentication when sending API requests.

#### **Return value:**
- Type: string
- Returns a string acces token to be used when sending API requests.


---

## api_get

#### **Definition:**
```py
def api_get(access_token:str, api_url:str, content_type:str=None, params:dict=None) -> Any:
```

#### **Parameters:**
- `access_token`: Access toke string generated from [`gen_access_token`](https://github.com/nacht29/Python-tools-for-Google/blob/main/docs/api.md#gen_access_token).
- `api_url`: The url of the API endpoint your script/programme is communicating with.
- `content_type`: The content type of the data payload to be received. The standard is `'application/json'`.

#### **Function call:**
```py

endpoint_url = "/api/students"

access_token = gen_access_token(
	token_url=TOKEN_URL,
	client_id=CLIENT_ID,
	client_secret=CLIENT_SECRET,
	api_base_url=API_BASE_URL
)

# call api_get() here
api_response = api_get(
	access_token,
	api_url=f'{API_BASE_URL}{endpoint_url}',
	content_type='application/json'
)
```

#### **Use case:**
Send API get requests and receive a data payload.

#### **Return value:**
- Type: Any
- Returns the JSON-decoded response body if the API request succeeds:
	- `dict` if the response contains a JSON object.
	- `list` if the response contains a JSON array.
	- Other JSON types (`str`, `int`, `float`, `bool`) depending on API response.
- Returns None if the HTTP request fails (connection error, timeout, etc.).