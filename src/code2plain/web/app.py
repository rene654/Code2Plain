from fastapi import APIRouter
from fastapi.responses import HTMLResponse


router = APIRouter()


@router.get(
    "/learn",
    response_class=HTMLResponse,
)
def learning_page():
    return HTMLResponse(
        r"""
<!doctype html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <meta
        name="viewport"
        content="width=device-width, initial-scale=1"
    >
    <title>Code2Plain</title>

    <style>
        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            background: #fafafa;
            color: #171717;
            font-family:
                Inter,
                system-ui,
                -apple-system,
                sans-serif;
        }

        main {
            width: min(1440px, 94%);
            margin: 32px auto 64px;
        }

        .app-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 24px;
            margin-bottom: 24px;
        }

        .brand-lockup {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .brand-mark {
            display: block;
            width: 40px;
            height: 40px;
            object-fit: contain;
            flex: 0 0 auto;
        }

        .brand-copy h1 {
            margin: 0;
            font-size: 20px;
            letter-spacing: -0.02em;
        }

        .brand-copy p {
            margin: 3px 0 0;
            color: #737373;
            font-size: 12px;
        }

        .privacy-badge {
            padding: 7px 11px;
            border: 1px solid #e5e5e5;
            border-radius: 999px;
            background: #ffffff;
            color: #525252;
            font-size: 11px;
            font-weight: 600;
            white-space: nowrap;
        }

        .workspace {
            display: grid;
            grid-template-columns:
                minmax(360px, 0.9fr)
                minmax(480px, 1.1fr);
            gap: 18px;
            align-items: start;
        }

        .workspace-panel {
            border: 1px solid #e5e5e5;
            border-radius: 16px;
            background: #ffffff;
            box-shadow:
                0 10px 30px
                rgba(0, 0, 0, 0.035);
            overflow: hidden;
        }

        .panel-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 12px;
            min-height: 54px;
            padding: 0 18px;
            border-bottom: 1px solid #eeeeee;
        }

        .panel-title {
            font-size: 13px;
            font-weight: 700;
        }

        .panel-kicker {
            color: #8a8a8a;
            font-size: 11px;
        }

        .source-panel-body {
            padding: 18px;
        }

        .learning-panel-body {
            min-height: 560px;
            padding: 8px 14px 14px;
        }

        .learning-empty {
            display: grid;
            place-items: center;
            min-height: 480px;
            padding: 48px;
            text-align: center;
            color: #737373;
        }

        .learning-empty strong {
            display: block;
            margin-bottom: 6px;
            color: #262626;
            font-size: 15px;
        }

        @media (max-width: 900px) {
            .workspace {
                grid-template-columns: 1fr;
            }

            .app-header {
                align-items: flex-start;
            }
        }

        h1 {
            margin-bottom: 4px;
            font-size: 32px;
        }

        .subtitle {
            margin-top: 0;
            color: #737373;
        }

        input[type="url"] {
            width: 100%;
            margin-top: 0;
            padding: 13px 15px;
            border:
                1px solid #dedede;
            border-radius: 10px;
            background: white;
            color: #171717;
            font-size: 14px;
        }

        .adaptive-note {
            margin: 8px 0 0;
            padding: 7px 9px;
            border-radius: 8px;
            background: #f7f7f7;
            color: #525252;
            font-size: 11px;
            line-height: 1.4;
        }

        .adaptive-note.reduced {
            background: #f0fdf4;
            color: #166534;
        }

        .adaptive-note.reinforcement {
            background: #fff7ed;
            color: #9a3412;
        }

        .learning-check {
            margin-top: 10px;
            border-top: 1px solid #eeeeee;
            padding-top: 9px;
        }

        .learning-check summary {
            list-style: none;
            cursor: pointer;
            font-size: 12px;
            font-weight: 700;
            color: #404040;
        }

        .learning-check summary::-webkit-details-marker {
            display: none;
        }

        .learning-check summary::after {
            content: " ▾";
            color: #8a8a8a;
        }

        .learning-check[open] summary::after {
            content: " ▴";
        }

        .learning-check-body {
            margin-top: 10px;
            padding: 10px;
            border: 1px solid #ececec;
            border-radius: 10px;
            background: #fafafa;
        }

        .learning-check-question {
            margin-bottom: 8px;
            font-size: 12px;
            font-weight: 600;
            line-height: 1.45;
        }

        .learning-check-option {
            display: flex;
            gap: 8px;
            align-items: flex-start;
            margin: 7px 0;
            font-size: 12px;
            line-height: 1.4;
        }

        .learning-check-verify {
            margin-top: 8px;
            padding: 7px 11px;
            border: 0;
            border-radius: 8px;
            background: #171717;
            color: #ffffff;
            font-size: 12px;
            font-weight: 700;
            cursor: pointer;
        }

        .learning-check-result {
            margin-top: 8px;
            font-size: 12px;
            line-height: 1.45;
        }

        .learning-check-result.success {
            color: #166534;
        }

        .learning-check-result.review {
            color: #991b1b;
        }

        .learning-feedback {
            margin-top: 12px;
            padding-top: 10px;
            border-top: 1px solid rgba(125, 125, 125, 0.15);
        }

        .learning-feedback-title {
            font-size: 12px;
            font-weight: 600;
            margin-bottom: 8px;
        }

        .learning-feedback-actions {
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
        }

        .learning-feedback-actions button {
            padding: 8px 12px;
            border-radius: 8px;
            border: 1px solid #d4d4d4;
            background: #ffffff;
            color: #171717;
            cursor: pointer;
            font-size: 12px;
            font-weight: 600;
        }

        .learning-feedback-actions button:hover {
            background: #f5f5f5;
        }

        .learning-feedback-message {
            margin-top: 10px;
            font-size: 12px;
            line-height: 1.45;
            color: #525252;
            max-width: 760px;
        }

        .privacy-note {
            margin-top: 12px;
            padding: 10px 12px;
            border: 1px solid rgba(125, 125, 125, 0.18);
            border-radius: 10px;
            font-size: 12px;
            line-height: 1.45;
            color: #525252;
            background: rgba(125, 125, 125, 0.04);
        }

        .privacy-note details {
            margin-top: 6px;
        }

        .privacy-note summary {
            cursor: pointer;
            font-weight: 600;
        }

        .privacy-note p {
            margin: 7px 0 0;
        }

        .source-separator {
            margin: 12px 0 -12px;
            text-align: center;
            color: #a3a3a3;
            font-size: 12px;
        }

        textarea {
            width: 100%;
            min-height: 360px;
            margin-top: 18px;
            padding: 20px;
            resize: vertical;

            border:
                1px solid #dedede;
            border-radius: 14px;

            background: white;
            color: #171717;

            font-family:
                "SFMono-Regular",
                Consolas,
                monospace;
            font-size: 14px;
            line-height: 1.6;
        }

        button {
            margin-top: 12px;
            padding: 11px 18px;

            border: 0;
            border-radius: 9px;

            background: #171717;
            color: white;

            font-weight: 600;
            cursor: pointer;
        }

        #results {
            margin-top: 0;
        }

        .item {
            margin: 12px 0;
            padding: 14px 16px;

            border-left:
                4px solid
                var(--accent);

            border-radius: 8px;
            background: white;

            box-shadow:
                0 1px 3px
                rgba(0,0,0,.06);
        }

        .meta {
            display: flex;
            justify-content:
                space-between;
            gap: 12px;

            font-size: 12px;
            color: #737373;
        }

        .concept {
            margin-top: 5px;
            font-weight: 700;
            display: flex;
            gap: 6px;
            flex-wrap: wrap;
        }

        .concept-chip {
            display: inline-block;
            padding: 2px 7px;
            border-radius: 999px;
            font-size: 11px;
            font-weight: 700;
            background:
                color-mix(
                    in srgb,
                    var(--chip-color) 18%,
                    white
                );
            border:
                1px solid
                color-mix(
                    in srgb,
                    var(--chip-color) 48%,
                    white
                );
        }

        .explanation {
            margin-top: 4px;
        }

        .code {
            margin-top: 8px;
            font-family:
                "SFMono-Regular",
                Consolas,
                monospace;
            font-size: 12px;
            color: #525252;
        }

        .code2plain-code-highlight {
            padding: 1px 2px;
            border-radius: 3px;
            font-weight: 600;
        }

        details {
            margin-top: 8px;
            font-size: 12px;
            color: #525252;
        }

        summary {
            cursor: pointer;
            font-weight: 600;
            opacity: 0.72;
            font-size: 12px;
        }

        .challenge {
            margin-top: 8px;
            font-size: 12px;
            color: #737373;
        }

        .empty {
            color: #737373;
        }
    </style>
</head>

<body>
<main>
    <header class="app-header">
        <div class="brand-lockup">
            <img
                class="brand-mark"
                src="/static/brand/code2plain-monogram.png"
                alt="Code2Plain"
            >

            <div class="brand-copy">
                <h1>Code2Plain</h1>
                <p>
                    Aprende con el código que ya estás usando.
                </p>
            </div>
        </div>

        <div class="privacy-badge">
            🔒 Código temporal · no almacenado
        </div>
    </header>

    <section class="workspace">
        <div class="workspace-panel">
            <div class="panel-header">
                <span class="panel-title">
                    Tu código
                </span>

                <span class="panel-kicker">
                    Python
                </span>
            </div>

            <div class="source-panel-body">
                <input
                    id="githubUrl"
                    type="url"
                    placeholder="Abrir archivo desde GitHub"
                >

                <div class="source-separator">
                    o pega código
                </div>

                <textarea
                    id="code"
                    placeholder="Pega o escribe código aquí..."
                    spellcheck="false"
                ></textarea>

                <button id="learn">
                    Explicar código
                </button>

                <div class="privacy-note">
                    🔒 Tu código se procesa temporalmente
                    y no se guarda.
                    Solo conservamos conceptos
                    de aprendizaje y progreso.

                    <details>
                        <summary>
                            ¿Qué significa esto?
                        </summary>

                        <p>
                            El código se utiliza únicamente
                            para generar la explicación actual.
                            No se conserva como memoria de
                            aprendizaje. Code2Plain recuerda
                            conceptos abstractos y tu progreso.
                        </p>
                    </details>
                </div>
            </div>
        </div>

        <div class="workspace-panel">
            <div class="panel-header">
                <span class="panel-title">
                    Entiende este código
                </span>

                <span class="panel-kicker">
                    Aprendizaje adaptativo
                </span>
            </div>

            <div class="learning-panel-body">
                <div
                    id="learningEmpty"
                    class="learning-empty"
                >
                    <div>
                        <strong>
                            Tu explicación aparecerá aquí
                        </strong>

                        Pega código o abre un archivo
                        de GitHub para empezar.
                    </div>
                </div>

                <div id="results"></div>
            </div>
        </div>
    </section>
</main>

<script>
const colors = [
    "#eab308",
    "#22c55e",
    "#ec4899",
    "#38bdf8",
    "#a855f7"
];

const button =
    document.getElementById("learn");

const code =
    document.getElementById("code");

const githubUrl =
    document.getElementById(
        "githubUrl"
    );

const results =
    document.getElementById("results");

const learningEmpty =
    document.getElementById(
        "learningEmpty"
    );


function getOrCreateLearningUserId() {
    const storageKey =
        "code2plain.learning_user_id";

    try {
        const existing =
            window.localStorage.getItem(
                storageKey
            );

        if (existing) {
            return existing;
        }

        const generated =
            (
                window.crypto
                && window.crypto.randomUUID
            )
            ? (
                "anon-"
                + window.crypto.randomUUID()
            )
            : (
                "anon-"
                + Date.now().toString(36)
                + "-"
                + Math.random()
                    .toString(36)
                    .slice(2)
            );

        window.localStorage.setItem(
            storageKey,
            generated
        );

        return generated;

    } catch (error) {
        return (
            "session-"
            + Date.now().toString(36)
            + "-"
            + Math.random()
                .toString(36)
                .slice(2)
        );
    }
}


const learningUserId =
    getOrCreateLearningUserId();


async function sendLearningFeedback(
    skillId,
    correct,
    container
) {
    const response = await fetch(
        "/v1/learning/answer",
        {
            method: "POST",
            headers: {
                "Content-Type":
                    "application/json"
            },
            body: JSON.stringify({
                user_id:
                    learningUserId,
                skill_id:
                    skillId,
                correct
            })
        }
    );

    if (!response.ok) {
        container.textContent =
            "No pude registrar el progreso.";
        return;
    }

    const data =
        await response.json();

    container.textContent =
        data.message
        + " "
        + data.next_step;
}


button.addEventListener(
    "click",
    async () => {

        const text =
            code.value.trim();

        const url =
            githubUrl.value.trim();

        if (
            !text
            && !url
        ) {
            return;
        }

        button.disabled = true;
        button.textContent =
            "Analizando...";

        results.innerHTML = "";

        if (learningEmpty) {
            learningEmpty.style.display =
                "none";
        }

        try {
            const endpoint =
                url
                ? "/v1/github-file/learn"
                : "/v1/context-block-learn";

            const requestBody =
                url
                ? { url }
                : {
                    code: text,
                    user_id:
                        learningUserId
                };

            const response =
                await fetch(
                    endpoint,
                    {
                        method: "POST",
                        headers: {
                            "Content-Type":
                                "application/json"
                        },
                        body:
                            JSON.stringify(
                                requestBody
                            )
                    }
                );

            const payload =
                await response.json();

            if (
                !payload.items?.length
            ) {
                results.innerHTML =
                    '<p class="empty">'
                    + 'No encontré conceptos '
                    + 'relevantes todavía.'
                    + '</p>';

                return;
            }

            payload.items.forEach(
                (item, index) => {

                    const element =
                        document.createElement(
                            "div"
                        );

                    element.className =
                        "item";

                    element.style
                        .setProperty(
                            "--accent",
                            colors[
                                index
                                % colors.length
                            ]
                        );

                    const meta =
                        document.createElement(
                            "div"
                        );

                    meta.className =
                        "meta";

                    const line =
                        document.createElement(
                            "span"
                        );

                    line.textContent =
                        item.start_line
                        === item.end_line
                        ? `Línea ${item.start_line}`
                        : `Líneas ${item.start_line}-${item.end_line}`;

                    const confidence =
                        document.createElement(
                            "span"
                        );

                    confidence.textContent =
                        item.input_from
                        ? `Entra: ${item.input_from}`
                        : "";

                    meta.append(
                        line,
                        confidence
                    );

                    const concept =
                        document.createElement(
                            "div"
                        );

                    concept.className =
                        "concept";

                    concept.textContent =
                        item.output_to
                        ? `Resultado → ${item.output_to}`
                        : "Paso del programa";

                    const explanation =
                        document.createElement(
                            "div"
                        );

                    explanation.className =
                        "explanation";

                    explanation.textContent =
                        item.explanation;

                    const why =
                        document.createElement(
                            "details"
                        );

                    const whyTitle =
                        document.createElement(
                            "summary"
                        );

                    whyTitle.textContent =
                        "¿Por qué?";

                    const whyText =
                        document.createElement(
                            "div"
                        );

                    whyText.textContent =
                        item.why;

                    why.append(
                        whyTitle,
                        whyText
                    );

                    const challenge =
                        document.createElement(
                            "div"
                        );

                    challenge.className =
                        "challenge";

                    if (item.experiment) {
                        challenge.textContent =
                            "Prueba mental: "
                            + item.experiment;
                    } else {
                        challenge.style.display =
                            "none";
                    }

                    const snippet =
                        document.createElement(
                            "div"
                        );

                    snippet.className =
                        "code";

                    const conceptText =
                        item.concept || "";

                    const conceptColors = {
                        "FILTER": "#ec4899",
                        "GROUP": "#eab308",
                        "SELECT": "#38bdf8",
                        "AGGREGATE": "#22c55e",
                    };

                    function appendColoredCode(
                        container,
                        codeText,
                        concepts
                    ) {
                        const mappings = [];

                        if (
                            concepts.includes("FILTER")
                        ) {
                            const match =
                                codeText.match(
                                    /\[[^\]]+==[^\]]+\]/
                                );

                            if (match) {
                                mappings.push({
                                    start: match.index,
                                    end:
                                        match.index
                                        + match[0].length,
                                    color:
                                        conceptColors.FILTER,
                                });
                            }
                        }

                        if (
                            concepts.includes("GROUP")
                        ) {
                            const match =
                                codeText.match(
                                    /\.groupby\([^)]*\)/
                                );

                            if (match) {
                                mappings.push({
                                    start: match.index,
                                    end:
                                        match.index
                                        + match[0].length,
                                    color:
                                        conceptColors.GROUP,
                                });
                            }
                        }

                        if (
                            concepts.includes("SELECT")
                        ) {
                            const matches = [
                                ...codeText.matchAll(
                                    /\[[\"'][^\]]+[\"']\]/g
                                )
                            ];

                            const match =
                                matches.at(-1);

                            if (match) {
                                mappings.push({
                                    start: match.index,
                                    end:
                                        match.index
                                        + match[0].length,
                                    color:
                                        conceptColors.SELECT,
                                });
                            }
                        }

                        if (
                            concepts.includes(
                                "AGGREGATE"
                            )
                        ) {
                            const match =
                                codeText.match(
                                    /\.sum\(\)/
                                );

                            if (match) {
                                mappings.push({
                                    start: match.index,
                                    end:
                                        match.index
                                        + match[0].length,
                                    color:
                                        conceptColors.AGGREGATE,
                                });
                            }
                        }

                        mappings.sort(
                            (a, b) =>
                                a.start - b.start
                        );

                        let cursor = 0;

                        for (
                            const mapping
                            of mappings
                        ) {
                            if (
                                mapping.start
                                > cursor
                            ) {
                                container.append(
                                    document.createTextNode(
                                        codeText.slice(
                                            cursor,
                                            mapping.start
                                        )
                                    )
                                );
                            }

                            const mark =
                                document.createElement(
                                    "span"
                                );

                            mark.className =
                                "code2plain-code-highlight";

                            mark.style.backgroundColor =
                                mapping.color + "33";

                            mark.style.boxShadow =
                                "inset 0 -2px 0 "
                                + mapping.color;

                            mark.textContent =
                                codeText.slice(
                                    mapping.start,
                                    mapping.end
                                );

                            container.append(
                                mark
                            );

                            cursor =
                                mapping.end;
                        }

                        if (
                            cursor
                            < codeText.length
                        ) {
                            container.append(
                                document.createTextNode(
                                    codeText.slice(
                                        cursor
                                    )
                                )
                            );
                        }
                    }

                    appendColoredCode(
                        snippet,
                        item.code,
                        conceptText
                    );

                    const learningCheck =
                        document.createElement(
                            "details"
                        );

                    learningCheck.className =
                        "learning-check";

                    if (
                        item.check
                        && item.skill_id
                    ) {
                        const summary =
                            document.createElement(
                                "summary"
                            );

                        summary.textContent =
                            "Comprueba lo que entendiste";

                        const body =
                            document.createElement(
                                "div"
                            );

                        body.className =
                            "learning-check-body";

                        const question =
                            document.createElement(
                                "div"
                            );

                        question.className =
                            "learning-check-question";

                        question.textContent =
                            item.check.question;

                        const optionInputs = [];

                        item.check.options.forEach(
                            (option, optionIndex) => {
                                const label =
                                    document.createElement(
                                        "label"
                                    );

                                label.className =
                                    "learning-check-option";

                                const radio =
                                    document.createElement(
                                        "input"
                                    );

                                radio.type = "radio";

                                radio.name =
                                    "check-"
                                    + index;

                                radio.value =
                                    optionIndex;

                                const optionText =
                                    document.createElement(
                                        "span"
                                    );

                                optionText.textContent =
                                    option;

                                label.append(
                                    radio,
                                    optionText
                                );

                                optionInputs.push(
                                    radio
                                );

                                body.append(
                                    label
                                );
                            }
                        );

                        const verifyButton =
                            document.createElement(
                                "button"
                            );

                        verifyButton.type =
                            "button";

                        verifyButton.className =
                            "learning-check-verify";

                        verifyButton.textContent =
                            "Verificar";

                        const resultMessage =
                            document.createElement(
                                "div"
                            );

                        resultMessage.className =
                            "learning-check-result";

                        verifyButton.addEventListener(
                            "click",
                            async () => {
                                const selected =
                                    optionInputs.find(
                                        input =>
                                            input.checked
                                    );

                                if (!selected) {
                                    resultMessage.textContent =
                                        "Selecciona una opción.";
                                    return;
                                }

                                verifyButton.disabled =
                                    true;

                                const response =
                                    await fetch(
                                        "/v1/learning/check-answer",
                                        {
                                            method: "POST",
                                            headers: {
                                                "Content-Type":
                                                    "application/json"
                                            },
                                            body:
                                                JSON.stringify({
                                                    user_id:
                                                        learningUserId,
                                                    skill_id:
                                                        item.skill_id,
                                                    code:
                                                        item.code,
                                                    input_from:
                                                        item.input_from,
                                                    output_to:
                                                        item.output_to,
                                                    selected_index:
                                                        Number(
                                                            selected.value
                                                        )
                                                })
                                        }
                                    );

                                const data =
                                    await response.json();

                                if (!response.ok) {
                                    resultMessage.textContent =
                                        "No pude verificar la respuesta.";
                                    verifyButton.disabled =
                                        false;
                                    return;
                                }

                                resultMessage.className =
                                    "learning-check-result "
                                    + (
                                        data.correct
                                        ? "success"
                                        : "review"
                                    );

                                resultMessage.textContent =
                                    (
                                        data.correct
                                        ? "✓ Correcto. "
                                        : "↻ Repasar. "
                                    )
                                    + data.explanation;

                                verifyButton.style.display =
                                    "none";

                                optionInputs.forEach(
                                    input => {
                                        input.disabled =
                                            true;
                                    }
                                );
                            }
                        );

                        body.append(
                            question
                        );

                        body.append(
                            verifyButton,
                            resultMessage
                        );

                        learningCheck.append(
                            summary,
                            body
                        );
                    }

                    const policyNote =
                        document.createElement(
                            "div"
                        );

                    policyNote.className =
                        "adaptive-note";

                    const policy =
                        item.teaching_policy;

                    if (policy) {
                        if (
                            policy.level
                            === "reduced"
                        ) {
                            policyNote.classList.add(
                                "reduced"
                            );

                            policyNote.textContent =
                                policy.message
                                || (
                                    "Ya tienes progreso en "
                                    + "esta habilidad, así que "
                                    + "reduciré parte de la ayuda."
                                );

                            why.style.display =
                                "none";

                            challenge.style.display =
                                "none";
                        }

                        if (
                            policy.level
                            === "independent"
                        ) {
                            policyNote.classList.add(
                                "reduced"
                            );

                            policyNote.textContent =
                                policy.message
                                || (
                                    "Esta habilidad ya muestra "
                                    + "dominio consistente."
                                );

                            why.style.display =
                                "none";

                            challenge.style.display =
                                "none";
                        }

                        if (
                            policy.level
                            === "reinforcement"
                        ) {
                            policyNote.classList.add(
                                "reinforcement"
                            );

                            policyNote.textContent =
                                policy.message
                                || (
                                    "Esta habilidad necesita "
                                    + "más práctica, así que "
                                    + "mantendré la explicación completa."
                                );
                        }
                    }

                    element.append(
                        meta,
                        concept,
                        explanation,
                        why,
                        challenge,
                        snippet
                    );

                    if (
                        policy
                        && policy.message
                    ) {
                        element.append(
                            policyNote
                        );
                    }

                    if (
                        item.check
                        && item.skill_id
                    ) {
                        element.append(
                            learningCheck
                        );
                    }

                    results.appendChild(
                        element
                    );
                }
            );

        } catch (error) {
            results.textContent =
                "No se pudo analizar el código.";
        } finally {
            button.disabled = false;
            button.textContent =
                "Explicar código";
        }
    }
);
</script>
</body>
</html>
        """
    )
