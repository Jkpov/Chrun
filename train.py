import pandas as pd
import joblib
 
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
 
# Charger les données
data = pd.read_csv('data/customer_churn.csv')
 
# Variables explicatives
X = data[['Age', 'Account_Manager', 'Years', 'Num_Sites']]
 
# Variable cible
y = data['Churn']
 
# Pipeline : standardisation + modèle
model = Pipeline([
    ('scaler', StandardScaler()),
    ('classifier', LogisticRegression())
])
 
# Entraînement
model.fit(X, y)
 
# Sauvegarde du pipeline complet
joblib.dump(model, 'data/churn_model_clean.pkl')
 
print("Pipeline entraîné et sauvegardé.")