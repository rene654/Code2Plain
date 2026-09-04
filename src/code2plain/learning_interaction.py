from dataclasses import dataclass


@dataclass(frozen=True)
class LearningInteraction:
    why: str
    challenge: str


class LearningInteractionBuilder:
    WHY = {
        "FILTER":
            "Se usa para conservar únicamente los datos que cumplen una condición.",
        "GROUP":
            "Se usa cuando necesitas calcular resultados separados por cada grupo.",
        "AGGREGATE":
            "Se usa para resumir muchos valores en un resultado, como suma o promedio.",
        "LOOP":
            "Se usa cuando una misma operación debe repetirse para varios elementos.",
        "CONDITION":
            "Se usa para ejecutar una acción solamente cuando una condición es verdadera.",
        "FUNCTION":
            "Se usa para encapsular lógica reutilizable y evitar repetir código.",
        "CLASS":
            "Se usa para agrupar datos y comportamiento relacionados en una estructura.",
        "ERROR HANDLING":
            "Se usa para controlar qué ocurre cuando una operación puede fallar.",
    }

    CHALLENGE = {
        "FILTER":
            "¿Qué cambiaría si la condición fuera status == 'cancelled'?",
        "GROUP":
            "¿Qué resultado obtendrías si agrupas por producto en vez de cliente?",
        "AGGREGATE":
            "¿Qué cambiaría si usas mean() en lugar de sum()?",
        "LOOP":
            "¿Cuántas veces se ejecutaría este bloque si hay 5 elementos?",
        "CONDITION":
            "¿Qué ocurre si la condición resulta False?",
        "FUNCTION":
            "¿Qué dato necesita recibir esta función para poder ejecutarse?",
        "CLASS":
            "¿Qué tipo de objeto representa esta clase?",
        "ERROR HANDLING":
            "¿Qué ocurre si la operación no genera ningún error?",
    }

    def build(
        self,
        concept: str,
    ) -> LearningInteraction:
        return LearningInteraction(
            why=self.WHY.get(
                concept,
                "Esta estructura existe para resolver una parte específica del flujo del programa.",
            ),
            challenge=self.CHALLENGE.get(
                concept,
                "¿Qué crees que cambiaría si modificas esta línea?",
            ),
        )
