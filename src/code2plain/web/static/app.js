const explainButton =
    document.getElementById("explainButton");

const codeInput =
    document.getElementById("codeInput");

const codeEditor =
    document.getElementById("codeEditor");

const learningOverlay =
    document.getElementById("learningOverlay");

const overlayNumber =
    document.getElementById("overlayNumber");

const overlayTitle =
    document.getElementById("overlayTitle");

const overlayCode =
    document.getElementById("overlayCode");

const overlayDoes =
    document.getElementById("overlayDoes");

const overlayLearn =
    document.getElementById("overlayLearn");

const overlayLines =
    document.getElementById("overlayLines");

const deepDiveSection =
    document.getElementById("deepDiveSection");

const overlayDeep =
    document.getElementById("overlayDeep");

const sectionCounter =
    document.getElementById("sectionCounter");

const modeButtons =
    document.querySelectorAll(".mode");


let sections = [];

let activeIndex = null;

let currentMode = "learn";


const colorMap = {
    blue: "#61a8ff",
    green: "#52df93",
    purple: "#bc83ff",
    orange: "#ff9d57",
    cyan: "#44d9ef",
    yellow: "#f8d568",
};


function escapeHtml(value) {
    return value
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}


function buildDeepExplanation(section) {
    return (
        `Category: ${section.category}. ` +
        `Lines ${section.start_line}–${section.end_line}. ` +
        `This block participates in the larger program flow ` +
        `and can be inspected at syntax level in a future version.`
    );
}


function renderCode() {
    codeEditor.innerHTML =
        sections
            .map(
                (section, index) => `
                    <article
                        class="code-section"
                        data-index="${index}"
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


    document
        .querySelectorAll(
            ".code-section"
        )
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
    activeIndex = index;

    const section =
        sections[index];

    if (!section) {
        return;
    }


    const color =
        colorMap[
            section.color_tag
        ] || colorMap.blue;


    document.documentElement
        .style
        .setProperty(
            "--active-color",
            color
        );


    codeEditor
        .classList
        .add("has-active");


    document
        .querySelectorAll(
            ".code-section"
        )
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


    overlayNumber.textContent =
        String(
            section.section_number
        ).padStart(2, "0");


    overlayTitle.textContent =
        section.concept || section.title;


    overlayCode.textContent =
        section.code;


    overlayDoes.textContent =
        section.what_it_does;


    overlayLearn.textContent =
        section.what_to_learn;


    overlayDeep.textContent =
        buildDeepExplanation(
            section
        );


    overlayLines.textContent =
        `L${section.start_line} — L${section.end_line}`;


    deepDiveSection
        .classList
        .toggle(
            "hidden",
            currentMode !== "deep"
        );


    learningOverlay
        .classList
        .remove("hidden");


    requestAnimationFrame(
        () => positionOverlay(index)
    );
}


function positionOverlay(index) {
    const activeElement =
        document.querySelector(
            `.code-section[data-index="${index}"]`
        );

    const stage =
        document.querySelector(".stage");

    if (
        !activeElement
        || !stage
        || window.innerWidth <= 900
    ) {
        return;
    }

    const blockCenter =
        activeElement.offsetTop
        + (
            activeElement.offsetHeight
            / 2
        );

    const overlayHeight =
        learningOverlay.offsetHeight;

    const minimumTop = 90;

    const maximumTop =
        stage.clientHeight
        - overlayHeight
        - 28;

    let targetTop =
        blockCenter
        - (
            overlayHeight
            / 2
        );

    targetTop =
        Math.max(
            minimumTop,
            Math.min(
                targetTop,
                maximumTop
            ),
        );

    learningOverlay.style.top =
        `${targetTop}px`;
}


async function explainCode() {
    const code =
        codeInput.value.trim();


    if (!code) {
        return;
    }


    explainButton.disabled = true;

    explainButton.textContent =
        "Analyzing";


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
                `Code2Plain API returned ${response.status}`
            );
        }


        const result =
            await response.json();


        sections =
            result.sections;


        sectionCounter.textContent =
            `${sections.length} learning blocks`;


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
            "Explain";

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
                            item.classList.remove(
                                "active"
                            )
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
