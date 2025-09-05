# secret_manager.py

## Set up

1. Create a service account key for the target Google Cloud project.
2. Build a credentials object using the service account key. The credentials allow your Python script/program to authenticate with Secret Manager.

```py
from google.oauth2 import service_account

JSON_KEYS_PATH = '/home/directory-for-keys'
SERVICE_ACCOUNT = f'{JSON_KEYS_PATH}/key.json'

# retrieve account credentials and project id from the service account key
credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT)
```

---

## get_secret

#### **Definition:**
```py
def get_secret(secret_id:str, project_id:str, credentials) -> Dict[str, Any]:
```

#### **Parameters:**
- `secret_id`: Unique name (ID) of the secret stored in Secret Manager.
- `project_id`: GCP project ID that owns the secret.
- `credentials`: Service account credentials created during [set up](https://github.com/nacht29/Python-tools-for-Google/blob/main/docs/secret_manager.md#set-up).

#### **Function call:**
```py
from python_utils.secret_manager import get_secret

secret = get_secret(
        secret_id="my-api-key",
        project_id=credentials.project_id,
        credentials=credentials
)
```

#### **Use case:**
Retrieve the latest version of a secret from Google Secret Manager. The secret payload is expected to be a JSON string.

#### **Return value:**
- Type: `Dict[str, Any]`
- Returns the secret payload as a Python dictionary.

