# Shneiderman's eight golden rules: implementation checklist

| Rule | Implementation | Check |
|---|---|---|
| Consistency | Same feedback structure and text labels in all modes | Compare two cards |
| Shortcuts | Quick replies, Enter to send, source-only shortcut, Tab navigation | Keyboard test |
| Informative feedback | Busy status, local/live mode, source, uncertainty, rating receipt | Demo ok/error paths |
| Closure | I'm done summary, human next step, Clear chat | End a session |
| Error prevention/recovery | Length checks, no essay generation, strict validator, retry | Automated tests |
| Reversal | Edit last message, previous hint, clear chat; draft is never changed | Try hint 3 then previous |
| User control | Style/focus selectors, manual hint levels, human button | Change APA to MLA |
| Memory load | Rule and source stay attached to cards; one hint at a time | Inspect card history |

Text labels carry meaning independently of color. High-contrast text, visible focus outlines, labelled form inputs, semantic landmarks, a skip link, native buttons, native dialog focus, and role=log with polite updates support keyboard and screen-reader use. No formal WCAG conformance audit is claimed. Test with actual users and assistive technologies.
