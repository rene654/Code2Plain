const explainButton =
    document.getElementById("explainButton");

const languageSelector =
    document.getElementById("languageSelector");

const compactLearningOverlay =
    document.getElementById(
        "compactLearningOverlay"
    );

const compactOverlayState =
    document.getElementById(
        "compactOverlayState"
    );

const compactSummaryText =
    document.getElementById(
        "compactSummaryText"
    );

const compactConceptNumber =
    document.getElementById(
        "compactConceptNumber"
    );

const compactConceptLabel =
    document.getElementById(
        "compactConceptLabel"
    );

const compactLearningText =
    document.getElementById(
        "compactLearningText"
    );

const compactOverlayMeta =
    document.getElementById(
        "compactOverlayMeta"
    );


const quickSummaryToast =
    document.getElementById(
        "quickSummaryToast"
    );

const quickSummaryText =
    document.getElementById(
        "quickSummaryText"
    );

const quickSummaryMeta =
    document.getElementById(
        "quickSummaryMeta"
    );

const passiveConnectionState =
    document.getElementById(
        "passiveConnectionState"
    );

const passiveConnectionText =
    document.getElementById(
        "passiveConnectionText"
    );

const clearSessionButton =
    document.getElementById(
        "clearSessionButton"
    );

const emptyLearningState =
    document.getElementById(
        "emptyLearningState"
    );

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
let currentMode =
    localStorage.getItem(
        MODE_STORAGE_KEY
    )
    || "learn";

if (
    ![
        "learn",
        "understand",
        "deep",
    ].includes(
        currentMode
    )
) {
    currentMode = "learn";
}

const LANGUAGE_STORAGE_KEY =
    "code2plain.language";

const MODE_STORAGE_KEY =
    "code2plain.mode";

const ACTIVE_BLOCK_STORAGE_KEY =
    "code2plain.activeBlock";

const LAST_CODE_STORAGE_KEY =
    "code2plain.lastCode";

const LAST_EXPLANATION_STORAGE_KEY =
    "code2plain.lastExplanation";

const LAST_SESSION_STORAGE_KEY =
    "code2plain.lastSession";

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

    localStorage.setItem(
        ACTIVE_BLOCK_STORAGE_KEY,
        String(index)
    );

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

// =========================================================
// SESSION-AWARE LIVE CHANNEL
// =========================================================

const SESSION_STORAGE_KEY =
    "code2plain.session";

const sessionFromUrl =
    new URLSearchParams(
        window.location.search
    ).get("session");

let currentSessionId =
    sessionFromUrl
    || localStorage.getItem(
        SESSION_STORAGE_KEY
    )
    || "default";

localStorage.setItem(
    SESSION_STORAGE_KEY,
    currentSessionId
);


let liveVersion = 0;

let livePolling = false;


let quickSummaryTimer = null;

let compactOverlayTimer = null;


function chooseCompactLearningSection(
    result
) {
    const resultSections =
        result?.sections || [];

    if (
        resultSections.length === 0
    ) {
        return null;
    }


    const priority = [
        "FILTER",
        "AGGREGATE",
        "DECIDE",
        "REPEAT",
        "TRANSFORM",
        "LOAD DATA",
        "EXPORT",
        "DEFINE",
        "CALL",
        "RETURN",
        "IMPORT",
    ];


    for (
        const concept
        of priority
    ) {
        const match =
            resultSections.find(
                (section) =>
                    section.concept
                    === concept
            );

        if (match) {
            return match;
        }
    }


    return resultSections[0];
}


function compactLearningTextFor(
    section
) {
    if (!section) {
        return "";
    }


    const modes =
        section.learning_modes
        || {};


    const selectedMode =
        modes[currentMode]
        || modes.learn
        || modes.understand
        || modes.deep;


    if (
        selectedMode
        && selectedMode.primary
    ) {
        return selectedMode.primary;
    }


    return (
        section.what_to_learn
        || section.what_it_does
        || ""
    );
}


function compactMetaText(
    result
) {
    const count =
        result?.sections?.length
        || 0;


    if (currentLanguage === "en") {
        return `${count} ${
            count === 1
                ? "step detected"
                : "steps detected"
        }`;
    }


    if (currentLanguage === "fr") {
        return `${count} ${
            count === 1
                ? "étape détectée"
                : "étapes détectées"
        }`;
    }


    return `${count} ${
        count === 1
            ? "paso detectado"
            : "pasos detectados"
    }`;
}


