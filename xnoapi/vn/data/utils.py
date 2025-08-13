class Config:
    """
    Configuration class for managing the API key and providing the API endpoint.

    Attributes:
        _api_key (str | None): The stored API key. Defaults to None.
    """

    _api_key = None

    @classmethod
    def set_api_key(cls, apikey: str):
        """
        Set the API key.

        Parameters:
            apikey (str): The API key to be set.
        """
        cls._api_key = apikey

    @classmethod
    def get_api_key(cls) -> str:
        """
        Retrieve the currently set API key.

        Returns:
            str: The current API key.

        Raises:
            ValueError: If the API key has not been set.
        """
        if cls._api_key is None:
            raise ValueError("API key is not set. Use client(apikey=...) to set it.")
        return cls._api_key

    @classmethod
    def get_link(cls) -> str:
        """
        Retrieve the default API endpoint.

        Returns:
            str: The API base URL.
        """
        return "https://d16sdkoet71cxx.cloudfront.net"


def client(apikey: str):
    """
    Set the API key for global use in the application.

    Parameters:
        apikey (str): The API key to be set.
    """
    Config.set_api_key(apikey)
