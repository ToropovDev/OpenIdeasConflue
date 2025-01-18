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


POSTGRES_HOST: str = env.str("POSTGRES_HOST", "0.0.0.0")
POSTGRES_PORT: int = env.int("POSTGRES_PORT", 5433)
POSTGRES_DATABASE: str = env.str("POSTGRES_DATABASE", "unknown")
POSTGRES_USER: str = env.str("POSTGRES_USER", "unknown")
POSTGRES_PASSWORD: str = env.str("POSTGRES_PASSWORD", "unknown")
OPEN_IDEAS_URL: str = env.str("OPEN_IDEAS_URL", "unknown")
OPEN_IDEAS_PROTECTED_ENDPOINT: str = env.str("OPEN_IDEAS_PROTECTED_ENDPOINT", "unknown")

POSTGRES = _PGSettings(
    host=POSTGRES_HOST,
    port=POSTGRES_PORT,
    user=POSTGRES_USER,
    database=POSTGRES_DATABASE,
    password=POSTGRES_PASSWORD,
)


S3_ENDPOINT_URL: str = env.str("S3_ENDPOINT_URL", "unknown")
S3_REGION_NAME: str = env.str("S3_REGION_NAME", "unknown")
S3_LOGIN: str = env.str("S3_LOGIN", "unknown")
S3_KEY_SECRET: str = env.str("S3_KEY_SECRET", "unknown")
S3_TENANT_ID: str = env.str("S3_TENANT_ID", "unknown")
S3_BUCKET: str = env.str("S3_BUCKET", "unknown")
