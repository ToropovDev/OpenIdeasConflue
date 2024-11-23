import pydantic
from environs import Env
from pydantic_settings import BaseSettings, SettingsConfigDict

env = Env()
env.read_env()


class _PGSettings(BaseSettings):
    scheme: str = "postgresql+asyncpg"
    host: str = "localhost"
    port: int = 5433
    user: str = "open-ideas"
    password: str = "12345678"
    database: str = "open-ideas-conflue"

    def build_dsn(self, *, scheme: str | None = None) -> str:
        return str(
            pydantic.PostgresDsn.build(
                scheme=scheme or self.scheme,
                host=self.host,
                port=self.port,
                username=self.user,
                password=self.password,
                path=self.database,
            ),
        )

    model_config = SettingsConfigDict(env_prefix="POSTGRES_")


POSTGRES = _PGSettings()
