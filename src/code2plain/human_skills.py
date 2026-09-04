from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class HumanSkill:
    skill_id: str
    name: str
    simple_meaning: str
    beginner_goal: str


SKILLS: dict[str, HumanSkill] = {
    "VARIABLE_USE": HumanSkill(
        skill_id="VARIABLE_USE",
        name="Guardar y reutilizar información",
        simple_meaning=(
            "Entender cómo un resultado se guarda "
            "con un nombre para utilizarlo después."
        ),
        beginner_goal=(
            "Reconocer qué valor entra en una variable "
            "y dónde vuelve a utilizarse."
        ),
    ),
    "FUNCTION_CALL": HumanSkill(
        skill_id="FUNCTION_CALL",
        name="Usar una función",
        simple_meaning=(
            "Entender cuándo el programa le pide "
            "a una función que haga una tarea."
        ),
        beginner_goal=(
            "Reconocer qué función se ejecuta, "
            "qué recibe y qué devuelve."
        ),
    ),
    "METHOD_CALL": HumanSkill(
        skill_id="METHOD_CALL",
        name="Pedirle una acción a un objeto",
        simple_meaning=(
            "Entender expresiones como "
            "`objeto.accion(...)`."
        ),
        beginner_goal=(
            "Identificar qué objeto recibe la acción "
            "y qué datos se le entregan."
        ),
    ),
    "DATA_FILTERING": HumanSkill(
        skill_id="DATA_FILTERING",
        name="Quedarse solo con los datos necesarios",
        simple_meaning=(
            "Seleccionar únicamente los datos "
            "que cumplen una condición."
        ),
        beginner_goal=(
            "Reconocer la condición y predecir "
            "qué datos permanecen."
        ),
    ),
    "DATA_GROUPING": HumanSkill(
        skill_id="DATA_GROUPING",
        name="Organizar datos por grupos",
        simple_meaning=(
            "Juntar elementos que comparten "
            "una característica."
        ),
        beginner_goal=(
            "Reconocer qué característica "
            "define cada grupo."
        ),
    ),
    "DATA_SUMMARY": HumanSkill(
        skill_id="DATA_SUMMARY",
        name="Convertir muchos datos en un resultado",
        simple_meaning=(
            "Resumir varios valores mediante "
            "una suma, promedio u otra operación."
        ),
        beginner_goal=(
            "Entender qué valores se resumen "
            "y qué representa el resultado."
        ),
    ),
    "IMPORT_USE": HumanSkill(
        skill_id="IMPORT_USE",
        name="Usar herramientas externas",
        simple_meaning=(
            "Entender cómo Python incorpora "
            "funciones y clases de otros módulos."
        ),
        beginner_goal=(
            "Reconocer qué herramienta se importa "
            "y dónde se utiliza."
        ),
    ),
    "INPUT_OUTPUT": HumanSkill(
        skill_id="INPUT_OUTPUT",
        name="Seguir el recorrido de la información",
        simple_meaning=(
            "Entender qué datos recibe una operación "
            "y qué resultado produce."
        ),
        beginner_goal=(
            "Seguir un dato desde que entra "
            "hasta que sale transformado."
        ),
    ),
    "CONTROL_FLOW": HumanSkill(
        skill_id="CONTROL_FLOW",
        name="Seguir las decisiones del programa",
        simple_meaning=(
            "Entender por qué algunas instrucciones "
            "se ejecutan y otras no."
        ),
        beginner_goal=(
            "Predecir qué camino seguirá el programa "
            "según una condición."
        ),
    ),
}


def get_human_skill(
    skill_id: str,
) -> HumanSkill | None:
    return SKILLS.get(
        skill_id
    )
