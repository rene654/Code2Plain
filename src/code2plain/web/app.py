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

        .owner-access-button {
            margin: 0;
            padding: 7px 10px;
            border: 1px solid #e5e5e5;
            border-radius: 999px;
            background: #ffffff;
            color: #525252;
            font-size: 11px;
            font-weight: 700;
            cursor: pointer;
        }

        .owner-access-button.active {
            background: #171717;
            color: #ffffff;
            border-color: #171717;
        }

        .demo-timer {
            margin-left: auto;
            margin-right: 10px;
            padding: 7px 11px;
            border: 1px solid #e5e5e5;
            border-radius: 999px;
            background: #ffffff;
            color: #404040;
            font-size: 11px;
            font-weight: 700;
            white-space: nowrap;
        }

        .demo-timer.expired {
            border-color: #fecaca;
            background: #fef2f2;
            color: #991b1b;
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

        /* CODE2PLAIN PROFESSIONAL UI SYSTEM */

        :root {
            --c2p-navy: #0f172a;
            --c2p-navy-soft: #1e293b;
            --c2p-cyan: #06b6d4;
            --c2p-cyan-soft: #ecfeff;
            --c2p-ivory: #faf9f6;
            --c2p-surface: #ffffff;
            --c2p-surface-soft: #f8fafc;
            --c2p-border: #e2e8f0;
            --c2p-border-strong: #cbd5e1;
            --c2p-text: #0f172a;
            --c2p-muted: #64748b;
            --c2p-danger: #b91c1c;
            --c2p-success: #166534;
            --c2p-radius-lg: 18px;
            --c2p-radius-md: 12px;
            --c2p-shadow:
                0 18px 50px rgba(15, 23, 42, 0.06);
        }

        body {
            background:
                radial-gradient(
                    circle at top,
                    rgba(6, 182, 212, 0.055),
                    transparent 34%
                ),
                var(--c2p-ivory);
            color: var(--c2p-text);
        }

        .app-shell {
            max-width: 1480px;
            margin: 0 auto;
            padding:
                28px
                clamp(18px, 3vw, 42px)
                42px;
        }

        .app-header {
            display: flex;
            align-items: center;
            gap: 14px;
            margin-bottom: 22px;
            padding: 4px 2px;
        }

        .brand {
            min-width: 0;
            margin-right: auto;
        }

        .brand-copy h1 {
            color: var(--c2p-navy);
            letter-spacing: -0.035em;
        }

        .brand-copy p {
            color: var(--c2p-muted);
        }

        .owner-access-button,
        .demo-timer,
        .privacy-badge {
            flex: 0 0 auto;
            min-height: 34px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            border-color: var(--c2p-border);
            box-shadow:
                0 1px 2px rgba(15, 23, 42, 0.025);
        }

        .owner-access-button {
            transition:
                transform 150ms ease,
                border-color 150ms ease,
                background 150ms ease,
                box-shadow 150ms ease;
        }

        .owner-access-button:hover {
            transform: translateY(-1px);
            border-color: var(--c2p-border-strong);
            box-shadow:
                0 4px 12px rgba(15, 23, 42, 0.07);
        }

        .owner-access-button.active {
            background: var(--c2p-navy);
            border-color: var(--c2p-navy);
        }

        .demo-timer {
            margin-left: 0;
            margin-right: 0;
        }

        .workspace {
            grid-template-columns:
                minmax(340px, 0.92fr)
                minmax(440px, 1.08fr);
            gap: 20px;
        }

        .workspace-panel {
            border-color: var(--c2p-border);
            border-radius: var(--c2p-radius-lg);
            box-shadow: var(--c2p-shadow);
        }

        .panel-header {
            min-height: 56px;
            padding: 0 20px;
            border-bottom-color: var(--c2p-border);
            background:
                linear-gradient(
                    180deg,
                    #ffffff,
                    #fdfefe
                );
        }

        .panel-title {
            color: var(--c2p-navy);
            font-size: 13px;
            font-weight: 750;
            letter-spacing: -0.01em;
        }

        .panel-kicker {
            color: var(--c2p-muted);
            font-size: 11px;
            font-weight: 600;
        }

        .source-panel-body {
            padding: 20px;
        }

        .learning-panel-body {
            min-height: 440px;
            padding: 10px 16px 16px;
        }

        .learning-empty {
            min-height: 360px;
            padding: 36px;
        }

        input[type="url"],
        textarea {
            border-color: var(--c2p-border-strong);
            background: #ffffff;
            transition:
                border-color 150ms ease,
                box-shadow 150ms ease;
        }

        input[type="url"]:focus,
        textarea:focus {
            outline: none;
            border-color: var(--c2p-cyan);
            box-shadow:
                0 0 0 3px rgba(6, 182, 212, 0.12);
        }

        textarea {
            min-height: 250px;
            margin-top: 16px;
            padding: 18px;
            border-radius: var(--c2p-radius-md);
            line-height: 1.55;
        }

        #learn {
            min-height: 42px;
            padding: 11px 18px;
            border-radius: 10px;
            background: var(--c2p-navy);
            box-shadow:
                0 5px 14px rgba(15, 23, 42, 0.14);
            transition:
                transform 150ms ease,
                box-shadow 150ms ease,
                opacity 150ms ease;
        }

        #learn:hover:not(:disabled) {
            transform: translateY(-1px);
            box-shadow:
                0 8px 18px rgba(15, 23, 42, 0.18);
        }

        #learn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
            box-shadow: none;
        }

        .privacy-note {
            border-color: var(--c2p-border);
            background: var(--c2p-surface-soft);
            color: var(--c2p-muted);
        }

        .learning-card {
            border-color: var(--c2p-border);
            border-radius: 14px;
            background: var(--c2p-surface);
            box-shadow:
                0 4px 16px rgba(15, 23, 42, 0.035);
        }

        .learning-check-body {
            border-color: var(--c2p-border);
            background: var(--c2p-surface-soft);
        }

        @media (max-width: 1100px) {
            .app-shell {
                padding-left: 20px;
                padding-right: 20px;
            }

            .workspace {
                grid-template-columns:
                    minmax(320px, 0.95fr)
                    minmax(400px, 1.05fr);
                gap: 16px;
            }
        }

        @media (max-width: 900px) {
            .app-shell {
                padding:
                    20px
                    18px
                    32px;
            }

            .app-header {
                display: grid;
                grid-template-columns:
                    1fr auto auto;
                align-items: center;
                gap: 10px;
                margin-bottom: 18px;
            }

            .brand {
                grid-column: 1 / -1;
                margin-bottom: 4px;
            }

            .workspace {
                grid-template-columns: 1fr;
                gap: 16px;
            }

            textarea {
                min-height: 220px;
            }

            .learning-panel-body {
                min-height: 320px;
            }

            .learning-empty {
                min-height: 260px;
            }
        }

        @media (max-width: 640px) {
            .app-shell {
                padding:
                    14px
                    12px
                    26px;
            }

            .app-header {
                grid-template-columns:
                    auto
                    1fr;
                gap: 8px;
            }

            .brand {
                grid-column: 1 / -1;
            }

            .owner-access-button {
                grid-column: 1;
                min-width: 76px;
            }

            .demo-timer {
                grid-column: 2;
                justify-self: start;
            }

            .privacy-badge {
                grid-column: 1 / -1;
                justify-self: stretch;
                text-align: center;
                white-space: normal;
            }

            .workspace-panel {
                border-radius: 14px;
            }

            .panel-header {
                min-height: 50px;
                padding: 0 15px;
            }

            .source-panel-body {
                padding: 14px;
            }

            textarea {
                min-height: 190px;
                padding: 15px;
                font-size: 13px;
            }

            #learn {
                width: 100%;
                min-height: 44px;
            }

            .privacy-note {
                margin-top: 10px;
            }

            .learning-panel-body {
                min-height: 260px;
                padding:
                    8px
                    12px
                    12px;
            }

            .learning-empty {
                min-height: 210px;
                padding: 24px 18px;
            }
        }

        @media (max-width: 390px) {
            .panel-kicker {
                max-width: 130px;
                text-align: right;
            }

            .owner-access-button,
            .demo-timer,
            .privacy-badge {
                font-size: 10px;
            }
        }


        /* CODE2PLAIN PREMIUM LEARNING CARDS */

        .item {
            margin: 10px 0;
            padding: 13px 15px;

            border:
                1px solid
                var(--c2p-border);

            border-left:
                3px solid
                var(--c2p-cyan);

            border-radius: 12px;

            background:
                var(--c2p-surface);

            box-shadow:
                0 3px 12px
                rgba(15, 23, 42, 0.025);
        }

        .meta {
            align-items: center;
            color: var(--c2p-muted);
            font-size: 10px;
            font-weight: 600;
            letter-spacing: 0.01em;
        }

        .concept {
            margin-top: 4px;
            gap: 5px;
            color: var(--c2p-navy);
            font-size: 13px;
            font-weight: 750;
            line-height: 1.35;
        }

        .concept-chip {
            padding: 2px 6px;

            border:
                1px solid
                rgba(6, 182, 212, 0.18);

            border-radius: 999px;

            background:
                var(--c2p-cyan-soft);

            color:
                var(--c2p-navy-soft);

            font-size: 9px;
            font-weight: 700;
        }

        .explanation {
            margin-top: 5px;
            color: var(--c2p-text);
            font-size: 14px;
            line-height: 1.48;
            letter-spacing: -0.01em;
        }

        .code {
            margin-top: 8px;
            padding: 8px 10px;

            overflow-x: auto;

            border:
                1px solid
                var(--c2p-border);

            border-radius: 8px;

            background:
                var(--c2p-surface-soft);

            color:
                var(--c2p-navy-soft);

            font-size: 11px;
            line-height: 1.5;
            white-space: pre-wrap;
            word-break: break-word;
        }

        .code2plain-code-highlight {
            padding: 1px 2px;
            border-radius: 3px;
            background:
                rgba(6, 182, 212, 0.08);
        }

        .item > details:not(.learning-check) {
            margin-top: 6px;
            color: var(--c2p-muted);
        }

        .item > details:not(.learning-check) summary {
            color: var(--c2p-muted);
            font-size: 11px;
            font-weight: 650;
            opacity: 1;
        }

        .challenge {
            margin-top: 6px;
            color: var(--c2p-muted);
            font-size: 11px;
            line-height: 1.45;
        }

        .adaptive-note {
            margin-top: 7px;
            padding: 6px 8px;
            font-size: 10px;
            line-height: 1.4;
        }

        .learning-check {
            margin-top: 9px;
            padding-top: 8px;

            border-top:
                1px solid
                var(--c2p-border);
        }

        .learning-check summary {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 10px;

            color:
                var(--c2p-navy-soft);

            font-size: 11px;
            font-weight: 700;
            opacity: 1;
        }

        .learning-check summary::after {
            margin-left: auto;
            color: var(--c2p-muted);
            font-size: 10px;
        }

        .learning-check[open] summary {
            color: var(--c2p-navy);
        }

        .learning-check-body {
            margin-top: 8px;
            padding: 9px 10px;

            border:
                1px solid
                var(--c2p-border);

            border-radius: 9px;

            background:
                var(--c2p-surface-soft);
        }

        .learning-check-question {
            margin-bottom: 7px;

            color: var(--c2p-navy);

            font-size: 11px;
            font-weight: 700;
            line-height: 1.4;
        }

        .learning-check-option {
            margin: 3px 0;
            padding: 5px 6px;

            border-radius: 7px;

            color:
                var(--c2p-navy-soft);

            font-size: 10px;
            line-height: 1.35;

            transition:
                background 120ms ease;
        }

        .learning-check-option:hover {
            background: #ffffff;
        }

        .learning-check-option input {
            flex: 0 0 auto;
            margin-top: 2px;
        }

        .learning-check-verify {
            margin-top: 7px;
            padding: 7px 10px;

            border-radius: 7px;

            background:
                var(--c2p-navy);

            font-size: 10px;
        }

        .learning-check-result {
            margin-top: 7px;
            font-size: 10px;
            line-height: 1.4;
        }

        @media (max-width: 640px) {
            .item {
                margin: 8px 0;
                padding: 11px 12px;
                border-radius: 11px;
            }

            .concept {
                font-size: 12px;
            }

            .explanation {
                font-size: 13px;
                line-height: 1.45;
            }

            .code {
                padding: 7px 9px;
                font-size: 11px;
            }

            .challenge {
                font-size: 10px;
            }

            .learning-check {
                margin-top: 8px;
                padding-top: 7px;
            }

            .learning-check-body {
                padding: 8px;
            }
        }


        /* CODE2PLAIN PREMIUM VISUAL IDENTITY */

        :root {
            --c2p-navy: #081f46;
            --c2p-navy-2: #163470;

            --c2p-blue: #1165e7;
            --c2p-blue-mid: #2c4f91;
            --c2p-blue-light: #a3bbe3;
            --c2p-blue-soft: #eaf0f9;

            --c2p-cyan: #1aa8d9;
            --c2p-cyan-soft: #e8f8fd;

            --c2p-surface: #ffffff;
            --c2p-surface-soft: #f7faff;

            --c2p-border: #dce6f3;
            --c2p-border-strong: #bdcce1;

            --c2p-text: #0a1d3b;
            --c2p-muted: #61738f;

            --c2p-success: #1f8a5b;
            --c2p-danger: #b42318;

            --c2p-shadow:
                0 18px 55px
                rgba(8, 31, 70, 0.09);

            --c2p-shadow-soft:
                0 8px 28px
                rgba(8, 31, 70, 0.055);
        }

        body {
            background:
                radial-gradient(
                    circle at 18% 0%,
                    rgba(26, 168, 217, 0.10),
                    transparent 32%
                ),
                radial-gradient(
                    circle at 90% 20%,
                    rgba(17, 101, 231, 0.09),
                    transparent 34%
                ),
                linear-gradient(
                    180deg,
                    #f8fbff 0%,
                    #eef5fc 55%,
                    #f8fbff 100%
                );

            color:
                var(--c2p-text);
        }

        main {
            position: relative;
        }

        .app-header {
            position: relative;

            padding:
                14px
                16px;

            border:
                1px solid
                rgba(189, 204, 225, 0.72);

            border-radius: 18px;

            background:
                rgba(255, 255, 255, 0.82);

            box-shadow:
                0 14px 40px
                rgba(8, 31, 70, 0.07);

            backdrop-filter:
                blur(18px);

            -webkit-backdrop-filter:
                blur(18px);
        }

        .brand-lockup {
            min-width: 0;
        }

        .brand-mark {
            width: 42px;
            height: 42px;

            filter:
                drop-shadow(
                    0 6px 14px
                    rgba(17, 101, 231, 0.10)
                );
        }

        .brand-copy h1 {
            color:
                var(--c2p-navy);

            font-weight: 800;
        }

        .brand-copy p {
            color:
                var(--c2p-muted);
        }

        .owner-access-button,
        .demo-timer,
        .privacy-badge {
            border:
                1px solid
                var(--c2p-border);

            background:
                rgba(255, 255, 255, 0.94);

            color:
                var(--c2p-blue-mid);

            box-shadow:
                0 4px 14px
                rgba(8, 31, 70, 0.04);
        }

        .owner-access-button:hover {
            border-color:
                var(--c2p-blue-light);

            color:
                var(--c2p-blue);
        }

        .owner-access-button.active {
            background:
                linear-gradient(
                    135deg,
                    var(--c2p-navy),
                    var(--c2p-navy-2)
                );

            border-color:
                transparent;

            color: #ffffff;

            box-shadow:
                0 8px 18px
                rgba(8, 31, 70, 0.20);
        }

        .demo-timer:not(.expired) {
            background:
                linear-gradient(
                    135deg,
                    #ffffff,
                    #f3f8ff
                );

            color:
                var(--c2p-blue);
        }

        .privacy-badge {
            background:
                linear-gradient(
                    135deg,
                    #ffffff,
                    #f6faff
                );

            color:
                var(--c2p-blue-mid);
        }

        .workspace {
            gap: 22px;
        }

        .workspace-panel {
            border:
                1px solid
                rgba(189, 204, 225, 0.72);

            border-radius: 20px;

            background:
                rgba(255, 255, 255, 0.92);

            box-shadow:
                var(--c2p-shadow);

            backdrop-filter:
                blur(14px);

            -webkit-backdrop-filter:
                blur(14px);
        }

        .panel-header {
            min-height: 58px;

            border-bottom:
                1px solid
                var(--c2p-border);

            background:
                linear-gradient(
                    180deg,
                    #ffffff 0%,
                    #f9fbff 100%
                );
        }

        .panel-title {
            color:
                var(--c2p-navy);

            font-size: 14px;
            font-weight: 800;
        }

        .panel-kicker {
            display: inline-flex;
            align-items: center;

            padding:
                5px
                9px;

            border:
                1px solid
                #d9e7fb;

            border-radius: 999px;

            background:
                #f5f9ff;

            color:
                var(--c2p-blue);

            font-size: 10px;
            font-weight: 700;
        }

        input[type="url"] {
            min-height: 46px;

            border:
                1px solid
                var(--c2p-border-strong);

            border-radius: 12px;

            background:
                #fbfdff;

            color:
                var(--c2p-text);

            box-shadow:
                inset
                0 1px 2px
                rgba(8, 31, 70, 0.025);
        }

        input[type="url"]:focus {
            border-color:
                var(--c2p-blue);

            box-shadow:
                0 0 0 4px
                rgba(17, 101, 231, 0.11);
        }

        .source-separator {
            color:
                #91a2ba;

            font-weight: 600;
        }

        textarea {
            border:
                1px solid
                var(--c2p-border-strong);

            border-radius: 14px;

            background:
                linear-gradient(
                    180deg,
                    #ffffff 0%,
                    #fbfdff 100%
                );

            color:
                var(--c2p-navy);

            box-shadow:
                inset
                0 1px 3px
                rgba(8, 31, 70, 0.025);
        }

        textarea:focus {
            border-color:
                var(--c2p-blue);

            box-shadow:
                0 0 0 4px
                rgba(17, 101, 231, 0.11);
        }

        #learn {
            width: 100%;
            min-height: 48px;

            margin-top: 14px;

            border-radius: 12px;

            background:
                linear-gradient(
                    110deg,
                    #0c56d6 0%,
                    #1165e7 52%,
                    #168deb 100%
                );

            color: #ffffff;

            font-size: 13px;
            font-weight: 800;

            letter-spacing:
                -0.01em;

            box-shadow:
                0 10px 26px
                rgba(17, 101, 231, 0.26);

            transition:
                transform 150ms ease,
                box-shadow 150ms ease,
                filter 150ms ease;
        }

        #learn:hover:not(:disabled) {
            transform:
                translateY(-2px);

            filter:
                saturate(1.08);

            box-shadow:
                0 14px 32px
                rgba(17, 101, 231, 0.34);
        }

        #learn:active:not(:disabled) {
            transform:
                translateY(0);
        }

        .privacy-note {
            position: relative;

            margin-top: 16px;
            padding: 14px 16px;

            border:
                1px solid
                #d8e7fa;

            border-radius: 12px;

            background:
                linear-gradient(
                    135deg,
                    #f7fbff,
                    #edf5ff
                );

            color:
                var(--c2p-blue-mid);
        }

        .privacy-note summary {
            color:
                var(--c2p-blue);

            opacity: 1;
        }

        .learning-panel-body {
            background:
                linear-gradient(
                    180deg,
                    #ffffff 0%,
                    #f8fbff 100%
                );
        }

        .learning-empty {
            position: relative;
        }

        .learning-empty::before {
            content: "✦";

            display: grid;
            place-items: center;

            width: 48px;
            height: 48px;

            margin:
                0 auto
                14px;

            border:
                1px solid
                #d4e5fb;

            border-radius: 16px;

            background:
                linear-gradient(
                    135deg,
                    #e9f7fd,
                    #edf3ff
                );

            color:
                var(--c2p-blue);

            font-size: 20px;

            box-shadow:
                0 8px 18px
                rgba(17, 101, 231, 0.10);
        }

        .item {
            position: relative;

            border:
                1px solid
                #dce7f4;

            border-left:
                3px solid
                var(--c2p-blue);

            background:
                linear-gradient(
                    180deg,
                    #ffffff 0%,
                    #fbfdff 100%
                );

            box-shadow:
                var(--c2p-shadow-soft);

            transition:
                transform 150ms ease,
                border-color 150ms ease,
                box-shadow 150ms ease;
        }

        .item:hover {
            transform:
                translateY(-1px);

            border-color:
                #bcd2ef;

            box-shadow:
                0 12px 30px
                rgba(8, 31, 70, 0.075);
        }

        .meta {
            color:
                #8193ad;
        }

        .concept {
            color:
                var(--c2p-navy);
        }

        .concept-chip {
            border-color:
                #cce7f5;

            background:
                var(--c2p-cyan-soft);

            color:
                #126d8b;
        }

        .explanation {
            color:
                #162b4b;
        }

        .code {
            border:
                1px solid
                #d9e5f2;

            background:
                #f4f8fd;

            color:
                var(--c2p-navy);
        }

        .code2plain-code-highlight {
            background:
                rgba(26, 168, 217, 0.11);
        }

        .item > details:not(.learning-check)
        summary {
            color:
                var(--c2p-blue-mid);
        }

        .challenge {
            color:
                #6d809b;
        }

        .learning-check {
            border-top-color:
                #dce7f4;
        }

        .learning-check summary {
            color:
                var(--c2p-blue-mid);
        }

        .learning-check[open] summary {
            color:
                var(--c2p-blue);
        }

        .learning-check-body {
            border:
                1px solid
                #dce7f4;

            background:
                linear-gradient(
                    180deg,
                    #f8fbff,
                    #f2f7fd
                );
        }

        .learning-check-question {
            color:
                var(--c2p-navy);
        }

        .learning-check-option {
            border:
                1px solid
                transparent;

            color:
                #304867;
        }

        .learning-check-option:hover {
            border-color:
                #d9e6f5;

            background:
                #ffffff;
        }

        .learning-check-verify {
            background:
                linear-gradient(
                    110deg,
                    var(--c2p-blue),
                    #1788ea
                );

            color: #ffffff;
        }

        @media (max-width: 900px) {
            .app-header {
                padding:
                    14px
                    14px;
            }

            .workspace {
                gap: 18px;
            }
        }

        @media (max-width: 640px) {
            .app-header {
                border-radius: 16px;
            }

            .brand-mark {
                width: 38px;
                height: 38px;
            }

            .workspace-panel {
                border-radius: 16px;
            }

            .panel-header {
                min-height: 52px;
            }

            #learn {
                min-height: 48px;
                font-size: 13px;
            }

            .item {
                box-shadow:
                    0 6px 20px
                    rgba(8, 31, 70, 0.05);
            }
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

        <button
            id="ownerAccessButton"
            class="owner-access-button"
            type="button"
        >
            Owner
        </button>

        <div
            id="demoTimer"
            class="demo-timer"
        >
            Demo 20:00
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


