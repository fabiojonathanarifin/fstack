---
name: copywriting-rules
description: User-facing copy rules: no em dashes, en dashes, or ellipses, a blacklist of AI phrases, plain concrete voice, regulated-category tone, and a pre-ship self-check. Use when writing or editing any onboarding, paywall, marketing, error, button, notification, or store copy.
---

# Copywriting rules

## Copywriting Rules

**These rules are NON-NEGOTIABLE for any user-facing copy.** Code comments are exempt; onboarding copy, paywall copy, marketing copy, error messages, headlines, button labels, push notifications, App Store descriptions, and anything a user reads must obey.

### Punctuation: zero tolerance

- **Never use em dashes (—)** in user-facing copy. They are the #1 tell that copy was written or edited by an AI. Use a period, comma, colon, or restructure the sentence.
- **Never use en dashes (–)** as substitutes. Even for numeric ranges, use a regular hyphen (`-`) or the word "to" (e.g., `2.5 to 15 mg`, not `2.5–15 mg`).
- **Never use ellipses (…)** for trailing-off effects in copy. Use a period.
- Use straight quotes (`"`, `'`) not smart/curly quotes unless the design system explicitly requires them.

### AI-ism blacklist — do not ship copy that uses these

Single biggest cause of copy that "feels off." If you've written any of these, rewrite:

- "Let's figure it out together"
- "We're here for you"
- "You're not alone"
- "Embark on your journey"
- "Your wellness journey"
- "Unlock the power of..."
- "Discover the..."
- "Introducing..."
- "Effortlessly..."
- "Seamlessly..."
- "Take control of..."
- "Elevate your..."
- "Empower yourself"
- "Cutting-edge"
- "Game-changer"
- "Revolutionize"
- "World-class"
- "Best-in-class"
- "Comprehensive"
- "Robust" (in user-facing copy)
- "Holistic"
- "End-to-end"
- "Synergy"
- "Trust the process"
- "We've got this"
- "Experience the..."
- "Optimize your..."
- "Harness the power of..."

If a sentence works without these words, the rewrite is the answer.

### Voice and structure

- Write like a human texting a friend who happens to be smart. Short sentences. Direct. No filler.
- Lead with what the user GETS, not what the product DOES.
- Cut every unnecessary adjective. "Powerful" / "intuitive" / "amazing" / "seamless" all signal weak copy.
- Concrete > abstract. "Your dose math takes 30 seconds" beats "Streamlined dose calculations."
- One thought per sentence. Two short sentences beat one long one.
- Plain words. "Use", not "utilize" or "leverage". No abstract metaphor nouns (surface, layer, flywheel, north star, paradigm, vector): name the concrete thing.
- Say what it does, not how it feels. Name the mechanism or the number. Cut any sentence that could appear unchanged in another product's copy.
- The rhythm test: read it out loud. If you stumble, rewrite.

### Tone for medical / regulated categories

- Never overclaim outcomes ("lose weight fast," "guaranteed results"). Regulators care, and users see through it.
- Acknowledge the legal/medical context where relevant ("Not medical advice. Informational only.").
- Don't pretend authority you don't have ("clinically proven" requires actual clinical trials).

### Humanize every long-form piece (changelogs, blog posts, release notes, LinkedIn posts)

Any copy longer than a few sentences gets a humanize pass before it ships: run the `humanizer`
skill on the draft, then re-read it out loud. The bar is clear and simple, never verbose.
- Say what changed and what the reader gets, in the words they'd use. "Long notes scroll
  properly now" beats "We've improved the note-taking experience."
- Plain words over clever ones. If a 12-year-old couldn't follow the sentence, rewrite it.
- Cut filler openers ("We're excited to share...", "In this update..."). Start with the thing.
- Short paragraphs, short sentences, no stacked adjectives, no rule-of-three padding.
- Concrete over abstract: name the feature, the screen, the number.
- Where a repo can enforce it (e.g. a content test that fails on dashes and blacklisted phrases),
  enforce it in code, not just in review.

### Self-check before shipping

Before any user-facing string goes live, ask:
1. Does this contain an em-dash, en-dash, or ellipsis? → fix
2. Does this contain any phrase from the AI-ism blacklist? → rewrite
3. If I read this out loud to a friend, does it sound natural? → if no, rewrite
4. Could I cut any word and the meaning survive? → cut it

Copy violations are a ship-blocker, not a polish item.
