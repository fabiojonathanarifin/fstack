---
name: engineering-principles
description: Architecture-first engineering judgment for any codebase: design for the scale the product implies, recognize recurring-bug smells, attack the premise, explain the number, build the lever, fix root causes, model the domain, minimize reader load, error handling at the edges, and critical-path testing. Use when planning a feature, debugging, refactoring, or reviewing code.
---

# Engineering principles

## Think at the Architecture Level First (see the whole board)

Before diving into a fix, step back and ask whether the DESIGN is right, not just whether this line is wrong. Tunnel-visioning on the local failing code path is how days get burned circling one symptom. A wrong-architecture problem disguises itself as an endless series of small bugs, each fix spawning the next. This rule is a hard, first-class constraint, not a nice-to-have: think like an architect on EVERY problem, not just when asked.

- **Lead with the architecture question.** When something breaks or a feature is requested, FIRST ask: what is the right SYSTEM design for this, given the product and its realistic scale? Then fix or build. The local patch comes after the design is confirmed sound, never instead of it.
- **Infer the real requirements from the product, not just the literal ask.** What the app already does tells you what it must support. "We handle lectures and meetings" already means long recordings (60-90 min, thousands of concurrent users) are a first-class case, even if no one says "90 minutes" or "enterprise scale." Read the intent and the implied upper bound, and design for THAT, not for the toy example in front of you. The user should not have to spell out a requirement that the product's own scope already implies.
- **Build for the realistic scale and the future, in one pass.** Pick the proven, standard, production-grade pattern that handles the actual workload and a plausible 10x, so the solution does not need re-architecting the moment it meets reality (real users, enterprise load, the long tail of inputs). When in doubt, choose the production-grade design (async/queue, decoupled, retryable, observable) over the quick one, unless the user explicitly wants a throwaway. Robust-and-scalable beats clever-and-local.
- **Reuse what already exists.** If a proven solution to this exact problem already exists (a system we built before, a battle-tested library, a standard industry pattern), reach for it before reinventing a fragile local version. Ask "has this been solved already, here or in the wider world?" EARLY, before writing a bespoke path.
- **Recognize the recurrence smell.** If the same issue keeps coming back, or a fix keeps failing in a new place each time, STOP patching. That pattern means the architecture is wrong, not that you need one more fix. Escalate to the design level (this is systematic-debugging Phase 4.5: question fundamentals after repeated failures). Hours spent circling one symptom is the signal you skipped this rule.
- **Attack the premise.** When two fixes that share one assumption have both failed, write that assumption down in one sentence and test it directly (find an observation that would come out differently if it were false) before writing a third fix.
- **Explain the number.** Before trusting or reporting a measurement (speedup, cost, conversion, latency), name what limits it and rule out that it measured something else: errors, cached or skipped work, code that never ran, noise. Keep the sample size with the number.
- **Build the lever.** For non-trivial or repetitive work (a sweep, migration, bulk edit, recurring check), write the small rerunnable script that does or proves it instead of doing it by hand. Do one unit by hand first, prove the script on it, never build a framework.
- **Ask whether the bad state should exist.** When a value or state triggers a bug, decide if it is legitimate. If it is, handle it where the code broke. If it should never exist, a guard there hides the bug: find what produced it. Then fix every place with the same fault, not just the one that surfaced.
- **Suspect the check before the system.** When a verification fails or contradicts itself, first rule out that you checked the wrong thing (stale cache, wrong environment, proxy signal) before changing code.
- **Model the domain in data, not branches.** Reach for a state machine, lookup table or typed model instead of scattered booleans and growing if/else chains. The warning sign is a second boolean that must stay in sync with the first. Keep boring code when the shape is small and local.
- **Minimize reader load.** Inline wrappers with one caller and adapters with one implementation. Derive values instead of syncing copies. A new reader should find where a value comes from and what can change it in under 30 seconds.
- **This is not a license to overengineer.** Architecture-level thinking means choosing the RIGHT altitude for the real requirements, not gold-plating for imaginary ones. The test: am I designing for a scale or need the product actually implies, or for a hypothetical no evidence supports? The former is required; the latter is the YAGNI violation. Both failure modes (patching too local, abstracting too early) come from not seeing the actual picture.

## Error Handling - Try/Catch Everywhere
Catch to log and re-throw inside the app; decide what the user sees only at the edges (API routes, UI handlers, jobs). Never swallow an error, return a fake default, or retry silently in the middle: that hides the bug instead of handling it.
```javascript
// ✅ Always wrap async calls
const fetchUserProfile = async (userId) => {
  try {
    const { data, error } = await supabase
      .from('users')
      .select()
      .eq('id', userId)
      .single();
    
    if (error) throw error;
    return data;
  } catch (error) {
    console.error('Failed to fetch user profile:', error);
    throw error; // Re-throw for caller to handle
  }
}

// ✅ Handle errors at UI boundaries
const ProfileScreen = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  useEffect(() => {
    fetchUserProfile(userId)
      .then(setProfile)
      .catch(setError)
      .finally(() => setLoading(false));
  }, []);
  
  if (error) return <ErrorView message={error.message} />;
  // ... render
}
```

## Testing Philosophy
- Test **critical paths only**: auth, payments, core user flows
- Ship fast, add tests where failure = user pain or revenue loss
- E2E tests for payment flows
- Unit tests for complex business logic
- Skip tests for UI components unless critical

## Code Quality Principles

### DRY (Don't Repeat Yourself) - Always
```javascript
// ✅ Always DRY by default - extract shared logic into reusable functions/components
// ✅ If you write the same pattern twice, extract it immediately
// ✅ Shared constants, helpers, and utilities belong in dedicated files
// ✅ When in doubt, DRY it out
// ❌ Never duplicate logic across files - find the existing implementation and reuse it
// ❌ Never copy-paste code blocks between components - extract a shared function
```

### Scalable but Not Overengineered
```javascript
// ✅ Good - simple now, easy to extend later
const useAuth = () => {
  const [user, setUser] = useState(null);
  
  const login = async (email, password) => {
    const { data } = await supabase.auth.signInWithPassword({ email, password });
    setUser(data.user);
  };
  
  return { user, login };
};

// ❌ Overengineered - building for future you don't need yet
class AuthenticationManager {
  constructor(authProvider, sessionManager, permissionService) {
    // ... 100 lines of abstraction
  }
}
```

### Robust Root Fixes
```javascript
// ✅ Fix the root cause
const saveUserPreferences = async (prefs) => {
  try {
    // Validate data shape before saving
    const validated = validatePreferences(prefs);
    
    // Use upsert to handle new and existing users
    const { error } = await supabase
      .from('user_preferences')
      .upsert(validated, { onConflict: 'user_id' });
    
    if (error) throw error;
  } catch (error) {
    console.error('Failed to save preferences:', error);
    throw error;
  }
};

// ❌ Quick patch that doesn't solve underlying issue
const saveUserPreferences = async (prefs) => {
  // Just try again if it fails (doesn't address WHY it failed)
  try {
    await supabase.from('user_preferences').insert(prefs);
  } catch {
    await supabase.from('user_preferences').insert(prefs);
  }
};
```
