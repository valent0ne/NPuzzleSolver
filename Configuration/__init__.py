class Configuration:
    def __init__(self, heuristic_type, perturbation):
        self.heuristic_type = heuristic_type
        self.perturbation = perturbation

    def set_perturnation(self, perturbation):
        self.perturbation = perturbation

    def set_heuristic_type(self, heuristic_type):
        self.heuristic_type = heuristic_type