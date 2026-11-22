---
name: expo-react-native
description: Expo and React Native rules: OTA updates (expo-updates, fingerprint runtime), RevenueCat entitlement-ID gotcha, iOS multiline TextInput scroll-jump fix, native Apple/Google/email auth with Supabase, centralized colors/typography and scaling utils, Reanimated motion stack, and the bottom-sheet pattern. Use whenever building or changing an Expo / React Native app.
---

# Expo and React Native

## Expo and React Native

### Follow Native Conventions
- **Expo**: Use `app/` directory structure, follow Expo Router patterns
- **Expo OTA updates are a MUST — set up `expo-updates` / EAS Update on every Expo app.** A
  build can only receive over-the-air JS/asset updates if `expo-updates` was compiled into it,
  so it must be wired BEFORE the first TestFlight/App Store build (a shipped build without it
  can never be OTA-updated). Use `runtimeVersion: { "policy": "fingerprint" }` (not
  `appVersion`) especially for native-heavy apps, so an update only lands on a matching native
  runtime. Configure with `eas init` → `eas update:configure` → `eas build:configure`. Remember
  OTA pushes JS + assets only; any native change needs a fresh build.
- **Supabase**: Use RLS policies, follow auth patterns, use realtime subscriptions properly
- **RevenueCat**: Follow their webhook patterns and subscription status checking
  - **Entitlement-identifier gotcha (cost a full debug session once):** `customerInfo.entitlements.active` is keyed by the RevenueCat **entitlement identifier**, NOT the App Store product ID. The string the code checks must match the dashboard identifier exactly (case-sensitive), and that identifier is **immutable** after creation (only its Display Name is editable). A mismatch makes every purchase succeed while access checks return false forever — paying users read as "inactive" and hit free-tier gates. Keep the identifier in ONE named constant, and verify it against the live dashboard (Product catalog → Entitlements) before any build that touches purchases. Never gate post-purchase navigation on the freshly-returned `customerInfo` either — entitlements can lag the StoreKit transaction on device; always advance after a non-throwing `purchasePackage`, and read access live afterward.
