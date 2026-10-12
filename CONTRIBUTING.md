# Contributing

Thanks for helping improve ToolStack.

## Before opening a change

1. Keep the site deployable as a static website unless a backend change is explicitly documented.
2. Use semantic HTML, accessible labels, keyboard-friendly controls, and responsive layouts.
3. Keep tool calculations in the browser where practical and explain limitations in the UI.
4. Do not commit API keys, credentials, private data, generated build output, or unrelated files.
5. Avoid publishing thin or placeholder blog posts just to increase the page count.

## Local checks

Run the static-link checker from the repository root:

```powershell
python scripts/check_site.py
```

Manually open any changed tool page and test its primary workflow at desktop and mobile widths. If a change adds dependencies or build steps, document them in `README.md`.

## Pull requests

Describe the user-visible problem, the change made, and how it was tested. Include screenshots for significant UI changes and call out known limitations. Do not claim tests passed unless they were run.
