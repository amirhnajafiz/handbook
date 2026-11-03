<div align="center">

<img src="public/bg.png" alt="The Handbook logo" width="220" />

# The Handbook

**A searchable personal knowledge base for computer science and engineering.**<br/>
Commands, configs, concepts, and war stories, written down once so I never have to re-learn them.

[![Site](https://img.shields.io/badge/read-the%20handbook-4caf50?style=for-the-badge)](https://amirhnajafiz.github.io/handbook/)

![GitHub Tag](https://img.shields.io/github/v/tag/amirhnajafiz/handbook?sort=semver&style=for-the-badge&color=2196f3)
![CI](https://img.shields.io/github/actions/workflow/status/amirhnajafiz/handbook/ci.yml?style=for-the-badge&label=CI&color=ff9800)
![Deploy](https://img.shields.io/github/actions/workflow/status/amirhnajafiz/handbook/static.yml?style=for-the-badge&label=Deploy&color=9c27b0)
![GitHub top language](https://img.shields.io/github/languages/top/amirhnajafiz/handbook?style=for-the-badge&color=e91e63)

</div>

## Why

When I hit a technical problem, I usually end up asking ChatGPT or searching Stack Overflow for something I have solved before: a command, a config, a technique. The Handbook is the fix. It is one place for my own notes, code snippets, setup steps, and debugging tips, built to be searched quickly and trusted.

## How it works

The site is plain Markdown rendered in the browser by [Docsify](https://docsify.js.org). There is no build step for the pages themselves: search, code copy buttons, syntax highlighting, KaTeX math, and Mermaid diagrams (write them as ` ```mermaid ` code blocks) all come from Docsify plugins loaded in [`index.html`](index.html).

```text
docs/
├── home.md                  landing page
├── _sidebar.md              generated, do not edit by hand
└── <section>/
    ├── index.md             section overview
    ├── 01_topic.md          pages, numbered in reading order
    └── <subsection>/        optional, e.g. storage_systems/ceph
scripts/                     page tooling (Python 3, standard library only)
templates/page.md            the template every page follows
```

## Run it locally

```sh
make serve        # then open http://localhost:3000
```

Or with Docker (Nginx):

```sh
docker build -f build/Dockerfile -t handbook .
docker run --rm -p 8080:80 handbook
```

## Writing a page

Every page follows [`templates/page.md`](templates/page.md): a title, an optional dedication, then **Quick Description**, **Installation**, **Useful Tips/Commands**, **Examples**, and **References**, in that order. A section with nothing to say can stay empty.

```sh
make new SECTION=linux TITLE="Systemd"                        # docs/linux/07_systemd.md
make new SECTION=storage_systems/minio TITLE="Getting Started"  # creates the sub-section too
make check                                                    # validate names and structure
```

`make new` numbers the page, fills in the template, and regenerates the sidebar. You can also run the **New page** workflow from the GitHub Actions tab, which opens a pull request with the generated page.

Page conventions:

- Filenames look like `01_snake_case.md`. A dedication, when present, is followed by a `---` line.
- Cite real sources, and check that each link loads.
- Say each thing once. Link to the page that owns a topic instead of repeating it.
- Keep secrets out: use placeholders such as `<token>`, never real credentials or hostnames.

## CI and deployment

| Workflow | Trigger | What it does |
| --- | --- | --- |
| [`ci.yml`](.github/workflows/ci.yml) | pull request, push to `main` | Fails if a page breaks the template or if `docs/_sidebar.md` is stale |
| [`new-page.yml`](.github/workflows/new-page.yml) | manual | Creates a page from the template and opens a pull request |
| [`static.yml`](.github/workflows/static.yml) | new tag, manual | Validates, regenerates the sidebar, and deploys to GitHub Pages |

To publish, merge to `main` and push a tag.

## Contributing

Pull requests are welcome, whether for a typo, a wrong command, or a whole new page. Run `make check` first, then open a PR and mention me. If I haven't replied within a week, [send me an email](docs/home.md).

---

<div align="center">
<sub>Written by <a href="https://github.com/amirhnajafiz">Amir Zadeh</a>, since Fall 2024.</sub>
</div>
