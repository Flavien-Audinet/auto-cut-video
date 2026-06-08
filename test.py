import subprocess

# Chemin vers le fichier Hello.py
chemin = "Detect_coupure.py"

# Utiliser la fonction run pour exécuter Hello.py
subprocess.run(["python", chemin])

from Detect_coupure import time
print(time())