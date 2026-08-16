const explainButton =
    document.getElementById("explainButton");

const languageSelector =
    document.getElementById("languageSelector");

const codeInput =
    document.getElementById("codeInput");

const codeEditor =
    document.getElementById("codeEditor");

const programFlow =
    document.getElementById("programFlow");

const sectionCounter =
    document.getElementById("sectionCounter");

const learningNote =
    document.getElementById("learningNote");

const noteNumber =
    document.getElementById("noteNumber");

const noteTitle =
    document.getElementById("noteTitle");

const noteCode =
    document.getElementById("noteCode");

const primaryLabel =
    document.getElementById("primaryLabel");

const secondaryLabel =
    document.getElementById("secondaryLabel");

const notePrimary =
    document.getElementById("notePrimary");

const noteSecondary =
    document.getElementById("noteSecondary");

const noteTechnical =
    document.getElementById("noteTechnical");

const conceptVisual =
    document.getElementById("conceptVisual");

const technicalSection =
    document.getElementById("technicalSection");

const noteLines =
    document.getElementById("noteLines");

const modeButtons =
    document.querySelectorAll(".mode");


let sections = [];
let activeIndex = null;
let currentMode = "learn";

const LANGUAGE_STORAGE_KEY =
    "code2plain.language";

let currentLanguage =
    localStorage.getItem(
        LANGUAGE_STORAGE_KEY
    )
    || "es";


if (
    languageSelector
    && ["es", "en", "fr"].includes(
        currentLanguage
    )
) {
    languageSelector.value =
        currentLanguage;
}


const colorMap = {
    blue: "#4f8fe8",
    green: "#52aa78",
    purple: "#9a6bc4",
    orange: "#e78c4c",
    cyan: "#45aabd",
    yellow: "#e6bd48",
};


const softColorMap = {
    blue: "rgba(79, 143, 232, 0.16)",
    green: "rgba(82, 170, 120, 0.16)",
    purple: "rgba(154, 107, 196, 0.16)",
    orange: "rgba(231, 140, 76, 0.17)",
    cyan: "rgba(69, 170, 189, 0.16)",
    yellow: "rgba(230, 189, 72, 0.18)",
};


function escapeHtml(value) {
    return value
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}



function renderProgramFlow() {
    if (!programFlow) {
        return;
    }


    programFlow.innerHTML =
        sections
            .map(
                (section, index) => {

                    const concept =
                        section.concept_label
                        || section.concept_label
                        || section.concept
                        || section.title
                        || "PASO";

                    const number =
                        String(
                            section.section_number
                        ).padStart(
                            2,
                            "0"
                        );

                    return `
                        <button
                            class="flow-step"
                            data-flow-index="${index}"
                            type="button"
                        >
                            <span
                                class="flow-dot"
                            >
                                ${number}
                            </span>

                            <span
                                class="flow-label"
                            >
                                ${escapeHtml(
                                    concept
                                )}
                            </span>
                        </button>
                    `;
                }
            )
            .join(
                '<span class="flow-line">→</span>'
            );


    document
        .querySelectorAll(
            ".flow-step"
        )
        .forEach(
            element => {

                element
                    .addEventListener(
                        "click",
                        () => {

                            activateSection(
                                Number(
                                    element
                                        .dataset
                                        .flowIndex
                                )
                            );

                        }
                    );

            }
        );
}


function updateProgramFlow(index) {
    document
        .querySelectorAll(
            ".flow-step"
        )
        .forEach(
            (element, elementIndex) => {

                element
                    .classList
                    .toggle(
                        "active",
                        elementIndex
                            === index
                    );

                element
                    .classList
                    .toggle(
                        "completed",
                        elementIndex
                            < index
                    );

            }
        );
}


