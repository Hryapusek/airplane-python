from enum import Enum


# Этот класс представляет различные состояния системы
class State(Enum):
    # Система находится в первом состоянии расстояния
    DISTANCE_1 = 1
    # Система находится во втором состоянии расстояния
    DISTANCE_2 = 2
    # Система находится в третьем состоянии расстояния
    DISTANCE_3 = 3
    # Система находится в безопасном состоянии расстояния
    SAFE_DISTANCE = 4

