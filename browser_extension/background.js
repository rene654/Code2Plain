const CODE2PLAIN_API =
    "http://127.0.0.1:8000/v1/auto-learn";


chrome.runtime.onMessage.addListener(
    (message, sender, sendResponse) => {

        if (
            !message
            || message.type !== "CODE2PLAIN_ANALYZE"
        ) {
            return;
        }

        fetch(
            CODE2PLAIN_API,
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
                 * Code2Plain being offline must never
                 * interrupt ChatGPT.
                 */
                sendResponse({
                    ok: false,
                });
            });

        return true;
    }
);
