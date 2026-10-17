#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "playwright",
#     "typer",
#     "rich",
# ]
# ///

# ─── How to run ───
# 1. Install uv (if not installed):
#      curl -LsSf https://astral.sh/uv/install.sh | sh
# 2. Chrome must already be installed locally:
#      The script uses channel="chrome"; it downloads no browser.
# 3. Run:
#      uv run lighthouse-audit.py https://example.com
#      uv run lighthouse-audit.py https://example.com --desktop-only
#      uv run lighthouse-audit.py https://example.com --threshold 95
# ──────────────────

"""Lighthouse audit via real Playwright Chrome.

Follows the frontend skill perfection ruleset:
  - NEVER use `lighthouse` CLI (uses headless-shell, not real Chrome)
  - Use Playwright with channel="chrome" (real Chrome stable)
  - Run lighthouse Node API via the Playwright CDP endpoint
  - Mobile preset (primary) + Desktop preset (secondary)
  - 100 in every category is the floor
"""

from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path

AUDIT_RUNTIME = Path('/home/secc/.local/share/opencode-skill-runtimes/frontend-audit')

import typer
from rich import print as rprint
from rich.table import Table


# Lighthouse config as Node.js script — run via subprocess
LIGHTHOUSE_RUNNER_JS = """\
import lighthouse from 'lighthouse';

const url = process.argv[2];
const port = parseInt(process.argv[3]);
const preset = process.argv[4];

const config = {
  extends: 'lighthouse:default',
  settings: {
    formFactor: preset === 'desktop' ? 'desktop' : 'mobile',
    throttling: preset === 'desktop'
      ? { rttMs: 40, throughputKbps: 10240, cpuSlowdownMultiplier: 1 }
      : undefined,
    screenEmulation: preset === 'desktop'
      ? { mobile: false, width: 1350, height: 940, deviceScaleFactor: 1 }
      : undefined,
    onlyCategories: ['performance', 'accessibility', 'best-practices', 'seo'],
  },
};

(async () => {
  const result = await lighthouse(url, { port, logLevel: 'error' }, config);
  const categories = result.lhr.categories;
  const output = {};
  for (const [key, cat] of Object.entries(categories)) {
    output[key] = Math.round(cat.score * 100);
  }
  console.log(JSON.stringify(output));
})();
"""


def _check_node_deps() -> bool:
    """Resolve the skill-local Lighthouse dependency."""
    result = subprocess.run(
        ["node", "--input-type=module", "-e", "await import('lighthouse')"],
        cwd=AUDIT_RUNTIME,
        capture_output=True,
        text=True,
    )
    return result.returncode == 0


def _install_node_deps() -> None:
    """Install the pinned dependency locally without admin permissions."""
    rprint("[yellow]Installing skill-local Lighthouse...[/yellow]")
    subprocess.run(
        ["npm", "ci", "--ignore-scripts", "--no-audit", "--no-fund"],
        cwd=AUDIT_RUNTIME,
        capture_output=True,
        check=True,
    )


def _run_lighthouse_via_cdp(url: str, cdp_port: int, preset: str) -> dict[str, int]:
    """Run ESM Lighthouse from its skill-local package directory."""
    result = subprocess.run(
        ["node", "--input-type=module", "-", url, str(cdp_port), preset],
        input=LIGHTHOUSE_RUNNER_JS,
        cwd=AUDIT_RUNTIME,
        capture_output=True,
        text=True,
        timeout=120,
    )
    if result.returncode != 0:
        rprint(f"[red]Lighthouse failed:[/red] {result.stderr}")
        raise SystemExit(1)
    return json.loads(result.stdout.strip())


def _run_with_playwright(url: str, preset: str) -> dict[str, int]:
    """Launch real Chrome via Playwright, run Lighthouse against CDP."""
    from playwright.sync_api import sync_playwright

    with tempfile.TemporaryDirectory(prefix="opencode-lighthouse-") as profile, sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            profile,
            channel="chrome",
            headless=True,
            args=["--remote-debugging-port=0"],
        )

        try:
            cdp_port = int((Path(profile) / "DevToolsActivePort").read_text().splitlines()[0])
            scores = _run_lighthouse_via_cdp(url, cdp_port, preset)
        finally:
            context.close()

    return scores


def _print_scores(scores: dict[str, int], preset: str, threshold: int) -> bool:
    """Print scores as a rich table. Returns True if all pass."""
    table = Table(title=f"Lighthouse — {preset}")
    table.add_column("Category")
    table.add_column("Score", justify="right")
    table.add_column("Status")

    all_pass = True
    for category, score in scores.items():
        status = "[green]✓ PASS[/green]" if score >= threshold else "[red]✗ FAIL[/red]"
        if score < threshold:
            all_pass = False
        color = "green" if score >= threshold else "red"
        table.add_row(category, f"[{color}]{score}[/{color}]", status)

    rprint(table)
    return all_pass


def main(
    url: str = typer.Argument(help="URL to audit"),
    threshold: int = typer.Option(100, "--threshold", "-t", help="Minimum passing score"),
    desktop_only: bool = typer.Option(False, "--desktop-only", help="Skip mobile audit"),
    mobile_only: bool = typer.Option(False, "--mobile-only", help="Skip desktop audit"),
) -> None:
    """Run Lighthouse audit via real Playwright Chrome."""
    # Check node deps
    if not _check_node_deps():
        _install_node_deps()

    all_pass = True

    if not desktop_only:
        rprint(f"\n[bold]Auditing (mobile):[/bold] {url}")
        mobile_scores = _run_with_playwright(url, "mobile")
        if not _print_scores(mobile_scores, "Mobile", threshold):
            all_pass = False

    if not mobile_only:
        rprint(f"\n[bold]Auditing (desktop):[/bold] {url}")
        desktop_scores = _run_with_playwright(url, "desktop")
        if not _print_scores(desktop_scores, "Desktop", threshold):
            all_pass = False

    if all_pass:
        rprint("\n[green bold]✓ All categories passed![/green bold]")
    else:
        rprint(f"\n[red bold]✗ Some categories below {threshold}. Not done yet.[/red bold]")
        raise SystemExit(1)


if __name__ == "__main__":
    typer.run(main)
