import pandas as pd
import requests
from xnoapi.vn.data.utils import Config

# Define the public API of the module
__all__ = ["list_liquid_asset", "get_hist"]

# Retrieve the Lambda function URL from Config
LAMBDA_URL = Config.get_link()


def list_liquid_asset():
    """
    Retrieve a list of highly liquid assets.

    Returns
    -------
    dict
        A dictionary containing the list of liquid assets.

    Raises
    ------
    Exception
        If an error occurs while calling the API.
    """
    api_key = Config.get_api_key()
    response = requests.get(
        f"{LAMBDA_URL}/list-liquid-asset", headers={"x-api-key": api_key}
    )

    if response.status_code == 200:
        return pd.DataFrame(response.json())
    else:
        raise Exception(f"Error: {response.status_code}, {response.text}")


def get_hist(asset_name: str):
    """
    Retrieve the historical data of an asset, forward-filling missing values.

    Parameters
    ----------
    asset_name : str
        The name of the asset (e.g., "VIC", "VHM").

    Returns
    -------
    dict
        A dictionary containing historical data including time, closing price, and volume.

    Raises
    ------
    Exception
        If an error occurs while calling the API.
    """
    api_key = Config.get_api_key()
    payload = {
        "asset_name": asset_name,
    }

    response = requests.post(
        f"{LAMBDA_URL}/data-stocks", json=payload, headers={"x-api-key": api_key}
    )

    if response.status_code == 200:
        return pd.DataFrame(response.json())
    else:
        raise Exception(f"Error: {response.status_code}, {response.text}")