from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from clients.supabase_storage_client import SupabaseStorageClient
from database.neo4j import get_neo4j_session
from database.postgresql import get_postgresql_db
from repositories.craft_plan_repository import CraftPlanRepository
from repositories.recipe_repository import RecipeRepository
from repositories.user_repository import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession
from services.auth_service import AuthService
from services.craft_plan_service import CraftPlanService
from services.user_service import UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')

def get_supabase_storage_client():
    return SupabaseStorageClient()

def get_recipe_repository(db: Neo4jSession):
    return RecipeRepository(db)

def get_user_repository(db: PostgreSQLSession):
    return UserRepository(db)

def get_craft_plan_repository(db: PostgreSQLSession):
    return CraftPlanRepository(db)

def get_auth_service(user_repository: UserRepositoryDependency):
    return AuthService(user_repository)

def get_user_service(user_Repository: UserRepositoryDependency, supabase_storage_client: SupabaseStorageClientDependency):
    return UserService(user_Repository, supabase_storage_client)

def get_craft_plan_service(recipe_repository: RecipeRepositoryDependency, craft_plan_repository: CraftPlanRepositoryDependency):
    return CraftPlanService(recipe_repository, craft_plan_repository)

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], user_Service: Annotated[UserService, Depends(get_user_service)]):
    return await user_Service.get_user(token)

PostgreSQLSession = Annotated[AsyncSession, Depends(get_postgresql_db)]
Neo4jSession = Annotated[AsyncSession, Depends(get_neo4j_session)]
UserRepositoryDependency = Annotated[UserRepository, Depends(get_user_repository)]
CraftPlanRepositoryDependency = Annotated[CraftPlanRepository, Depends(get_craft_plan_repository)]
RecipeRepositoryDependency = Annotated[RecipeRepository, Depends(get_recipe_repository)]
SupabaseStorageClientDependency = Annotated[SupabaseStorageClient, Depends(get_supabase_storage_client)]