# LandingVerify — the verification layer that makes agents explain why

**Open Agent Hackathon 2026 · Track: The Agent That Can Explain Why**

## The problem
AI agents report "done" constantly — but the reader-side truth is often different: a page
returns 404, a published link is dead, a description was cut off mid-sentence, or the
content users actually see is empty. A success claim without evidence is indistinguishable
from a hallucination. In production agent networks this is the #1 failure mode:
**unverified success reporting**.

## What it does
LandingVerify fetches any published URL **the way a real reader would** and refuses to
let an agent declare success until the reader-side reality is proven:

- HTTP 200 **and real visible content** (not just status code)
- expected text actually present on the rendered page
- truncation detection (content cut at platform limits, e.g. 320-char task descriptions)
- up to 10 outbound links re-fetched: dead links are named, with their status codes
- verdicts in plain language: every FAIL says **why** it failed, with the exact evidence

The output is not "OK/ERROR" — it is an explanation: which check failed, what the
reader would have seen, and what to fix. That explanation is what makes an agent's
success claim checkable by anyone.

## Proven in production
LandingVerify v1.0 runs inside the Shimi Network (58 autonomous agents). Real catch on
Oct 24, 2026: it discovered that a published product page was missing its main visual
asset — before any human reader saw the broken page — and the delivery was held back
until fixed. It now guards every delivery the network publishes.

## Usage
```bash
python3 landing_verify.py https://example.com --expect "welcome text" --cut 320
```
JSON verdict with reasons. Exit output is agent-friendly: `PASS`, `WARN`,
or `FAIL: <explanation>`.

## Run tests
```bash
python3 test_landing_verify.py   # offline, no external network needed
```

## Why "The Agent That Can Explain Why"
Every verdict carries its evidence: status codes, measured content length, the exact
dead links, and the truncation window. An agent using LandingVerify can answer
"how do you know it worked?" with data instead of confidence.

## License
MIT — Shimi Network (Sun Raz-Levona), 2026.
