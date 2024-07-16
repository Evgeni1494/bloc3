1. Modèle Conceptuel des Données (MCD)

Le MCD identifie les entités, les associations et les attributs de manière indépendante des considérations techniques.
Entités et Attributs

    État (state) : state_name, latitude, longitude
    Émissions (emissions) : year, state_name, sector_name, fuel_name, value

Associations

    État-Émissions : Un état peut avoir plusieurs enregistrements d'émissions pour différentes années, secteurs et types de carburant.

2. Modèle Logique des Données (MLD)

Le MLD transforme le MCD en un schéma relationnel. On transforme les entités en tables et les associations en clés étrangères.
Tables et Relations

    État (state)
        state_name (TEXT, PRIMARY KEY)
        latitude (REAL)
        longitude (REAL)

    Émissions (emissions)
        year (INTEGER)
        state_name (TEXT, FOREIGN KEY REFERENCES state(state_name))
        sector_name (TEXT)
        fuel_name (TEXT)
        value (REAL)

3. Modèle Physique des Données (MPD)

Le MPD implémente le MLD sur le SGBD SQLite3.
Script SQL pour la Création des Tables

script SQL basé sur la structure MLD :

sql

-- Création de la table 'state'
CREATE TABLE IF NOT EXISTS state (
    state_name TEXT PRIMARY KEY,
    latitude REAL,
    longitude REAL
);

-- Création de la table 'emissions'
CREATE TABLE IF NOT EXISTS emissions (
    year INTEGER,
    state_name TEXT,
    sector_name TEXT,
    fuel_name TEXT,
    value REAL,
    FOREIGN KEY (state_name) REFERENCES state(state_name)
);