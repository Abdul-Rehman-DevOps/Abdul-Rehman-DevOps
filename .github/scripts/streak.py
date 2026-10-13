#!/usr/bin/env python3
"""Generate streak/streak.svg from real GitHub contribution data.

Runs in the Profile Assets workflow (GITHUB_TOKEN). Counts every day since the
account was created, so the numbers are always live and verifiable.
Local test without network:  python3 streak.py --fake
"""
import datetime as dt, json, os, sys, urllib.request

USER = os.environ.get("GH_USER", "Abdul-Rehman-DevOps")
OUT = os.environ.get("OUT", "streak/streak.svg")
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


def render(total, first, cur, best, bs, be):
    best_label = f"{fmt_day(bs)} — {fmt_day(be)}" if best else "start a streak"
    cur_label = "days · keep going" if cur else "commit today to start"
    synced = dt.datetime.now(dt.timezone.utc).strftime("synced %Y-%m-%d %H:%M UTC")
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="1180" height="180" viewBox="0 0 1180 180" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" role="img" aria-label="{total} total contributions, current streak {cur} days, longest streak {best} days">
  <rect width="1180" height="180" rx="14" fill="#070B16" stroke="#22D3EE" stroke-opacity="0.4" stroke-width="1.5"/>
  <text x="28" y="30" font-size="12" letter-spacing="2" fill="#22D3EE">$ ./streak.sh --live --animate</text>
  <text x="1152" y="30" text-anchor="end" font-size="11" fill="#64748B">{synced}
    <animate attributeName="opacity" values="1;0.25;1" dur="1.2s" repeatCount="2"/>
  </text>
  <line x1="28" y1="42" x2="1152" y2="42" stroke="#A78BFA" stroke-opacity="0.35">
    <animate attributeName="x2" from="28" to="1152" dur="0.9s" fill="freeze"/>
  </line>

  <g opacity="0"><animate attributeName="opacity" from="0" to="1" begin="0.20s" dur="0.50s" fill="freeze"/>
    <rect x="40" y="58" width="340" height="100" rx="12" fill="#0A101F" stroke="#22D3EE" stroke-opacity="0.3"/>
    <text x="210" y="100" text-anchor="middle" font-size="42" font-weight="700" fill="#F8FAFC">{total:,}</text>
    <text x="210" y="128" text-anchor="middle" font-size="13" fill="#22D3EE">Total Contributions</text>
    <text x="210" y="148" text-anchor="middle" font-size="11" fill="#94A3B8">{fmt(first)} — Present</text>
  </g>

  <g opacity="0"><animate attributeName="opacity" from="0" to="1" begin="0.40s" dur="0.50s" fill="freeze"/>
    <rect x="420" y="58" width="340" height="100" rx="12" fill="#0A101F" stroke="#A78BFA" stroke-opacity="0.35"/>
    <circle cx="590" cy="91" r="22" fill="none" stroke="#A78BFA" stroke-width="3" opacity="0.7">
      <animate attributeName="stroke-dasharray" values="0 140;138 140" dur="1.2s" begin="0.5s" fill="freeze"/>
    </circle>
    <text x="590" y="99" text-anchor="middle" font-size="22" font-weight="700" fill="#F8FAFC">{cur}</text>
    <text x="590" y="131" text-anchor="middle" font-size="13" fill="#34D399">Current Streak</text>
    <text x="590" y="148" text-anchor="middle" font-size="11" fill="#94A3B8">{cur_label}</text>
  </g>

  <g opacity="0"><animate attributeName="opacity" from="0" to="1" begin="0.60s" dur="0.50s" fill="freeze"/>
    <rect x="800" y="58" width="340" height="100" rx="12" fill="#0A101F" stroke="#22D3EE" stroke-opacity="0.3"/>
    <text x="970" y="100" text-anchor="middle" font-size="42" font-weight="700" fill="#F8FAFC">{best}</text>
    <text x="970" y="128" text-anchor="middle" font-size="13" fill="#22D3EE">Longest Streak</text>
    <text x="970" y="148" text-anchor="middle" font-size="11" fill="#94A3B8">{best_label}</text>
  </g>
</svg>
'''


if __name__ == "__main__":
    if "--fake" in sys.argv:
        import random
        random.seed(7); base = dt.date(2025, 7, 1)
        days = {(base + dt.timedelta(i)).isoformat(): (random.random() < 0.7) * random.randint(1, 9) for i in range(470)}
    else:
        days = fetch_days()
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    s = stats(days)
    open(OUT, "w").write(render(*s))
    print(f"total={s[0]} current={s[2]} longest={s[3]} -> {OUT}")
