from os import environ

from dotenv import load_dotenv

from exceptions import IncorrectSettingsSetupError, IncorrectEnvVarSetupError
from project_dataclasses import Settings


def get_settings() -> Settings:

    load_dotenv()

    received_env_vars = {}

    for env_var_name, env_var_type in Settings.__annotations__.items():

        env_var_value = environ.get(env_var_name)

        if not env_var_value:
            raise IncorrectEnvVarSetupError(f'{env_var_name} environment variable not found, set it')

        if env_var_type is str:
            pass

        elif env_var_type is bool:
            env_var_value = env_var_value.lower() == 'true'

        else:
            raise IncorrectSettingsSetupError(f'Unknown environment variable type found: {env_var_type}')

        received_env_vars[env_var_name] = env_var_value

    return Settings(**received_env_vars)


SETTINGS = get_settings()
