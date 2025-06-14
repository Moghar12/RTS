# fatigue-detector

# 🚘 Système de Freinage d'Urgence Automatique — Détection de Fatigue

## 📑 Description

Ce projet implémente un système embarqué de **détection de fatigue du conducteur** à partir d’une webcam, via la détection :
- des **clignements d’yeux**
- des **bâillements**
- d’un **score de fatigue** visuel en temps réel

Lorsque le score de fatigue atteint un seuil critique, le système déclenche une alerte sonore.

Le système est développé sous **Python**, fonctionne avec **OpenCV**, **MediaPipe**, et s’intègre via **ROS 2** (Foxy / Humble / Iron).

---

## 📌 Fonctionnalités

- 📷 Détection en temps réel de clignements et bâillements via webcam
- 📊 Affichage graphique du score de fatigue (barre dynamique)
- 🔊 Alerte sonore en cas de score critique
- 🛰️ Communication entre nodes ROS 2
- 📦 Modulaire et facilement intégrable à un système embarqué

---

## 📦 Architecture ROS 2
