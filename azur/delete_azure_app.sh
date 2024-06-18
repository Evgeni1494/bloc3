#!/bin/bash

# Paramètres
SUBSCRIPTION="Simplon HDF Roubaix Dev IA P1"
RESOURCE_GROUP="END_Project_Evgeni"
APP_SERVICE_PLAN="myAppServicePlan"
WEB_APP="myFastApiApp"

# Définir l'abonnement
az account set --subscription "$SUBSCRIPTION"

# Supprimer la Web App
az webapp delete \
  --name $WEB_APP \
  --resource-group $RESOURCE_GROUP

# Supprimer le plan de service App
az appservice plan delete \
  --name $APP_SERVICE_PLAN \
  --resource-group $RESOURCE_GROUP \
  --yes

echo "L'application $WEB_APP et le plan de service $APP_SERVICE_PLAN ont été supprimés avec succès du groupe de ressources $RESOURCE_GROUP."

# executer avec ./create_azure_app.sh
