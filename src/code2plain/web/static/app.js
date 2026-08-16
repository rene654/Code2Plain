const explainButton =
    document.getElementById("explainButton");

const codeInput =
    document.getElementById("codeInput");

const codeEditor =
    document.getElementById("codeEditor");

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

const technicalSection =
    document.getElementById("technicalSection");

const noteLines =
    document.getElementById("noteLines");

const modeButtons =
    document.querySelectorAll(".mode");


let sections = [];
let activeIndex = null;
let currentMode = "learn";


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


function renderCode() {
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
        || section.concept
        || section.title;


    noteCode.textContent =
        section.code;


    primaryLabel.textContent =
        mode.primary_label
        || "WHAT IT DOES";


    notePrimary.textContent =
        mode.primary
        || section.what_it_does;


    secondaryLabel.textContent =
        mode.secondary_label
        || "LEARN";


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
        "Studying...";


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
            `${sections.length} study blocks`;


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
            "Explain code";

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


function applyLiveExplanation(
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


    sections =
        result.sections;


    sectionCounter.textContent =
        `LIVE · ${sections.length} study blocks`;


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

            applyLiveExplanation(
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
