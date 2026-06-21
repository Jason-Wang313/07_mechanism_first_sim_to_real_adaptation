# Paper07 VLA Highlight Hardening Plan

Date: 2026-06-21

## Objective

Make `C:/Users/wangz/Downloads/07.pdf` explicitly match the visible VLA-v4
role model's boxed-link behavior while preserving the final 25-page
mechanism-first sim-to-real adaptation paper:

- citation links use green one-point boxes;
- internal figure/table/equation/section links use red one-point boxes;
- URL links use green one-point boxes;
- the final PDF is rebuilt, copied to Downloads, visually checked, and leaves
  no local `paper/main.pdf`.

## Plan-Start Evidence

Baseline artifact:

- Canonical PDF: `C:/Users/wangz/Downloads/07.pdf`
- Pages: 25
- Size: 1,197,170 bytes
- SHA256: `C8E12AAFCD142564E1CFFF837895CBB98B00953F0291E7777694A703463E8EFA`
- Local `paper/main.pdf`: absent
- Repository branch: `master`

Baseline link inventory from the current Downloads PDF:

- Link pages: `[]`
- Annotation colors: green = 0, red = 0, cyan = 0
- Border widths: none

Source finding:

- `paper/main.tex` is the active manuscript source.
- The active manuscript preamble does not currently load `hyperref`, so the
  baseline PDF has no boxed citation or internal-reference links.
- The target is to install `hyperref` plus the VLA role-model border policy so
  citation/URL links become green boxed links and internal references become red
  boxed links.
- Use the documented manual LaTeX flow from `paper/`: `pdflatex`, `bibtex`,
  and repeated `pdflatex` passes before export.

## Role-Model Target

Install the same explicit hyperref policy as the visible VLA-v4 role model:

```tex
\usepackage{hyperref}
\hypersetup{
  colorlinks=false,
  pdfborder={0 0 1},
  citebordercolor={0 1 0},
  linkbordercolor={1 0 0},
  urlbordercolor={0 1 0}
}
```

## Execution Plan

1. Add `\usepackage{hyperref}` and the VLA `\hypersetup` block in the active
   `paper/main.tex` preamble.
2. Rebuild manually from `paper/` with `pdflatex`, `bibtex`, and repeated
   `pdflatex` passes.
3. If the log asks for another pass for cross-references, run the final
   canonical pass before recording metadata.
4. Copy the rebuilt `paper/main.pdf` to `C:/Users/wangz/Downloads/07.pdf`.
5. Remove local `paper/main.pdf` after export.
6. Recompute page count, byte size, SHA256, annotation colors, border widths,
   and link pages from the final Downloads PDF.
7. Render every page that contains final link annotations into
   `tmp/pdfs/paper07_after`.
8. Visually inspect rendered affected pages:
   - green citation and URL boxes are crisp and aligned;
   - red internal-reference boxes are crisp and aligned;
   - no cyan boxes appear;
   - layout, figures, tables, headers, and page count remain stable.
9. Update README/status/audit/version/validation metadata with the new hash and
   VLA-style boxed-link inventory.
10. Validate build logs, diff hygiene, final PDF hash, and absence of local
    `paper/main.pdf`.
11. Remove Paper07 temp renders, leaving only the shared role-model render
    directory.
12. Stage only Paper07 source and metadata files, commit, push, and verify a
    clean repository before moving to Paper06.

## Non-Goals

- Do not alter experiment results, claims, figures, tables, bibliography
  content, or page count.
- Do not add or remove citations, references, URLs, or template examples merely
  to change link counts.
- Do not create an additional `7.pdf`; keep the repository's canonical
  Downloads target as `07.pdf`.
- Do not leave intermediate PDFs or render folders behind.

## Completion Evidence

- Added `\usepackage{hyperref}` and the explicit VLA `\hypersetup` block in
  active `paper/main.tex`.
- Rebuilt from `paper/` with `pdflatex`, `bibtex`, `pdflatex`, `pdflatex`.
- Exported canonical PDF: `C:/Users/wangz/Downloads/07.pdf`
- Pages: 25
- Size: 1,241,363 bytes
- SHA256: `EF54EDF6F2F0396D0C784CF563C8E8957D4253A29CEF0D050A9B99083BF43764`
- Link inventory: 41 annotations on pages `[(1, 13), (4, 2), (5, 2), (7, 1), (8, 2), (9, 1), (10, 6), (11, 14)]`; green = 33, red = 8, cyan = 0; all borders `(0, 0, 1)`.
- Visual audit: rendered pages 1, 4, 5, 7, 8, 9, 10, and 11; green citation/URL boxes and red internal-reference boxes are crisp and aligned.
- Local `paper/main.pdf`: removed after export.
- Duplicate `C:/Users/wangz/Downloads/7.pdf`: not created.
