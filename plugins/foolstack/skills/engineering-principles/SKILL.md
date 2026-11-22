---
name: engineering-principles
description: Architecture-first engineering judgment for any codebase: design for the scale the product implies, recognize recurring-bug smells, attack the premise, explain the number, build the lever, fix root causes, model the domain, minimize reader load, test behavior not implementation, replace then delete, validate at the edges, make bad states hard to write, separate before you lock, prototype the fork, protect the main context, surgical changes, stating assumptions, defining the check first, matching speed to reversibility, safe retries, error handling at the edges, and critical-path testing. Use when planning a feature, debugging, refactoring, or reviewing code.
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
- **Surgical changes.** Touch only what the task needs. Match the existing style. Don't "improve" nearby code, comments or formatting on the way past. Remove imports, variables and files your own change left unused; flag old dead code instead of deleting it unasked.
- **Comments earn their place.** No comment when good names make the code clear. When one is needed, it is one or two lines on a why the code can't show (a workaround, a constraint, a trap). Never restate the code, never record history or who asked for it, never leave commented-out code.
- **State assumptions before coding.** Say what you are assuming and name any other reading of the request instead of silently picking one. On reversible work, state it and proceed; on anything irreversible or genuinely ambiguous, ask first.
- **Define the check first, then show evidence.** Turn the task into a verifiable goal before writing code ("fix the bug" becomes "a test that reproduces it fails, then passes"). When reporting done, show the test output, command result or screenshot, not just a claim.
- **Match speed to reversibility.** Move fast on changes that are easy to undo. Slow down on one-way doors: schema migrations, money movement, deletes, anything sent to users. Ship in small batches so each change is easy to review and roll back.
- **Make retries safe.** Webhooks, payment events, jobs and lifecycle steps can run twice or crash halfway. Running them again must end in the same state: key on an event or request id, check before acting, never assume exactly-once delivery.
- **Test behavior, not implementation.** Assert what a user or caller can observe. A test that still passes when the behavior breaks, or fails when only internals change, gets fixed or deleted.
- **Replace, then delete.** When a new API or pattern replaces an old one, move every caller and delete the old one in the same change. Two ways to do one thing is how agents copy the wrong one.
- **Validate at the edges.** Parse and check outside input (requests, webhooks, env vars, third-party responses) where it enters. Inside the app, trust it. No defensive checks sprinkled through the middle.
- **Make bad states hard to write.** In TypeScript, use unions and branded IDs so an invalid state doesn't compile. In JavaScript, give each important object one create or parse function and make it the only way in.
- **Separate before you lock.** When two jobs, requests or agents can write the same thing, remove the sharing first (one owner, per-item keys) before reaching for locks or retries.
- **Prototype the fork.** For a new UX or architecture decision with no precedent, build two or three quick throwaway versions and compare them before committing to one.
- **Protect the main context.** Send bulky reading (long logs, many files, transcripts) to a subagent and keep only its conclusion.
- **This is not a license to overengineer.** Architecture-level thinking means choosing the RIGHT altitude for the real requirements, not gold-plating for imaginary ones. The test: am I designing for a scale or need the product actually implies, or for a hypothetical no evidence supports? The former is required; the latter is the YAGNI violation. Both failure modes (patching too local, abstracting too early) come from not seeing the actual picture.

## Error Handling
Catch to log and re-throw inside the app; decide what the user sees only at the edges (API routes, UI handlers, jobs). Never swallow an error, return a fake default, or retry silently in the middle: that hides the bug instead of handling it.
```javascript
// ✅ Always wrap async calls
const fetchUserProfile = async (userId) => {
  try {
    return await db.users.findById(userId);
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

### DRY (Don't Repeat Yourself) - One Source of Truth
```javascript
// ✅ One source of truth for every decision, constant and business rule (prices, limits, IDs)
// ✅ Extract shared logic on the third copy, or the second when the copies must change together
// ✅ Shared constants, helpers, and utilities belong in dedicated files
// ✅ Two similar-looking blocks that change for different reasons are not duplication; leave them
// ❌ Never duplicate logic across files - find the existing implementation and reuse it
// ❌ Never copy-paste code blocks between components - extract a shared function
```

### Scalable but Not Overengineered
```javascript
// ✅ Good - simple now, easy to extend later
const useAuth = () => {
  const [user, setUser] = useState(null);
  
  const login = async (email, password) => {
    const session = await auth.signIn(email, password);
    setUser(session.user);
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
    
    // Upsert so new and existing users take the same path
    await db.userPreferences.upsert(validated, { key: 'userId' });
  } catch (error) {
    console.error('Failed to save preferences:', error);
    throw error;
  }
};

// ❌ Quick patch that doesn't solve underlying issue
const saveUserPreferences = async (prefs) => {
  // Just try again if it fails (doesn't address WHY it failed)
  try {
    await db.userPreferences.insert(prefs);
  } catch {
    await db.userPreferences.insert(prefs);
  }
};
```
