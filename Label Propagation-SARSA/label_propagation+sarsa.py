# -*- coding: utf-8 -*-
"""Label Propagation+SARSA.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1iLdiIcWHjFxQy_Jbe8nzR0-yQRTJOTDD
"""

import csv
import numpy as np
import pandas as pd

np.random.seed(0)

# Chargement du dataset existant
df = pd.read_csv('donnees_sante.csv')

# Calcul du nombre de records à supprimer
n_samples = len(df)
n_labels_to_remove = int(0.6 * n_samples)
n_labels_to_remove_normal = int(0.3 * n_labels_to_remove)
n_labels_to_remove_critical = n_labels_to_remove - n_labels_to_remove_normal

# Sélection aléatoire des indices des labels à supprimer de classe "Normal"
indices_normal = df[df['Class'] == 'Normal'].index
indices_to_remove_normal = np.random.choice(indices_normal, size=n_labels_to_remove_normal, replace=False)

# Sélection aléatoire des indices des labels à supprimer de classe "Critical"
indices_critical = df[df['Class'] == 'Critical'].index
indices_to_remove_critical = np.random.choice(indices_critical, size=n_labels_to_remove_critical, replace=False)

# Fusion des indices à supprimer
indices_to_remove = np.concatenate((indices_to_remove_normal, indices_to_remove_critical))

# Suppression des labels correspondants
df.loc[indices_to_remove, 'Class'] = ''

# Chemin du fichier CSV de sortie
output_file = 'nouveau_dataset.csv'

# Écriture du nouveau dataset dans un fichier CSV
df.to_csv(output_file, index=False)

# Affichage des données générées
print(df.to_string(index=False))

# Calcul du nombre de records avec labels
n_records_with_labels = df[df['Class'] != ''].shape[0]

# Calcul du nombre de records sans labels
n_records_without_labels = df[df['Class'] == ''].shape[0]

# Affichage du nombre de records avec labels et sans labels
print("Nombre de records avec labels : ", n_records_with_labels)
print("Nombre de records sans labels : ", n_records_without_labels)

import pandas as pd
import numpy as np
from sklearn.semi_supervised import LabelPropagation
from sklearn.metrics import classification_report, roc_curve, auc
from sklearn.preprocessing import label_binarize
import matplotlib.pyplot as plt

# Chargement du dataset
dataset = pd.read_csv('nouveau_dataset.csv')

# Séparation des données et des classes
X_labeled = dataset[~dataset['Class'].isnull()].drop('Class', axis=1)
X_unlabeled = dataset[dataset['Class'].isnull()].drop('Class', axis=1)
y_labeled = dataset[~dataset['Class'].isnull()]['Class']

# Conversion des classes en valeurs numériques
label_map = {'Critical': 0, 'Normal': 1}
y_numeric = np.array([label_map[label] for label in y_labeled])

# Création du modèle de propagation de labels
model = LabelPropagation()

# Entraînement du modèle sur les données étiquetées
model.fit(X_labeled, y_numeric)

# Prédiction des classes pour les données non étiquetées
y_pred = model.predict(X_unlabeled)

# Remplacement des valeurs numériques par les étiquettes originales
y_pred_labels = np.array(['Critical' if label == 0 else 'Normal' for label in y_pred])

# Mise à jour du dataset avec les classes prédites
dataset.loc[dataset['Class'].isnull(), 'Class'] = y_pred_labels

# Affichage des prédictions de labels pour les données non étiquetées
for i, label in enumerate(y_pred_labels):
    print(f"Record {i+1} - Predicted Label: {label}")

# Chargement du dataset initial avec les classes réelles
dataset_initial = pd.read_csv('donnees_sante.csv')

# Extraction des classes réelles du dataset initial
y_true = dataset_initial['Class'].values

# Extraction des classes prédites du nouveau dataset
y_pred = dataset['Class'].values

# Conversion des étiquettes en valeurs binaires
y_true_binary = label_binarize(y_true, classes=['Critical', 'Normal'])
y_pred_binary = label_binarize(y_pred, classes=['Critical', 'Normal'])

# Calcul de la courbe ROC et de l'AUC
fpr, tpr, thresholds = roc_curve(y_true_binary.ravel(), y_pred_binary.ravel())
roc_auc = auc(fpr, tpr)

# Affichage de la courbe ROC
plt.figure()
plt.plot(fpr, tpr, color='darkorange', lw=2, label='Courbe ROC (AUC = %0.2f)' % roc_auc)
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('Taux de faux positifs')
plt.ylabel('Taux de vrais positifs')
plt.title('Courbe ROC')
plt.legend(loc="lower right")
plt.show()

# Calcul des métriques de classification
classification_metrics = classification_report(y_true, y_pred)
print(classification_metrics)

# Sauvegarde du dataset mis à jour
dataset.to_csv('Predictions-semi-supervise.csv', index=False)

