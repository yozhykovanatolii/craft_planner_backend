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


