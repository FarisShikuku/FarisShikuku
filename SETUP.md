# Production Setup

## 1. Profile repository

Your profile repository should be:

`FarisShikuku/FarisShikuku`

GitHub uses the repository matching your username for the profile README.

## 2. Add the files

Copy the supplied files into that repository:

- `README.md`
- `.github/workflows/metrics.yml`
- `.github/workflows/snake.yml`
- `.github/workflows/private-stats.yml`
- `scripts/generate_private_stats.py`

The workflows create:

- `assets/metrics.svg`
- `assets/private-stats.svg`
- `assets/github-contribution-grid-snake.svg`
- `assets/github-contribution-grid-snake-dark.svg`

## 3. Create the `METRICS_TOKEN` secret

Create a GitHub Personal Access Token with access to the private repositories whose aggregate contribution data you want included.

Then add it under:

`Settings → Secrets and variables → Actions → New repository secret`

Secret name:

`METRICS_TOKEN`

Never put the token in the README or workflow files.

The metrics project documents `repo` as the optional scope for private repositories. Use the least access that works for your account and repositories.

## 4. Enable private contributions

On GitHub, enable:

`Settings → Profile → Contribution settings → Include private contributions on my profile`

This matters because GitHub can return zero restricted/private contribution counts when private contributions are not enabled for the profile.

## 5. Workflow permissions

The workflows use only:

```yaml
permissions:
  contents: write
```

The write permission is needed because the generated SVG assets are committed back to the profile repository.

## 6. Run the workflows

Open the repository's **Actions** tab and manually run:

1. `Generate GitHub Metrics`
2. `Generate Private Contribution Stats`
3. `Generate Contribution Snake`

After successful runs, refresh the profile page.

## 7. Visitor counter

The profile-view counter uses Komarev. Unlike the metrics and snake assets, a visitor counter requires a service that records views; the counter is therefore not fully self-hosted.

## 8. Pinned repositories

GitHub itself controls the actual pinned section. The README also contains a six-repository Featured Repositories table matching the repositories currently displayed as pinned on your profile.

You can change the actual GitHub pins from:

`GitHub Profile → Customize your pins`

Personal profiles support up to six pinned public repositories/gists.