- **React Native**: Follow their lifecycle patterns, use hooks properly
  - **Multiline-TextInput scroll-jump gotcha (cost a long debug session):** an auto-growing `multiline` TextInput with `scrollEnabled={false}` inside a ScrollView / KeyboardAwareScrollView has a long-standing iOS bug (RN #49226 / #48412, still UNFIXED on the new architecture as of late 2025): when you type at the **end** of the text and it wraps to a new line, iOS yanks the outer scroll up to the TOP of that input, then snaps back on the next keystroke. It only shows on the bottom-most/last line. The cure is to let the input own its own caret-scroll: set **`scrollEnabled={true}`** AND drive an explicit `height` from `onContentSizeChange` (height === content height, so it never actually scrolls internally and still looks auto-grown). This keeps any block/card layout intact, so you do NOT need to rewrite to a single TextInput or a WebView editor (e.g. @10play/tentap) just to beat this jump. Read `e.nativeEvent.contentSize.height` **synchronously** into a local inside the handler, never inside the `setState` updater, or event pooling nulls it out (`Cannot read property 'contentSize' of null`). Note: bumping `react-native-keyboard-controller` fixes the keyboard-avoidance / caret-visibility cases but does NOT fix this specific overflow jump on new arch; the `scrollEnabled` + managed-height combo is what fixes it.

### Don't Fight The Tools
```javascript
// ✅ Good - follow Expo's asset pattern
import logo from '../assets/logo.png';

// ❌ Bad - trying to customize against framework conventions
const logo = require('../../custom-assets/branding/logo.png');
```
## Authentication Pattern (Expo + Supabase)

When building auth for any Expo React Native app with Supabase, always use this pattern:

### Apple Sign-In
- Use `expo-apple-authentication` native module on iOS
- Exchange the identity token directly: `supabase.auth.signInWithIdToken({ provider: 'apple', token: credential.identityToken })`
- No redirect URLs needed — fully native, no browser popup

### Google Sign-In
- Use `@react-native-google-signin/google-signin` (native SDK, NOT browser-based OAuth)
- Configure once: `GoogleSignin.configure({ webClientId, iosClientId })`
- Sign in: `await GoogleSignin.signIn()` → extract `idToken` → `supabase.auth.signInWithIdToken({ provider: 'google', token: idToken })`
- No redirect URLs needed — no browser popup, instant native sheet
- Required env vars: `EXPO_PUBLIC_GOOGLE_WEB_CLIENT_ID`, `EXPO_PUBLIC_GOOGLE_IOS_CLIENT_ID`

### Email Sign-In/Up
- Use `supabase.auth.signInWithPassword()` and `supabase.auth.signUp()`
- Always validate: non-empty email, password min 6 chars
- Handle email confirmation case: `data.user` exists but `data.session` is null

### Never use these patterns:
- ❌ `supabase.auth.signInWithOAuth` + `WebBrowser.openAuthSessionAsync` — browser-based, needs redirect URLs, worse UX
- ❌ `expo-auth-session` for Google/Apple — unnecessary complexity
- ❌ Redirect URLs in Supabase for mobile OAuth — only needed for web apps

### Post-auth flow (always do all 3):
```js
setSession(data.session, user, onboardingCompleted);
hydrateFromAuth(user);
useLibraryStore.getState().syncLibraryFromDB();
```

## UI Constants — Centralized, Always

All colors, typography, and sizing must live in centralized constant files. Never hardcode these inline.

### Colors — single source of truth
- All color values in `constants/colors.js` (or `colors.ts`)
- Consumed via a `useTheme()` hook that returns the active palette (supports dark/light mode)
- Never use raw hex strings in components — always reference `colors.accent`, `colors.background`, etc.
```js
// ✅ Good
const { colors } = useTheme();
<View style={{ backgroundColor: colors.surface }} />

// ❌ Bad
<View style={{ backgroundColor: '#141416' }} />
```

### Typography — single source of truth
- All text styles in `constants/typography.js` as named presets: `h1`, `h2`, `h3`, `body`, `bodyBold`, `caption`, `small`
- Spread into component styles, then override only `fontSize` via scaling
```js
// ✅ Good
import Typography from '@/constants/typography';
label: { ...Typography.body, fontSize: moderateScale(16) }

// ❌ Bad
label: { fontFamily: 'Merriweather', fontSize: 16, fontWeight: '400' }
```

### Responsive Scaling (Mobile) — always use scaling utils
- All numeric sizes must go through scaling utilities — no raw px values for sizing
- Create `utils/scaling.js` in every React Native project with these three functions:
```js
import { Dimensions } from 'react-native';
const { width, height } = Dimensions.get('window');
const BASE_WIDTH = 390;   // iPhone 14 base
const BASE_HEIGHT = 844;

export const horizontalScale = (size) => (width / BASE_WIDTH) * size;
export const verticalScale = (size) => (height / BASE_HEIGHT) * size;
export const moderateScale = (size, factor = 0.5) =>
  size + (horizontalScale(size) - size) * factor;
```
- **Rule of thumb:**
  - Fonts, icon sizes, border radii → `moderateScale`
  - Widths, horizontal padding/margin → `horizontalScale`
  - Heights, vertical padding/margin → `verticalScale`
  - Hairline borders (0.5–1px) → raw value OK
```js
// ✅ Good
import { horizontalScale, verticalScale, moderateScale } from '@/utils/scaling';
fontSize: moderateScale(16),
paddingHorizontal: horizontalScale(24),
paddingVertical: verticalScale(12),

// ❌ Bad
fontSize: 16,
paddingHorizontal: 24,
```
### Motion Stack (React Native)
- **Reanimated** for all animations — `FadeInUp`, `FadeIn`, `withTiming`, `withDelay`, `useAnimatedStyle`, `useAnimatedProps`
- **Stagger pattern**: `FadeInUp.duration(400).delay(200 + i * 80)` — base delay + per-item offset
- **SVG draw-in**: `strokeDashoffset` animated from `CIRCUMFERENCE` to `CIRCUMFERENCE * (1 - fraction)` with `withDelay` so the card settles before the ring draws
- Never use the old RN `Animated` API
- **NEVER use spring animations** — no `withSpring`, no `.springify()`, no spring-based entering/exiting. Always use `withTiming` with explicit duration and easing instead. Springs feel bouncy and uncontrolled.
```js
// ✅ Good — explicit timing
withTiming(1, { duration: 300, easing: Easing.out(Easing.cubic) })
FadeInDown.duration(400).easing(Easing.out(Easing.cubic))

// ❌ Bad — springy, bouncy, unpredictable
withSpring(1, { damping: 15 })
FadeInDown.springify().damping(18)
```

### Bottom Sheets — Panel Slides Up, Backdrop Only Fades
Every bottom sheet, action sheet, and picker sheet must animate as TWO independent layers: the **sheet panel slides up** from the bottom edge, while the **backdrop (dim scrim) only fades in** behind it. The backdrop must NEVER slide up with the panel. This is the premium-app standard (Apple sheets, Linear, things, etc.); the heavy/stock feel comes from moving the scrim and the panel together as one block.

- **The trap with React Native `Modal`**: `animationType` moves the entire modal as one unit. `"slide"` drags the backdrop up with the panel (wrong, stock feel); `"fade"` kills the slide so the panel doesn't rise (also wrong). Neither animates the two layers independently. So do NOT rely on `Modal`'s `animationType` for sheets.
- **The fix**: render the `Modal` with `animationType="none"` and drive both layers with Reanimated `withTiming` (no springs, per the motion rules):
  - backdrop: `opacity` 0 → 1 (ease-out in, ease-in out), `~300ms`
  - panel: `translateY` measuredHeight → 0 (slides up), same timing
  - Keep the `Modal` mounted through the close animation (an internal `mounted` flag cleared in the `withTiming` finish callback) so the slide-down actually plays before unmount.
- **Build it once**: ship a single reusable `BottomSheet` shell component (owns the Modal, the fading backdrop, the sliding panel, the grabber, safe-area padding, the radius) and compose EVERY sheet from it. One implementation means the behavior is identical everywhere by construction, and a new sheet is just children. Do not re-implement the animation per sheet.
- **Keyboard-avoiding sheets extend their background behind the keyboard (iOS 26 rounded-corner fix).** A sheet that rises above the keyboard (a text input inside it) drives its lift with a `KeyboardAvoidingView` `behavior: 'padding'`. iOS 26 keyboards have ROUNDED top corners, so a panel whose flat opaque bottom stops exactly at the keyboard top leaks the dimmed backdrop through the two corner slivers. The fix is to extend the panel's OWN background down behind the keyboard, WITHOUT moving the content: on the panel, set `marginBottom: -tuck` (lets the border box run `tuck` px past the keyboard top so its bg fills the corners) AND add the same `tuck` to `paddingBottom` (so the input/controls stay exactly where they were). Put it ONCE in the shell, gated on `avoidKeyboard && Platform.OS === 'ios'` (no-op on Android and on older flat-topped keyboards), so every keyboard-avoiding sheet inherits it. `tuck ~= verticalScale(32)` is a tuned constant that just needs to exceed the keyboard's corner radius; the extra bg hangs harmlessly off-screen when the keyboard is down. **Do NOT do this with a negative `keyboardVerticalOffset`** (the first instinct): that moves the WHOLE panel down, so any sheet with controls near its bottom edge (an add-todo's date/priority/mic row) ends up jammed against the keys. The margin/padding pair fills the corners while keeping the original comfortable gap.
- **Prefer RNGH's `ScrollView` for a scrollable inside a sheet.** A sheet lives in its own per-Modal `GestureHandlerRootView` alongside the grabber's `Gesture.Pan()`. A scrollable in the panel must be the `ScrollView` from `react-native-gesture-handler` (not React Native's) so its drags negotiate in the same gesture arena; the plain RN one sits outside it and a long list's swipe gets intermittently swallowed. This is the current, documented RNGH pattern (not the legacy `Gesture.Native()` + `blocksExternalGesture` route, which is only for OVERLAPPING gestures).
- This is a global rule: every sheet that sits at `justifyContent: 'flex-end'` follows it. Full-screen pushed routes (navigation transitions) and centered alert/dialog modals are exempt — this rule is specifically the bottom-sheet pattern.
