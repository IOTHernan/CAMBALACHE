# adaptive_learning.py
# Módulo base para aprendizaje dinámico adaptativo con gestión de incertidumbre

import numpy as np

class AdaptiveLearner:
    def __init__(self, input_dim, uncertainty_threshold=0.1):
        self.input_dim = input_dim
        self.uncertainty_threshold = uncertainty_threshold
        # Inicialización de parámetros internos
        self.knowledge_base = {}
        self.confidence_levels = {}

    def update_knowledge(self, input_vector, output_value):
        key = tuple(input_vector)
        current_confidence = self.confidence_levels.get(key, 0)
        # Evaluar incertidumbre y actualizar conocimiento si supera el umbral
        if current_confidence < (1 - self.uncertainty_threshold):
            self.knowledge_base[key] = output_value
            self.confidence_levels[key] = current_confidence + 0.1  # Incremento adaptativo
            return True
        return False

    def query_knowledge(self, input_vector):
        key = tuple(input_vector)
        return self.knowledge_base.get(key, None)

    def assess_uncertainty(self, input_vector):
        key = tuple(input_vector)
        confidence = self.confidence_levels.get(key, 0)
        return 1 - confidence

# Ejemplo de uso
if __name__ == "__main__":
    learner = AdaptiveLearner(input_dim=3)
    input_sample = np.array([0.5, 0.3, 0.9])
    learner.update_knowledge(input_sample, output_value=1)
    print("Conocimiento consultado:", learner.query_knowledge(input_sample))
    print("Nivel de incertidumbre:", learner.assess_uncertainty(input_sample))