const demoTimer =
    document.getElementById(
        "demoTimer"
    );



document.addEventListener(
    "click",
    (event) => {
        if (
            !(event.target instanceof Element)
        ) {
            return;
        }

        const summary =
            event.target.closest(
                ".learning-check > summary"
            );

        if (!summary) {
            return;
        }

        const currentCheck =
            summary.parentElement;

        document
            .querySelectorAll(
                ".learning-check[open]"
            )
            .forEach(
                (check) => {
                    if (
                        check
                        !== currentCheck
                    ) {
                        check.removeAttribute(
                            "open"
                        );
                    }
                }
            );
    }
);


let demoToken = null;
let demoExpiresAt = null;

let ownerToken = null;


const ownerAccessButton =
    document.getElementById(
        "ownerAccessButton"
    );


async function restoreOwnerSession() {
    const key =
        "code2plain.owner_token";

    const storedToken =
        window.localStorage.getItem(
            key
        );

    if (!storedToken) {
        return false;
    }

    const response =
        await fetch(
            "/v1/owner/status",
            {
                method: "POST",
                headers: {
                    "Content-Type":
                        "application/json"
                },
                body:
                    JSON.stringify({
                        token:
                            storedToken
                    })
            }
        );

    if (!response.ok) {
        window.localStorage.removeItem(
            key
        );

        return false;
    }

    const status =
        await response.json();

    if (!status.valid) {
        window.localStorage.removeItem(
            key
        );

        return false;
    }

    ownerToken =
        storedToken;

    if (ownerAccessButton) {
        ownerAccessButton.textContent =
            "Exit Owner";

        ownerAccessButton.classList.add(
            "active"
        );
    }

    return true;
}


