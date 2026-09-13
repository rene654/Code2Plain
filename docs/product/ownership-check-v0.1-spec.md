# Code2Plain — Ownership Check v0.1
## Product Specification / Especificación de Producto

**Status / Estado:** Frozen for implementation
**Phase / Fase:** 11.6 — Differentiation & Product-Market Audit
**Implementation:** Next development session
**Baseline:** main @ 038fef7
**Documentation:** Spanish + English

---

## 1. Product Direction / Dirección
ES: Code2Plain es una capa post-generación. El usuario genera código donde quiera y después lo trae a Code2Plain.
EN: Code2Plain is a post-generation learning layer. Users generate code anywhere and then bring it to Code2Plain.
Example: Claude genera Pandas; Code2Plain comprueba si el usuario puede controlarlo.
Why: No interceptamos, limitamos ni actuamos como proxy de otra IA.

## 2. Ownership Check v0.1
ES: Cada check dura aproximadamente 60–120 segundos y evalúa un concepto principal.
EN: Each check lasts approximately 60–120 seconds and evaluates one primary concept.
Example: Boolean filtering.
Why: Mantiene baja la fricción.

## 3. Core Loop / Ciclo Central
Understand → Predict → Modify.
Example: entender un filtro, predecir el cambio de 1000 a 2500 y modificarlo.
Why: Combina comprensión, razonamiento y control práctico.

## 4. Recovery System / Recuperación
Attempt → Hint → Line Breakdown → Focused Explanation → Retry.
Example: si falla groupby, primero recibe pista y luego explicación sólo si la necesita.
Why: Leer una explicación no cuenta como aprendizaje demostrado.

## 5. Learning Evidence / Evidencia
Medimos seis dimensiones:
- Understanding / Comprensión
- Prediction / Predicción
- Modification / Modificación
- Help Required / Ayuda requerida
- Repetition & Consistency / Repetición y consistencia
- Transfer / Transferencia

Why: Una respuesta correcta aislada no demuestra dominio.

## 6. Mastery Policy / Política de Dominio
Seen → Understood Once → Verified → Transfer Demonstrated → Autonomous.
ES: Dos o tres aciertos son evidencia inicial, no dominio.
EN: Two or three correct attempts are initial evidence, not mastery.
Why: Evita métricas falsas.

## 7. Ownership Meter
ES: Muestra evidencia actual de control sobre el concepto.
EN: Shows current evidence of control over the concept.
It does NOT measure intelligence or overall programming ability.
Example: Pandas Boolean Filtering — Developing.

## 8. Meter Visual Design / Diseño
3D liquid capsule/tube with smooth animation.
Red → Orange → Yellow → Light Green → Green.
Why: Feedback premium y visible sin convertir la página en un dashboard.

## 9. Percentage Integrity / Integridad
ES: El porcentaje representa evidencia acumulada, no dominio absoluto.
EN: The percentage represents accumulated evidence, not absolute mastery.
Rule: Una sola sesión nunca produce Autonomous.
Why: Los estados altos requieren consistencia y transferencia.

## 10. How It Is Measured / Cómo se mide
Control: "Cómo se mide / How it is measured ⓘ"
Desktop: hover, focus or click.
Mobile: tap.
Shows the six learning dimensions in a compact floating card.
Why: Transparencia sin sobrecarga visual.

## 11. Main Screen Hierarchy / Jerarquía
Visible by default:
Code context → Current concept → Ownership Meter → Current challenge.
Everything else appears on demand.
Why: Simple outside, sophisticated inside.

## 12. Session Completion / Fin de Sesión
A clean modal shows honest evidence.
Example:
Understand ✓
Predict ✓
Modify Assisted
Transfer Pending
Why: Termina con información útil, no sólo con celebración.

## 13. Session Summary Sharing / Compartir
Actions:
- WhatsApp
- Email
- Copy Summary
- Native Share when supported
Why: Permite conservar y compartir qué salió bien y qué necesita repaso.

## 14. Shared Result Privacy / Privacidad
Source code is NOT shared by default.
Only concept, evidence, help required, current state and review recommendation are shared.
Why: Protege código privado, laboral y propietario.

## 15. Sharing v0.1
Prefer:
Web Share API
WhatsApp share URL
mailto:
clipboard
No transactional email or WhatsApp Business infrastructure in v0.1.
Why: Menor costo y complejidad.

## 16. Skill Memory
Skill Memory stores evidence per user and concept across sessions.
Minimum evidence:
user_id
session_id
concept_id
challenge_type
result
assistance_level
timestamp
evidence_state
Why: Code2Plain recuerda qué sabe y qué necesita practicar cada usuario.

## 17. Skill Memory Plans / Planes
Anonymous: session-only memory.
Registered Free: basic persistent Skill Memory.
Paid: extended history, more concepts, transfer checks, spaced review, analytics and reports.
Exact commercial limits remain TBD.
Why: La memoria básica es parte del valor central y no debe desaparecer completamente detrás del paywall.

