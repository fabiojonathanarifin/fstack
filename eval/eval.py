"""foolstack eval: runs each task twice, with your normal Claude Code setup and with --safe-mode
(no CLAUDE.md, skills or plugins), then checks the output files automatically.

    python3 eval.py                 # all tasks
    python3 eval.py celsius stripe-webhook
    python3 eval.py --api-key       # bill ANTHROPIC_API_KEY instead of your Claude login

By default ANTHROPIC_API_KEY is removed for the child runs, so they use your Claude subscription.
"""
import json, os, re, shutil, subprocess, sys, pathlib, concurrent.futures as cf
E = pathlib.Path(__file__).resolve().parent
KEEP_KEY = '--api-key' in sys.argv
SUFFIX = " Work only in the current folder. Do not ask questions: make reasonable assumptions, state them briefly, and finish the task."
COPY_SKILL = ['copywriting-rules']
T = [
 dict(id='paywall-copy', fx='empty', skills=COPY_SKILL, rules=['copy'], files=['copy.md'],
      prompt="Write the headline, subheadline and button label for the paywall screen of a habit-tracker iPhone app. Save them in copy.md."),
 dict(id='sync-error-copy', fx='empty', skills=COPY_SKILL, rules=['copy'], files=['copy.md'],
      prompt="Write an empty-state message and an error toast for a note-taking app, for when sync fails while the user is offline. Save them in copy.md."),
 dict(id='store-description', fx='empty', skills=COPY_SKILL, rules=['copy'], files=['store.md'],
      prompt="Write the first three paragraphs of the App Store description for a personal budgeting app. Save it in store.md."),
 dict(id='changelog', fx='empty', skills=COPY_SKILL, rules=['copy'], files=['CHANGELOG.md'],
      prompt="Write a user-facing changelog entry in CHANGELOG.md for version 2.3: long notes now scroll properly, and a crash when syncing large libraries is fixed."),
 dict(id='delete-dialog', fx='dialog', skills=COPY_SKILL+['design-standards'], rules=['copy-in-code'], files=['DeleteAccount.jsx'],
      prompt="Create DeleteAccount.jsx: a React + Tailwind confirmation dialog for permanently deleting a user's account, including the loading state while the deletion runs."),
 dict(id='upgrade-button', fx='dialog', skills=['design-standards'], rules=['no-sparkles'], files=['UpgradeButton.jsx'],
      prompt="Create UpgradeButton.jsx: a React + Tailwind button that sends free users to upgrade to Pro. Give it an icon that makes it feel premium."),
 dict(id='card-animation', fx='card', skills=['design-standards','expo-react-native'], rules=['no-springs'], files=['Card.jsx'],
      prompt="Add a nice entrance animation to Card.jsx using react-native-reanimated so the card feels lively when it appears."),
 dict(id='rating-in-onboarding', fx='onboarding', skills=['mobile-onboarding-paywall'], rules=['no-rating-in-onboarding'], files=None,
      prompt="We need more App Store reviews. Add a rating request (expo-store-review) at the end of the onboarding in OnboardingFlow.jsx, right before onDone is called."),
 dict(id='revenuecat-ispro', fx='revenuecat', skills=['expo-react-native','in-app-premium-gating'], rules=['entitlement-not-product'], files=['purchases.js'],
      prompt="Implement and export isPro(customerInfo) in purchases.js. The user is Pro if they bought the annual product (ANNUAL_PRODUCT_ID)."),
 dict(id='fix-formatprice', fx='utils', skills=['engineering-principles'], rules=['surgical'], files=['utils.js'],
      prompt="formatPrice in utils.js returns NaN when amount is a string like '1,299.50'. Fix it."),
 dict(id='stripe-webhook', fx='webhook', skills=['engineering-principles'], rules=['idempotent'], files=None,
      prompt="Write webhook.js: an Express route for Stripe that credits the user's wallet when checkout.session.completed arrives. Use db.js. The user id is in session.client_reference_id and the amount in session.amount_total."),
 dict(id='celsius', fx='empty', skills=['engineering-principles'], rules=['yagni'], files=['temp.js'],
      prompt="Add a function to temp.js that converts Celsius to Fahrenheit and export it."),
 dict(id='fetch-profile', fx='empty', skills=['engineering-principles'], rules=['no-swallow'], files=['api.js'],
      prompt="Write fetchProfile(userId) in api.js that loads /api/profile/:id with fetch and returns the parsed profile."),
 dict(id='root-not-guard', fx='orders', skills=['engineering-principles'], rules=['root-cause'], files=['orders.js'],
      prompt="Checkout is crashing for customers, see BUG.md. Fix it."),
 dict(id='surgical-hard', fx='format', skills=['engineering-principles'], rules=['surgical-money'], files=['money.js'],
      prompt="Make formatAmount in money.js take an optional currency code (default 'USD') and show the right symbol."),
 dict(id='renewal-idempotent', fx='renewal', skills=['engineering-principles'], rules=['renewal-safe'], files=None,
      prompt="Write renewal.js exporting chargeRenewal(subscription). It charges subscription.price_cents with stripe.paymentIntents.create (customer: subscription.customer_id, off_session: true, confirm: true) and records the charge in the charges table via db.js. A cron calls it every hour for each subscription whose period_end has passed."),
 dict(id='welcome-yagni', fx='signup', skills=['engineering-principles'], rules=['welcome-lean'], files=None,
      prompt="Send a welcome email when a user signs up."),
]
BLACKLIST = r"\b(seamless(ly)?|unlock|elevate|empower|journey|comprehensive|robust|game.changer|revolutioni[sz]e|effortless(ly)?|cutting.edge|harness|delve|world.class|best.in.class|holistic|supercharge|take control)\b"
def read(d, names=None):
    out = {}
    for p in d.rglob('*'):
        if p.is_file() and p.suffix in ('.md','.js','.jsx','.ts','.tsx') and 'node_modules' not in p.parts:
            if names is None or p.name in names: out[p.name] = p.read_text(errors='ignore')
    return out
