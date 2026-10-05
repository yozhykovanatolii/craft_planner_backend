<div align="center">

# 🛠️ Craft Planner — Backend

**Backend API for crafting dependency planning, resource analysis and personalized crafting plans for Abiotic Factor**

</div>

## 📄 About

Craft Planner Backend is a REST API designed to help players plan crafting in [Abiotic Factor](https://store.steampowered.com/app/427410/Abiotic_Factor/).

Instead of manually calculating nested crafting dependencies, the application analyzes the selected target item, the player's current inventory and unlocked recipes to determine which components need to be crafted and which resources are still required.

## ✨ Features

* 🔐 **Authentication & Profile** – User registration, login, JWT-based authentication and profile management
* 🛠️ **Crafting Planner** – Calculate required components and resources for a selected item and quantity
* 🔗 **Dependency Resolution** – Resolve nested crafting dependencies using a graph-based approach
* 🎒 **Inventory Analysis** – Take the player's current inventory into account when calculating missing resources
* 📋 **Craft Plans** – Create, retrieve, recalculate and delete saved crafting plans
* 📊 **Resource Usage** – Find items that directly use a specific resource
* 🧭 **Usage Paths** – Find a dependency path between a resource and a target item
* 💾 **Save File Parsing** – Extract player inventory and unlocked recipes from save files
* 🗄️ **Database** – PostgreSQL for persistent application data and Neo4j for crafting dependencies
* 🔒 **Security** – Password hashing and JWT-based access and refresh tokens

## 🛠 Tech Stack

**Core Framework**
- **FastAPI** – Web framework for building the REST API 
- **Python** – Programming language    

**Database**
- **PostgreSQL** – Relational database
- **Neo4j** – Graph database for crafting recipes and item dependencies
- **SQLAlchemy** – ORM and database interaction
- **asyncpg** – Asynchronous PostgreSQL driver

**Validation & Configuration**
- **Pydantic** – Data validation and serialization
- **Pydantic Settings** – Environment-based configuration

**Authentication & Security**
- **JWT** – Access and refresh token authentication
- **pwdlib** – Password hashing

**Infrastructure**
- **Docker** – Containerization
- **Docker Compose** – Multi-container application setup

**External Services**
- **Supabase Storage** – File storage for user uploads and media management

## 🚀 Getting Started

### Prerequisites
- Python 3.x
- Docker

### Installation
1. Clone the repository
```
git clone https://github.com/yozhykovanatolii/smart_courier_assistant_backend.git
```

2. Convert the player save file to JSON

Craft Planner requires the player's save file in JSON format to extract inventory and unlocked recipes.

Download **UeSaveConverter** from its [GitHub repository](https://github.com/CrystalFerrai/UeSaveConverter) and use it to convert the `.sav` file to `.json`. The tool requires .NET Runtime 8.0 x64.

```bash
UeSaveConverter --to-json --overwrite path\to\savefile.sav
```

3. Configure environment variables

This project uses external services to provide Supabase Storage as file storage.

To configure this service, it needs to create a project in Supabase at https://supabase.com and get your project credentials(URL and anon key)

For creating SECRET_KEY and using for access and refresh tokens, you have to execute this code:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Use .env.example for creating the .env file in the project root and set the following values:

```env
# Security
SECRET_KEY=

# Supabase
SUPABASE_PROJECT_URL=
SUPABASE_ANON_KEY=

# PostgreSQL
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_DB=craft_planner
POSTGRES_USER=postgres

#Neo4j
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=password123
```

3. Run the application
```
docker compose up --build
```
The API and API documentation will be available at: http://localhost:8000 and http://localhost:8000/docs

## 📡 API Endpoints

The API provides endpoints for:

* Authentication and user management
* Crafting plans
* Resource usage
* Resource usage paths
* Plan recalculation

For the complete API reference, see the interactive [Swagger UI](http://localhost:8000/docs).