function renderCode() {
    renderProgramFlow();

    codeEditor.innerHTML =
        sections
            .map(
                (section, index) => `
                    <article
                        class="code-section"
                        data-index="${index}"
                        style="--block-index: ${index};"
                    >

                        <div class="code-gutter">
                            ${String(
                                section.section_number
                            ).padStart(2, "0")}
                        </div>

                        <div class="code-body">

                            <pre
                                class="code-content"
                            >${escapeHtml(
                                section.code
                            )}</pre>

                        </div>

                    </article>
                `
            )
            .join("");


    codeEditor
        .classList
        .remove("is-revealing");


    requestAnimationFrame(
        () => {
            codeEditor
                .classList
                .add("is-revealing");
        }
    );


    document
        .querySelectorAll(".code-section")
        .forEach(
            element => {

                element.addEventListener(
                    "mouseenter",
                    () => {
                        activateSection(
                            Number(
                                element.dataset.index
                            )
                        );
                    }
                );


                element.addEventListener(
                    "click",
                    () => {
                        activateSection(
                            Number(
                                element.dataset.index
                            )
                        );
                    }
                );

            }
        );
}



function getQuotedValues(code) {
    const matches =
        [
            ...code.matchAll(
                /["']([^"']+)["']/g
            )
        ];

    return matches.map(
        match => match[1]
    );
}


function renderConceptVisual(section) {
    const concept =
        section.concept || "PROCESS";

    const code =
        section.code || "";

    const values =
        getQuotedValues(code);


    let html = "";


    if (concept === "IMPORT") {

        html = `
            <div class="visual-flow">

                <div class="visual-node">
                    Python
                </div>

                <div class="visual-arrow">
                    <span>carga</span>
                    <b>↓</b>
                </div>

                <div
                    class="visual-node emphasized"
                >
                    external tool
                </div>

            </div>
        `;

    } else if (concept === "LOAD DATA") {

        const filename =
            values[0]
            || "data file";


        html = `
            <div class="visual-flow">

                <div class="visual-file">
                    <span class="file-icon">
                        ▤
                    </span>

                    <strong>
                        ${escapeHtml(filename)}
                    </strong>
                </div>

                <div class="visual-arrow">

                    <span>
                        LOAD
                    </span>

                    <b>
                        ↓
                    </b>

                </div>

                <div
                    class="visual-node emphasized"
                >
                    DataFrame
                </div>

            </div>
        `;

    } else if (concept === "FILTER") {

        const field =
            values[0]
            || "condition";

        const target =
            values[1]
            || "match";


        html = `
            <div class="filter-visual">

                <div class="mini-table before">

                    <div class="mini-row">
                        <span>1</span>
                        <strong>${escapeHtml(target)}</strong>
                    </div>

                    <div class="mini-row muted">
                        <span>2</span>
                        <strong>Other</strong>
                    </div>

                    <div class="mini-row">
                        <span>3</span>
                        <strong>${escapeHtml(target)}</strong>
                    </div>

                    <div class="mini-row muted">
                        <span>4</span>
                        <strong>Other</strong>
                    </div>

                </div>


                <div class="visual-arrow condition">

                    <span>
                        ${escapeHtml(field)}
                        ==
                        ${escapeHtml(target)}
                    </span>

                    <b>
                        →
                    </b>

                </div>


                <div class="mini-table after">

                    <div class="mini-row survive">
                        <span>1</span>
                        <strong>${escapeHtml(target)}</strong>
                    </div>

                    <div class="mini-row survive">
                        <span>3</span>
                        <strong>${escapeHtml(target)}</strong>
                    </div>

                </div>

            </div>
        `;

    } else if (concept === "AGGREGATE") {

        const group =
            values[0]
            || "group";

        const amount =
            values[1]
            || "value";


        html = `
            <div class="aggregate-visual">

                <div class="aggregate-input">

                    <div class="agg-row">
                        <span>A</span>
                        <strong>10</strong>
                    </div>

                    <div class="agg-row">
                        <span>B</span>
                        <strong>20</strong>
                    </div>

                    <div class="agg-row">
                        <span>A</span>
                        <strong>15</strong>
                    </div>

                    <div class="agg-row">
                        <span>B</span>
                        <strong>5</strong>
                    </div>

                </div>


                <div class="visual-arrow condition">

                    <span>
                        AGRUPAR POR
                        ${escapeHtml(group)}
                    </span>

                    <small>
                        SUM
                        ${escapeHtml(amount)}
                    </small>

                    <b>
                        →
                    </b>

                </div>


                <div class="aggregate-output">

                    <div class="agg-result">
                        <span>A</span>
                        <strong>25</strong>
                    </div>

                    <div class="agg-result">
                        <span>B</span>
                        <strong>25</strong>
                    </div>

                </div>

            </div>
        `;

    } else if (concept === "EXPORT") {

        const filename =
            values[0]
            || "output file";


        html = `
            <div class="visual-flow">

                <div
                    class="visual-node emphasized"
                >
                    Result
                </div>

                <div class="visual-arrow">

                    <span>
                        EXPORT
                    </span>

                    <b>
                        ↓
                    </b>

                </div>

                <div class="visual-file">

                    <span class="file-icon">
                        ↗
                    </span>

                    <strong>
                        ${escapeHtml(filename)}
                    </strong>

                </div>

            </div>
        `;

    } else {

        html = `
            <div class="visual-flow">

                <div class="visual-node">
                    Input
                </div>

                <div class="visual-arrow">
                    <b>→</b>
                </div>

                <div
                    class="visual-node emphasized"
                >
                    ${escapeHtml(concept)}
                </div>

                <div class="visual-arrow">
                    <b>→</b>
                </div>

                <div class="visual-node">
                    Output
                </div>

            </div>
        `;

    }


    conceptVisual.innerHTML =
        html;


    conceptVisual
        .classList
        .remove("visual-enter");


    void conceptVisual.offsetWidth;


    conceptVisual
        .classList
        .add("visual-enter");
}


