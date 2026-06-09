FROM python:3.12-slim
 
# Définir le répertoire de travail dans le conteneur
WORKDIR /app
 
# Copier le fichier des dépendances
COPY requirements.txt requirements.txt
 
# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt
 
# Copier les fichiers nécessaires dans l'image Docker
 
COPY app.py app.py
COPY data data
COPY templates templates
COPY tests tests
 
EXPOSE 5000
 
ENV PYTHONPATH=/app
 
# Commande pour démarrer l'application Flask
CMD ["python", "app.py"]
