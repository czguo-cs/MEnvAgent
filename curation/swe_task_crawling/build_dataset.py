#!/usr/bin/env python3

import argparse
import json
import logging
import os
from typing import Optional
# import sys
# sys.path.append("../")
from utils import (
    extract_patches,
    extract_problem_statement_and_hints,
    Repo,
)
from filter_instances import (
    is_valid_pull,
    is_valid_instance_base,
    is_valid_instance_medium,
    is_valid_instance_high,

)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def create_instance(repo: Repo, pull: dict) -> dict:
    """
    Create a single task instance from a pull request, where task instance is:

    {
        repo (str): owner/repo this task instance is from,
        pull_number (int): number of PR this task instance is from,
        base_commit (str): SHA of the base commit PR is based on,
        patch (str): reference solution as .patch (apply to base commit),
        test_patch (str): test suite as .patch (apply to base commit),
        version (str): repository version at time of PR
    }
    """
    patch, test_patch = extract_patches(pull, repo)
    problem_statement, hint_text, all_hint_text, commit_urls = extract_problem_statement_and_hints(pull, repo)
    
    # Get version from base commit
    version = None
    try:
        version = repo.get_version_at_commit(pull["base"]["sha"])
    except Exception as e:
        logger.warning(f"Failed to get version for {repo.full_name} at {pull['base']['sha']}: {e}")
    
    return {
        "repo": repo.full_name,
        "pull_number": pull["number"],
        "instance_id": (repo.full_name + "-" + str(pull["number"])).replace(
            "/", "__"
        ),
        "issue_numbers": pull["resolved_issues"],
        "base_commit": pull["base"]["sha"],
        "patch": patch,
        "test_patch": test_patch,
        "problem_statement": problem_statement,
        "hints_text": hint_text,
        "all_hints_text": all_hint_text,
        "commit_urls": commit_urls,
        "created_at": pull["created_at"],
        "version": version if version else "0.0",
        "language":repo.language
    }


def main(pr_file: str, output: str, language:str,token: Optional[str] = None):
    """
    Main thread for creating task instances from pull requests

    Args:
        pr_file (str): path to pull request JSONL file
        output (str): output file name
        token (str): GitHub token
    """
    if token is None:
        # Get GitHub token from environment variable if not provided
        token = os.environ.get("GITHUB_TOKEN")

    def load_repo(repo_name,language):
        # Return repo object for a given repo name
        owner, repo = repo_name.split("/")
        return Repo(owner, repo, language,token=token)

    repos = dict()
    base_instances = 0
    medium_instances = 0
    high_instances = 0
    total_instances = 0
    base_output = output + ".base"
    medium_output = output + ".medium"
    high_output = output + ".high"
    seen_prs = set()

    # Continue where we left off if output file already exists
    if os.path.exists(base_output):
        with open(base_output) as f:
            for line in f:
                pr = json.loads(line)
                if "instance_id" not in pr:
                    pr["instance_id"] = (
                        pr["repo"] + "-" + str(pr["pull_number"])
                    ).replace("/", "__")
                instance_id = pr["instance_id"]
                seen_prs.add(instance_id)
                if is_valid_instance_base(pr):
                    base_instances += 1
                    if is_valid_instance_medium(pr):
                        medium_instances += 1
                        if is_valid_instance_high(pr):
                            high_instances += 1

    logger.info(f"Will skip {len(seen_prs)} pull requests that have already been inspected")

    # Write to .all file for all PRs
    write_mode_base = "w" if not os.path.exists(base_output) else "a"
    with open(base_output, write_mode_base) as base_output:
        # Write to output file for PRs with test suites
        write_mode_medium = "w" if not os.path.exists(medium_output) else "a"
        with open(medium_output, write_mode_medium) as medium_output:
                write_mode_high = "w" if not os.path.exists(high_output) else "a"
                with open(high_output, write_mode_high) as high_output:
                    for ix, line in enumerate(open(pr_file)):
                        total_instances += 1
                        pull = json.loads(line)
                        if ix % 100 == 0:
                            logger.info(
                                f"[{pull['base']['repo']['full_name']}] (Up to {ix} checked) "
                                f"base_intances: {base_instances}, medium_instances: {medium_instances}, high_instances: {high_instances}"
                            )
                        # Construct instance fields
                        instance_id = (
                            pull["base"]["repo"]["full_name"] + "-" + str(pull["number"])
                        )
                        instance_id = instance_id.replace("/", "__")
                        if instance_id in seen_prs:
                            # seen_prs -= {instance_id}
                            continue
                        if not is_valid_pull(pull):
                            # Throw out invalid PRs
                            continue
                        # Create task instance
                        repo_name = pull["base"]["repo"]["full_name"]
                        if repo_name not in repos:
                            repos[repo_name] = load_repo(repo_name,language)
                        repo = repos[repo_name]
                        try:
                            instance = create_instance(repo, pull)
                            if is_valid_instance_base(instance):
                                # If base valid, write to .base output file
                                print(
                                    json.dumps(instance), end="\n", flush=True, file=base_output
                                )  # write 
                                base_instances += 1
                                if is_valid_instance_medium(instance):
                                    # If medium valid, write to .medium output file
                                    print(json.dumps(instance), end="\n", flush=True, file=medium_output)
                                    medium_instances += 1
                                    if is_valid_instance_high(instance):
                                        # If high valid, write to .high output file
                                        print(json.dumps(instance), end="\n", flush=True, file=high_output)
                                        high_instances += 1
                        except Exception as e:
                            logger.error(f"[{repo_name}] fail to create instance for {instance_id} {e}")
                            continue
    logger.info(f"[{', '.join(repos.keys())}] 🎤 Total instances: {total_instances}, base_intances: {base_instances}, medium_instances: {medium_instances}, high_instances: {high_instances}")
    logger.info(f"[{', '.join(repos.keys())}] 🎤 Skipped {len(seen_prs)} pull requests that have already been inspected")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--pr_file", default="./keras-team__keras-contrib-selected_pulls.jsonl", type=str, help="Path to pull request JSONL file")
    parser.add_argument("--output", default="./keras-contrib-task-instances.jsonl", type=str, help="Output file name")
    parser.add_argument("--token",default=os.getenv("GITHUB_TOKEN"), type=str, help="GitHub token")
    args = parser.parse_args()
    main(**vars(args))