async function exitOwner() {
    const key =
        "code2plain.owner_token";

    ownerToken = null;

    window.localStorage.removeItem(
        key
    );

    if (ownerAccessButton) {
        ownerAccessButton.textContent =
            "Owner";

        ownerAccessButton.classList.remove(
            "active"
        );
    }

    demoToken = null;
    demoExpiresAt = null;

    try {
        await startOrRestoreDemo();
    } catch (error) {
        demoTimer.textContent =
            "Demo unavailable";

        demoTimer.classList.add(
            "expired"
        );

        button.disabled =
            true;

        return;
    }

    updateDemoTimer();
}


async function handleOwnerAccess() {
    if (ownerToken) {
        await exitOwner();
        return;
    }

    await loginOwner();
}


async function loginOwner() {
    const credential =
        window.prompt(
            "Owner access"
        );

    if (!credential) {
        return;
    }

    const response =
        await fetch(
            "/v1/owner/login",
            {
                method: "POST",
                headers: {
                    "Content-Type":
                        "application/json"
                },
                body:
                    JSON.stringify({
                        credential
                    })
            }
        );

    if (!response.ok) {
        window.alert(
            "Credencial incorrecta."
        );

        return;
    }

    const data =
        await response.json();

    ownerToken =
        data.token;

    window.localStorage.setItem(
        "code2plain.owner_token",
        ownerToken
    );

    if (ownerAccessButton) {
        ownerAccessButton.textContent =
            "Exit Owner";

        ownerAccessButton.classList.add(
            "active"
        );
    }

    demoTimer.textContent =
        "Acceso completo";

    demoTimer.classList.remove(
        "expired"
    );

    button.disabled =
        false;

    button.textContent =
        "Explicar código";
}