function showCompactLearningOverlay(
    result
) {
    if (
        !compactLearningOverlay
        || !result
    ) {
        return;
    }


    const summary =
        result.quick_summary;


    const section =
        chooseCompactLearningSection(
            result
        );


    if (
        compactSummaryText
        && summary?.text
    ) {
        compactSummaryText.textContent =
            summary.text;
    }


    if (section) {

        if (compactConceptNumber) {
            compactConceptNumber
                .textContent =
                    String(
                        section.section_number
                        || 1
                    ).padStart(
                        2,
                        "0"
                    );
        }


        if (compactConceptLabel) {
            compactConceptLabel
                .textContent =
                    (
                        section.concept_label
                        || section.concept
                        || section.title
                        || ""
                    );
        }


        if (compactLearningText) {
            compactLearningText
                .textContent =
                    compactLearningTextFor(
                        section
                    );
        }

    }


    if (compactOverlayMeta) {
        compactOverlayMeta
            .textContent =
                compactMetaText(
                    result
                );
    }


    if (compactOverlayState) {

        const states = {
            es:
                "Código recibido",

            en:
                "Code received",

            fr:
                "Code reçu",
        };


        compactOverlayState
            .textContent =
                states[
                    currentLanguage
                ]
                || states.es;
    }


    compactLearningOverlay
        .classList
        .remove(
            "is-visible"
        );


    void compactLearningOverlay
        .offsetWidth;


    compactLearningOverlay
        .classList
        .add(
            "is-visible"
        );


    if (compactOverlayTimer) {
        window.clearTimeout(
            compactOverlayTimer
        );
    }


    compactOverlayTimer =
        window.setTimeout(
            () => {

                compactLearningOverlay
                    .classList
                    .remove(
                        "is-visible"
                    );

            },
            10000
        );
}





function showEmptyLearningState(
    visible
) {
    if (!emptyLearningState) {
        return;
    }

    emptyLearningState
        .classList
        .toggle(
            "is-visible",
            visible
        );
}


function clearStoredLearningState() {
    const keys = [
        MODE_STORAGE_KEY,
        ACTIVE_BLOCK_STORAGE_KEY,
        LAST_CODE_STORAGE_KEY,
        LAST_EXPLANATION_STORAGE_KEY,
        LAST_SESSION_STORAGE_KEY,
    ];

    keys.forEach(
        (key) => {
            localStorage.removeItem(
                key
            );
        }
    );

    sections = [];

    if (codeInput) {
        codeInput.value = "";
    }

    showEmptyLearningState(
        true
    );

    setPassiveState(
        "waiting",
        "Esperando código"
    );
}


function persistLearningState(
    result
) {
    if (!result) {
        return;
    }

    try {
        if (result.code) {
            localStorage.setItem(
                LAST_CODE_STORAGE_KEY,
                result.code
            );
        }

        localStorage.setItem(
            LAST_EXPLANATION_STORAGE_KEY,
            JSON.stringify(result)
        );

        localStorage.setItem(
            LAST_SESSION_STORAGE_KEY,
            currentSessionId
        );

    } catch (error) {
        console.warn(
            "Could not persist learning state:",
            error
        );
    }
}


function restoreLastExplanation() {
    const raw =
        localStorage.getItem(
            LAST_EXPLANATION_STORAGE_KEY
        );

    if (!raw) {
        return false;
    }

    try {
        const result =
            JSON.parse(raw);

        if (
            !result
            || !Array.isArray(
                result.sections
            )
            || result.sections.length === 0
        ) {
            return false;
        }

        sections =
            result.sections;

        if (
            codeInput
            && result.code
        ) {
            codeInput.value =
                result.code;
        }

        renderCode();

        const storedIndex =
            Number(
                localStorage.getItem(
                    ACTIVE_BLOCK_STORAGE_KEY
                )
                || 0
            );

        const safeIndex =
            Number.isInteger(
                storedIndex
            )
            && storedIndex >= 0
            && storedIndex < sections.length
                ? storedIndex
                : 0;

        activateSection(
            safeIndex
        );

        setPassiveState(
            "connected",
            "Sesión recuperada"
        );

        return true;

    } catch (error) {
        console.warn(
            "Could not restore previous session:",
            error
        );

        localStorage.removeItem(
            LAST_EXPLANATION_STORAGE_KEY
        );

        localStorage.removeItem(
            LAST_CODE_STORAGE_KEY
        );

        showEmptyLearningState(
            true
        );

        return false;
    }
}





