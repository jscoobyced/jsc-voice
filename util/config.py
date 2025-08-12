import toml

class JscConfig:
    _instance = None

    def __new__(cls, *args, **kwargs):
        """ Singleton pattern to ensure only one instance of the config is created """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.config = {}
        with open("pyproject.toml", "r") as f:
            data = toml.load(f)
            self.config["version"] = data["project"]["version"]
            self.config["name"] = data["project"]["name"]
            self.config["description"] = data["project"]["description"]
            self.config["port"] = data["project"]["port"]

    def get_config(self):
        return self.config