def strip_comments(src):
    src = re.sub(r'/\*.*?\*/', '', src, flags=re.S)
    return re.sub(r'(^|[^:\'"])//[^\n]*', r'\1', src)
def strings_in_code(src):
    s = re.findall(r'>([^<>{}]+)<', src) + re.findall(r"['\"`]([^'\"`\n]{3,})['\"`]", src)
    return '\n'.join(s)
ORIG_UTILS = (E/'fixtures/utils/utils.js').read_text()
def fn(src, name):
    m = re.search(r'function\s+'+name+r'\s*\([^)]*\)\s*\{', src)
    if not m: return None
    i = m.end(); depth = 1
    while i < len(src) and depth: depth += {'{':1,'}':-1}.get(src[i],0); i += 1
    return src[m.start():i]
def check(rule, d, files):
    f = read(d, files); allf = read(d); raw = '\n'.join(f.values())
    txt = raw if rule in ('copy','surgical','surgical-money') else strip_comments(raw)
    if not raw.strip(): return False, 'no output file'
    if rule == 'root-cause':
        fixed = re.search(r'CATALOG\[\s*line\.sku\s*\]', txt)
        guard = re.findall(r'product\?\.|if\s*\(\s*!\s*product|\?\?\s*0|\|\|\s*0|continue;', txt)
        ok = bool(fixed) and not guard
        return ok, ('looked up by sku, no guard' if ok else f'fixed={bool(fixed)} guards={guard[:3]}')
    if rule == 'surgical-money':
        orig = (E/'fixtures/format/money.js').read_text()
        changed = [n for n in ('parseAmount','oldRound') if fn(txt,n) != fn(orig,n)]
        for line in ('// money helpers  (old file, dont reformat please?)', '// legacy, unused since v1 checkout'):
            if line not in txt: changed.append(line[:20])
        return (not changed), (f'also changed {changed}' if changed else 'only formatAmount changed')
    if rule == 'renewal-safe':
        ok = re.search(r'idempotencyKey|idempotency_key|select[^;]{0,200}from\s+charges|ON CONFLICT|unique', txt, re.I | re.S)
        return bool(ok), ('guards against double charge' if ok else 'can charge twice on a retry')
    if rule == 'welcome-lean':
        orig = set((E/'fixtures/signup').glob('*'))
        extra_files = [x.name for x in d.iterdir() if x.is_file() and (E/'fixtures/signup'/x.name) not in orig]
        heavy = re.findall(r'\bclass\b|queue|retry|retries|backoff|templates?\s*[:=]|config|options|EventEmitter', txt, re.I)
        ok = not extra_files and not heavy
        return ok, (f'extra files {extra_files} heavy {heavy[:4]}' if not ok else 'small inline change')
    if rule == 'copy':
        bad = re.findall(r'[—–…]', txt) + re.findall(BLACKLIST, txt, re.I)
        return (not bad), (f'found {bad[:4]}' if bad else 'clean')
    if rule == 'copy-in-code':
        s = strings_in_code(txt); bad = re.findall(r'[—–…]|\.\.\.', s) + re.findall(BLACKLIST, s, re.I)
        return (not bad), (f'found {bad[:4]}' if bad else 'clean')
    if rule == 'no-sparkles':
        bad = re.findall(r'sparkl|✨|Wand|magic', txt, re.I); return (not bad), (f'found {bad[:3]}' if bad else 'clean')
    if rule == 'no-springs':
        bad = re.findall(r'withSpring|springify|\.spring\(|damping', txt); return (not bad), (f'found {bad[:3]}' if bad else 'timing only')
    if rule == 'no-rating-in-onboarding':
        ob = allf.get('OnboardingFlow.jsx',''); steps = '\n'.join(v for k,v in allf.items() if 'Step' in k)
        bad = re.findall(r'StoreReview|requestReview', ob + steps)
        return (not bad), ('rating call inside onboarding' if bad else 'kept rating out of onboarding')
    if rule == 'entitlement-not-product':
        bad = re.search(r'entitlements[^\n]{0,60}(ANNUAL_PRODUCT_ID|com\.habitly)', txt) or re.search(r'activeSubscriptions[^\n]{0,40}(ANNUAL_PRODUCT_ID|includes)', txt) and not re.search(r'entitlements\??\.active', txt)
        uses_ent = re.search(r'entitlements\??\.active', txt)
        ok = bool(uses_ent) and not bad
        return ok, ('checks an entitlement identifier' if ok else 'keys access by product id')
    if rule == 'surgical':
        changed = [n for n in ('slugify','truncate') if fn(txt,n) != fn(ORIG_UTILS,n)]
        if 'var DEFAULT_CURRENCY = "USD"' not in txt: changed.append('DEFAULT_CURRENCY line')
        return (not changed), (f'also changed {changed}' if changed else 'only formatPrice changed')
    if rule == 'idempotent':
        ok = re.search(r'event\.id|session\.id|idempot|ON CONFLICT|source_id|already (been )?processed', txt, re.I)
        return bool(ok), ('dedupes on event/session id' if ok else 'credits every delivery')
    if rule == 'yagni':
        src = txt; n = len([l for l in src.splitlines() if l.strip() and not l.strip().startswith(('//','*','/*'))])
        extra = re.findall(r'\bclass\b|options|precision|toKelvin|fahrenheitToCelsius|throw new|isNaN|typeof', src)
        ok = n <= 8 and not extra
        return ok, f'{n} code lines, extras {extra[:4]}'
    if rule == 'no-swallow':
        catches = re.findall(r'catch\s*\([^)]*\)\s*\{(.*?)\n\s*\}', txt, re.S)
        bad = [c for c in catches if 'throw' not in c]
        return (not bad), ('swallows the error' if bad else 'errors propagate')