function activateSection(index) {
    const previousIndex =
        activeIndex;

    activeIndex = index;

    const section =
        sections[index];

    if (!section) {
        return;
    }


    const colorName =
        section.color_tag || "blue";


    const activeColor =
        colorMap[colorName]
        || colorMap.blue;


    const activeSoft =
        softColorMap[colorName]
        || softColorMap.blue;


    document.documentElement
        .style
        .setProperty(
            "--active-color",
            activeColor
        );


    document.documentElement
        .style
        .setProperty(
            "--active-soft",
            activeSoft
        );


    codeEditor
        .classList
        .add("has-active");


    updateProgramFlow(index);


    document
        .querySelectorAll(".code-section")
        .forEach(
            (element, elementIndex) => {

                element
                    .classList
                    .toggle(
                        "active",
                        elementIndex === index
                    );

            }
        );


    const modes =
        section.learning_modes || {};


    const mode =
        modes[currentMode]
        || modes.learn
        || {};


    noteNumber.textContent =
        String(
            section.section_number
        ).padStart(2, "0");


    noteTitle.textContent =
        mode.heading
        || section.concept_label
        || section.concept_label
        || section.concept
        || section.title;


    noteCode.textContent =
        section.code;


    renderConceptVisual(
        section
    );


    primaryLabel.textContent =
        mode.primary_label
        || "QUÉ HACE";


    notePrimary.textContent =
        mode.primary
        || section.what_it_does;


    secondaryLabel.textContent =
        mode.secondary_label
        || "APRENDER";


    noteSecondary.textContent =
        mode.secondary
        || section.what_to_learn;


    noteTechnical.textContent =
        mode.technical
        || "";


    technicalSection
        .classList
        .toggle(
            "hidden",
            currentMode !== "deep"
        );


    noteLines.textContent =
        `L${section.start_line} — L${section.end_line}`;


    learningNote
        .classList
        .remove("hidden");


    if (
        previousIndex !== index
    ) {
        learningNote
            .classList
            .remove("note-enter");

        void learningNote.offsetWidth;

        learningNote
            .classList
            .add("note-enter");
    }


    requestAnimationFrame(
        () => positionLearningNote(index)
    );
}


function positionLearningNote(index) {
    if (
        window.innerWidth <= 980
    ) {
        return;
    }


    const activeElement =
        document.querySelector(
            `.code-section[data-index="${index}"]`
        );


    const workspace =
        document.querySelector(
            ".learning-workspace"
        );


    if (
        !activeElement
        || !workspace
    ) {
        return;
    }


    const center =
        activeElement.offsetTop
        + (
            activeElement.offsetHeight
            / 2
        );


    const noteHeight =
        learningNote.offsetHeight;


    const minimumTop = 100;


    const maximumTop =
        workspace.clientHeight
        - noteHeight
        - 32;


    let target =
        center
        - (
            noteHeight
            / 2
        );


    target =
        Math.max(
            minimumTop,
            Math.min(
                target,
                maximumTop
            )
        );


    learningNote.style.top =
        `${target}px`;
}


