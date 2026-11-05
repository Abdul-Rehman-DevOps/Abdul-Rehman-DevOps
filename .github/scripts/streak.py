#!/usr/bin/env python3
"""Generate streak/streak-{dark,light}.svg from real GitHub contribution data.

Runs in the Profile Assets workflow (GITHUB_TOKEN). Counts every day since the
account was created, so the numbers are always live and verifiable.
Local test without network:  python3 streak.py --fake
"""
import datetime as dt, json, os, sys, urllib.request

sys.path.insert(0, os.path.dirname(__file__))
from theme import THEMES, SANS, MONO, WIDTH, frame, header  # noqa: E402

USER = os.environ.get("GH_USER", "Abdul-Rehman-DevOps")
OUT_DIR = os.environ.get("OUT_DIR", "streak")
API = "https://api.github.com/graphql"


def gql(query, variables):
    req = urllib.request.Request(
        API,
        data=json.dumps({"query": query, "variables": variables}).encode(),
        headers={"Authorization": f"bearer {os.environ['GITHUB_TOKEN']}",
                 "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.load(r)
    if "errors" in data:
        raise SystemExit(f"GraphQL error: {data['errors']}")
    return data["data"]


def fetch_days():
    created = gql("query($u:String!){user(login:$u){createdAt}}", {"u": USER})["user"]["createdAt"]
    start = dt.datetime.fromisoformat(created.replace("Z", "+00:00"))
    now = dt.datetime.now(dt.timezone.utc)
    days = {}
    q = """query($u:String!,$f:DateTime!,$t:DateTime!){user(login:$u){
      contributionsCollection(from:$f,to:$t){contributionCalendar{weeks{contributionDays{date contributionCount}}}}}}"""
    cur = start
    while cur < now:  # API allows at most a 1-year window per call
        end = min(cur + dt.timedelta(days=365), now)
        cal = gql(q, {"u": USER, "f": cur.isoformat(), "t": end.isoformat()})
        for w in cal["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]:
            for d in w["contributionDays"]:
                days[d["date"]] = d["contributionCount"]
        cur = end
    return dict(sorted(days.items()))


def stats(days):
    dates = [dt.date.fromisoformat(d) for d in days]
    total = sum(days.values())
    first = next((d for d in dates if days[d.isoformat()] > 0), dates[0])
    # longest streak
    best = run = 0; best_end = None
    for d in dates:
        if days[d.isoformat()] > 0:
            run += 1
            if run > best: best, best_end = run, d
        else:
            run = 0
    # current streak: today may still be empty, so allow ending yesterday
    today = dates[-1]; cur = 0; i = len(dates) - 1
    if days[today.isoformat()] == 0: i -= 1
    while i >= 0 and days[dates[i].isoformat()] > 0:
        cur += 1; i -= 1
    best_start = best_end - dt.timedelta(days=best - 1) if best_end else None
    return total, first, cur, best, best_start, best_end


def fmt(d):
    return d.strftime("%b %Y")


def fmt_day(d):
    return d.strftime("%b %d").replace(" 0", " ")


def render(t, total, first, cur, best, bs, be):
    best_label = f"{fmt_day(bs)} — {fmt_day(be)}" if best else "start a streak"
    cur_label = "days · keep going" if cur else "commit today to start"
    synced = dt.datetime.now(dt.timezone.utc).strftime("synced %Y-%m-%d %H:%M UTC")
    tiles = [
        (f"{total:,}", "Total contributions", f"{fmt(first)} — Present", t["a1"]),
        (f"{cur}", "Current streak", cur_label, t["a3"]),
        (f"{best}", "Longest streak", best_label, t["a2"]),
    ]
    gap, x0 = 14, 32
    w = (WIDTH - 2 * x0 - gap * 2) / 3
    body = [header(t, 48, 38, "./streak.sh --live", synced)]
    for i, (num, label, sub, col) in enumerate(tiles):
        x = x0 + i * (w + gap); y = 60
        cx = x + w / 2
        body.append(f'    <rect x="{x:.0f}" y="{y}" width="{w:.0f}" height="112" rx="12" fill="{t["panel"]}" stroke="{t["border"]}"/>')
        body.append(f'    <rect x="{x:.0f}" y="{y}" width="{w:.0f}" height="3" rx="1.5" fill="{col}"/>')
        body.append(f'    <text x="{cx:.0f}" y="{y + 52}" text-anchor="middle" font-family="{SANS}" font-size="38" font-weight="700" fill="{col}">{num}</text>')
        body.append(f'    <text x="{cx:.0f}" y="{y + 80}" text-anchor="middle" font-family="{SANS}" font-size="14" fill="{t["text"]}">{label}</text>')
        body.append(f'    <text x="{cx:.0f}" y="{y + 99}" text-anchor="middle" font-family="{MONO}" font-size="12" fill="{t["muted"]}">{sub}</text>')
    return frame(t, 196, "\n".join(body), f"{total} total contributions, current streak {cur} days, longest streak {best} days")


if __name__ == "__main__":
    if "--fake" in sys.argv:
        import random
        random.seed(7); base = dt.date(2025, 7, 1)
        days = {(base + dt.timedelta(i)).isoformat(): (random.random() < 0.7) * random.randint(1, 9) for i in range(470)}
    else:
        days = fetch_days()
    os.makedirs(OUT_DIR, exist_ok=True)
    s = stats(days)
    for mode, t in THEMES.items():
        out = os.path.join(OUT_DIR, f"streak-{mode}.svg")
        with open(out, "w", encoding="utf-8", newline="\n") as f:
            f.write(render(t, *s))
        print(f"total={s[0]} current={s[2]} longest={s[3]} -> {out}")