import pandas as pd

# Chargement des fichiers
dataset_original = pd.read_csv('donnees_sante.csv')
dataset_semi_supervise = pd.read_csv('nouveau_dataset.csv')
predictions_semi_supervise = pd.read_csv('Predictions-semi-supervise.csv')

# Division du fichier 'donnees_sante.csv' en train_initial et test_initial
train_initial = dataset_original.sample(frac=0.8, random_state=42)
test_initial = dataset_original.drop(train_initial.index)

train_semi_supervise = dataset_semi_supervise.sample(frac=0.8, random_state=42)
test_semi_supervise = dataset_semi_supervise.drop(train_initial.index)

train_predictions = predictions_semi_supervise.sample(frac=0.8, random_state=42)
test_predictions = predictions_semi_supervise.drop(train_predictions.index)

# Sauvegarde des fichiers train_initial.csv et test_initial.csv
train_initial.to_csv('train_initial.csv', index=False)
test_initial.to_csv('test_initial.csv', index=False)

train_semi_supervise.to_csv('train_semi_supervise.csv',index=False)
test_semi_supervise.to_csv('test_semi_supervise.csv',index=False)

# Sauvegarde du fichier train_predictions.csv
train_predictions.to_csv('train_predictions.csv', index=False)

# Suppression de la colonne 'classe' du fichier test_predictions
test_predictions_without_class = test_predictions.iloc[:, :-1]

# Sauvegarde du fichier test_predictions.csv sans la colonne 'classe'
test_predictions_without_class.to_csv('test_predictions.csv', index=False)

# Affichage du nombre de lignes de chaque fichier
print("Nombre de lignes dans train_initial.csv :", len(train_initial))
print("Nombre de lignes dans test_initial.csv :", len(test_initial))
print("Nombre de lignes dans train_predictions.csv :", len(train_predictions))
print("Nombre de lignes dans test_predictions.csv :", len(test_predictions_without_class))

import pandas as pd
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import accuracy_score, roc_auc_score, recall_score, f1_score
from sklearn.preprocessing import LabelEncoder

# Chargement des données d'entraînement
train_data = pd.read_csv("train_predictions.csv")

# Séparation des features (X) et de la variable cible (y)
X_train = train_data.iloc[:, :-1]  # Toutes les colonnes sauf la dernière
y_train = train_data.iloc[:, -1]  # Dernière colonne

# Entraînement du modèle SARSA
sarsa_model = SGDClassifier(loss='log')
sarsa_model.fit(X_train, y_train)

# Chargement des données de test
test_data = pd.read_csv("test_semi_supervise.csv")
X_test = test_data.iloc[:, :-1]  # Toutes les colonnes sauf la dernière

# Prédiction des classes pour les données de test
predicted_classes = sarsa_model.predict(X_test)

# Création d'un nouveau dataframe avec les prédictions
sarsa_predictions = pd.DataFrame({
    "Classe Prédite": predicted_classes
})

SARSA_vs_Label_propagation = pd.DataFrame({
    "Prédictions SARSA        |": predicted_classes
})

# Chargement des données réelles pour comparaison
actual_data = pd.read_csv("test_initial.csv")

# Extraction des classes réelles
y_actual = actual_data.iloc[:, -1]

#chargement des données prédites du semi-supervisé pour comparaison
Label_propagation_data=pd.read_csv("test_predictions.csv")

#Extraction des données prédites de Label Propagation
y_semi = Label_propagation_data.iloc[:, -1]

# Ajout de la colonne des classes réelles dans le dataframe des prédictions
sarsa_predictions["Classe Réelle"] = y_actual

# Ajout de la colonne des classes prédites par Label Propagation
SARSA_vs_Label_propagation["Prédictions Label Propagation"] = y_semi

# Affichage des classes prédites et réelles côte à côte
print(sarsa_predictions)

# Encodage des classes réelles en valeurs numériques catégorielles
label_encoder = LabelEncoder()
y_actual_encoded = label_encoder.fit_transform(y_actual)
y_predicted_encoded = label_encoder.transform(predicted_classes)

# Calcul de la précision
accuracy = accuracy_score(y_actual_encoded, y_predicted_encoded)
print("Précision : ", accuracy)

# Calcul du rappel
recall = recall_score(y_actual_encoded, y_predicted_encoded, average='macro')
print("Rappel : ", recall)

# Calcul du score F1
f1 = f1_score(y_actual_encoded, y_predicted_encoded, average='macro')
print("Score F1 : ", f1)

# Calcul du taux d'erreur
error_rate = 1 - accuracy
print("Taux d'erreur : ", error_rate)

# Calcul de la courbe ROC (stratégie "ovo")
roc_auc = roc_auc_score(y_actual_encoded, sarsa_model.decision_function(X_test), multi_class='ovo')
print("Courbe ROC : ", roc_auc)