async function explainCode() {
    const code =
        codeInput.value.trim();


    if (!code) {
        return;
    }


    explainButton.disabled = true;

    explainButton.textContent =
        "Analizando...";


    try {

        const response =
            await fetch(
                "/v1/explain",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json",
                    },

                    body:
                        JSON.stringify({
                            code,
                            language:
                                currentLanguage,
                        }),
                }
            );


        if (!response.ok) {
            throw new Error(
                `API returned ${response.status}`
            );
        }


        const result =
            await response.json();


        sections =
            result.sections;


        sectionCounter.textContent =
            `${sections.length} bloques de aprendizaje`;


        renderCode();


        if (
            sections.length > 0
        ) {
            activateSection(0);
        }


    } catch (error) {

        sectionCounter.textContent =
            error.message;

    } finally {

        explainButton.disabled = false;

        explainButton.textContent =
            "Explicar código";

    }
}


modeButtons.forEach(
    button => {

        button.addEventListener(
            "click",
            () => {

                modeButtons
                    .forEach(
                        item =>
                            item
                                .classList
                                .remove("active")
                    );


                button
                    .classList
                    .add("active");


                currentMode =
                    button.dataset.mode;


                if (
                    activeIndex !== null
                ) {
                    activateSection(
                        activeIndex
                    );
                }

            }
        );

    }
);


if (languageSelector) {

    languageSelector
        .addEventListener(
            "change",
            async () => {

                currentLanguage =
                    languageSelector.value;

                localStorage.setItem(
                    LANGUAGE_STORAGE_KEY,
                    currentLanguage
                );


                if (
                    codeInput.value.trim()
                ) {
                    await explainCode();
                }

            }
        );

}


explainButton
    .addEventListener(
        "click",
        explainCode
    );


window.addEventListener(
    "DOMContentLoaded",
    explainCode
);


// ============================================================
// LIVE AI SYNC
// ============================================================

let liveVersion = 0;

let livePolling = false;


async function applyLiveExplanation(
    livePayload
) {
    const result =
        livePayload.explanation;

    if (
        !result
        || !Array.isArray(
            result.sections
        )
    ) {
        return;
    }


    if (
        result.language
        && result.language
            !== currentLanguage
    ) {

        const response =
            await fetch(
                "/v1/explain",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json",
                    },

                    body:
                        JSON.stringify({
                            code:
                                result.code,
                            language:
                                currentLanguage,
                        }),
                }
            );


        if (response.ok) {
            const localized =
                await response.json();

            sections =
                localized.sections;

        } else {
            sections =
                result.sections;
        }

    } else {
        sections =
            result.sections;
    }


    sectionCounter.textContent =
        `EN VIVO · ${sections.length} bloques de aprendizaje`;


    sectionCounter
        .classList
        .remove("live-arrival");


    void sectionCounter.offsetWidth;


    sectionCounter
        .classList
        .add("live-arrival");


    renderCode();


    if (
        sections.length > 0
    ) {
        activateSection(0);
    }
}


async function checkLiveExplanation() {
    if (livePolling) {
        return;
    }

    livePolling = true;


    try {

        const response =
            await fetch(
                `/v1/live?after=${liveVersion}`,
                {
                    cache: "no-store",
                }
            );


        if (!response.ok) {
            return;
        }


        const payload =
            await response.json();


        if (
            payload.changed
            && payload.version > liveVersion
        ) {
            liveVersion =
                payload.version;

            await applyLiveExplanation(
                payload
            );
        }

    } catch (error) {

        // Live sync is intentionally silent.
        // A temporary network interruption should not
        // break the learning canvas.

    } finally {

        livePolling = false;

    }
}


function startLiveSync() {
    checkLiveExplanation();

    window.setInterval(
        checkLiveExplanation,
        800
    );
}


window.addEventListener(
    "DOMContentLoaded",
    startLiveSync
);
