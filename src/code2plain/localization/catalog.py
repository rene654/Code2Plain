from __future__ import annotations

from typing import Any


DEFAULT_LANGUAGE = "es"

SUPPORTED_LANGUAGES = (
    "es",
    "en",
    "fr",
)


CATALOGS: dict[str, dict[str, str]] = {

    # ========================================================
    # ESPAÑOL
    # ========================================================

    "es": {
        # Concept labels
        "concept.IMPORT":
            "IMPORTAR (IMPORT)",

        "concept.LOAD DATA":
            "CARGAR DATOS (LOAD DATA)",

        "concept.FILTER":
            "FILTRAR (FILTER)",

        "concept.AGGREGATE":
            "AGRUPAR Y RESUMIR (AGGREGATE)",

        "concept.EXPORT":
            "EXPORTAR (EXPORT)",

        "concept.TRANSFORM":
            "TRANSFORMAR (TRANSFORM)",

        "concept.DECIDE":
            "DECIDIR (DECIDE)",

        "concept.REPEAT":
            "REPETIR (LOOP)",

        "concept.DEFINE":
            "DEFINIR (DEFINE)",

        "concept.CALL":
            "LLAMAR (CALL)",

        "concept.RETURN":
            "DEVOLVER (RETURN)",

        "concept.HANDLE ERROR":
            "MANEJAR ERROR",

        "concept.MODEL":
            "MODELAR (CLASS)",

        "concept.PROCESS":
            "PROCESAR (PROCESS)",


        # Learning mode labels
        "mode.learn.simple":
            "EN PALABRAS SIMPLES",

        "mode.learn.key":
            "IDEA CLAVE",

        "mode.understand.simple":
            "EXPLICACIÓN SIMPLE",

        "mode.understand.why":
            "POR QUÉ EXISTE",

        "mode.deep.mechanics":
            "CÓMO FUNCIONA",

        "mode.deep.syntax":
            "ENFOQUE DE SINTAXIS",

        "mode.deep.note":
            "NOTA TÉCNICA",

        "mode.understand.heading":
            "{concept} · EN EL FLUJO",

        "mode.deep.heading":
            "{concept} · A FONDO",


        # Semantic titles
        "title.import":
            "Importar herramientas",

        "title.load":
            "Cargar datos",

        "title.filter":
            "Filtrar registros",

        "title.aggregate":
            "Agrupar y resumir",

        "title.export":
            "Exportar resultado",


        # Semantic explanations
        "semantic.import.does":
            "Carga herramientas externas que el programa "
            "utilizará más adelante.",

        "semantic.import.learn":
            "Importar permite reutilizar funciones de "
            "librerías en lugar de construir todo desde cero.",

        "semantic.load.does":
            "Lee información desde {source} y guarda el "
            "resultado para que el programa pueda trabajar "
            "con esos datos.",

        "semantic.load.learn":
            "Cargar datos suele ser la etapa de entrada de un "
            "flujo: primero la información entra al programa "
            "y después puede filtrarse, transformarse o "
            "analizarse.",

        "semantic.filter.does":
            "Conserva únicamente las filas que cumplen la "
            "condición escrita entre corchetes.",

        "semantic.filter.status_late":
            'Conserva únicamente las filas donde la columna '
            '"status" es igual a "Late".',

        "semantic.filter.learn":
            "Un filtro aplica una regla a cada fila y conserva "
            "solamente las que cumplen esa regla.",

        "semantic.aggregate.does":
            "Agrupa registros relacionados y calcula "
            "{operation} para cada grupo.",

        "semantic.aggregate.supplier_amount":
            'Agrupa los registros por "supplier" y suma los '
            'valores de "amount" para obtener un total por '
            "proveedor.",

        "semantic.aggregate.learn":
            "Agrupar reúne filas que comparten un valor. "
            "Después, una agregación como suma, promedio o "
            "conteo produce un resultado por grupo.",

        "semantic.export.does":
            "Guarda el resultado procesado en {destination} "
            "para poder utilizarlo fuera del programa de "
            "Python.",

        "semantic.export.learn":
            "Exportar es una etapa de salida: convierte el "
            "resultado interno del programa en algo que una "
            "persona u otro sistema puede usar.",


        # Data source labels
        "source.generic":
            "una fuente de datos",

        "source.excel":
            "un archivo de Excel",

        "source.csv":
            "un archivo CSV",

        "source.sql":
            "una fuente SQL",

        "source.json":
            "un archivo JSON",

        "source.parquet":
            "un archivo Parquet",


        # Aggregation operation labels
        "operation.generic":
            "un cálculo",

        "operation.sum":
            "una suma",

        "operation.mean":
            "un promedio",

        "operation.count":
            "un conteo",

        "operation.min":
            "un mínimo",

        "operation.max":
            "un máximo",


        # Export destination labels
        "destination.generic":
            "un archivo de salida",

        "destination.excel":
            "un archivo de Excel",

        "destination.csv":
            "un archivo CSV",

        "destination.json":
            "un archivo JSON",

        "destination.parquet":
            "un archivo Parquet",


        # Beginner
        "beginner.IMPORT.primary":
            "Python trae una herramienta que este programa "
            "necesitará más adelante.",

        "beginner.IMPORT.key":
            "Importar significa agregar una herramienta al "
            "programa en lugar de construirla tú.",

        "beginner.LOAD DATA.primary":
            "Esta línea abre el archivo de datos y mete su "
            "información dentro de Python para que podamos "
            "trabajar con ella.",

        "beginner.LOAD DATA.key":
            "Antes de analizar datos, primero tienen que "
            "entrar al programa.",

        "beginner.FILTER.primary":
            "Esta línea quita los datos que no queremos y "
            "conserva solamente los que cumplen la regla.",

        "beginner.FILTER.key":
            "Filtrar significa quedarte solamente con los "
            "datos que cumplen una regla.",

        "beginner.AGGREGATE.primary":
            "Este paso junta registros parecidos y los "
            "convierte en un resumen más pequeño.",

        "beginner.AGGREGATE.key":
            "Agrupar y resumir significa convertir muchos "
            "registros detallados en totales o resúmenes "
            "útiles.",

        "beginner.EXPORT.primary":
            "Esta línea guarda el resultado en un archivo que "
            "puedes abrir o compartir fuera de Python.",

        "beginner.EXPORT.key":
            "Exportar significa sacar el resultado de Python "
            "y guardarlo en un lugar útil.",

        "beginner.TRANSFORM.primary":
            "Esta línea cambia información para dejarla lista "
            "para el siguiente paso.",

        "beginner.TRANSFORM.key":
            "Transformar significa cambiar datos de una forma "
            "a otra.",

        "beginner.DECIDE.primary":
            "Esta parte permite que el programa elija qué "
            "hacer dependiendo de si una condición se cumple "
            "o no.",

        "beginner.DECIDE.key":
            "Las condiciones permiten que un programa tome "
            "decisiones.",

        "beginner.REPEAT.primary":
            "Esta parte repite automáticamente la misma acción "
            "varias veces.",

        "beginner.REPEAT.key":
            "Los ciclos evitan escribir la misma acción una y "
            "otra vez.",

        "beginner.DEFINE.primary":
            "Aquí se crea un conjunto de instrucciones que "
            "puede reutilizarse más adelante.",

        "beginner.DEFINE.key":
            "Las funciones permiten reutilizar instrucciones.",

        "beginner.CALL.primary":
            "Aquí Python ejecuta unas instrucciones que ya "
            "existen.",

        "beginner.CALL.key":
            "Llamar una función significa pedirle a Python que "
            "ejecute algo ya definido.",

        "beginner.RETURN.primary":
            "Esta línea devuelve un resultado desde una función "
            "hacia la parte del programa que la llamó.",

        "beginner.RETURN.key":
            "Return entrega el resultado producido por una "
            "función.",


        # Understand
        "understand.IMPORT.primary":
            "El programa prepara las herramientas externas "
            "que necesitará antes de comenzar el trabajo "
            "principal.",

        "understand.IMPORT.why":
            "Sin este paso, Python no conocería las funciones "
            "que proporciona esa librería.",

        "understand.LOAD DATA.primary":
            "Aquí la información entra al programa y queda "
            "disponible para los siguientes pasos.",

        "understand.LOAD DATA.why":
            "Un programa no puede analizar información hasta "
            "que esa información entre al flujo.",

        "understand.FILTER.primary":
            "El programa reduce el conjunto de datos y se "
            "queda solo con los registros relevantes.",

        "understand.FILTER.why":
            "Quitar registros irrelevantes permite que los "
            "siguientes cálculos trabajen solamente con los "
            "datos importantes.",

        "understand.AGGREGATE.primary":
            "Los registros detallados se convierten en un "
            "resumen más fácil de analizar.",

        "understand.AGGREGATE.why":
            "Las filas individuales suelen tener demasiado "
            "detalle. Agruparlas las convierte en información "
            "más útil para tomar decisiones.",

        "understand.EXPORT.primary":
            "El programa toma su resultado interno y lo guarda "
            "fuera de Python.",

        "understand.EXPORT.why":
            "Un resultado se vuelve útil para otras personas "
            "o sistemas cuando puede salir del programa.",

        "understand.TRANSFORM.primary":
            "Este paso prepara o modifica información para "
            "otra parte del programa.",

        "understand.TRANSFORM.why":
            "Las transformaciones intermedias acercan los "
            "datos a la forma que necesita el resultado final.",

        "understand.DECIDE.primary":
            "El programa elige qué camino seguir según una "
            "condición.",

        "understand.DECIDE.why":
            "Las condiciones permiten que el software "
            "reaccione de manera distinta según la situación.",

        "understand.REPEAT.primary":
            "La misma operación se aplica varias veces sin "
            "tener que escribirla repetidamente.",

        "understand.REPEAT.why":
            "Los ciclos automatizan trabajo repetitivo y "
            "evitan duplicar código.",

        "understand.DEFINE.primary":
            "Un comportamiento reutilizable se guarda para "
            "poder utilizarlo después.",

        "understand.DEFINE.why":
            "Las funciones reutilizables facilitan mantener, "
            "probar y entender el código.",

        "understand.CALL.primary":
            "En este punto se ejecuta un comportamiento que "
            "ya estaba definido.",

        "understand.CALL.why":
            "Las llamadas conectan una función con el momento "
            "en que necesitamos ejecutarla.",


        # Deep dive
        "deep.IMPORT.mechanics":
            "Python localiza el módulo solicitado y hace que "
            "sus objetos estén disponibles dentro de este "
            "archivo.",

        "deep.IMPORT.syntax":
            "`import ... as ...` carga un módulo y puede "
            "asignarle un alias más corto dentro del programa.",

        "deep.IMPORT.technical":
            "Python guarda los módulos importados en "
            "`sys.modules`, por lo que normalmente un módulo "
            "se inicializa una sola vez por proceso.",

        "deep.LOAD DATA.mechanics":
            "Una función de la librería lee una fuente externa, "
            "crea una estructura de datos en memoria y la "
            "asigna a una variable.",

        "deep.LOAD DATA.syntax":
            "Python evalúa primero la expresión situada a la "
            "derecha de `=` y después asigna el resultado a "
            "la variable de la izquierda.",

        "deep.LOAD DATA.technical":
            "Con conjuntos de datos grandes, cargar todo en "
            "memoria puede ser costoso. El procesamiento por "
            "bloques o el filtrado desde la base de datos "
            "puede reducir el uso de memoria.",

        "deep.FILTER.mechanics":
            "La comparación crea una máscara booleana: cada "
            "fila produce True o False. Los corchetes externos "
            "conservan únicamente las filas cuyo valor es True.",

        "deep.FILTER.syntax":
            "`df[condición]` es sintaxis de selección en "
            "pandas. La expresión dentro de los corchetes "
            "decide qué filas se conservan.",

        "deep.FILTER.technical":
            "En pandas, las máscaras booleanas deben alinearse "
            "con el índice del DataFrame. Los valores faltantes "
            "y tipos incompatibles pueden afectar las "
            "comparaciones.",

        "deep.AGGREGATE.mechanics":
            "Los datos se dividen en grupos y una función de "
            "agregación se calcula de manera independiente para "
            "cada grupo.",

        "deep.AGGREGATE.syntax":
            "El encadenamiento de métodos aplica operaciones "
            "de izquierda a derecha: primero agrupa, después "
            "selecciona una columna y finalmente agrega.",

        "deep.AGGREGATE.technical":
            "`groupby()` suele seguir el modelo dividir → "
            "aplicar → combinar: separa filas en grupos, aplica "
            "una operación y combina los resultados.",

        "deep.EXPORT.mechanics":
            "El objeto que existe en memoria se convierte en "
            "un formato externo y se escribe en un archivo.",

        "deep.EXPORT.syntax":
            "La notación con punto llama un método del objeto "
            "actual, por ejemplo `.to_excel()`.",

        "deep.EXPORT.technical":
            "El formato elegido afecta tamaño del archivo, "
            "tipos de datos, interoperabilidad y velocidad "
            "de escritura.",

        "deep.generic.mechanics":
            "Python evalúa esta instrucción según su sintaxis "
            "y utiliza o almacena el valor resultante.",

        "deep.generic.assignment":
            "`=` representa asignación: Python evalúa el lado "
            "derecho y vincula ese resultado al nombre situado "
            "a la izquierda.",

        "deep.generic.syntax":
            "Lee primero las operaciones internas y después "
            "avanza hacia afuera siguiendo las reglas de "
            "evaluación de Python.",

        "deep.generic.technical":
            "El comportamiento técnico depende de los tipos "
            "de datos, la librería utilizada y el contexto de "
            "ejecución.",

        "understand.generic.why":
            "Este paso forma parte de la entrada, "
            "transformación, decisión o salida del programa.",
    },


    # ========================================================
    # ENGLISH
    # ========================================================

    "en": {
        "concept.IMPORT": "IMPORT",
        "concept.LOAD DATA": "LOAD DATA",
        "concept.FILTER": "FILTER",
        "concept.AGGREGATE": "AGGREGATE",
        "concept.EXPORT": "EXPORT",
        "concept.TRANSFORM": "TRANSFORM",
        "concept.DECIDE": "DECIDE",
        "concept.REPEAT": "REPEAT",
        "concept.DEFINE": "DEFINE",
        "concept.CALL": "CALL",
        "concept.RETURN": "RETURN",
        "concept.HANDLE ERROR": "HANDLE ERROR",
        "concept.MODEL": "MODEL",
        "concept.PROCESS": "PROCESS",

        "mode.learn.simple": "IN SIMPLE WORDS",
        "mode.learn.key": "KEY IDEA",
        "mode.understand.simple": "PLAIN ENGLISH",
        "mode.understand.why": "WHY IT EXISTS",
        "mode.deep.mechanics": "HOW IT WORKS",
        "mode.deep.syntax": "SYNTAX FOCUS",
        "mode.deep.note": "TECHNICAL NOTE",

        "mode.understand.heading":
            "{concept} · IN THE FLOW",

        "mode.deep.heading":
            "{concept} · DEEP DIVE",

        "beginner.IMPORT.primary":
            "Python brings in a tool that this program will "
            "need later.",

        "beginner.IMPORT.key":
            "Importing means adding a tool instead of building "
            "it yourself.",

        "beginner.LOAD DATA.primary":
            "This line opens the data file and puts its "
            "information inside Python so we can use it.",

        "beginner.LOAD DATA.key":
            "Data has to enter the program before Python can "
            "analyze it.",

        "beginner.FILTER.primary":
            "This line removes data we do not want and keeps "
            "only the data that follows the rule.",

        "beginner.FILTER.key":
            "Filtering means keeping only data that matches "
            "a rule.",

        "beginner.AGGREGATE.primary":
            "This step joins similar records and turns them "
            "into a smaller summary.",

        "beginner.AGGREGATE.key":
            "Aggregating turns detailed records into useful "
            "totals or summaries.",

        "beginner.EXPORT.primary":
            "This line saves the result to a file that can be "
            "opened or shared outside Python.",

        "beginner.EXPORT.key":
            "Exporting means taking a result out of Python and "
            "saving it somewhere useful.",

        "understand.IMPORT.primary":
            "The program prepares external tools before doing "
            "the main work.",

        "understand.IMPORT.why":
            "Without this step Python would not know about the "
            "library functionality.",

        "understand.LOAD DATA.primary":
            "Information enters the program here and becomes "
            "available for later processing.",

        "understand.LOAD DATA.why":
            "A program cannot analyze information until it "
            "enters the workflow.",

        "understand.FILTER.primary":
            "The program reduces the dataset to the records "
            "that matter.",

        "understand.FILTER.why":
            "Removing irrelevant records makes later "
            "calculations work only on useful data.",

        "understand.AGGREGATE.primary":
            "Detailed records become a smaller summary that "
            "is easier to analyze.",

        "understand.AGGREGATE.why":
            "Aggregation turns detailed rows into information "
            "that is easier to use for decisions.",

        "understand.EXPORT.primary":
            "The program writes its internal result outside "
            "Python.",

        "understand.EXPORT.why":
            "Results become useful to people or systems when "
            "they can leave the program.",

        "deep.IMPORT.mechanics":
            "Python resolves the requested module and makes "
            "its objects available to this file.",

        "deep.IMPORT.syntax":
            "`import ... as ...` loads a module and can give "
            "it a shorter local alias.",

        "deep.IMPORT.technical":
            "Imports are cached in `sys.modules`, so modules "
            "normally initialize once per Python process.",

        "deep.LOAD DATA.mechanics":
            "A library function reads an external source and "
            "returns an in-memory data structure.",

        "deep.LOAD DATA.syntax":
            "Python evaluates the right side of `=` first and "
            "then assigns the result to the variable.",

        "deep.LOAD DATA.technical":
            "Large datasets may require chunking or "
            "database-side filtering to reduce memory use.",

        "deep.FILTER.mechanics":
            "The comparison creates a Boolean mask. Each row "
            "becomes True or False, and only True rows remain.",

        "deep.FILTER.syntax":
            "`df[condition]` is pandas selection syntax. The "
            "condition inside the brackets chooses the rows.",

        "deep.FILTER.technical":
            "Boolean masks must align with the DataFrame index. "
            "Missing values and type mismatches can affect "
            "comparisons.",

        "deep.AGGREGATE.mechanics":
            "Data is divided into groups and an aggregation "
            "runs independently for every group.",

        "deep.AGGREGATE.syntax":
            "Method chaining applies operations from left to "
            "right: group, select, then aggregate.",

        "deep.AGGREGATE.technical":
            "`groupby()` commonly follows split → apply → "
            "combine.",

        "deep.EXPORT.mechanics":
            "The in-memory object is serialized into an "
            "external format and written to a file.",

        "deep.EXPORT.syntax":
            "Dot notation calls a method on the current object, "
            "such as `.to_excel()`.",

        "deep.EXPORT.technical":
            "File format affects size, data types, "
            "interoperability, and write performance.",

        "deep.generic.mechanics":
            "Python evaluates this statement according to its "
            "syntax and uses or stores the result.",

        "deep.generic.assignment":
            "`=` assigns the value evaluated on the right to "
            "the name on the left.",

        "deep.generic.syntax":
            "Read inner operations first and then move outward "
            "according to Python evaluation rules.",

        "deep.generic.technical":
            "Technical behavior depends on data types, library "
            "implementation, and runtime context.",

        "understand.generic.why":
            "This step contributes to the program's input, "
            "transformation, decision, or output flow.",
    },


    # ========================================================
    # FRANÇAIS
    # ========================================================

    "fr": {
        "concept.IMPORT": "IMPORTER (IMPORT)",
        "concept.LOAD DATA": "CHARGER LES DONNÉES (LOAD DATA)",
        "concept.FILTER": "FILTRER (FILTER)",
        "concept.AGGREGATE": "REGROUPER ET RÉSUMER (AGGREGATE)",
        "concept.EXPORT": "EXPORTER (EXPORT)",
        "concept.TRANSFORM": "TRANSFORMER (TRANSFORM)",
        "concept.DECIDE": "DÉCIDER (DECIDE)",
        "concept.REPEAT": "RÉPÉTER (LOOP)",
        "concept.DEFINE": "DÉFINIR (DEFINE)",
        "concept.CALL": "APPELER (CALL)",
        "concept.RETURN": "RETOURNER (RETURN)",
        "concept.HANDLE ERROR": "GÉRER UNE ERREUR",
        "concept.MODEL": "MODÉLISER (CLASS)",
        "concept.PROCESS": "TRAITER (PROCESS)",

        "mode.learn.simple": "EN TERMES SIMPLES",
        "mode.learn.key": "IDÉE CLÉ",
        "mode.understand.simple": "EXPLICATION SIMPLE",
        "mode.understand.why": "POURQUOI CETTE ÉTAPE EXISTE",
        "mode.deep.mechanics": "COMMENT ÇA FONCTIONNE",
        "mode.deep.syntax": "FOCUS SUR LA SYNTAXE",
        "mode.deep.note": "NOTE TECHNIQUE",

        "mode.understand.heading":
            "{concept} · DANS LE FLUX",

        "mode.deep.heading":
            "{concept} · EN PROFONDEUR",

        "beginner.IMPORT.primary":
            "Python ajoute un outil dont le programme aura "
            "besoin plus tard.",

        "beginner.IMPORT.key":
            "Importer signifie ajouter un outil au programme "
            "au lieu de le construire soi-même.",

        "beginner.LOAD DATA.primary":
            "Cette ligne ouvre le fichier de données et place "
            "son contenu dans Python pour pouvoir l'utiliser.",

        "beginner.LOAD DATA.key":
            "Les données doivent entrer dans le programme "
            "avant de pouvoir être analysées.",

        "beginner.FILTER.primary":
            "Cette ligne retire les données inutiles et garde "
            "seulement celles qui respectent la règle.",

        "beginner.FILTER.key":
            "Filtrer signifie conserver uniquement les données "
            "qui respectent une règle.",

        "beginner.AGGREGATE.primary":
            "Cette étape regroupe des enregistrements similaires "
            "et les transforme en un résumé plus petit.",

        "beginner.AGGREGATE.key":
            "Agréger signifie transformer de nombreux détails "
            "en totaux ou résumés utiles.",

        "beginner.EXPORT.primary":
            "Cette ligne enregistre le résultat dans un fichier "
            "qui peut être ouvert ou partagé hors de Python.",

        "beginner.EXPORT.key":
            "Exporter signifie sortir le résultat de Python et "
            "l'enregistrer dans un format utile.",

        "understand.IMPORT.primary":
            "Le programme prépare les outils externes avant de "
            "commencer son travail principal.",

        "understand.IMPORT.why":
            "Sans cette étape, Python ne connaîtrait pas les "
            "fonctions fournies par la bibliothèque.",

        "understand.LOAD DATA.primary":
            "Les informations entrent ici dans le programme et "
            "deviennent disponibles pour les étapes suivantes.",

        "understand.LOAD DATA.why":
            "Un programme ne peut pas analyser des informations "
            "avant qu'elles n'entrent dans le flux.",

        "understand.FILTER.primary":
            "Le programme réduit le jeu de données aux "
            "enregistrements utiles.",

        "understand.FILTER.why":
            "Supprimer les données inutiles permet aux calculs "
            "suivants de travailler uniquement sur les données "
            "pertinentes.",

        "understand.AGGREGATE.primary":
            "Les enregistrements détaillés deviennent un résumé "
            "plus facile à analyser.",

        "understand.AGGREGATE.why":
            "L'agrégation transforme les lignes détaillées en "
            "informations plus utiles pour décider.",

        "understand.EXPORT.primary":
            "Le programme enregistre son résultat en dehors "
            "de Python.",

        "understand.EXPORT.why":
            "Un résultat devient utile lorsqu'une personne ou "
            "un autre système peut l'utiliser.",

        "deep.IMPORT.mechanics":
            "Python localise le module demandé et rend ses "
            "objets disponibles dans ce fichier.",

        "deep.IMPORT.syntax":
            "`import ... as ...` charge un module et peut lui "
            "attribuer un alias plus court.",

        "deep.IMPORT.technical":
            "Les imports sont mémorisés dans `sys.modules`, "
            "donc un module est normalement initialisé une "
            "seule fois par processus.",

        "deep.LOAD DATA.mechanics":
            "Une fonction de bibliothèque lit une source "
            "externe et crée une structure de données en "
            "mémoire.",

        "deep.LOAD DATA.syntax":
            "Python évalue d'abord l'expression à droite de "
            "`=` puis assigne le résultat à la variable.",

        "deep.LOAD DATA.technical":
            "Pour de grands jeux de données, le traitement par "
            "blocs ou le filtrage côté base de données peut "
            "réduire l'utilisation de mémoire.",

        "deep.FILTER.mechanics":
            "La comparaison crée un masque booléen. Chaque "
            "ligne devient True ou False et seules les lignes "
            "True sont conservées.",

        "deep.FILTER.syntax":
            "`df[condition]` est une syntaxe de sélection "
            "pandas. La condition choisit les lignes.",

        "deep.FILTER.technical":
            "Les masques booléens doivent être alignés avec "
            "l'index du DataFrame.",

        "deep.AGGREGATE.mechanics":
            "Les données sont séparées en groupes et une "
            "agrégation est calculée pour chaque groupe.",

        "deep.AGGREGATE.syntax":
            "Le chaînage de méthodes applique les opérations "
            "de gauche à droite : regrouper, sélectionner, "
            "puis agréger.",

        "deep.AGGREGATE.technical":
            "`groupby()` suit généralement le modèle "
            "séparer → appliquer → combiner.",

        "deep.EXPORT.mechanics":
            "L'objet en mémoire est converti dans un format "
            "externe et écrit dans un fichier.",

        "deep.EXPORT.syntax":
            "La notation par point appelle une méthode de "
            "l'objet courant, par exemple `.to_excel()`.",

        "deep.EXPORT.technical":
            "Le format choisi influence la taille, les types "
            "de données, l'interopérabilité et les "
            "performances.",

        "deep.generic.mechanics":
            "Python évalue cette instruction selon sa syntaxe "
            "et utilise ou stocke le résultat.",

        "deep.generic.assignment":
            "`=` associe la valeur calculée à droite au nom "
            "situé à gauche.",

        "deep.generic.syntax":
            "Lisez d'abord les opérations internes puis "
            "progressez vers l'extérieur.",

        "deep.generic.technical":
            "Le comportement technique dépend des types de "
            "données, de la bibliothèque et du contexte "
            "d'exécution.",

        "understand.generic.why":
            "Cette étape participe à l'entrée, la "
            "transformation, la décision ou la sortie du "
            "programme.",
    },
}


class Localizer:
    def __init__(
        self,
        language: str = DEFAULT_LANGUAGE,
    ) -> None:
        if language not in SUPPORTED_LANGUAGES:
            raise ValueError(
                "Unsupported language: "
                f"{language}. "
                "Supported languages: "
                f"{', '.join(SUPPORTED_LANGUAGES)}"
            )

        self.language = language

    def t(
        self,
        key: str,
        **values: Any,
    ) -> str:
        catalog = CATALOGS[
            self.language
        ]

        value = catalog.get(key)

        if value is None:
            # English is the neutral fallback.
            value = (
                CATALOGS["en"]
                .get(key)
            )

        if value is None:
            # Never crash the product because copy is missing.
            return key

        if values:
            return value.format(
                **values
            )

        return value

    def concept_label(
        self,
        concept: str,
    ) -> str:
        return self.t(
            f"concept.{concept}"
        )
