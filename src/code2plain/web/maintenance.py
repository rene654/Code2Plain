MAINTENANCE_HTML = r"""
<!doctype html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <meta
        name="viewport"
        content="width=device-width, initial-scale=1"
    >
    <title>Code2Plain · Leveling up</title>
    <style>
        * {
            box-sizing: border-box;
        }
        body {
            margin: 0;
            min-height: 100vh;
            display: grid;
            place-items: center;
            padding: 28px;
            background:
                radial-gradient(
                    circle at top,
                    #eef2ff 0,
                    #fafafa 45%
                );
            color: #171717;
            font-family:
                Inter,
                system-ui,
                -apple-system,
                sans-serif;
        }
        .card {
            width: min(760px, 100%);
            padding: 52px 36px;
            text-align: center;
            background: rgba(255, 255, 255, .94);
            border: 1px solid #e5e7eb;
            border-radius: 28px;
            box-shadow: 0 24px 70px rgba(0, 0, 0, .08);
        }
        .mascot {
            font-size: 72px;
            margin-bottom: 22px;
        }
        .badge {
            display: inline-block;
            padding: 8px 14px;
            margin-bottom: 18px;
            border-radius: 999px;
            background: #eef2ff;
            font-size: 13px;
            font-weight: 700;
        }
        h1 {
            margin: 0;
            font-size: clamp(34px, 6vw, 56px);
            letter-spacing: -0.045em;
        }
        .lead {
            max-width: 590px;
            margin: 20px auto 0;
            color: #525252;
            font-size: 18px;
            line-height: 1.65;
        }
        .code {
            max-width: 520px;
            margin: 30px auto 0;
            padding: 18px 20px;
            text-align: left;
            border-radius: 16px;
            background: #171717;
            color: #f5f5f5;
            font-family: ui-monospace, monospace;
            line-height: 1.7;
        }
        .accent {
            color: #a5b4fc;
        }
        .footer {
            margin-top: 26px;
            color: #737373;
            font-size: 13px;
        }
    </style>
</head>
<body>
    <main class="card">
        <div class="mascot">🤖🔧📚</div>
        <div class="badge">
            LEARNING ENGINE UPGRADE
        </div>
        <h1>
            Code2Plain está subiendo de nivel.
        </h1>
        <p class="lead">
            La IA ya sabe escribir el código.
            Nosotros estamos mejorando cómo
            Code2Plain te ayuda a entenderlo,
            practicarlo y aprenderlo de verdad.
        </p>
        <div class="code">
            <span class="accent">AI</span>
            → writes it<br>
            <span class="accent">Code2Plain</span>
            → translates it<br>
            <span class="accent">You</span>
            → actually learn it 🚀
        </div>
        <div class="footer">
            Estamos cocinando algo mejor.
            Volvemos pronto.
        </div>
    </main>
</body>
</html>
"""
