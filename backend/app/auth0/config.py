from pydantic import BaseSettings, validator


class Settings(BaseSettings):
    auth0_audience: str
    auth0_domain: str
    auth0_mgmt_client_id: str
    auth0_mgmt_client_secret: str
    client_origin_url: str
    port: int
    reload: bool

    @classmethod
    @validator("client_origin_url", "auth0_audience", "auth0_domain", "auth0_mgmt_client_id", "auth0_mgmt_client_secret")
    def check_not_empty(cls, v):
        assert v != "", f"{v} is not defined"
        return v

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
