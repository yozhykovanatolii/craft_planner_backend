from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    secret_key: str
    supabase_project_url: str
    supabase_anon_key: str
    postgres_password: str 
    postgres_host: str 
    postgres_port: int 
    postgres_db: str
    postgres_user: str
    neo4j_uri: str 
    neo4j_username: str 
    neo4j_password: str 
    
    model_config = SettingsConfigDict(env_file=".env")
    
    @property
    def database_url(self):
        return f'postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}'
    
    
settings = Settings()