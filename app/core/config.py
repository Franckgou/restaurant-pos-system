from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator
from typing import List, Optional
from functools import lru_cache

class Setting(BaseSettings):
    #Database Settings
    DATABASE_URL : str 
    test_database_url : str = Field(alias = "TEST_DATABASE_URL")


    #Security Settings
    secret_key : str = Field(alias = "SECRET_KEY")
    algorithm : str = "HS256"
    access_token_expire_minutes : int =30

    #CORS Settings
    #cors_origins: List[str] = Field(alias = "BACKEND_CORS_ORIGINS")
    cors_methods: List[str] = ["GET", "POST", "PUT", "DELETE"]
    cors_headers: List[str] = ["Authorization", "Content-Type"]

    debug : bool = Field(alias = "DEBUG")
    redis_url : str = Field(alias = "REDIS_URL")

    #Environment settings
    ENVIRONMENT : str = Field("development", alias = "ENVIRONMENT")



    model_config = SettingsConfigDict(env_file= ".env", env_file_encoding= "utf-8", extra = "ignore")

    # @field_validator('cors_origins', mode = 'before')
    # @classmethod
    # def parse_cors_origins(cls, v):
    #     if isinstance(v, str):
    #         return [origin.strip() for origin in v.split(',')]
    #     return v
@lru_cache()
def get_settings():

    return Setting()  # type: ignore