## 18. Multi-User Persistence / Persistencia Multiusuario
Before launch we must audit the existing storage layer.
Requirements:
- strict isolation by user_id
- concurrent users
- backup strategy
- deletion capability
- retention policy
- migration strategy
Why: No asumiremos que la lógica actual ya está validada para decenas o cientos de usuarios.

## 19. Python Input Strategy / Estrategia Python
Principle:
Broad input → capability detection → verified learning only where supported.
ES: Code2Plain debe aceptar una gama amplia de Python, pero v0.1 no promete evaluar correctamente cada construcción existente.
EN: Code2Plain should accept broad Python input, but v0.1 does not claim verified ownership coverage for every Python construct.
Why: Aceptar código y demostrar aprendizaje son problemas distintos.

## 20. Valid and Invalid Python / Python Válido e Inválido
Valid syntax: analyze structure without executing unknown code.
Syntax errors: detect and teach from the error.
Runtime errors: require traceback or sufficient context when code is not executed.
Example: SyntaxError can be detected directly; KeyError normally requires traceback/data context.
Why: Code2Plain must never invent the cause of an error it cannot verify.

## 21. Initial Ownership Coverage / Cobertura Inicial
Initial verified concepts:
variables, comparisons, boolean filters, basic function calls,
pandas.read_csv, groupby + aggregation and simple conditions.
Why: Sólo evaluamos lo que podemos verificar bien.

## 22. Language Expansion / Expansión
Python first.
SQL/PostgreSQL, Java and other languages follow after product validation.
Skill Memory and Ownership Evidence should be language-agnostic at the data-model level.
Why: Podemos ampliar lenguajes sin reconstruir el núcleo pedagógico.

## 23. Beginner and Senior Positioning / Posicionamiento
One product, different cognitive depth.
Beginner example: What changes if 1000 becomes 2500?
Senior example: What invariant or behavior could break if the input type changes?
Why: Permite marketing diferente para Hybridge, startups y developers senior.

## 24. Existing Components to Reuse / Reutilización
Block Overview → recovery
Line explanation → recovery
Line Breakdown → remediation
Learning Checks → Understand
Mini exercises → retry/support
Active Modification → Modify
Skill Memory → accumulated evidence
Python analysis → concept detection
Why: Reorganizamos Code2Plain; no lo reconstruimos desde cero.

## 25. New Core Components / Nuevos Componentes
A. Ownership Orchestrator
B. Predict Challenge Engine
C. Ownership Evidence Model
D. Ownership Meter
E. Session Summary
Why: Convierten features aisladas en un sistema coherente.

## 26. User Content & Responsibility Policy / Responsabilidad
Before paid public launch create:
- Terms of Use
- Privacy Notice
- Acceptable Use rules

User must represent that they have the right or authorization to upload the code.
User remains responsible for the uploaded content, legality, deployment and use.
Warn users not to upload credentials, secrets, personal data or confidential code without authorization.
Code2Plain is an educational and analysis tool, not a warranty of correctness, security, production fitness or legal compliance.
These terms do not remove Code2Plain own legal obligations.
Final legal language requires professional review before paid launch.

## 27. Data Retention & Deletion / Retención
Define:
- what data is stored
- retention period
- deletion process
- what is derived from uploaded code
Whenever possible Skill Memory stores learning evidence instead of full source code.
Why: Minimiza riesgo y exposición de información sensible.

## 28. Out of Scope / Fuera de Alcance
No AI interception or proxying.
No AI response restriction.
No full IDE.
No SQL implementation in v0.1.
No global programmer score.
No fake mastery percentages.
No lives/hearts or childish gamification.
No enterprise dashboard.
No paid messaging infrastructure.
No broad frontend refactor.
Why: Protege enfoque, costo y velocidad.

## 29. UX + Product Rule + North Star + Done
UX:
Minimal visible interface.
Depth on demand.
One meaningful concept at a time.
Actions over passive reading.
Teach after detecting a gap.
Preserve AI-driven development speed.

Product Rule:
Does this turn AI-generated code into demonstrable human capability?
¿Convierte esto código generado por IA en capacidad humana demostrable?

North Star:
Can the user now solve independently something equivalent to what they previously needed AI to solve?
¿Puede resolver ahora sin ayuda algo equivalente a lo que anteriormente necesitaba que la IA resolviera?

v0.1 Done:
Concept selection + Understand + Predict + Modify + progressive remediation +
retry + assistance tracking + Ownership Meter + measurement explainer +
honest session summary + sharing + Skill Memory evidence + automated tests.

---

## Frozen Product Decision / Decisión Congelada

Code2Plain evolves from:

Explain code → Test understanding

to:

Detect control → Require action → Teach gaps → Verify again → Accumulate evidence

Build with AI. Keep the skill.
