import os
import joblib
import pytest
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

MODEL_PATH = "data/churn_model_clean.pkl"


def test_model_file_exists():
    """Le fichier .pkl existe bien sur le disque."""
    assert os.path.exists(MODEL_PATH), f"Modèle introuvable : {MODEL_PATH}"


def test_model_loads_without_error():
    """Le fichier .pkl se charge sans erreur avec joblib."""
    model = joblib.load(MODEL_PATH)
    assert model is not None


def test_model_is_pipeline():
    """Le modèle chargé est bien un Pipeline sklearn."""
    model = joblib.load(MODEL_PATH)
    assert isinstance(model, Pipeline), "Le modèle n'est pas un Pipeline"


def test_pipeline_has_scaler():
    """Le pipeline contient bien un StandardScaler."""
    model = joblib.load(MODEL_PATH)
    assert "scaler" in model.named_steps, "Étape 'scaler' manquante"
    assert isinstance(model.named_steps["scaler"], StandardScaler)


def test_pipeline_has_classifier():
    """Le pipeline contient bien une LogisticRegression."""
    model = joblib.load(MODEL_PATH)
    assert "classifier" in model.named_steps, "Étape 'classifier' manquante"
    assert isinstance(model.named_steps["classifier"], LogisticRegression)


def test_model_expected_features():
    """Le modèle accepte exactement les 4 champs attendus."""
    import pandas as pd

    model = joblib.load(MODEL_PATH)

    expected_columns = ["Age", "Account_Manager", "Years", "Num_Sites"]

    sample = pd.DataFrame([{col: 0 for col in expected_columns}])

    try:
        model.predict(sample)
    except Exception as e:
        pytest.fail(f"Le modèle a rejeté les champs attendus : {e}")


def test_model_rejects_missing_feature():
    """Le modèle échoue si un champ est manquant."""
    import pandas as pd

    model = joblib.load(MODEL_PATH)

    incomplete = pd.DataFrame([{
        "Age": 42,
        "Years": 6,
        # Account_Manager et Num_Sites manquants
    }])

    with pytest.raises(Exception):
        model.predict(incomplete)


def test_model_predicts():
    """Le modèle prédit bien 0 ou 1 sur un exemple."""
    import pandas as pd

    model = joblib.load(MODEL_PATH)

    sample = pd.DataFrame([{
        "Age": 42,
        "Account_Manager": 1,
        "Years": 6,
        "Num_Sites": 18
    }])

    prediction = model.predict(sample)

    assert len(prediction) == 1, "La prédiction doit retourner 1 valeur"
    assert prediction[0] in [0, 1], "La prédiction doit être 0 ou 1"
