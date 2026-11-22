# AGENTS.md — Random Signal Analysis Tutorial

## Project mission
Build a rigorous, independently readable Chinese stochastic-signal textbook, not a slide deck, shallow topic listing, or generic landing page. Treat the 28 chapters as a dependency graph, but make **every HTML page self-contained** for a reader arriving from search.

## Repository contract
- \`index.html\`: static semantic landing page, all chapter links in initial HTML (do not require JS/fetch to populate).
- \`courses.json\`: canonical title, topics, destination, stage metadata. Keep 28 entries and align with the homepage.
- \`chapters/01.html\` … \`28.html\`: canonical content paths. 01–03 are freshly audited; **04–28 remain legacy** pending review.
- \`assets/css/site.css\`: shared styles for new pages; never introduce 28 divergent inline themes.
- \`assets/js/site.js\`: unobtrusive enhancement; default content always visible without JS.
- \`assets/svg/NN-*.svg\`: original, standalone diagrams with XML namespace, viewBox, title and desc. New images must have meaningful HTML alt and captions.
- \`chapters/theme.css\`: unchanged legacy CSS so unreviewed chapters render as before.
- Root \`01.html\` … \`28.html\`: compatibility redirects. Never break old bookmarks by deleting them.
- \`examples/test_intro_math.py\`: deterministic mathematical assertions; \`scripts/validate_site.py\`: site integrity.
- Pages source: \`main\` / root; no Jekyll build required.

## Olah-style teaching contract (adapted)
Use https://github.com/1998x-stack/Olah-style-posts/tree/main/skills/olah-style-paper-posts/SKILL.md as the methodology reference. For every chapter:

1. **Question**: begin with a realistic mathematical question, not “本讲义介绍了” or fabricated anecdotes.
2. **Concrete example**: one small, fully specified probability model. Distinguish sample paths, random variables, observed values and model assumptions.
3. **Figure storyboard**: ask a different, verifiable question per SVG. Use consistent semantics: teal=primary signal/probability flow, coral=alternative/errors, violet=conditional/secondary structure.
4. **Formal derivation**: define every variable, conditioning set, interval convention, normalization, assumptions and domain. Pair diagrams with native MathML for substantive equations, avoid fake formula formatting.
5. **Executable check**: exact arithmetic or deterministic seeded experiment with declared dependencies. No fabricated measurements or undocumented benchmarks.
6. **Counterexample & boundaries**: explicitly tell readers when a theorem fails (e.g., uncorrelated ≠ independent unless jointly Gaussian; CLT requires conditions; PDF height ≠ probability; nonstationarity invalidates WSS shortcuts).
7. **Synthesis**: a concept bridge, 1–3 self-checks with answers, and direct primary textbook/institutional citations. No production-process prose in article headings, hero, captions or footer.

## Scientific correctness
- Define event independence \`P(A∩B)=P(A)P(B)\`; do not conflate with uncorrelated variables.
- A CDF is right-continuous; \`P(a<X≤b)=F(b)-F(a)\`, while inclusion of atom at a changes the result.
- Density describes mass per unit x; integrate PDF for probabilities; mixed distributions can contain atoms.
- \`N(μ,σ²)\`: σ is standard deviation. Centered iid finite-variance CLT is a limiting statement, **not** “all noise is exactly Gaussian”.
- Covariance matrix must be symmetric positive semidefinite; nonsingular Gaussian density requires positive definite covariance.
- Zero covariance implies independence only for a **jointly Gaussian** vector, not merely Gaussian marginals.
- In chapters 08/09, distinguish strict vs wide-sense stationarity and autocorrelation vs autocovariance; always state Fourier convention and whether DC impulse is included when using spectral formulas.
- Verify references using NIST, MIT OCW, Penn State, primary papers, original software documentation; avoid invented historical timelines and engineering accidents.

## Accessibility and visual checks
- Semantic \`header/nav/main/article/section/footer\`, exactly one H1, clear H2 hierarchy, functional TOC anchors.
- Responsive at 1440, 390, 360 px; no global horizontal scroll. SVG labels legible at target size; use zoomable figures and text equivalents as needed.
- Every \`<svg>\` has viewBox, title, desc, unique IDs. Standalone XML parse should succeed; avoid externally loaded fonts and imported figures.
- Native controls with labels, focus-visible and aria-live result labels. Interactions must be optional enhancements with meaningful starting values.
- MathML Core formulas: real mfrac/msubsup/mtable, scrollable named containers, confirm rendered fraction geometry in a real browser. No MathML inside SVG text.
- Test print media and prefers-reduced-motion.
- Check source links and numerical identities. Never claim a browser or Pages verification unless actually performed.

## Required workflow for each next chapter
1. Read existing chapter and adjacent chapters; list mathematical inaccuracies and missing prerequisites.
2. Search/verify primary educational references; maintain an evidence log (source URL + claim + check).
3. Draft a figure-by-figure concept map and technical facts before CSS.
4. Write a complete standalone article, 2–4 meaningful SVGs, MathML, a reproducible micro-example and counterexample.
5. Run \`python3 scripts/validate_site.py\` and \`python3 -m unittest discover -s examples -p 'test_*.py' -v\`.
6. Browser QA manually/with Playwright: 1440px desktop and 390px/360px mobile, all figures, controls, console errors, overflow, keyboard, print. Record what wasn't verified.
7. Submit PR, review diffs and checks; only call it live after verifying deployed Pages URL.
8. Mark chapter \`stage=refactored\` in \`courses.json\` and update matching homepage badge **only after** evidence and QA.

## Safety for future refactors
- Preserve all existing chapter content or retain copies until migrated. Move legacy files with their exact blob bytes; avoid accidental technical rewrites during path changes.
- Keep redirect shims and relative links. No destructive branch force-push.
- Never claim the full 28 chapters are technically audited when only three are.
