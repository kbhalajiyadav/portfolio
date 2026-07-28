# Portfolio content taxonomy

This note records the canonical distinction between research training and applied
innovation on the public portfolio. It exists to prevent future edits from merging
activities that provide different kinds of evidence.

## Canonical public labels

| Source collection | Public label | Current record |
| --- | --- | --- |
| `professional_development` | **Research training** | 1st National Neutron Scattering School, Oak Ridge National Laboratory, September 2025 |
| `applied_innovation` | **Applied innovation** | Prototype Demonstrator, Shelfie Program, VCU da Vinci Center Feedback Friday, Spring 2026 |

The source collection name `professional_development` is retained for backward
compatibility and commit-history continuity. Its homepage label is narrower and more
informative: **Research training**.

## Classification rationale

### Research training

Use this category for formal scientific instruction that develops a research method or
technical capability. The current record is the **1st National Neutron Scattering
School** at **Oak Ridge National Laboratory**, where Bhalaji was a selected participant.
The public portfolio describes it conservatively as foundational training supporting
scattering-informed soft-matter research.

Preserve the institution's official program title. Do not rename the program as a
workshop or use informal variants such as “Netroschooltraining” unless an authoritative
source establishes that wording.

### Applied innovation

Use this category for translating a technical or materials concept into a prototype,
demonstration, evaluated use case, or innovation-oriented presentation. The current
record is the **Shelfie Program** prototype demonstration at **VCU da Vinci Center ·
Feedback Friday**. The public record states that Bhalaji demonstrated a battery-free
thermochromic sock concept and completed credentials in **Design Thinking**,
**Prototyping**, and **Pitching & Storytelling**.

This activity is not classified as service because the primary evidence is prototype
translation and demonstration rather than committee, review, volunteer, or judging
work.

## Historical decision

During the July 28, 2026 academic-status and classification pass, the Shelfie record was
moved out of the `service` collection and placed in a dedicated
`applied_innovation` collection. The homepage later used the combined heading
“Applied innovation & professional development,” while the neutron school was already
shown under “Professional development.” That repeated phrase blurred the intended
classification.

The corrected homepage labels are therefore:

- **Research training** for the neutron-scattering school; and
- **Applied innovation** for the Shelfie prototype record.

The two source collections remain separate because they answer different portfolio
questions:

- What formal research capability was developed?
- What concept was translated into a prototype or demonstration?

## Future classification rules

Add a record to **Research training** when the primary evidence is structured scientific
or technical instruction, such as an instrument school, methods course, specialist
summer school, or formally documented research training program.

Add a record to **Applied innovation** when the primary evidence is prototype creation,
translation, demonstration, innovation-program participation, or an applied design
credential earned as part of that work.

Do not place routine conference attendance, general webinars, ordinary coursework,
service activities, or unsupported product claims in either collection.

## Validation

`scripts/audit_source.py` protects the following invariants:

- both source collections remain present;
- the neutron-school and Shelfie source details remain identifiable;
- the homepage displays **Research training** and **Applied innovation**;
- the former combined heading does not return; and
- the informal “Netroschooltraining” wording is not introduced.
