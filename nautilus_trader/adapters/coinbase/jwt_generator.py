import time

from cryptography.hazmat.primitives import serialization
import jwt
import secrets

# adapted from 
# https://github.com/coinbase/coinbase-advanced-py/blob/master/coinbase/jwt_generator.py


def build_jwt(key_var: str, secret_var: str, uri:str=None) -> str:
    """
    :meta private:
    """
    try:
        private_key_bytes = secret_var.encode("utf-8")
        private_key = serialization.load_pem_private_key(
            private_key_bytes, password=None
        )
    except ValueError as e:
        # This handles errors like incorrect key format
        raise Exception(
            f"{e}\n"
            "Are you sure you generated your key at https://cloud.coinbase.com/access/api ?"
        )

    jwt_data = {
        "sub": key_var,
        "iss": "cdp",
        "nbf": int(time.time()),  # should this come from the clock ?
        "exp": int(time.time()) + 120,
    }

    if uri:
        jwt_data["uri"] = uri

    jwt_token = jwt.encode(
        jwt_data,
        private_key,
        algorithm="ES256",
        headers={"kid": key_var, "nonce": secrets.token_hex()},
    )

    return jwt_token


def build_rest_jwt(uri: str, key_var: str, secret_var: str) -> str:
    """
    **Build REST JWT**
    __________

    **Description:**

    Builds and returns a JWT token for connecting to the REST API.

    __________

    Parameters:

    - **uri (str)** - Formatted URI for the endpoint (e.g. "GET api.coinbase.com/api/v3/brokerage/accounts") Can be generated using ``format_jwt_uri``
    - **key_var (str)** - The API key
    - **secret_var (str)** - The API key secret
    """
    return build_jwt(key_var, secret_var, uri=uri)


def build_ws_jwt(key_var: str, secret_var: str) -> str:
    """
    **Build WebSocket JWT**
    __________

    **Description:**

    Builds and returns a JWT token for connecting to the WebSocket API.

    __________

    Parameters:

    - **key_var (str)** - The API key
    - **secret_var (str)** - The API key secret
    """
    return build_jwt(key_var, secret_var)


def format_jwt_uri(method: str, base_url: str, path: str) -> str:
    """
    **Format JWT URI**
    __________

    **Description:**

    Formats method and path into valid URI for JWT generation.

    __________

    Parameters:

    - **method (str)** - The REST request method. E.g. GET, POST, PUT, DELETE
    - **path (str)** - The path of the endpoint. E.g. "/api/v3/brokerage/accounts"

    """
    return f"{method} {base_url}{path}"