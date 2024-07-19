import pytest
from sklearn.datasets import make_regression
from model.model_training import train_model, evaluate_model, log_training_results

def test_model_r2():
    # Générer un problème de régression aléatoire
    X, y = make_regression(n_samples=100, n_features=10, noise=0.1)
    
    # Entraîner le modèle
    model, X_test, y_test = train_model(X, y)
    
    # Évaluer le modèle
    mse, r2 = evaluate_model(model, X_test, y_test)
    
    # Vérifier si le score R2 est supérieur à 0.55
    assert r2 > 0.55, f"Le score R2 est trop bas : {r2}"
    
    # Tester l'enregistrement des résultats d'entraînement dans une base de données en mémoire
    log_training_results(mse, r2, db_path=':memory:')

if __name__ == "__main__":
    pytest.main()

