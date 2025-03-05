import toml


class ConfigLoader:
    def __init__(self, config_path: str):
        self.config_path = config_path

    def load_config(self) -> dict:
        try:
            with open(self.config_path, "r") as file:
                return toml.load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"Config file not found at {self.config_path}")
        except ValueError as error:
            raise ValueError(f"Failed to decode TOML file. Details: {error}")


def get_config(config_path: str = "config.toml") -> dict:
    loader = ConfigLoader(config_path)
    return loader.load_config()