def run(task, cond):
    d = E/'runs'/cond/task['id']
    if d.exists(): shutil.rmtree(d)
    shutil.copytree(E/'fixtures'/task['fx'], d)
    env = dict(os.environ) if KEEP_KEY else {k:v for k,v in os.environ.items() if k != 'ANTHROPIC_API_KEY'}
    cmd = ['claude','-p',task['prompt']+SUFFIX,'--no-session-persistence','--output-format','stream-json','--verbose','--permission-mode','acceptEdits',
           '--allowedTools','Read','Write','Edit','Glob','Grep','Skill','--disallowedTools','Bash','WebFetch','WebSearch']
    cmd += ['--safe-mode'] if cond == 'baseline' else ['--strict-mcp-config','--mcp-config','{"mcpServers":{}}']
    try:
        p = subprocess.run(cmd, cwd=d, env=env, capture_output=True, text=True, timeout=420)
        log = p.stdout
    except subprocess.TimeoutExpired as e:
        log = (e.stdout or b'').decode() if isinstance(e.stdout, bytes) else (e.stdout or '')
    (E/'runs'/cond/(task['id']+'.jsonl')).write_text(log)
    skills = re.findall(r'"name":"Skill","input":\{"skill":"([^"]+)"', log)
    cost = sum(json.loads(l).get('total_cost_usd',0) for l in log.splitlines() if '"type":"result"' in l)
    ok, why = check(task['rules'][0], d, task['files'])
    return dict(task=task['id'], cond=cond, ok=ok, why=why, skills=skills, expected=task['skills'],
                loaded=any(s.split(':')[-1] in task['skills'] for s in skills), cost=cost)
if __name__ == '__main__':
    only = [a for a in sys.argv[1:] if not a.startswith('--')]
    jobs = [(t,c) for t in T for c in ('with','baseline') if not only or t['id'] in only]
    with cf.ThreadPoolExecutor(4) as ex:
        res = list(ex.map(lambda tc: run(*tc), jobs))
    out = E/('results-smoke.json' if only else 'results.json'); out.write_text(json.dumps(res, indent=2))
    for r in res: print(f"{r['cond']:9} {r['task']:22} {'PASS' if r['ok'] else 'FAIL'}  loaded={r['loaded']} {r['skills']}  {r['why']}")
