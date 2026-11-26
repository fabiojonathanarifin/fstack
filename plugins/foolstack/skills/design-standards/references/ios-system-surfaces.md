# iOS system surfaces: Dynamic Island, status bar, tips, share

Rules learned shipping Protos (Nov 2026), written to be reused in any app.
Apple's source: HIG > Live Activities (expanded presentation, specifications).

## Surfaces that grow out of the Dynamic Island

An in-app banner may grow out of the island (Drops-style). If you do it, do it
the way iOS does its own expanded island, or it reads as broken:

- **Pure black, always.** The island is a black hardware cutout; any other color
  shows a seam where the cutout ends. Dark is not a style choice here.
- **Detect, don't list devices.** Island iPhones are the only ones with a top
  safe-area inset of 59pt or more (notch 44 to 50, older 20). Island geometry:
  126 x 37pt, 11pt from the top. Everything else gets a fallback: a dark pill
  just under the status bar.
- **Grow from the island's outline.** Scale from island width/height to full
  size, anchored at the top (`transformOrigin: "top"`), ~460ms ease-out. Text
  fades in only after ~55% of the grow, so it is never seen squashed.
- **Close back into it.** Reverse the open: content fades first, then the shape
  shrinks into the cutout, ~320ms ease-in. Keep the component mounted until
  the exit finishes (a `rendered` flag, not `if (!visible) return null`), and
  hold the last message, because stores usually clear it on hide. Vanishing on
  dismiss is the most common way this pattern looks cheap.
- **Lay it out like an expanded Live Activity:**
  - The row beside the camera carries content from the margin to the cutout
    (leading: icon plus a short bold label in the brand color; trailing: the
    close mark). Two lone icons hugging the camera with empty wings looks thin;
    content stranded in the far corners looks worse. HIG: "wrap content tightly
    around the TrueDepth camera".
  - The message goes below, leading-aligned with the icon, medium weight or
    heavier, 16pt or larger.
  - Margins are even and concentric: about 28pt sides, about 12pt top, about
    20pt bottom, with a corner radius of about 44 to follow the display's
    corners. Nothing pokes into the rounded corner or sits on the top rim.
- **Own the status bar row while open.** iOS always draws the status bar above
  app content, so the clock and battery show through an island card. Hide the
  status bar while it is up (fade) and restore it on close. That hides nothing
  for good, and it is what iOS does under its own expanded island.
  - React Native with `UIViewControllerBasedStatusBarAppearance = true` (the
    Expo default with react-native-screens): the imperative
    `setStatusBarHidden` / `<StatusBar hidden>` throws "RCTStatusBarManager
    requires ... set to NO". Drive it as a screen option instead, on the root
    stack: `statusBarHidden`, `statusBarAnimation: "fade"`.
- **Specs** (expanded): width 371pt on a 393pt screen, 408pt on 430pt; height
  84 to 160pt, using only the height the content needs.

## Teaching tips (coach marks)

- A tip that teaches a gesture should SHOW the gesture: nudge the content the
  way the gesture moves it (for example, the page slides ~8% left and back once,
  380ms out and 420ms back, about 1s after the tip appears). Words alone teach
  less than a felt motion.
- Drop "Tip:" from the copy when an icon (a lightbulb) already says it.
- A floating card mid-screen over reading content cuts a line of text in half
  and crowds the bottom controls. Prefer the island (above) or the top edge.
- Tips that belong to one screen must hide when the user leaves it. A reader
  tip showing on the dashboard is a bug.

## Sheets, share and modal sequencing

- iOS will not present a share sheet, alert or second modal while another modal
  is still dismissing; it drops it silently and the button "does nothing".
  Run the follow-up action from the sheet's dismissal-finished callback
  (`onDismiss` of the RN Modal / `onClosed`), never right after calling close,
  and never on a timer.

## Invite / share messages

- Link to the website, not a store listing: the sender does not know the
  friend's platform, and the site offers both stores.
- Keep one builder function for the message so every share button agrees.
- Do not name a reward length if tiers can differ (an advisor or partner code
  that pays more must never be advertised in-app).
