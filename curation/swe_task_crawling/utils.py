from __future__ import annotations

import json
import logging
import re
import requests
import time
import urllib3

from dateutil import parser
from bs4 import BeautifulSoup
from typing import Callable, Iterator, Optional
from unidiff import PatchSet
from urllib.error import URLError
from http.client import RemoteDisconnected

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

class Repo:
    def __init__(self, owner: str, name: str, language:str = "Python",token: Optional[str] = None):
        """
        Init to retrieve target repository and create ghapi tool

        Args:
            owner (str): owner of target repository
            name (str): name of target repository
            token (str): github token
        """
        self.language = language
        self.owner = owner
        self.name = name
        self.token = token
        self.api_url = 'https://api.github.com/graphql'
        self.headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        self.full_name = f"{self.owner}/{self.name}"
        # Cache for storing tags with their dates
        self._tags_cache = None
        self._tags_cache_loaded = False

    def _load_tags_cache(self):
        """
        Load all tags with their dates into cache
        """
        if self._tags_cache_loaded:
            return
        
        logger.info(f"Loading tags cache for {self.full_name}")
        
        # Get all tags
        query = """
        query($owner: String!, $name: String!) {
            repository(owner: $owner, name: $name) {
                refs(refPrefix: "refs/tags/", first: 100) {
                    nodes {
                        name
                        target {
                            oid
                        }
                    }
                }
            }
        }
        """
        variables = {
            "owner": self.owner,
            "name": self.name
        }
        
        try:
            response = self.call_api(query, variables)
            if response and response.status_code == 200:
                data = response.json()["data"]
                if data["repository"]["refs"]["nodes"]:
                    self._tags_cache = []
                    
                    # Get dates for all tags
                    for tag in data["repository"]["refs"]["nodes"]:
                        tag_oid = tag["target"]["oid"]
                        tag_query = """
                        query($owner: String!, $name: String!, $oid: GitObjectID!) {
                            repository(owner: $owner, name: $name) {
                                object(oid: $oid) {
                                    ... on Commit {
                                        committedDate
                                    }
                                }
                            }
                        }
                        """
                        tag_variables = {
                            "owner": self.owner,
                            "name": self.name,
                            "oid": tag_oid
                        }
                        
                        tag_response = self.call_api(tag_query, tag_variables)
                        if tag_response and tag_response.status_code == 200:
                            tag_data = tag_response.json()["data"]
                            if tag_data["repository"]["object"]:
                                tag_date = tag_data["repository"]["object"]["committedDate"]
                                self._tags_cache.append({
                                    "name": tag["name"],
                                    "oid": tag_oid,
                                    "date": tag_date
                                })
                                logger.debug(f"Cached tag: {tag['name']} with date: {tag_date}")
                    
                    # Sort tags by date (newest first)
                    self._tags_cache.sort(key=lambda x: parser.parse(x["date"]), reverse=True)
                    logger.info(f"Loaded {len(self._tags_cache)} tags into cache for {self.full_name}")
                    
            self._tags_cache_loaded = True
        except Exception as e:
            logger.error(f"Failed to load tags cache for {self.full_name}: {e}")
            self._tags_cache = []
            self._tags_cache_loaded = True

    def call_api(self, query: str, variables: dict = None, max_retries: int = 10) -> dict|None:
        """
        API call wrapper with rate limit handling (checks every 5 minutes if rate limit is reset)

        Args:
            query (str): GraphQL query string
            variables (dict): variables for the GraphQL query
        Return:
            values (dict): response object of `query`
        """
        attempt = 0
        while True:
            try:
                response = requests.post(self.api_url, json={'query': query, 'variables': variables}, headers=self.headers)
                if response.status_code == 200:
                    response_json = response.json()
                    rl = int(response.headers.get('x-ratelimit-remaining'))
                    if rl < 1000:
                        print(f"❗️ Waiting for 10 minutes, remaining calls for token {self.token[:20]}****: {rl}")
                        time.sleep(60 * 10)
                    if rl < 100:
                        print(f"❗️ Waiting for 1 hour, remaining calls for token {self.token[:20]}****: {rl}")
                        time.sleep(60 * 60)
                    if "data" in response_json:
                        return response
                    else:
                        raise Exception(f"GraphQL Query failed to return data: {response_json}")
                elif response.status_code == 403:
                    while True:
                        rl = response.headers.get('x-ratelimit-remaining')
                        logger.error(f"Got 403 error for token {self.token[:20]}****, wait for 5 minutes")
                        if rl > 0:
                            break
                        time.sleep(60 * 5)
                else:
                    raise Exception(f"GraphQL Query failed to run with status code {response.status_code} for token {self.token[:20]}****. {response.json()}")
            except (requests.exceptions.RequestException, URLError, RemoteDisconnected, urllib3.exceptions.MaxRetryError, requests.exceptions.ConnectTimeout) as e:
                print(f"❗️ 📢 Attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    time.sleep(20)
                    attempt += 1
                else:
                    print(f"❗️ 📢 Still got connection error after {max_retries} attempts")
                    return None
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 403:
                    while True:
                        rl = int(response.headers.get('x-ratelimit-remaining'))
                        logger.error(f"Got 403 error for token {self.token[:20]}****, wait for 5 minutes")
                        if rl > 0:
                            break
                        time.sleep(60 * 5)

    def get_file_content_at_commit(self, file_path: str, commit_sha: str) -> str:
        """
        Get file content at specific commit using GitHub API
        
        Args:
            file_path (str): path to file in repository
            commit_sha (str): commit SHA to check file at
        Returns:
            str: file content or None if not found
        """
        query = """
        query($owner: String!, $name: String!, $expression: String!) {
            repository(owner: $owner, name: $name) {
                object(expression: $expression) {
                    ... on Blob {
                        text
                    }
                }
            }
        }
        """
        variables = {
            "owner": self.owner,
            "name": self.name,
            "expression": f"{commit_sha}:{file_path}"
        }
        
        try:
            response = self.call_api(query, variables)
            if response and response.status_code == 200:
                data = response.json()["data"]
                if data["repository"]["object"]:
                    return data["repository"]["object"]["text"]
            return None
        except Exception as e:
            logger.warning(f"Failed to get file {file_path} for {self.full_name} at {commit_sha}: {e}")
            return None
    def get_version_at_commit(self, commit_sha: str) -> str:
        """
        Get repository version at specific commit by checking Git tags pointing to the commit.
        
        Args:
            commit_sha (str): commit SHA to check version for
        Returns:
            str: version string or None if not found
        """
        try:
            # Print crawling flag
            logger.info(f"🔍 Crawling version for commit: {commit_sha}")
            
            # Load tags cache if not already loaded
            self._load_tags_cache()
            
            # Get commit date
            commit_query = """
            query($owner: String!, $name: String!, $oid: GitObjectID!) {
                repository(owner: $owner, name: $name) {
                    object(oid: $oid) {
                        ... on Commit {
                            committedDate
                        }
                    }
                }
            }
            """
            commit_variables = {
                "owner": self.owner,
                "name": self.name,
                "oid": commit_sha
            }
            
            commit_response = self.call_api(commit_query, commit_variables)
            commit_date = None
            if commit_response and commit_response.status_code == 200:
                commit_data = commit_response.json()["data"]
                if commit_data["repository"]["object"]:
                    commit_date = commit_data["repository"]["object"]["committedDate"]
                    logger.debug(f"Commit {commit_sha} date: {commit_date}")
            
            # First try: exact match using cache
            if self._tags_cache:
                matching_tags = [
                    tag for tag in self._tags_cache
                    if tag["oid"] == commit_sha
                ]
                logger.debug(f"Found {len(matching_tags)} exact matching tags for commit {commit_sha}")
                
                if matching_tags:
                    # Extract version from tag name
                    tag_name = matching_tags[0]["name"]
                    tag_date = matching_tags[0]["date"]
                    logger.debug(f"Using tag: {tag_name}")
                    # Use regex pattern to extract major.minor version
                    match = re.search(r"(\d+\.\d+)(?:\.\d+)?", tag_name)
                    if match:
                        version = match.group(1)
                        # Print version and date info
                        logger.info(f"✅ Found exact match - Version: {version}, Tag: {tag_name}, Date: {tag_date}, Commit: {commit_sha}")
                        return version
                    else:
                        logger.debug(f"No version match in tag name: {tag_name}")
                else:
                    # Second try: find tag with closest date to commit
                    if commit_date and self._tags_cache:
                        # Find tag with closest date to commit
                        commit_timestamp = parser.parse(commit_date).timestamp()
                        closest_tag = min(self._tags_cache, key=lambda x: abs(parser.parse(x["date"]).timestamp() - commit_timestamp))
                        logger.debug(f"Closest tag: {closest_tag['name']} with date {closest_tag['date']}")
                        
                        # Extract version from tag name
                        tag_name = closest_tag["name"]
                        tag_date = closest_tag["date"]
                        match = re.search(r"(\d+\.\d+)(?:\.\d+)?", tag_name)
                        if match:
                            version = match.group(1)
                            # Print version and date info
                            logger.info(f"🎯 Found closest match - Version: {version}, Tag: {tag_name}, Tag Date: {tag_date}, Commit Date: {commit_date}, Commit: {commit_sha}")
                            return version
                        else:
                            logger.debug(f"No version match in closest tag name: {tag_name}")
                    else:
                        logger.debug(f"Could not get commit date or no tags in cache")
                    
                    # Fallback: use the newest tag if no date-based matching works
                    if self._tags_cache:
                        fallback_tag = self._tags_cache[0]  # Already sorted by date (newest first)
                        tag_name = fallback_tag["name"]
                        tag_date = fallback_tag["date"]
                        logger.debug(f"Using fallback tag: {tag_name}")
                        match = re.search(r"(\d+\.\d+)(?:\.\d+)?", tag_name)
                        if match:
                            version = match.group(1)
                            # Print version and date info
                            logger.info(f"🔄 Using fallback - Version: {version}, Tag: {tag_name}, Date: {tag_date}, Commit: {commit_sha}")
                            return version
                        else:
                            logger.debug(f"No version match in fallback tag name: {tag_name}")
            else:
                logger.debug(f"No tags found in cache for {self.full_name}")
            
            logger.warning(f"❌ Version not found for {self.full_name} at {commit_sha}")
            return None
            
        except Exception as e:
            logger.error(f"Failed to get version for {self.full_name} at {commit_sha}: {str(e)}")
            return None

    def get_all_loop(
        self,
        query: str,
        variables: dict,
        data_path: list[str],
        per_page: int = 100,
        num_pages: Optional[int] = None,
        quiet: bool = True,
    ) -> Iterator:
        """
        Return all values from a paginated API endpoint.

        Args:
            query (str): GraphQL query string
            variables (dict): variables for the GraphQL query
            per_page (int): number of values to return per page
            num_pages (int): number of pages to return
            quiet (bool): whether to print progress
        """
        variables.update({"per_page": per_page, "after": None})
        page = 1
        while True:
            try:
                logger.debug(f"Request variables: {variables}")  # Log the request variables
                response = self.call_api(query, variables)
                data = response.json()
                for key in data_path:
                    data = data[key]
                values = data["nodes"]
                logger.debug(f"Page {page} values: {values}")  # Log the values returned
                if not values:
                    break
                yield from values
                if not quiet:
                    rl = int(response.headers.get('x-ratelimit-remaining'))
                    logger.info(
                        f"[{self.owner}/{self.name}] Processed page {page} ({per_page} values per page). "
                        f"Remaining calls: {rl}"
                    )
                if num_pages is not None and page >= num_pages:
                    break
                if not data["pageInfo"]["hasNextPage"]:
                    break
                variables["after"] = data["pageInfo"]["endCursor"]
                page += 1
            except Exception as e:
                logger.error(
                    f"[{self.owner}/{self.name}] Error processing page {page} "
                    f"w/ token {self.token[:10]} - {e}"
                )
                while True:
                    rl = int(response.headers.get('x-ratelimit-remaining'))
                    if rl > 0:
                        break
                    logger.info(
                        f"[{self.owner}/{self.name}] Waiting for rate limit reset "
                        f"for token {self.token[:10]}, checking again in 5 minutes"
                    )
                    time.sleep(60 * 5)
        if not quiet:
            logger.info(
                f"[{self.owner}/{self.name}] Processed {(page-1)*per_page + len(values)} values"
            )

    def get_pull_commits(self, pull_number: int, quiet: bool = True) -> Iterator:
        """
        Get all commits for a pull request.
        """
        query = """
        query($owner: String!, $name: String!, $pull_number: Int!, $after: String) {
            repository(owner: $owner, name: $name) {
                pullRequest(number: $pull_number) {
                    commits(first: 100, after: $after) {
                        pageInfo {
                            endCursor
                            hasNextPage
                        }
                        nodes {
                            commit {
                                message
                                author {
                                    date
                                }
                                url
                            }
                        }
                    }
                }
            }
        }
        """
        variables = {
            "owner": self.owner,
            "name": self.name,
            "pull_number": pull_number,
            "after": None,
        }
        return self.get_all_loop(query, variables, ["data", "repository", "pullRequest", "commits"], quiet=quiet)

    def get_issue_comments(self, issue_number: int, quiet: bool = True) -> Iterator:
        """
        Get all comments for an issue.
        """
        query = """
        query($owner: String!, $name: String!, $issue_number: Int!, $after: String) {
            repository(owner: $owner, name: $name) {
                issue(number: $issue_number) {
                    comments(first: 100, after: $after) {
                        pageInfo {
                            endCursor
                            hasNextPage
                        }
                        nodes {
                            body
                            updatedAt
                        }
                    }
                }
            }
        }
        """
        variables = {
            "owner": self.owner,
            "name": self.name,
            "issue_number": issue_number,
            "after": None,
        }
        return self.get_all_loop(query, variables, ["data", "repository", "issue", "comments"], quiet=quiet)

    def get_pull(self, pull_number: int) -> dict:
        """
        Wrapper for API call to get a single PR

        Args:
            pull_number (int): number of PR to return
        """
        query = """
        query($owner: String!, $name: String!, $pull_number: Int!) {
            repository(owner: $owner, name: $name) {
                pullRequest(number: $pull_number) {
                    number
                    title
                    body
                    baseRefName
                    baseRefOid
                    baseRepository {
                        nameWithOwner
                    }
                    url
                    createdAt
                    mergedAt
                }
            }
        }
        """
        variables = {
            "owner": self.owner,
            "name": self.name,
            "pull_number": pull_number,
        }
        return self.call_api(query, variables)

    def get_issue(self, issue_number: int) -> dict:
        """
        Wrapper for API call to get a single issue
        
        Args:
            issue_number (int): number of issue to return
        """
        query = """
        query($owner: String!, $name: String!, $issue_number: Int!) {
            repository(owner: $owner, name: $name) {
                issue(number: $issue_number) {
                    number
                    title
                    body
                }
            }
        }
        """
        variables = {
            "owner": self.owner,
            "name": self.name,
            "issue_number": issue_number,
        }
        return self.call_api(query, variables)


def extract_problem_statement_and_hints(pull: dict, repo: Repo) -> tuple[str, str]:
    """
    Extract problem statement from issues associated with a pull request

    Args:
        pull (dict): PR dictionary object from GitHub
        repo (Repo): Repo object
    Return:
        text (str): problem statement
        hints (str): hints
    """
    if repo.name == "django":
        return extract_problem_statement_and_hints_django(pull, repo)

    problem_text = ""   # issue title and body
    hint_text = ""      # issue discussions (cutoff at first commit)
    all_hint_text = ""  # all issue discussions

    for issue_number in pull["resolved_issues"]:
        issue = repo.get_issue(issue_number)
        if issue is None:
            continue
        issue = issue.json()["data"]

        title = issue["repository"]["issue"]["title"] if issue["repository"]["issue"]["title"] else ""
        body = issue["repository"]["issue"]["body"] if issue["repository"]["issue"]["body"] else ""
        problem_text += f"{title}\n{body}\n"

        issue_number = issue["repository"]["issue"]["number"]
        single_hint, single_all_hint, commit_urls = _extract_hints(pull, repo, issue_number)
        hint_text += (single_hint + "\n\n")
        all_hint_text += (single_all_hint + "\n\n")

    return problem_text, hint_text, all_hint_text, commit_urls


def _extract_hints(pull: dict, repo: Repo, issue_number: int) -> list[str]:
    """
    Extract hints from comments associated with a pull request (before first commit)

    Args:
        pull (dict): PR dictionary object from GitHub
        repo (Repo): Repo object
        issue_number (int): issue number
    Return:
        issue_hint_comments: issue comments (cutoff at first commit)
        issue_all_comments: issue comments
        commit_urls: list of commit urls
    """
    # Get all commits in PR
    commits = repo.get_pull_commits(pull["number"])

    commits = list(commits)
    if len(commits) == 0:
        # If there are no comments, return no hints
        return "", "", []

    # Get time of first commit in PR
    commit_time = commits[0]["commit"]["author"]["date"]  # str
    commit_time = parser.parse(commit_time).timestamp()

    # Get commit urls
    commit_urls = []
    for commit in commits:
        commit_urls.append(commit["commit"]["url"])

    # Get all comments in issue
    all_issue_comments = repo.get_issue_comments(issue_number)
    all_issue_comments = list(all_issue_comments)
    # Iterate through all comments, only keep comments created before first commit
    issue_hint_comments = list()
    issue_all_comments = list()
    for comment in all_issue_comments:
        comment_time = time.mktime(
            time.strptime(comment["updatedAt"], "%Y-%m-%dT%H:%M:%SZ")
        )  # use updated_at instead of created_at
        if comment_time < commit_time:
            # only include information available before the first commit was created
            issue_hint_comments.append(comment)
        issue_all_comments.append(comment)
    assert len(issue_hint_comments) <= len(issue_all_comments)

    # Keep text from comments
    issue_hint_comments = "\n".join([comment["body"] for comment in issue_hint_comments])
    issue_all_comments = "\n".join([comment["body"] for comment in issue_all_comments])
    # return issue_hint_comments, issue_all_comments
    return issue_hint_comments, issue_all_comments, commit_urls


def wrapped_requests_get(url: str, max_retries: int = 10) -> requests.Response:
    attempt = 0
    while attempt < max_retries:
        try:
            response = requests.get(url)
            return response
        except requests.exceptions.HTTPError as e:
            logger.info(f"Resource not found: {e}")
            return None
        except (requests.exceptions.RequestException, URLError, RemoteDisconnected, \
            urllib3.exceptions.MaxRetryError, requests.exceptions.ConnectTimeout)  as e:
            print(f"❗️ 📢 Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(20)
                attempt += 1
            else:
                print(f"❗️ 📢 Still got connection error after {max_retries} attempts")
                return None

def extract_patches(pull: dict, repo: Repo) -> tuple[str, str]:
    """
    Get patch and test patch from PR

    Args:
        pull (dict): PR dictionary object from GitHub
        repo (Repo): Repo object
    Return:
        patch_change_str (str): gold patch
        patch_test_str (str): test patch
    """
    # patch = requests.get(pull["diff_url"]).text
    patch = wrapped_requests_get(pull["diff_url"]).text
    patch_test = ""
    patch_fix  = ""
    for hunk in PatchSet(patch):
        if any(
            test_word in hunk.path for test_word in
            ['test', 'tests', 'e2e', 'testing']
        ):
            patch_test += str(hunk)
        else:
            patch_fix += str(hunk)
    return patch_fix, patch_test


### MARK: Repo Specific Parsing Functions ###
def extract_problem_statement_and_hints_django(
    pull: dict, repo: Repo
) -> tuple[str, list[str]]:
    """
    Get problem statement and hints from issues associated with a pull request

    Args:
        pull (dict): PR dictionary object from GitHub
        repo (Repo): Repo object
    Return:
        text (str): problem statement
        hints (str): hints
    """
    text = ""
    all_hints_text = list()
    for issue_number in pull["resolved_issues"]:
        url = f"https://code.djangoproject.com/ticket/{issue_number}"
        # resp = requests.get(url)
        resp = wrapped_requests_get(url)
        if resp.status_code != 200:
            continue
        soup = BeautifulSoup(resp.text, "html.parser")

        # Get problem statement (title + body)
        issue_desc = soup.find("div", {"id": "ticket"})
        title = issue_desc.find("h1", class_="searchable").get_text()
        title = re.sub(r"\s+", " ", title).strip()
        body = issue_desc.find("div", class_="description").get_text()
        body = re.sub(r"\n+", "\n", body)
        body = re.sub(r"    ", "\t", body)
        body = re.sub(r"[ ]{2,}", " ", body).strip()
        text += f"{title}\n{body}\n"

        # Get time of first commit in PR
        commits = repo.get_all_loop(
            repo.api.pulls.list_commits, pull_number=pull["number"]
        )
        commits = list(commits)
        if len(commits) == 0:
            continue
        commit_time = commits[0].commit.author.date
        commit_time = time.mktime(time.strptime(commit_time, "%Y-%m-%dT%H:%M:%SZ"))

        # Get all comments before first commit
        comments_html = soup.find("div", {"id": "changelog"})
        div_blocks = comments_html.find_all("div", class_="change")
        # Loop through each div block
        for div_block in div_blocks:
            # Find the comment text and timestamp
            comment_resp = div_block.find("div", class_="comment")
            timestamp_resp = div_block.find("a", class_="timeline")
            if comment_resp is None or timestamp_resp is None:
                continue

            comment_text = re.sub(r"\s+", " ", comment_resp.text).strip()
            timestamp = timestamp_resp["title"]
            if timestamp.startswith("See timeline at "):
                timestamp = timestamp[len("See timeline at ") :]
            if "/" in timestamp:
                timestamp = time.mktime(time.strptime(timestamp, "%m/%d/%y %H:%M:%S"))
            elif "," in timestamp:
                timestamp = time.mktime(time.strptime(timestamp, "%b %d, %Y, %I:%M:%S %p"))
            else:
                raise ValueError(f"Timestamp format not recognized: {timestamp}")

            # Append the comment and timestamp as a tuple to the comments list
            if timestamp < commit_time:
                all_hints_text.append((comment_text, timestamp))

    return text, all_hints_text