if (ownerAccessButton) {
    ownerAccessButton.addEventListener(
        "click",
        handleOwnerAccess
    );
}


async function startOrRestoreDemo() {
    const tokenKey =
        "code2plain.demo_token";

    const expiryKey =
        "code2plain.demo_expires_at";

    const storedToken =
        window.localStorage.getItem(
            tokenKey
        );

    const storedExpiry =
        window.localStorage.getItem(
            expiryKey
        );

    if (
        storedToken
        && storedExpiry
    ) {
        const response =
            await fetch(
                "/v1/demo/status",
                {
                    method: "POST",
                    headers: {
                        "Content-Type":
                            "application/json"
                    },
                    body:
                        JSON.stringify({
                            token:
                                storedToken
                        })
                }
            );

        const status =
            await response.json();

        if (
            response.ok
            && status.valid
            && status.user_id
                === learningUserId
        ) {
            demoToken =
                storedToken;

            demoExpiresAt =
                status.expires_at;

            return;
        }

        /*
        Important:
        An expired token is NOT replaced automatically.
        Otherwise refreshing or reopening the browser
        would create unlimited trials.
        */
        if (
            response.ok
            && !status.valid
        ) {
            demoToken =
                storedToken;

            demoExpiresAt =
                storedExpiry;

            return;
        }
    }

    const response =
        await fetch(
            "/v1/demo/start",
            {
                method: "POST",
                headers: {
                    "Content-Type":
                        "application/json"
                },
                body:
                    JSON.stringify({
                        user_id:
                            learningUserId
                    })
            }
        );

    if (!response.ok) {
        throw new Error(
            "Could not start demo."
        );
    }

    const data =
        await response.json();

    demoToken =
        data.token;

    demoExpiresAt =
        data.expires_at;

    window.localStorage.setItem(
        tokenKey,
        demoToken
    );

    window.localStorage.setItem(
        expiryKey,
        demoExpiresAt
    );
}


