# Research Note 001 — pre-staging red-team record

This record documents the adversarial review performed **before** the author release decision. The Research Note itself and its figures remain private/local and have not been committed to public Git.

## Verdict

**Pass after targeted red-team edits.**

The reviewed candidate remains technically eligible for public-source staging as `draft: true`, but the author release decision is still `pending`. No automatic promotion is permitted.

## Material findings

1. **Categorical title risk.** The working title was stronger than the evidence required. The private candidate now uses the less categorical working title **“What a Peel Trace Can Tell You Beyond a Single Force Value.”**
2. **Crack-initiation terminology risk.** The peer-reviewed study labels `Fci` as crack-initiation force but operationally defines it from retained high local maxima in the selected analysis window. The revised candidate states the operational definition and does not equate it with a universal physical measurement of the instant of crack nucleation.
3. **Oscillation/mechanism risk.** Force-trace oscillation alone does not prove a specific stick–slip mechanism. The revised note distinguishes an operational trace descriptor from mechanism identification and adds counter-literature on machine-compliance dependence in peel testing.
4. **Generalization risk.** The underlying textile comparison is now explicitly described as a proof of concept for a defined system, not a universally validated ranking framework.
5. **Repeatability/reproducibility risk.** The revised text limits repeatability claims to the tested replicate set and rejects cross-laboratory/protocol inference.
6. **Standards boundary.** The practical reading sequence is explicitly identified as interpretive guidance, not a replacement for an applicable test standard, validated laboratory SOP, or acceptance criterion.
7. **Lifecycle overconfidence.** The initial note lifecycle status is changed from `stable` to `evolving` because the note is new and is partly tied to release-candidate software.
8. **Contributor transparency.** The candidate now identifies the underlying study as co-authored work and the Research Note as B.Y.K.'s explanatory synthesis.
9. **AI/editorial transparency.** The candidate records that AI-assisted tools supported editorial/adversarial review, were not used as scientific evidence, and do not replace author responsibility.
10. **COI transparency.** The candidate now carries the underlying peer-reviewed study's statement that the authors declared no conflicts of interest.
11. **Source-review traceability.** A source-status review date is recorded; substantive changes reopen the relevant review.
12. **Figure security/accessibility.** The two original SVGs were checked for scripts, event handlers, external links and foreign objects; none were found. Both contain accessible `<title>` and `<desc>` metadata and no experimental data.

## Counter-literature check

A deliberate search for evidence that could undermine a simple “oscillations = interface stick–slip” interpretation identified:

- Andrews, E. H.; Khan, T. A.; Majid, H. A. **Adhesion to skin: Part 1 Peel tests with hard and soft machines.** *Journal of Materials Science* 1985, 20, 3621–3630. DOI `10.1007/BF01113769`.

The DOI/title record was independently verified and no retraction, correction, or expression-of-concern notice was found. Its machine-compliance result is used only to support the caution that measured peel dynamics can depend on the test system.

## Standards/metrology check

Current public standards metadata reinforces the same boundary:

- ASTM lists `D1876-08(2023)` for T-peel resistance of adhesives.
- ASTM lists `D2724-19(2025)e1` for bond strength of bonded/fused/laminated apparel fabrics; the published textile study reports an adapted protocol based on ASTM D2724-19.
- ISO lists `ISO 11339:2022` for T-peel testing of flexible-to-flexible bonded assemblies and states that the test procedure does not provide design information.

The Research Note therefore remains explanatory and system-specific rather than standard-setting.

## Pre-mortem outcomes

The red-team explicitly tested these plausible future criticisms:

- `Fci` was presented as a fundamental crack-nucleation measurement;
- oscillations were automatically labeled as a physical stick–slip mechanism;
- PSI/SSA were presented as transferable material constants;
- a proof-of-concept ranking was presented as a validated universal method;
- an author recommendation was presented as an ASTM/ISO procedure;
- a single-author note appeared to appropriate co-authored work;
- AI assistance was hidden or treated as evidence;
- later software/source changes could silently stale the note.

The private v4 candidate has been revised against each of these failure modes.

## Remaining boundary

The only irreversible step remains the author's intentional release decision. Until then:

- no Note 001 prose enters `content/notes/`;
- no Note 001 figure enters public Git;
- `author_release_decision` remains `pending`;
- staging/publishing automation must not promote the candidate.
