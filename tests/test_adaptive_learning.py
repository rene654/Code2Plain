from code2plain.adaptive_learning import (
    AdaptiveLearningEngine,
)


def test_mastered_concept_becomes_compact():
    result = AdaptiveLearningEngine().adapt(
        concept="GROUP",
        explanation="Agrupa datos.",
        challenge="¿Qué cambiaría?",
        level="dominado",
    )

    assert result.mode == "compacto"


def test_weak_concept_gets_reinforcement():
    result = AdaptiveLearningEngine().adapt(
        concept="FILTER",
        explanation="Filtra datos.",
        challenge="¿Qué cambiaría?",
        level="reforzar",
    )

    assert result.mode == "refuerzo"
    assert "Presta especial atención" in (
        result.explanation
    )
