---
name: launch-assets
description: Produce and file every visual asset for a product launch or major release - in-app welcome/onboarding clips, App Store and Play screenshots and preview videos, device-framed clips for press and App Store feature nominations, and a shareable press/changelog page - then store them in the EchoForge central system. Use for mobile app releases (iPhone, iPad, iPhone Duo, Android) and web app launches. Triggers - "re-record the welcome video", "App Store screenshots", "preview video", "press kit", "feature nomination", "changelog for press", "launch assets", "marketing assets for the release".
---

# Launch assets

One release, one capture pass, many outputs. Plan the shots once, record each
flow once per device, and derive every deliverable from those masters.

## 1. Inventory before capturing

- List what the release shipped from the changelog, git log and the Notion
  project. Every headline feature needs at least one shot.
- Find what already exists and what it is used for: in-app clips (search the
  code for `.mp4` / asset hosts), current store screenshots (Notion task, ASC),
  older press pages. Make a contact sheet of each existing clip
  (`ffmpeg -i URL -vf "fps=1/3,scale=200:-1,tile=6x2" -frames:v 1 sheet.png`)
  and decide per asset: keep, extend, or re-record.
- One Notion task for the whole pass, linked to the product's changelog and
  outreach projects. Note blockers in it.

## 2. Devices and environment

- One dedicated simulator per form factor, created for the pass
  (`xcrun simctl create "<App> Capture iPhone" <devicetype> <runtime>`), so
  other sessions' apps and state cannot leak in.
- Form factors for iOS: iPhone 6.9" (17 Pro Max), iPad 13", and iPhone Duo
  when the app supports it. The Duo needs its own device-specific runtime
  (`iOS-<ver>-iPhone19-4`); if every Duo shows "runtime profile not found",
  re-download the platform (`xcodebuild -downloadPlatform iOS -buildVersion <ver>`)
  or Xcode > Settings > Components.
- Build with `npx expo run:ios --device <UDID> --port <free port>`. Do not
  start Metro separately and deep-link the dev client into it: a
  mismatched JS engine shows "Property 'MessageQueue' doesn't exist".
- Marketing status bar: `xcrun simctl status_bar <UDID> override --time "9:41"
  --dataNetwork wifi --wifiMode active --wifiBars 3 --cellularMode active
  --cellularBars 4 --batteryState charged --batteryLevel 100 --operatorName ""`.
  `--time` takes a short time string; ISO dates are rejected.
- Locale en_US, 12-hour time, light mode unless a dark shot is planned.
- One simulator at a time on a laptop: shut the previous one down before
  booting the next, and close each form factor's tasks before moving on.
- Pre-warm public content (e.g. today's devotional row) before sign-in so the
  first frame after sign-in is never an empty dark card.
- Account: a real account with Premium unlocked (dev override is fine) and
  believable content. Never record test junk like a note called "test".
  Signing in to production auth needs the human; ask once, early.

## 3. Storyboard each clip before recording

Per clip: device, length, beats in order, and where it is used. Rules:
- Open on the newest, most visual feature. The first 3 seconds sell it.
- One idea per beat, 2-4 s each, deliberate taps, no hunting.
- App Store previews: max 30 s, captured from the app, no device frames, no
  fake UI, per-device resolution.
- In-app welcome clips: new versioned key per recording
  (`welcome-<device>-v<N>.mp4`) because CDN copies are immutable for a year.

## 4. Record

`xcrun simctl io <UDID> recordVideo --codec h264 --force <file>.mov`, drive the
flow with the simulator tools, stop with SIGINT. Re-take rather than edit
around a stumble. Screenshots: `xcrun simctl io <UDID> screenshot <file>.png`
at the exact moment, same status bar.

## 5. Derive outputs (ffmpeg)

- **Simulator recordings are variable frame rate**: `recordVideo` writes a
  frame only when the screen changes, so a still screen has almost no frames
  and a `trim` over it comes out empty. Always run `fps=30` BEFORE `trim`
  (`[0:v]fps=30,split=N[s1]...;[s1]trim=a:b,setpts=PTS-STARTPTS[c1]...concat`).
- Pick cut points from a contact sheet: `fps=1/2,scale=150:-1,tile=13x4`
  (frame i = second 2i). Cut dead waits; one idea per 3-6 s.
- Store preview sizes that App Store Connect accepts: iPhone 6.9" 886x1920,
  iPad 13" 1200x1600, 30 fps, H.264 high, <=30 s, plus a silent AAC track
  (`-f lavfi -i anullsrc=r=44100:cl=stereo -shortest`).

- Welcome clips: trim, scale to the existing clip's width, H.264, `+faststart`,
  no audio.
- Store previews: trim to <=30 s at the store's required size.
- Press clips: composite into an iPhone, iPad or Duo frame so the device is
  obvious, plus a poster frame.

## 6. Press / changelog page

- Artifact pages block media from other hosts (CSP), so the clips and posters
  ship WITH the page (`files` + relative `src`), never as R2 URLs.
- Device frames are CSS around a `<video autoplay muted loop playsinline>`,
  shaped like the hardware (Dynamic Island pill for iPhone, flat bezel for iPad).

A private shareable page (Artifact): the release story, one section per
feature, each with its framed clip and two sentences of plain copy
(copywriting-rules). Lead with what a reader gains. Share only when the human
says so.

## 7. File centrally

- Bytes: R2 under `marketing/<product>/<version>/<kind>/<file>` (never
  Supabase Storage).
- Index: one `record_content` row per asset in echoforge-db on the MSI
  (kind video / store_asset / other, product slug, R2 key in the caption,
  tags like `<product>-<version>`, `launch-assets`), plus the Notion task.
- Upload with `wrangler r2 object put <bucket>/<key> --file <f> --remote`;
  in-app clips get `--cache-control "public, max-age=31536000, immutable"`.
- App changes (new clip keys in code) are committed; OTA publish is the
  human's call.

## Checklist

- [ ] Every shipped headline feature appears in at least one clip and one screenshot
- [ ] Every form factor the app supports has its own welcome clip
- [ ] Status bar 9:41 everywhere, no debug toasts or red boxes on screen
- [ ] Previews <=30 s and unframed; press clips framed
- [ ] Assets filed in R2 + indexed; Notion task updated with links
