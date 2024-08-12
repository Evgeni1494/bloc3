#!/bin/bash

# Paramètres
SUBSCRIPTION="Simplon HDF Roubaix Dev IA P1"
RESOURCE_GROUP="End_project_evgeni"
APP_SERVICE_PLAN="EvgeniServicePlan"
WEB_APP="FastApiAppEvgeni"
LOCATION="westeurope"
RUNTIME="PYTHON|3.11"

# Définir l'abonnement
az account set --subscription "$SUBSCRIPTION"

# Créer le plan de service App avec le SKU B1 (gratuit)
az appservice plan create \
  --name $APP_SERVICE_PLAN \
  --resource-group $RESOURCE_GROUP \
  --sku B1 \
  --is-linux \
  --location $LOCATION

# Vérifier si l'application Web existe déjà
EXISTING_APP=$(az webapp show --resource-group $RESOURCE_GROUP --name $WEB_APP --query "name" -o tsv)

if [ -n "$EXISTING_APP" ]; then
  echo "L'application $WEB_APP existe déjà. Suppression..."
  az webapp delete --resource-group $RESOURCE_GROUP --name $WEB_APP
  echo "L'application $WEB_APP a été supprimée."
fi

# Créer la Web App
az webapp create \
  --resource-group $RESOURCE_GROUP \
  --plan $APP_SERVICE_PLAN \
  --name $WEB_APP \
  --runtime $RUNTIME

echo "L'application $WEB_APP a été créée avec succès dans le groupe de ressources $RESOURCE_GROUP."
