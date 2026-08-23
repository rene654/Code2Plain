const ASSISTANT_SELECTOR =
    '[data-message-author-role="assistant"]';

const CODE_SELECTOR =
    "pre code";

const seenBlocks = new Set();


function fingerprint(text) {
    let hash = 2166136261;

    for (
        let index = 0;
        index < text.length;
        index += 1
    ) {
        hash ^= text.charCodeAt(index);

        hash = Math.imul(
            hash,
            16777619
        );
    }

    return String(hash >>> 0);
}


function renderLearning(
    codeElement,
    payload
) {
    if (
        !payload
        || !payload.should_teach
        || !payload.items
        || payload.items.length === 0
    ) {
        return;
    }

    const pre =
        codeElement.closest("pre");

    if (!pre) {
        return;
    }

    if (
        pre.nextElementSibling
        ?.classList
        .contains(
            "code2plain-learning"
        )
    ) {
        return;
    }

    const panel =
        document.createElement("div");

    panel.className =
        "code2plain-learning";

    const title =
        document.createElement("div");

    title.className =
        "code2plain-title";

    title.textContent =
        payload.items.length === 1
            ? "Code2Plain · 1 idea importante"
            : `Code2Plain · ${payload.items.length} ideas importantes`;

    panel.appendChild(title);

    payload.items.forEach(
        item => {
            const row =
                document.createElement("div");

            row.className =
                "code2plain-item";

            const concept =
                document.createElement("span");

            concept.className =
                "code2plain-concept";

            concept.textContent =
                item.concept;

            const explanation =
                document.createElement("span");

            explanation.className =
                "code2plain-explanation";

            explanation.textContent =
                item.explanation;

            const line =
                document.createElement("span");

            line.className =
                "code2plain-line";

            line.textContent =
                `L${item.line_number}`;

            row.appendChild(line);
            row.appendChild(concept);
            row.appendChild(explanation);

            panel.appendChild(row);
        }
    );

    pre.insertAdjacentElement(
        "afterend",
        panel
    );
}


function analyzeCodeBlock(
    codeElement
) {
    const assistantMessage =
        codeElement.closest(
            ASSISTANT_SELECTOR
        );

    if (!assistantMessage) {
        return;
    }

    const code =
        codeElement.textContent.trim();

    if (!code) {
        return;
    }

    const id =
        fingerprint(code);

    if (seenBlocks.has(id)) {
        return;
    }

    seenBlocks.add(id);

    chrome.runtime.sendMessage(
        {
            type:
                "CODE2PLAIN_ANALYZE",

            payload: {
                source:
                    "chatgpt",

                author_role:
                    "assistant",

                content_type:
                    "code",

                text:
                    code,
            },
        },
        response => {
            if (
                chrome.runtime.lastError
                || !response
                || !response.ok
            ) {
                return;
            }

            renderLearning(
                codeElement,
                response.payload
            );
        }
    );
}


function scan() {
    document
        .querySelectorAll(
            `${ASSISTANT_SELECTOR} ${CODE_SELECTOR}`
        )
        .forEach(
            analyzeCodeBlock
        );
}


let scanTimer = null;

const observer =
    new MutationObserver(
        () => {
            clearTimeout(
                scanTimer
            );

            scanTimer =
                setTimeout(
                    scan,
                    250
                );
        }
    );


observer.observe(
    document.documentElement,
    {
        childList: true,
        subtree: true,
    }
);


scan();
