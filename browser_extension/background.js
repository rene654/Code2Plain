const DEFAULT_API_BASE =
    "http://127.0.0.1:8000";


async function getApiBase() {
    const stored =
        await chrome.storage.local.get(
            "code2plainApiBase"
        );

    return (
        stored.code2plainApiBase
        || DEFAULT_API_BASE
    );
}


chrome.runtime.onMessage.addListener(
    (message, sender, sendResponse) => {

        if (
            !message
            || message.type !== "CODE2PLAIN_ANALYZE"
        ) {
            return;
        }

        getApiBase()
            .then(apiBase =>
                fetch(
                    `${apiBase}/v1/auto-learn`,
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json",
                        },

                        body: JSON.stringify(
                            message.payload
                        ),
                    }
                )
            )
            .then(response => {
                if (!response.ok) {
                    throw new Error(
                        `HTTP ${response.status}`
                    );
                }

                return response.json();
            })
            .then(payload => {
                sendResponse({
                    ok: true,
                    payload,
                });
            })
            .catch(() => {
                /*
                 * Code2Plain must remain invisible
                 * when its backend is unavailable.
                 */
                sendResponse({
                    ok: false,
                });
            });

        return true;
    }
);
