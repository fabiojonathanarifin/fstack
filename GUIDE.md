# fstack in one page

## Install

```
/plugin marketplace add fabiojonathanarifin/fstack
/plugin install fstack@fstack          # any codebase
/plugin install fstack-mobile@fstack   # B2C mobile apps
```

## How it works

Two kinds of skills.

- **Rules load themselves.** When you write copy, the copy rules load. When you design a screen, the design rules load. When you debug, the engineering rules load. You do nothing.
- **Checks wait for you.** Commands like `/in-your-own-words` or `/correct` interrupt the work to question it, so they only run when you type them.

## A normal day

1. Give the agent a task. If it's big or fuzzy, type `/in-your-own-words` first and confirm it understood.
2. It builds, using the rules that apply.
3. Before a change to money, auth, data or migrations ships, it runs `blast-radius` and proves the one fact the change is safe because of.
4. For UI work, it proves the result in the running app with your project's verify skill and shows you the screenshots.
5. At the end of a long session, type `/reflect`. It proposes skill edits from what went wrong, and you approve them.

## Set up once per project

1. `/create-verification-skill`: writes `verify-<app>` so agents can launch your app, sign in a test account, reach any feature and capture proof. Read its Safety section if your local setup can touch real data or money.
2. `/correct`: finds the mistakes agents keep making in that repo and turns them into lint rules, type rules or checks that fail with the fix in the error.

## Keep it sharp

- `/maintain-verification-skill` when the app changes and the feature map drifts.
- `/correct` again whenever you catch yourself making the same correction twice.
- `python3 eval/eval.py` after changing a skill, to check it still helps.

## What it won't do

Push, deploy or merge on its own. Spend money or contact users during verification. Hide a broken test to make a check pass.
