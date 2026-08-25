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
            width: min(920px, 92%);
            margin: 64px auto;
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
            margin-top: 28px;
            padding: 13px 15px;
            border:
                1px solid #dedede;
            border-radius: 10px;
            background: white;
            color: #171717;
            font-size: 14px;
        }

        .source-separator {
            margin: 12px 0 -12px;
            text-align: center;
            color: #a3a3a3;
            font-size: 12px;
        }

        textarea {
            width: 100%;
            min-height: 260px;
            margin-top: 28px;
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
            margin-top: 30px;
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
    <h1>Code2Plain</h1>

    <p class="subtitle">
        Entiende el código que estás usando.
    </p>

    <input
        id="githubUrl"
        type="url"
        placeholder="URL de archivo GitHub (opcional)"
    >

    <div class="source-separator">
        o
    </div>

    <textarea
        id="code"
        placeholder="Pega o escribe código aquí..."
        spellcheck="false"
    ></textarea>

    <button id="learn">
        Explicar código
    </button>

    <div id="results"></div>
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

        try {
            const endpoint =
                url
                ? "/v1/github-file/learn"
                : "/v1/context-block-learn";

            const requestBody =
                url
                ? { url }
                : { code: text };

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

                    if (item.concept) {
                        const parts =
                            item.concept.split(
                                " + "
                            );

                        parts.forEach(
                            part => {
                                const chip =
                                    document.createElement(
                                        "span"
                                    );

                                chip.className =
                                    "concept-chip";

                                chip.textContent =
                                    part;

                                const colorMap = {
                                    "FILTER":
                                        "#ec4899",
                                    "GROUP":
                                        "#eab308",
                                    "SELECT":
                                        "#38bdf8",
                                    "AGGREGATE":
                                        "#22c55e",
                                };

                                chip.style
                                    .setProperty(
                                        "--chip-color",
                                        colorMap[part]
                                        || "#a3a3a3"
                                    );

                                concept.appendChild(
                                    chip
                                );
                            }
                        );
                    } else {
                        concept.textContent =
                            `Línea ${item.line_number}`;
                    }

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
                        "Why?";

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

                    if (item.challenge) {
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

                    element.append(
                        meta,
                        concept,
                        explanation,
                        why,
                        challenge,
                        snippet
                    );

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
