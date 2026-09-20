# Lecture content

Each lecture is either a **Quarto source** (converted) or a **legacy `.json`
file** (not yet converted). The course schedule reads both, so lectures can be
migrated one at a time.

```
content/lectures/
  _quarto.yml          project config + the two output formats every lecture shares
  _theme/              shared accessibility styles and the reading-list filter
  1_1_HTTP/            a converted lecture
    1_1_HTTP.qmd       title, reading list, and content - the only source of truth
    assets/            images used by that lecture
  0-intro.json         a lecture still awaiting conversion
```

A converted lecture renders to two outputs from that single `.qmd`:

- `slides.html` — Reveal.js deck
- `index.html` — the same lecture as one readable page

Rendered output is committed to `static_files/lectures/`, so running the site
does **not** require Quarto.

## Editing a lecture

```bash
# One-time: install Quarto locally into .tools/
bash tools/install-quarto.sh

# Edit content/lectures/1_1_HTTP/1_1_HTTP.qmd, then:
bash tools/render-lectures.sh 1_1_HTTP   # one lecture
bash tools/render-lectures.sh            # all lectures

# Commit the source and the rendered output together
git add content/lectures static_files/lectures
```

### Format-specific content

To show something on only one of the two outputs, use `unless-format`, not
`when-format="html"`. Reveal.js *is* an HTML format, so `when-format="html"`
matches the slides too and the content ends up in both:

```markdown
::: {.content-visible unless-format="revealjs"}
Readable page only - a Mermaid diagram, a long explanation.
:::

::: {.content-visible when-format="revealjs"}
Slides only - a short list that fits on one slide.
:::
```

## Lecture front matter

The formats live in `_quarto.yml`, so a lecture only declares its own metadata:

```yaml
---
title: "HTTP Request/Response"
subtitle: "CSE312 — Web Development"
lang: en
description: "One-sentence summary of the lecture."
reading-list:
  - url: "https://en.wikipedia.org/wiki/Hypertext_Transfer_Protocol"
    text: "HTTP (Wikipedia)"
# Show Quarto Slides + Readable Page on the schedule. Until this is true, the
# schedule links the original PDF instead.
released: true
---
```

`reading-list` is used twice from this one definition:

- `_theme/reading-list.lua` appends a **Further Reading** section to the deck
  and the readable page.
- `cse312_app.py` reads the same front matter to build the reading list on the
  course schedule.

### Releasing a lecture

Converted decks default to `released: false` (or omit the field — same effect).
While unreleased, the schedule shows the lecture title and reading list, but
links **Slides** to the original PDF under `static_files/slides/` rather than
the Quarto outputs.

After conversion, flip the flag and commit:

```yaml
released: true
```

No re-render is required — Flask reads this from the `.qmd` on each request.
Direct URLs to the rendered HTML still work if someone has the path; this only
controls what the schedule advertises.

## Why this is a website project

`_quarto.yml` uses `type: website` so every lecture shares one `site_libs/`
directory. With the default project type each lecture carries its own copy of
reveal.js, Bootstrap, and Mermaid — about 9 MB apiece, or roughly 180 MB once
the full course is converted. Sharing them keeps the committed output at about
9 MB total plus ~190 KB per lecture.

> Render once, not once per format. Running `quarto render --to revealjs` and
> then `quarto render --to html` makes the second render delete the first one's
> libraries, which silently strips `reveal.js` out of the deck. The deck then
> displays as one long scrolling page. `tools/verify_output.py` fails the build
> if this ever happens again.

## Accessibility (WCAG 2.1 AA)

`_theme/page.scss`, `_theme/slides.scss`, and the lecture sources target Level AA:

- Document language set on every page.
- One `h1` per page with `h2` sections, so slides stay top-level and the
  readable page keeps a real heading hierarchy.
- Visible keyboard focus indicators and a skip link to main content.
- Text alternatives for images, and text descriptions for diagrams.
- Contrast-checked colors (dark text on light background).
- `prefers-reduced-motion` and forced-colors support.
- Linear slide navigation, which is more predictable for screen readers.
- Schedule links carry per-lecture `aria-label`s, so "Slides" and "Readable
  Page" are distinguishable out of context.

`tools/verify_output.py` checks the structural parts automatically. Color
contrast and alt-text quality still need a human and a tool like axe DevTools
or WAVE before publishing.
