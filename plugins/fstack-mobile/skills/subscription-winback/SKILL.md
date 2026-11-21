---
name: subscription-winback
description: Subscription cancellation intercept and win-back: survey, reason-conditional StoreKit promotional offer, honest savings anchoring, Apple handoff, when to burn the offer flag, Settings placement, and funnel analytics. Use when building or changing cancel/manage-subscription flows, retention offers, or the Settings account section.
---

# Cancellation and win-back

## Cancellation & Win-Back (Subscription Retention)

Ship a cancellation INTERCEPT on every subscription app, never a bare "cancel" link straight to the
system settings. This is RevenueCat's own default Customer Center retention flow, hand-built in the
app's brand language (custom UI clears the design bar; their prebuilt shell does not). After the
paywall it is the highest-leverage retention surface you have.

### The Apple constraint (why it's an intercept, not a button)
Apple forbids canceling an in-app subscription from inside the app; the real cancellation always
happens on the iOS system Subscriptions screen. So the flow can only (a) learn WHY, (b) make a save
offer redeemable in-app, and (c) hand off to Apple. Always keep a plain "Manage subscription" escape
hatch AND an always-present "keep it" bail-out at every step, or App Review 3.1.2 rejects it. Bailing
out is the BEST outcome (they didn't cancel), so make it first-class and easy, never buried.

### The flow (3 steps + a terminal win)
1. **Survey** - ONE optional question ("What's making you think about canceling?"), 4-6 one-tap reasons
   (Too expensive / Not using it enough / Missing a feature I need / Found something better / Just
   taking a break / Something else), plus a quiet Skip. Capture the reason even from the people the
   offer saves, so you learn why either way.
2. **Win-back offer** - a discounted-annual save offer, with framing CONDITIONAL on the reason (lead
   hard with the price for "too expensive", a generic "here's X off to stay" otherwise).
3. **Handoff** - honest copy that Apple handles the cancellation, the renewal date when known, a primary
   "Open subscription settings", a secondary "Never mind, keep [Premium]".
   Terminal **accepted** - a small celebratory confirmation; they stay subscribed at the new price.

### The offer is a real StoreKit Promotional Offer, NOT a separate public SKU
- Gated to existing/lapsed subscribers, so it CANNOT leak to free/new users. A separate cheap product
  is public on your store listing and cannibalizes full-price sales.
- ONE product, a first-term discount that REVERTS to full price after year one (protects margin +
  anti-gaming), redeemed in-app via `getPromotionalOffer` + `purchaseDiscountedPackage` (RevenueCat).
- Requires the In-App Purchase Key uploaded to RevenueCat so it can sign the offer (that key is also
  required for StoreKit 2 purchases to record at all).
- Separate/independent products are the right tool ONLY for A/B PRICE TESTING or a permanent
  (non-reverting) discount, a different goal. Note: the App Store listing's "In-App Purchases" section
  shows products, NOT offers, so a competitor's many SKUs are price tests, not proof they avoid promos.

### Pricing + the anchor (make the number big AND honest)
- Keep the discount MODERATE, not too deep: protect margin, and don't train happy annual subscribers to
  fake-cancel every renewal for half off. A meaningful ~25-40% off the standard annual is usually enough
  to move a fence-sitter; going deeper is usually margin given away, not saves bought.
- Anchor the savings % AND a STRIKETHROUGH on a YEAR OF THE APP'S SHORTEST RECURRING PLAN (monthly x12,
  or weekly x52 if that's the honest comparison the app sells), for EVERY subscriber regardless of their
  current plan. It's the same "vs paying monthly" framing the paywall already uses, it's honest, and it
  makes the number big. Anchor the % on the SAME figure you strike through so they AGREE
  (e.g. ~~$227.88~~ $69.99 = 69% off); anchoring the % on the annual while striking the monthly year
  makes the two contradict.
- NEVER hardcode a price. Read the discounted price, the reverting standard price, and the anchor LIVE
  from the store (localized), through a pure, unit-tested savings helper (annualize the anchor, round,
  positive-only).

### "Used up" only on a real decision
Burn the once-per-user "offer shown" flag ONLY when the user actually DECIDES (accepts, or explicitly
taps "continue to cancel"), NEVER on mere display or on canceling Apple's payment sheet, a mis-tap must
not cost them the deal. Dev builds always re-show so the flow stays testable. The flag is a per-user
device-local cache (wipe it on account switch).

### Top-tier 2026 UIUX (per Design & Motion Standards)
Full-screen, one thing per step, staggered entrances (timing + ease-out, never springs), press-scale on
every tap target, haptics mirroring each beat (select on a reason tap, success/celebrate on redeem). The
discounted price is the HERO: a small muted STRIKETHROUGH anchor above a large accent price, the
reverting price as fine print. Brand colors/type/scaling, no leaking backend fields.

### Settings placement (don't prime churn)
Keep manage/cancel/restore/sign-out OUT of the top of Settings; put them in a low-key "Account" section
at the BOTTOM, past everything. Seeing "Cancel subscription" every time Settings opens is a repeated
nudge toward churn (mere-exposure effect). The top keeps only POSITIVE prompts: identity + status,
"Upgrade" for free users, "Sign in" for logged-out.

### Analytics (if the app uses these tools)
Fire the full funnel to PostHog: `cancel_flow_opened`, the survey `cancel_reason` (one property per
reason, so you can slice save-rate by reason), `winback_offer_shown` / `_unavailable` / `_accepted` /
`_declined`, `cancel_handoff_appstore`. Report the win-back PAYMENT as revenue: to PostHog as the
accepted event carrying price + currency, and to the attribution/MMP tool (e.g. Singular) as a revenue
event for the iOS SKAN conversion value / ROAS, the same choke point normal purchases use. Survey and
funnel steps stay in PostHog only (they are not attribution signals). All copy obeys the Copywriting
Rules (no em/en dashes, no ellipses, no AI-isms).
