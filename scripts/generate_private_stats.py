import json
import os
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from xml.sax.saxutils import escape

TOKEN = os.environ["GITHUB_TOKEN"]
USERNAME = os.environ.get("GITHUB_USERNAME", "FarisShikuku")

QUERY = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar { totalContributions }
      restrictedContributionsCount
      totalCommitContributions
      totalIssueContributions
      totalPullRequestContributions
      totalPullRequestReviewContributions
    }
  }
}
"""

payload = json.dumps({
    "query": QUERY,
    "variables": {"login": USERNAME},
}).encode()

request = urllib.request.Request(
    "https://api.github.com/graphql",
    data=payload,
    headers={
        "Authorization": f"Bearer {TOKEN}",
        "Accept": "application/vnd.github+json",
        "Content-Type": "application/json",
        "User-Agent": "FarisShikuku-profile-metrics",
    },
    method="POST",
)

with urllib.request.urlopen(request, timeout=30) as response:
    result = json.load(response)

if result.get("errors"):
    raise RuntimeError(json.dumps(result["errors"], indent=2))

cc = result["data"]["user"]["contributionsCollection"]

total = cc["contributionCalendar"]["totalContributions"]
private = cc["restrictedContributionsCount"]
public = max(total - private, 0)
commits = cc["totalCommitContributions"]
issues = cc["totalIssueContributions"]
prs = cc["totalPullRequestContributions"]
reviews = cc["totalPullRequestReviewContributions"]
generated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="900" height="300" viewBox="0 0 900 300" role="img" aria-labelledby="title desc">
<title id="title">Faris Shikuku GitHub contribution statistics</title>
<desc id="desc">Aggregate GitHub contribution statistics including restricted private contributions.</desc>
<style>
.bg{{fill:#0d1117}} .card{{fill:#161b22;stroke:#30363d}}
.title{{fill:#f0f6fc;font:700 24px -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}}
.label{{fill:#8b949e;font:500 13px -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}}
.value{{fill:#58a6ff;font:700 27px -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}}
.small{{fill:#8b949e;font:400 11px -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}}
</style>
<rect class="bg" width="900" height="300" rx="14"/>
<text class="title" x="30" y="42">GitHub Contribution Statistics</text>
<text class="small" x="30" y="64">FarisShikuku · generated {escape(generated)}</text>

<g transform="translate(30,88)"><rect class="card" width="195" height="82" rx="10"/><text class="label" x="18" y="27">TOTAL CONTRIBUTIONS</text><text class="value" x="18" y="61">{total:,}</text></g>
<g transform="translate(245,88)"><rect class="card" width="195" height="82" rx="10"/><text class="label" x="18" y="27">PRIVATE / RESTRICTED</text><text class="value" x="18" y="61">{private:,}</text></g>
<g transform="translate(460,88)"><rect class="card" width="195" height="82" rx="10"/><text class="label" x="18" y="27">PUBLIC CONTRIBUTIONS</text><text class="value" x="18" y="61">{public:,}</text></g>
<g transform="translate(675,88)"><rect class="card" width="195" height="82" rx="10"/><text class="label" x="18" y="27">COMMITS</text><text class="value" x="18" y="61">{commits:,}</text></g>

<g transform="translate(30,190)"><rect class="card" width="195" height="70" rx="10"/><text class="label" x="18" y="27">PULL REQUESTS</text><text class="value" x="18" y="57">{prs:,}</text></g>
<g transform="translate(245,190)"><rect class="card" width="195" height="70" rx="10"/><text class="label" x="18" y="27">ISSUES</text><text class="value" x="18" y="57">{issues:,}</text></g>
<g transform="translate(460,190)"><rect class="card" width="195" height="70" rx="10"/><text class="label" x="18" y="27">PR REVIEWS</text><text class="value" x="18" y="57">{reviews:,}</text></g>
<g transform="translate(675,190)"><rect class="card" width="195" height="70" rx="10"/><text class="label" x="18" y="27">DATA SOURCE</text><text class="small" x="18" y="52">GitHub GraphQL API</text></g>
</svg>
"""

Path("assets/private-stats.svg").write_text(svg, encoding="utf-8")
