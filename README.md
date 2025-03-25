# 🚗 Projet ROS2 : Détection d'obstacle avec sonar et freinage automatique

Ce projet ROS2 implémente un système de détection d'obstacles à l'aide d'un capteur **sonar** (ultrason), dans l'objectif d'intégrer un **freinage automatique** sur une voiture robotisée.

---

## 📦 Package ROS2 : `sonar_sensor`

Ce package contient :

- `sonar_sensor_node.py` : un nœud ROS2 écrit en Python
- Il publie une distance simulée (0.5 m) sur le topic `/distance` à 10 Hz

---

## 🗂 Structure du package

├── package.xml
├── resource
│   └── sonar_sensor
├── setup.cfg
├── setup.py
└── sonar_sensor
    ├── __init__.py
    └── sonar_sensor_node.py


    
---

## 🚀 Instructions

### 🔧 Compilation

```bash
cd ~/ros2_ws
colcon build
source install/setup.bash
ros2 run sonar_sensor sonar_sensor_node
```

### ▶️ Exécution du noeud
```bash
ros2 run sonar_sensor sonar_sensor_node
```

### Tu devrais voir :
[INFO] [sonar_sensor_node]: Distance: 0.50 m



