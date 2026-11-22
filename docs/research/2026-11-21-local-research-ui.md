# Minimal local research UI

Date: 2026-11-21 (America/New_York).

## Implemented

A chat-style evidence-search page now wraps existing local retrieval. It includes a question box with Enter/Shift+Enter behavior, four example prompts, an in-tab question/result thread and recent-search shortcuts. New search clears the thread and cancels in-flight work; refresh clears all tab history. Nothing is persisted as a conversation, and earlier questions do not influence subsequent searches.

Search returns up to five original anchor passages with title, edition, source ID, PDF page and reviewed printed label when available. Complete verified page context is expandable. Mission/evidence/review notes and provenance IDs remain accessible. Local original-PDF links use the PDF page fragment. Search options expose source scope and ranking; `page` remains the default, with experimental `context` opt-in. Empty matches and failures are displayed explicitly, without claiming automatic absence of evidence or sufficient support.

There are no generated answers, external model calls, uploads, internet research, voice, document acquisition or new runtime dependencies. All five existing indexes and nine original PDF hashes remain unchanged. The current ranking and source-review limitations still apply; the UI does not improve them.

## Run

From the project root:

```sh
.venv/bin/mars-rag serve
```

Open http://127.0.0.1:8765. Stop with Ctrl+C. An occupied port can be changed with `--port 8766`. No frontend build is required; assets are included in the Python package.

## Design and boundaries

The interface uses a charcoal palette, a restrained Mars-colored accent, a clear question composer and readable source cards. Long page context and technical provenance stay behind disclosures. Narrow-screen layout rules collapse the sidebar and keep the composer separate from a scrollable conversation.

The standard-library server binds only to 127.0.0.1. It serves three fixed frontend assets and a source-ID-based PDF route, not arbitrary project paths. Registered PDFs must resolve within the raw collection and match their registered hashes. JSON search requests have body/question bounds and source/ranking validation. Host/origin checks restrict requests to the local application origins; no CORS is enabled. The content security policy permits local scripts/styles and inline image data only. Source/query strings enter the DOM as text. Queries are not written to application logs or browser storage. This is a local, single-user MVP, not a remotely deployable/authenticated service.

Implementation: [server](../../src/mars_rag/web.py), [HTML](../../src/mars_rag/web_static/index.html), [CSS](../../src/mars_rag/web_static/app.css), [JavaScript](../../src/mars_rag/web_static/app.js), [HTTP tests](../../tests/test_web.py).

## Verification

- All 27 software tests pass on Python 3.11. Five new synthetic-source HTTP tests cover routes, metadata, actual search/context/provenance, no-match/input errors, origin/host boundaries, PDF hash/path checks and broken-index errors. Earlier extraction/ranking tests remain intact.
- JavaScript syntax and Python compilation pass. Python 3.9 syntax compatibility was checked; remote CI/runtime on Python 3.9 was not run here.
- Built a wheel without downloading dependencies and verified it contains all three frontend assets.
- Browser search for food/water recycling returned five passages, with the life-support paper's PDF page 6 first. Complete page expansion displayed that page; the original-PDF route was verified in HTTP tests.
- Browser source filtering returned only the selected life-support source. Experimental ranking selection worked. An unmatched query displayed the qualified no-match message. A simulated 503 restored the question and re-enabled Search. HTML-like query text remained literal text, with no injected image element.
- A fixed-composer overlap and sidebar-history overflow were found during visual review and corrected. Browser geometry confirmed that the conversation ends at the composer's top and horizontal content does not overflow in the embedded viewport.
- Integrated-browser viewport resizing was overridden/reset by the preview environment; apparent small screenshots were crops, not reliable mobile-layout validation. Narrow-screen CSS is implemented, but a physical phone or reliable device-emulation check remains outstanding. Native computer-use inspection was unavailable; the integrated browser and Playwright checks supplied the working QA path.
- A CSP conflict with local data-image decorations was found and fixed. The observed 503 browser-console entry was the intentionally injected retry test.

Preview processes used for testing are stopped after verification. Temporary screenshots and wheel artifacts are removed. No push, publication, hosted Site or external provider was configured. The Sites skill's local-only workflow was used.

## Next useful review

Run the app and try the outbound-journey and everyday-transit questions. Review whether the cited passages and page expansion are understandable. The next product increment would require model/provider and document-transfer decisions before implementing generated answers. Retrieval relevance, concept boundaries and evidence sufficiency still need separate evaluation.