function updateDemoTimer() {
    if (ownerToken) {
        demoTimer.textContent =
            "Acceso completo";

        demoTimer.classList.remove(
            "expired"
        );

        button.disabled =
            false;

        return;
    }

    if (
        !demoTimer
        || !demoExpiresAt
    ) {
        return;
    }

    const remaining =
        Math.max(
            0,
            Math.floor(
                (
                    new Date(
                        demoExpiresAt
                    ).getTime()
                    - Date.now()
                )
                / 1000
            )
        );

    const minutes =
        Math.floor(
            remaining / 60
        );

    const seconds =
        remaining % 60;

    if (remaining > 0) {
        demoTimer.textContent =
            "Demo "
            + String(minutes)
            + ":"
            + String(seconds)
                .padStart(
                    2,
                    "0"
                );

        return;
    }

    demoTimer.textContent =
        "Demo terminada";

    demoTimer.classList.add(
        "expired"
    );

    button.disabled =
        true;

    button.textContent =
        "Demo terminada";
}


restoreOwnerSession()
    .then(
        ownerActive => {
            if (ownerActive) {
                demoTimer.textContent =
                    "Acceso completo";

                updateDemoTimer();

                window.setInterval(
                    updateDemoTimer,
                    1000
                );

                return;
            }

            return startOrRestoreDemo()
                .then(
                    () => {
                        updateDemoTimer();

                        window.setInterval(
                            updateDemoTimer,
                            1000
                        );
                    }
                );
        }
    )
    .catch(
        () => {
            if (demoTimer) {
                demoTimer.textContent =
                    "Demo no disponible";

                demoTimer.classList.add(
                    "expired"
                );
            }
        }
    );


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
                        learningUserId,
                    demo_token:
                        demoToken,
                    owner_token:
                        ownerToken
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
                                                        ),
                                                    demo_token:
                                                        demoToken,
                                                    owner_token:
                                                        ownerToken
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
