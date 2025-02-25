terraform {
  required_providers {
    azurerm = {
      source = "hashicorp/azurerm"
      version = ">= 3.8"
    }
  }

  backend "azurerm" {
    resource_group_name  = "cohort32-33_KatLin_ProjectExercise"
    storage_account_name = "katlintfstorageacc"
    container_name       = "katlintfcontainer"
    key                  = "terraform.tfstate"
  }
}

provider "azurerm" {
  features {}
  subscription_id = "d33b95c7-af3c-4247-9661-aa96d47fccc0"
}

data "azurerm_resource_group" "main" {
  name     = "cohort32-33_KatLin_ProjectExercise"
}

resource "azurerm_service_plan" "main" {
  name                = "${var.prefix}-terraformed-asp"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  os_type             = "Linux"
  sku_name            = "B1"
}

resource "azurerm_linux_web_app" "main" {
  name                = "${var.prefix}-todo-app"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  service_plan_id     = azurerm_service_plan.main.id

  site_config {
    application_stack {
      docker_image_name     = "katielht/todo-app:prod"
      docker_registry_url   = "https://index.docker.io"
    }
  }

  app_settings = {
    "FLASK_APP" = "todo_app/app"
    "FLASK_DEBUG" = "false"
    "MONGO_COLLECTION_NAME" = "todo_app_collection"
    "MONGO_DATABASE_NAME" = "todo_app_database"
    "MONGOBD_PRIMARY_CONNECTION_STRING" = azurerm_cosmosdb_account.main.primary_mongodb_connection_string
    "OAUTH_CLIENT_ID" = var.OAUTH_CLIENT_ID
    "OAUTH_CLIENT_SECRET" = var.OAUTH_CLIENT_SECRET
    "SECRET_KEY" = "56e3f04a1a898d891d92128b0cd046900c106d82b8c103d61fa2568e5c3e07a0"
    "WEBSITES_ENABLE_APP_SERVICE_STORAGE" = "false"
    "WEBSITES_PORT" = 5000
  }
  
  connection_string {
    name  = "Database"
    type  = "SQLServer"
    value = "Server=some-server.mydomain.com;Integrated Security=SSPI"
  }
}

resource "azurerm_cosmosdb_account" "main" {
  name                = "${var.prefix}-cosmosdb"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  offer_type          = "Standard"
  kind                = "MongoDB"

  capabilities {
    name = "MongoDBv3.4"
  }

  capabilities {
    name = "EnableMongo"
  }

  capabilities {
    name = "EnableServerless"
  } 

  consistency_policy {
    consistency_level       = "BoundedStaleness"
    max_interval_in_seconds = 300
    max_staleness_prefix    = 100000
  }

  geo_location {
    location          = "uksouth"
    failover_priority = 0
  }

  lifecycle { 
    prevent_destroy = true 
  }
}

resource "azurerm_cosmosdb_mongo_database" "main" {
  name                = "${var.prefix}-cosmosdb-mongo"
  resource_group_name = data.azurerm_resource_group.main.name
  account_name        = azurerm_cosmosdb_account.main.name
}