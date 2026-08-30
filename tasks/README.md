# `tasks/` - standalone pages, published verbatim

Self-contained HTML that `tools/build_site.py` copies into `site/tasks/` **byte for byte** and
publishes to GitHub Pages beside the reader. One folder per page, each with an `index.html`, so a
page lands at a clean directory URL:

| On disk | Published at |
|---|---|
| `tasks/<slug>/index.html` | `https://0xchamin.github.io/mincha_brain/tasks/<slug>/` |

## What this folder is not

**It sits outside the evidence pipeline, deliberately.** A page here is **not** a source, produces
no nodes, is promoted to nothing, and appears in no index. It is not a fourth content layer beside
`sources/`, `foundations/` and `reports/` - those three are defined by their evidence status, and
this folder has none. Do not put anything here that makes a claim the brain should believe; if it
does, the thing to ingest is whatever it cites.

**Nothing here is rendered, rewritten or checked.** `build_site.py` runs no markdown conversion, no
citation rewriting and no mermaid pass over these files, and `validate.py` does not lint them. The
page is exactly what you wrote, which is the point: a bundled app has already resolved its own
assets and any "helpful" post-processing would corrupt it.

## The rules a page has to keep

- **Be self-contained.** Inline the CSS, the JS and the fonts. External CDN references break the
  offline story and add a runtime dependency the rest of the site does not have.
- **Own your whole folder.** Extra assets are fine next to the `index.html`; they are copied along
  with it.
- **Expect a fresh copy every build.** `site/` is deleted and rebuilt from scratch, so `site/tasks/`
  is disposable output. Edit the file here, never there.

## Why these pages are not precached

The service worker precaches every `.html` it emits so the brain reads offline on a phone. **Pages
under `tasks/` are excluded from that list**, for the same reason the 3.4MB mermaid bundle already
is: a bundled app with embedded fonts runs to megabytes, and precaching one would make every visitor
to the reader pay for it on cellular whether or not they ever open it.

They are still available offline, just lazily. The worker is network-first for documents and writes
each response into the shell cache, so a page works offline **after its first view** rather than
before it.