function setPassiveState(
    state,
    text
) {
    if (
        !passiveConnectionState
        || !passiveConnectionText
    ) {
        return;
    }

    passiveConnectionState
        .classList.remove(
            "is-waiting",
            "is-connected",
            "is-received",
            "is-reconnecting"
        );

    passiveConnectionState
        .classList.add(
            `is-${state}`
        );

    passiveConnectionText
        .textContent =
            text;
}


function showQuickSummary(
    summary
) {
    if (
        !quickSummaryToast
        || !quickSummaryText
        || !summary
        || !summary.text
    ) {
        return;
    }

    quickSummaryText.textContent =
        summary.text;

    if (quickSummaryMeta) {
        const steps =
            summary.step_count || 0;

        quickSummaryMeta.textContent =
            `${steps} ${
                steps === 1
                    ? "paso detectado"
                    : "pasos detectados"
            }`;
    }

    quickSummaryToast
        .classList
        .remove(
            "is-visible"
        );

    void quickSummaryToast
        .offsetWidth;

    quickSummaryToast
        .classList
        .add(
            "is-visible"
        );


    if (quickSummaryTimer) {
        window.clearTimeout(
            quickSummaryTimer
        );
    }


    quickSummaryTimer =
        window.setTimeout(
            () => {
                quickSummaryToast
                    .classList
                    .remove(
                        "is-visible"
                    );
            },
            8500
        );
}


async function applyLiveExplanation(
    livePayload
) {
    const result =
        livePayload.explanation;

    setPassiveState(
        "received",
        "Código recibido"
    );

    showQuickSummary(
        result?.quick_summary
    );

    showCompactLearningOverlay(
        result
    );

    persistLearningState(
        result
    );

    showEmptyLearningState(
        false
    );

    window.setTimeout(
        () => {
            setPassiveState(
                "connected",
                "Conectado"
            );
        },
        1700
    );

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
                `/v1/live?after=${liveVersion}&session_id=${encodeURIComponent(currentSessionId)}`,
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

function restoreModeButtons() {
    document.querySelectorAll(
        "[data-mode]"
    ).forEach(
        (button) => {
            button.classList.toggle(
                "active",
                button.dataset.mode
                    === currentMode
            );
        }
    );
}


window.addEventListener(
    "DOMContentLoaded",
    () => {
        restoreModeButtons();

        const restored =
            restoreLastExplanation();

        if (!restored) {
            showEmptyLearningState(
                true
            );

            setPassiveState(
                "waiting",
                "Esperando código"
            );

        } else {
            showEmptyLearningState(
                false
            );
        }
    }
);


if (clearSessionButton) {

    clearSessionButton.addEventListener(
        "click",
        () => {
            clearStoredLearningState();

            clearSessionButton
                .classList
                .add(
                    "is-confirmed"
                );

            const originalText =
                clearSessionButton
                    .textContent;

            clearSessionButton
                .textContent =
                    "Sesión limpiada";

            window.setTimeout(
                () => {
                    clearSessionButton
                        .classList
                        .remove(
                            "is-confirmed"
                        );

                    clearSessionButton
                        .textContent =
                            originalText;
                },
                1800
            );
        }
    );

}


// ============================================================
// GITHUB LEARNING FEEDBACK
// ============================================================

function showGitHubFeedback(feedback) {
    const section =
        document.getElementById(
            "compactFailureSection"
        );

    const text =
        document.getElementById(
            "compactFailureText"
        );

    const meta =
        document.getElementById(
            "compactFailureMeta"
        );

    if (
        !section
        || !text
        || !meta
        || !feedback
    ) {
        return;
    }

    text.textContent =
        feedback.what_failed
        || feedback.headline
        || "Algo salió mal";

    const parts = [];

    if (feedback.where_to_look) {
        parts.push(
            feedback.where_to_look
        );
    }

    if (feedback.concept) {
        parts.push(
            feedback.concept
        );
    }

    meta.textContent =
        parts.join(" · ");

    section.classList.remove(
        "hidden"
    );
}


// ============================================================
// GITHUB FEEDBACK SYNC
// ============================================================

let githubFeedbackVersion = 0;

async function checkGitHubFeedback() {
    try {
        const response =
            await fetch(
                "/v1/github/feedback/latest",
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
            && payload.feedback
            && payload.version > githubFeedbackVersion
        ) {
            githubFeedbackVersion =
                payload.version;

            showGitHubFeedback(
                payload.feedback
            );
        }

    } catch (error) {
        // Feedback sync should never interrupt
        // the main learning experience.
    }
}

window.addEventListener(
    "DOMContentLoaded",
    () => {
        checkGitHubFeedback();

        window.setInterval(
            checkGitHubFeedback,
            1500
        );
    }
);
