import json
import time
from itertools import cycle
import os
import fire
import requests
from rich.console import Console
from rich.progress import BarColumn, Progress, TextColumn
import random
BASE_URL = "https://api.github.com/search/repositories"


def load_tokens(tokens_file):
    with open(tokens_file, "r") as f:
        tokens = [line.strip() for line in f if line.strip()]
    if not tokens:
        raise ValueError("Token file is empty!")
    return cycle(tokens)


def make_query(language, stars_min, stars_max):
    parts = []
    if language:
        parts.append(f"language:{language}")
    if stars_min is not None and stars_max is not None:
        parts.append(f"stars:{stars_min}..{stars_max}")
    elif stars_min is not None:
        parts.append(f"stars:>={stars_min}")
    elif stars_max is not None:
        parts.append(f"stars:<={stars_max}")
    # parts.append("topic:django")
    return " ".join(parts)


def github_api_request(session, token_cycle, url, params=None):
    """Make a request to GitHub API with rotating tokens and retry on rate limit."""
    while True:
        token = next(token_cycle)
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        resp = session.get(url, headers=headers, params=params)
        if resp.status_code == 403:
            # Rate limit, try next token
            time.sleep(1)
            continue
        resp.raise_for_status()
        return resp.json()


def get_total_count(session, token_cycle, query):
    params = {"q": query, "per_page": 1}
    data = github_api_request(session, token_cycle, BASE_URL, params)
    return data.get("total_count", 0)


def fetch_repos_in_range(session, token_cycle, query, progress, task):
    all_items = []
    per_page = 100
    max_pages = 10

    for page in range(1, max_pages + 1):
        params = {
            "q": query,
            "sort": "stars",
            "order": "desc",
            "per_page": per_page,
            "page": page,
        }
        data = github_api_request(session, token_cycle, BASE_URL, params)
        items = data.get("items", [])
        if not items:
            break

        progress.update(task, advance=len(items))
        all_items.extend(items)

        if len(items) < per_page:
            break

    return all_items


def bfs_star_range(
    session, token_cycle, language, stars_min, stars_max, progress, task
):
    queue = [(stars_min if stars_min is not None else 0, stars_max)]
    all_results = []

    while queue:
        s_min, s_max = queue.pop(0)
        query = make_query(language, s_min, s_max)

        try:
            total_count = get_total_count(session, token_cycle, query)
            progress.log(
                f"[bold blue]Query:[/bold blue] {query}, [bold blue]Total:[/bold blue] {total_count}"
            )
        except Exception as e:
            progress.log(f"[red]Failed getting count for query {query}: {e}[/red]")
            continue

        if total_count == 0:
            continue

        if total_count > 1000:
            if s_max is None:
                mid = s_min + 5000
                if mid <= s_min:
                    continue
                queue.append((s_min, mid))
                queue.append((mid + 1, None))
            else:
                mid = (s_min + s_max) // 2
                if mid <= s_min:
                    continue
                queue.append((s_min, mid))
                queue.append((mid + 1, s_max))
            continue

        try:
            repos = fetch_repos_in_range(session, token_cycle, query, progress, task)
            all_results.extend(repos)
        except Exception as e:
            progress.log(f"[red]Failed fetching repos for {query}: {e}[/red]")
            queue.append((s_min, s_max))
            continue

    return all_results


def crawl_github_repos(
    language="Python",
    min_stars=1000,
    max_stars=None,
    tokens_file=".cache/tokens.txt",
    output_file="repos.jsonl",
    reponame=None,
):
    # Check if output directory exists, create if not
    if not os.path.exists(os.path.dirname(output_file)):
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

    console = Console()

    session = requests.Session()
    token_cycle = load_tokens(tokens_file)

    progress = Progress(
        "[progress.description]{task.description}",
        BarColumn(),
        TextColumn("Fetched [bold blue]{task.completed}[/bold blue] repos"),
        console=console,
    )

    with progress:
        task_id = progress.add_task("Fetching Repositories...", total=None)

        if reponame:
            progress.log(f"[bold cyan]Fetching single repo:[/bold cyan] {reponame}")
            try:
                token = next(token_cycle)
                headers = {
                    "Authorization": f"Bearer {token}",
                    "Accept": "application/vnd.github+json",
                    "X-GitHub-Api-Version": "2022-11-28",
                }
                repo_url = f"https://api.github.com/repos/{reponame}"
                resp = session.get(repo_url, headers=headers)
                resp.raise_for_status()
                repos = [resp.json()]
                progress.update(task_id, advance=1)
            except Exception as e:
                progress.log(f"[red]Failed fetching repo {reponame}: {e}[/red]")
                repos = []
        else:
            progress.log(
                f"[bold cyan]Crawling repos with language={language}, stars=[{min_stars}, {max_stars}][/bold cyan]"
            )

            repos = bfs_star_range(
                session=session,
                token_cycle=token_cycle,
                language=language,
                stars_min=min_stars,
                stars_max=max_stars,
                progress=progress,
                task=task_id,
            )
    random.seed(42)
    random.shuffle(repos)
    # Write to .jsonl file
    with open(output_file, "w", encoding="utf-8") as f:
        for repo in repos:
            repo["language"] = language
            json.dump(repo, f)
            f.write("\n")

    console.print(
        f"\n[bold green]Done.[/bold green] Saved [bright_white]{len(repos)}[/bright_white] repos to [italic]{output_file}[/italic]"
    )


if __name__ == "__main__":
    fire.Fire(crawl_github_repos)
