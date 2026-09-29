
import os
import json
import urllib.request
from pathlib import Path


# ============================================================
# Configuration
# ============================================================

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
GITHUB_USERNAME = os.environ.get("GITHUB_USERNAME", "FarisShikuku")

if not GITHUB_TOKEN:
    raise RuntimeError(
        "GITHUB_TOKEN environment variable is not set. "
        "Make sure METRICS_TOKEN is configured in the workflow."
    )


# ============================================================
# GitHub GraphQL API
# ============================================================

GRAPHQL_URL = "https://api.github.com/graphql"

query = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar {
        totalContributions
      }

      restrictedContributionsCount

      totalCommitContributions
      totalIssueContributions
      totalPullRequestContributions
      totalPullRequestReviewContributions
    }
  }
}
"""


# ============================================================
# Request GitHub
# ============================================================

payload = {
    "query": query,
    "variables": {
        "login": GITHUB_USERNAME
    }
}

request = urllib.request.Request(
    GRAPHQL_URL,
    data=json.dumps(payload).encode("utf-8"),
    headers={
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Content-Type": "application/json",
        "User-Agent": "FarisShikuku-GitHub-Metrics"
    },
    method="POST"
)


with urllib.request.urlopen(request) as response:
    result = json.loads(response.read().decode("utf-8"))


# ============================================================
# Validate API response
# ============================================================

if "errors" in result:
    raise RuntimeError(
        "GitHub GraphQL API returned an error:\n"
        + json.dumps(result["errors"], indent=2)
    )


if "data" not in result or not result["data"].get("user"):
    raise RuntimeError(
        f"Could not find GitHub user: {GITHUB_USERNAME}"
    )


# ============================================================
# Extract contribution statistics
# ============================================================

contributions = result["data"]["user"]["contributionsCollection"]

calendar = contributions["contributionCalendar"]

total_contributions = calendar["totalContributions"]

private_contributions = contributions["restrictedContributionsCount"]

commits = contributions["totalCommitContributions"]

issues = contributions["totalIssueContributions"]

pull_requests = contributions["totalPullRequestContributions"]

reviews = contributions["totalPullRequestReviewContributions"]


# ============================================================
# Helper functions
# ============================================================

def escape_xml(value):
    """Escape text so it is safe inside SVG/XML."""
    return (
        str(value)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&apos;")
    )


def percentage(part, total):
    """Return a percentage safely."""
    if total == 0:
        return 0

    return round((part / total) * 100, 1)


private_percentage = percentage(
    private_contributions,
    total_contributions
)


# ============================================================
# Generate SVG
# ============================================================

username = escape_xml(GITHUB_USERNAME)

svg = f"""<svg xmlns="http://www.w3.org/2000/svg"
     width="900"
     height="360"
     viewBox="0 0 900 360">

  <defs>
    <linearGradient id="background"
                    x1="0"
                    y1="0"
                    x2="1"
                    y2="1">
      <stop offset="0%" stop-color="#161b22"/>
      <stop offset="100%" stop-color="#0d1117"/>
    </linearGradient>
  </defs>

  <rect
      x="0"
      y="0"
      width="900"
      height="360"
      rx="18"
      fill="url(#background)"
  />

  <!-- Header -->

  <text
      x="45"
      y="55"
      font-family="Arial, Helvetica, sans-serif"
      font-size="26"
      font-weight="700"
      fill="#f0f6fc">
      Private Contribution Statistics
  </text>

  <text
      x="45"
      y="82"
      font-family="Arial, Helvetica, sans-serif"
      font-size="14"
      fill="#8b949e">
      GitHub contribution activity for {username}
  </text>


  <!-- Main contribution count -->

  <text
      x="45"
      y="145"
      font-family="Arial, Helvetica, sans-serif"
      font-size="48"
      font-weight="700"
      fill="#58a6ff">
      {total_contributions}
  </text>

  <text
      x="47"
      y="172"
      font-family="Arial, Helvetica, sans-serif"
      font-size="15"
      fill="#8b949e">
      Total contributions
  </text>


  <!-- Private contribution count -->

  <text
      x="300"
      y="145"
      font-family="Arial, Helvetica, sans-serif"
      font-size="48"
      font-weight="700"
      fill="#a371f7">
      {private_contributions}
  </text>

  <text
      x="302"
      y="172"
      font-family="Arial, Helvetica, sans-serif"
      font-size="15"
      fill="#8b949e">
      Private contributions
  </text>


  <!-- Private percentage -->

  <text
      x="600"
      y="145"
      font-family="Arial, Helvetica, sans-serif"
      font-size="48"
      font-weight="700"
      fill="#3fb950">
      {private_percentage}%
  </text>

  <text
      x="602"
      y="172"
      font-family="Arial, Helvetica, sans-serif"
      font-size="15"
      fill="#8b949e">
      Private contribution share
  </text>


  <!-- Divider -->

  <line
      x1="45"
      y1="205"
      x2="855"
      y2="205"
      stroke="#30363d"
      stroke-width="1"
  />


  <!-- Contribution breakdown -->

  <text
      x="45"
      y="240"
      font-family="Arial, Helvetica, sans-serif"
      font-size="14"
      font-weight="600"
      fill="#f0f6fc">
      Contribution breakdown
  </text>


  <text
      x="45"
      y="275"
      font-family="Arial, Helvetica, sans-serif"
      font-size="14"
      fill="#8b949e">
      Commits
  </text>

  <text
      x="145"
      y="275"
      font-family="Arial, Helvetica, sans-serif"
      font-size="14"
      font-weight="700"
      fill="#f0f6fc">
      {commits}
  </text>


  <text
      x="270"
      y="275"
      font-family="Arial, Helvetica, sans-serif"
      font-size="14"
      fill="#8b949e">
      Issues
  </text>

  <text
      x="345"
      y="275"
      font-family="Arial, Helvetica, sans-serif"
      font-size="14"
      font-weight="700"
      fill="#f0f6fc">
      {issues}
  </text>


  <text
      x="455"
      y="275"
      font-family="Arial, Helvetica, sans-serif"
      font-size="14"
      fill="#8b949e">
      Pull requests
  </text>

  <text
      x="555"
      y="275"
      font-family="Arial, Helvetica, sans-serif"
      font-size="14"
      font-weight="700"
      fill="#f0f6fc">
      {pull_requests}
  </text>


  <text
      x="680"
      y="275"
      font-family="Arial, Helvetica, sans-serif"
      font-size="14"
      fill="#8b949e">
      Reviews
  </text>

  <text
      x="755"
      y="275"
      font-family="Arial, Helvetica, sans-serif"
      font-size="14"
      font-weight="700"
      fill="#f0f6fc">
      {reviews}
  </text>


  <!-- Footer -->

  <text
      x="45"
      y="325"
      font-family="Arial, Helvetica, sans-serif"
      font-size="12"
      fill="#6e7681">
      Generated automatically by GitHub Actions
  </text>

</svg>
"""


# ============================================================
# Save SVG
# ============================================================

# IMPORTANT:
# Create the assets directory automatically.
# This fixes:
# FileNotFoundError: assets/private-stats.svg

output_path = Path("assets/private-stats.svg")

output_path.parent.mkdir(
    parents=True,
    exist_ok=True
)

output_path.write_text(
    svg,
    encoding="utf-8"
)


# ============================================================
# Confirmation
# ============================================================

print("==============================================")
print("Private GitHub statistics generated")
print("==============================================")
print(f"User:                 {GITHUB_USERNAME}")
print(f"Total contributions:  {total_contributions}")
print(f"Private contributions:{private_contributions}")
print(f"Commits:              {commits}")
print(f"Issues:               {issues}")
print(f"Pull requests:        {pull_requests}")
print(f"Reviews:              {reviews}")
print(f"Private percentage:   {private_percentage}%")
print(f"Output:               {output_path}")
print("==============================================")
