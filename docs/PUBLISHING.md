# Publishing checklist

Maintainer notes for putting this repo at `https://github.com/andpurnell-code/sunday-roast`.

```
cd github   # this folder
git remote add origin https://github.com/andpurnell-code/sunday-roast.git   # create the empty repo first
git push -u origin main --tags
```

1. Create an empty repo named `sunday-roast` (no README or licence, they are here). Start private.
2. Push (above). Check the README renders and CI is green.
3. Settings: enable Issues, Discussions, private vulnerability reporting. Add topics: claude, claude-skill, agent-skills, productivity.
4. Create a Release from tag `v1.0.0`, attach `dist/sunday-roast-skill.zip`, paste the CHANGELOG entry.
5. In a clean Claude Code, run `/plugin marketplace add andpurnell-code/sunday-roast` and install. Upload the zip to a Claude.ai account.
6. Then make the repo public.
