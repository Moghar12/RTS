# Sonar Sensor - ROS2 Package 🚗📡

Ce package ROS2 s'appelle `sonar_sensor`. Il a été développé dans le cadre d'un projet de **détection d'obstacle avec un capteur sonar** et de **freinage automatique d'une voiture robotisée**.

---

## 📦 Contenu du package

- `sonar_sensor_node.py` : un nœud ROS2 écrit en Python qui lit une valeur de distance simulée (ou réelle depuis un capteur HC-SR04) et la publie sur un topic `/distance`.

---

## 📁 Structure

sonar_sensor/ ├── sonar_sensor/ │ ├── init.py │ └── sonar_sensor_node.py ├── package.xml ├── setup.py ├── setup.cfg ├── README.md

yaml
Copier
Modifier

---

## 🚀 Utilisation

### 1. Build le workspace

```bash
cd ~/ros2_ws
colcon build
source install/setup.bash


2. Lancer le noeud
ros2 run sonar_sensor sonar_sensor_node

🔧 À venir
Intégration du capteur HC-SR04 (ultrason réel)

Freinage automatique (commande d'un moteur/servo)

Détection d'obstacle avec seuil


🧠 Dépendances
rclpy

std_msgs
