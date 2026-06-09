import pytest
from app import app


@pytest.fixture
def client():
    """Client de test Flask."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# ── Route ──────────────────────────────────────────────────────────────────

def test_route_predict_exists(client):
    """La route /predict répond (pas de 404)."""
    res = client.post("/predict", data={
        "Age": 42,
        "Account_Manager": 1,
        "Years": 6,
        "Num_Sites": 18
    })
    assert res.status_code != 404


# ── Réponse valide ──────────────────────────────────────────────────────────

def test_predict_returns_json(client):
    """La réponse est bien du JSON."""
    res = client.post("/predict", data={
        "Age": 42,
        "Account_Manager": 1,
        "Years": 6,
        "Num_Sites": 18
    })
    assert res.content_type == "application/json"


def test_predict_contains_prediction_key(client):
    """La réponse contient bien la clé 'prediction'."""
    res = client.post("/predict", data={
        "Age": 42,
        "Account_Manager": 1,
        "Years": 6,
        "Num_Sites": 18
    })
    data = res.get_json()
    assert "prediction" in data


def test_predict_contains_message_key(client):
    """La réponse contient bien la clé 'message'."""
    res = client.post("/predict", data={
        "Age": 42,
        "Account_Manager": 1,
        "Years": 6,
        "Num_Sites": 18
    })
    data = res.get_json()
    assert "message" in data


def test_predict_value_is_0_or_1(client):
    """La prédiction retournée est bien 0 ou 1."""
    res = client.post("/predict", data={
        "Age": 42,
        "Account_Manager": 1,
        "Years": 6,
        "Num_Sites": 18
    })
    data = res.get_json()
    assert data["prediction"] in [0, 1]


def test_predict_message_matches_prediction(client):
    """Le message correspond bien à la prédiction (Churn / No Churn)."""
    res = client.post("/predict", data={
        "Age": 42,
        "Account_Manager": 1,
        "Years": 6,
        "Num_Sites": 18
    })
    data = res.get_json()
    if data["prediction"] == 1:
        assert data["message"] == "Churn"
    else:
        assert data["message"] == "No Churn"


# ── Champs manquants ────────────────────────────────────────────────────────

def test_missing_field_returns_400(client):
    """Un champ manquant retourne une erreur 400."""
    res = client.post("/predict", data={
        "Age": 42,
        "Years": 6,
        # Account_Manager et Num_Sites manquants
    })
    assert res.status_code == 400


def test_missing_field_returns_error_key(client):
    """Un champ manquant retourne bien une clé 'error' dans la réponse."""
    res = client.post("/predict", data={
        "Age": 42,
        "Years": 6,
    })
    data = res.get_json()
    assert "error" in data


# ── Champs invalides ────────────────────────────────────────────────────────

def test_invalid_field_type_returns_400(client):
    """Une valeur non numérique retourne une erreur 400."""
    res = client.post("/predict", data={
        "Age": "abc",
        "Account_Manager": 1,
        "Years": 6,
        "Num_Sites": 18
    })
    assert res.status_code == 400


# ── Méthode GET refusée ─────────────────────────────────────────────────────

def test_get_method_not_allowed(client):
    """La route /predict n'accepte pas les requêtes GET."""
    res = client.get("/predict")
    assert res.status_code == 405
