# The Handbook

![GitHub Tag](https://img.shields.io/github/v/tag/amirhnajafiz/handbook)
![GitHub top language](https://img.shields.io/github/languages/top/amirhnajafiz/handbook)

The Handbook is a web application I built to organize and store useful materials related to computer science and engineering.

As an engineer, I've explored a wide range of topics and worked with countless tools and technologies. However, when I face a technical challenge, I often find myself turning to ChatGPT or Stack Overflow to recall specific commands, configurations, or techniques I’ve used before.

The Handbook solves this problem by providing a unified, searchable interface where I can store and quickly access personal notes, code snippets, setup instructions, debugging tips, and other valuable resources. 

It's essentially a personalized knowledge base that helps me retain and retrieve important information more efficiently, boosting my productivity and reducing time spent re-learning or re-searching things I already encountered.

## Adding a page

Every page follows [`templates/page.md`](templates/page.md).

```sh
make new SECTION=linux TITLE="Systemd"   # creates docs/linux/NN_systemd.md and updates the sidebar
make check                               # validate filenames and template sections
make serve                               # preview at http://localhost:3000
```

Or use the **New page** workflow in the GitHub Actions tab, which opens a pull request with the generated page.

CI (`.github/workflows/ci.yml`) fails a pull request if a page does not match the template or if `docs/_sidebar.md` is stale. The deploy workflow validates and regenerates the sidebar before publishing.

## Contribution

Open pull requests and mention me (send an email if you didn't get any response within a week).
