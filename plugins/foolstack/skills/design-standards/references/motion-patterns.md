# Micro-Interaction Pattern Library

Ready-to-use code for React Native (Reanimated + expo-haptics) and Web (Tailwind/CSS/Framer Motion).

> **React Native note:** All patterns use `Pressable` (the current standard). `TouchableOpacity`, `TouchableHighlight`, and `TouchableWithoutFeedback` are legacy components. If you encounter them in existing code, migrate to `Pressable` with `onPressIn`/`onPressOut` for press feedback and `style` function for pressed state styling.

## Table of Contents
1. [Button Press](#button-press)
2. [Card Tap](#card-tap)
3. [Toggle / Chip Select](#toggle--chip-select)
4. [List Stagger Entrance](#list-stagger-entrance)
5. [Modal / Bottom Sheet](#modal--bottom-sheet)
6. [Like / Heart Animation](#like--heart-animation)
7. [Progress Ring Fill](#progress-ring-fill)
8. [Counter Increment](#counter-increment)
9. [Milestone Celebration](#milestone-celebration)
10. [Pull to Refresh Haptic](#pull-to-refresh-haptic)
11. [Swipe Action](#swipe-action)
12. [Skeleton Loading](#skeleton-loading)
13. [Notification Toast](#notification-toast)
14. [Tab Switch](#tab-switch)
15. [Haptic Escalation Sequence](#haptic-escalation-sequence)

---

## Button Press

The most common interaction. Must feel instant and physical.

### React Native
```jsx
import Animated, {
  useSharedValue,
  useAnimatedStyle,
  withTiming,
  withSequence,
  Easing,
} from 'react-native-reanimated';
import * as Haptics from 'expo-haptics';

const AnimatedPressable = Animated.createAnimatedComponent(Pressable);

function Button({ onPress, children }) {
  const scale = useSharedValue(1);
  const animatedStyle = useAnimatedStyle(() => ({
    transform: [{ scale: scale.value }],
  }));

  const handlePress = () => {
    scale.value = withSequence(
      withTiming(0.93, { duration: 60, easing: Easing.out(Easing.cubic) }),
      withTiming(1, { duration: 180, easing: Easing.out(Easing.cubic) })
    );
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium);
    onPress();
  };

  return (
    <AnimatedPressable style={animatedStyle} onPress={handlePress}>
      {children}
    </AnimatedPressable>
  );
}
```

### Web (CSS)
```css
.button {
  transition: transform 180ms cubic-bezier(0.33, 1, 0.68, 1);
}
.button:active {
  transform: scale(0.93);
  transition-duration: 60ms;
}
```

---

## Card Tap

Lighter than a button. The card dips slightly to acknowledge the touch.

### React Native
```jsx
function TappableCard({ onPress, children }) {
  const scale = useSharedValue(1);
  const opacity = useSharedValue(1);

  const animatedStyle = useAnimatedStyle(() => ({
    transform: [{ scale: scale.value }],
    opacity: opacity.value,
  }));

  const handlePressIn = () => {
    scale.value = withTiming(0.98, { duration: 80, easing: Easing.out(Easing.cubic) });
    opacity.value = withTiming(0.85, { duration: 80 });
  };

  const handlePressOut = () => {
    scale.value = withTiming(1, { duration: 200, easing: Easing.out(Easing.cubic) });
    opacity.value = withTiming(1, { duration: 200 });
  };

  return (
    <AnimatedPressable
      style={animatedStyle}
      onPressIn={handlePressIn}
      onPressOut={handlePressOut}
      onPress={() => {
        Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
        onPress();
      }}
    >
      {children}
    </AnimatedPressable>
  );
}
```

---

## Toggle / Chip Select

Instant color transition + selection haptic. The key is zero delay between tap and visual change.

### React Native
```jsx
function SelectionChip({ label, isActive, onPress }) {
  const handlePress = () => {
    Haptics.selectionAsync();
    onPress();
  };

  return (
    <Pressable
      style={[
        styles.chip,
        isActive && { borderColor: colors.accent, backgroundColor: colors.accentDim },
      ]}
      onPress={handlePress}
    >
      <Text style={[styles.chipText, isActive && { color: colors.accent }]}>
        {label}
      </Text>
    </Pressable>
  );
}
```

---

## List Stagger Entrance

Elements enter sequentially, guiding the eye top-to-bottom. The first item appears fast, each subsequent item has a slight delay.

### React Native
```jsx
import Animated, { FadeInUp, Easing } from 'react-native-reanimated';

function StaggeredList({ items }) {
  return items.map((item, i) => (
    <Animated.View
      key={item.id}
      entering={
        FadeInUp
          .duration(350)
          .delay(200 + i * 80)
          .easing(Easing.out(Easing.cubic))
      }
    >
      <ListItem item={item} />
    </Animated.View>
  ));
}
```

**Rules:**
- Base delay: 200ms (let the screen settle)
- Per-item: 60-100ms
- Cap at ~8 items animated (rest appear instantly)
- Duration: 300-400ms per item

---

## Like / Heart Animation

The heart pops bigger than its resting size, then settles. Creates a satisfying "burst" feeling.

### React Native
```jsx
function LikeButton({ isLiked, onToggle }) {
  const scale = useSharedValue(1);

  const animatedStyle = useAnimatedStyle(() => ({
    transform: [{ scale: scale.value }],
  }));

  const handlePress = () => {
    if (!isLiked) {
      // Like: pop effect
      scale.value = withSequence(
        withTiming(1.35, { duration: 100, easing: Easing.out(Easing.cubic) }),
        withTiming(0.9, { duration: 80 }),
        withTiming(1, { duration: 150, easing: Easing.out(Easing.cubic) })
      );
      Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium);
    } else {
      // Unlike: subtle shrink
      scale.value = withSequence(
        withTiming(0.8, { duration: 80 }),
        withTiming(1, { duration: 150 })
      );
      Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
    }
    onToggle();
  };

  return (
    <AnimatedPressable style={animatedStyle} onPress={handlePress}>
      <Heart
        size={24}
        color={isLiked ? colors.accent : colors.textTertiary}
        fill={isLiked ? colors.accent : 'none'}
      />
    </AnimatedPressable>
  );
}
```

---

## Progress Ring Fill

The ring draws in after the container settles. The delay is key: it creates a "reveal" moment.

### React Native
```jsx
// Animate strokeDashoffset from CIRCUMFERENCE to target
const progress = useSharedValue(0);

useEffect(() => {
  // Delay ring draw until card/container has entered (300ms)
  progress.value = withDelay(
    300,
    withTiming(fraction, { duration: 700, easing: Easing.out(Easing.cubic) })
  );
}, [fraction]);

const animatedProps = useAnimatedProps(() => ({
  strokeDashoffset: CIRCUMFERENCE * (1 - progress.value),
}));
```

---

## Counter Increment

Numbers don't just change — they count up. Creates a feeling of accumulation.

### React Native
```jsx
function AnimatedCounter({ value }) {
  const displayed = useSharedValue(0);

  useEffect(() => {
    displayed.value = withTiming(value, {
      duration: 600,
      easing: Easing.out(Easing.cubic),
    });
  }, [value]);

  const animatedProps = useAnimatedProps(() => ({
    text: Math.round(displayed.value).toString(),
  }));

  return <AnimatedText animatedProps={animatedProps} />;
}
```

---

## Milestone Celebration

Escalating sequence: the achievement builds up, peaks, and settles. Three-beat rhythm.

### React Native
```jsx
function MilestonePop({ children }) {
  const scale = useSharedValue(0);
  const opacity = useSharedValue(0);

  useEffect(() => {
    // Beat 1: Appear (200ms)
    opacity.value = withTiming(1, { duration: 200 });
    scale.value = withSequence(
      // Beat 2: Overshoot (250ms)
      withTiming(1.2, { duration: 250, easing: Easing.out(Easing.cubic) }),
      // Beat 3: Settle (200ms)
      withTiming(1, { duration: 200, easing: Easing.out(Easing.cubic) })
    );

    // Haptic escalation
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
    setTimeout(() => Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium), 150);
    setTimeout(() => Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success), 350);
  }, []);

  const animatedStyle = useAnimatedStyle(() => ({
    transform: [{ scale: scale.value }],
    opacity: opacity.value,
  }));

  return <Animated.View style={animatedStyle}>{children}</Animated.View>;
}
```

---

## Haptic Escalation Sequence

For progressive experiences (checklist filling up, streak growing, goal approaching).

### React Native
```jsx
// As items complete in sequence, escalate haptic weight
function escalateHaptic(completedCount, totalCount) {
  const ratio = completedCount / totalCount;

  if (ratio >= 1) {
    // Complete! Full celebration
    Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
  } else if (ratio >= 0.75) {
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Heavy);
  } else if (ratio >= 0.5) {
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium);
  } else {
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
  }
}
```

---

## Skeleton Loading

Instead of a spinner, show the shape of the content with a shimmer. Feels faster even though the load time is the same.

### React Native
```jsx
function SkeletonBlock({ width, height }) {
  const shimmer = useSharedValue(0);

  useEffect(() => {
    shimmer.value = withRepeat(
      withTiming(1, { duration: 1200, easing: Easing.inOut(Easing.ease) }),
      -1,
      true
    );
  }, []);

  const animatedStyle = useAnimatedStyle(() => ({
    opacity: 0.3 + shimmer.value * 0.3, // pulses between 0.3 and 0.6
  }));

  return (
    <Animated.View
      style={[
        { width, height, borderRadius: 8, backgroundColor: colors.card },
        animatedStyle,
      ]}
    />
  );
}
```

---

## Notification Toast

Slides in from top, auto-dismisses. The entrance is fast (attention-grabbing), the exit is gentle (non-disruptive).

### React Native
```jsx
// Enter: slide down from -100, ease-out, 300ms
entering={SlideInUp.duration(300).easing(Easing.out(Easing.cubic))}

// Exit: slide up to -100, ease-in, 250ms (faster exit)
exiting={SlideOutUp.duration(250).easing(Easing.in(Easing.cubic))}

// Auto-dismiss after 3 seconds
useEffect(() => {
  const timer = setTimeout(() => setVisible(false), 3000);
  return () => clearTimeout(timer);
}, []);
```

---

## Quick Reference: Interaction → Animation + Haptic

| Interaction | Scale | Duration | Easing | Haptic |
|-------------|-------|----------|--------|--------|
| Button press | 0.93 → 1 | 60ms down, 180ms up | ease-out | Medium impact |
| Card tap | 0.98 → 1 | 80ms down, 200ms up | ease-out | Light impact |
| Like toggle (on) | 1 → 1.35 → 0.9 → 1 | 100+80+150ms | ease-out | Medium impact |
| Like toggle (off) | 1 → 0.8 → 1 | 80+150ms | ease-out | Light impact |
| Chip/toggle select | (color only) | 200ms | ease-out | Selection |
| List item entrance | FadeInUp | 350ms + stagger | ease-out | None |
| Modal enter | SlideInUp | 350ms | ease-out | Light impact |
| Modal exit | SlideOutDown | 250ms | ease-in | None |
| Progress fill | (dashoffset) | 600-800ms | ease-out | None (or Success at 100%) |
| Milestone pop | 0 → 1.2 → 1 | 250+200ms | ease-out | Escalating |
| Destructive confirm | — | — | — | Warning notification |
| Success complete | — | — | — | Success notification |
| Error | — | — | — | Error notification |
| Pull-to-refresh threshold | — | — | — | Light impact |

---

## Web Patterns (CSS + Framer Motion)

Web doesn't have native haptics, but you can use the Vibration API on supported devices and focus on visual + audio micro-feedback instead.

### Button Press (Tailwind)
```html
<button class="transition-transform duration-[180ms] ease-out active:scale-[0.93] active:duration-[60ms] focus-visible:outline-2 focus-visible:outline-accent focus-visible:outline-offset-2">
  Click me
</button>
```

### Button Press (CSS fallback)
```css
.btn {
  transition: transform 180ms cubic-bezier(0.33, 1, 0.68, 1);
  will-change: transform;
}
.btn:active {
  transform: scale(0.93);
  transition-duration: 60ms;
}
.btn:focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
}
```

### Card Hover + Click (Tailwind)
```html
<div class="transition-all duration-200 ease-out hover:-translate-y-0.5 hover:shadow-lg active:scale-[0.98] active:duration-[80ms] cursor-pointer">
  Card content
</div>
```

### Card Hover + Click (CSS fallback)
```css
.card {
  transition: transform 200ms cubic-bezier(0.33, 1, 0.68, 1),
              box-shadow 200ms cubic-bezier(0.33, 1, 0.68, 1);
}
.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}
.card:active {
  transform: scale(0.98);
  transition-duration: 80ms;
}
```

### List Stagger (Framer Motion)
```jsx
import { motion } from 'framer-motion';

const container = {
  hidden: {},
  show: { transition: { staggerChildren: 0.08, delayChildren: 0.2 } },
};
const item = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0, transition: { duration: 0.35, ease: [0.33, 1, 0.68, 1] } },
};

function List({ items }) {
  return (
    <motion.ul variants={container} initial="hidden" animate="show">
      {items.map((i) => (
        <motion.li key={i.id} variants={item}>{i.name}</motion.li>
      ))}
    </motion.ul>
  );
}
```

### Modal (Framer Motion)
```jsx
<AnimatePresence>
  {isOpen && (
    <>
      <motion.div
        className="backdrop"
        initial={{ opacity: 0 }}
        animate={{ opacity: 0.6 }}
        exit={{ opacity: 0 }}
        transition={{ duration: 0.2 }}
        onClick={onClose}
      />
      <motion.div
        className="modal"
        initial={{ opacity: 0, y: 40 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: 40 }}
        transition={{ duration: 0.35, ease: [0.33, 1, 0.68, 1] }}
      >
        {children}
      </motion.div>
    </>
  )}
</AnimatePresence>
```

### Toggle / Chip (Tailwind)
```html
<!-- Inactive -->
<button class="border border-border bg-surface text-secondary transition-colors duration-200 ease-out rounded-full px-4 py-2">
  Option
</button>

<!-- Active -->
<button class="border border-accent bg-accent/10 text-accent transition-colors duration-200 ease-out rounded-full px-4 py-2">
  Option
</button>
```

### Toggle (CSS fallback)
```css
.toggle {
  transition: background-color 200ms cubic-bezier(0.33, 1, 0.68, 1),
              border-color 200ms cubic-bezier(0.33, 1, 0.68, 1);
}
.toggle[data-active="true"] {
  background-color: var(--accent-dim);
  border-color: var(--accent);
  color: var(--accent);
}
```

### Skeleton Loading (Tailwind)
```html
<div class="bg-muted rounded-lg animate-pulse h-12 w-full" />

<!-- Custom pulse (slower, subtler) — add to tailwind.config.js -->
<!-- animation: { 'skeleton': 'skeleton-pulse 1.2s ease-in-out infinite alternate' } -->
<!-- keyframes: { 'skeleton-pulse': { from: { opacity: '0.3' }, to: { opacity: '0.6' } } } -->
```

### Skeleton Loading (CSS fallback)
```css
.skeleton {
  background: var(--surface);
  border-radius: 8px;
  animation: skeleton-pulse 1.2s ease-in-out infinite alternate;
}
@keyframes skeleton-pulse {
  from { opacity: 0.3; }
  to { opacity: 0.6; }
}
```

### Toast / Notification (CSS + Framer Motion)
```jsx
<motion.div
  initial={{ y: -100, opacity: 0 }}
  animate={{ y: 0, opacity: 1 }}
  exit={{ y: -100, opacity: 0 }}
  transition={{ duration: 0.3, ease: [0.33, 1, 0.68, 1] }}
  className="toast"
>
  {message}
</motion.div>
```

### Web Haptics (Vibration API, limited support)
```js
// Only works on Android Chrome and some browsers — always feature-detect
function webHaptic(pattern = [10]) {
  if ('vibrate' in navigator) navigator.vibrate(pattern);
}
// Light tap: webHaptic([10])
// Medium tap: webHaptic([20])
// Success: webHaptic([10, 50, 10])
// Warning: webHaptic([30, 30, 30])
```

### Reduced Motion (CSS)
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

### Web Quick Reference

| Interaction | CSS Property | Duration | Easing |
|-------------|-------------|----------|--------|
| Button press | `transform: scale(0.93)` | 60ms active, 180ms release | `cubic-bezier(0.33, 1, 0.68, 1)` |
| Card hover | `transform: translateY(-2px)` + box-shadow | 200ms | same |
| Card click | `transform: scale(0.98)` | 80ms | same |
| Toggle state | `background-color` + `border-color` | 200ms | same |
| List stagger | Framer `staggerChildren: 0.08` | 350ms per item | same |
| Modal enter | Framer `y: 40 → 0` | 350ms | same |
| Modal exit | Framer `y: 0 → 40` | 250ms | same |
| Skeleton | `opacity` keyframe | 1200ms alternate | ease-in-out |
| Page transition | Framer `opacity` + `x` | 300ms | same |
