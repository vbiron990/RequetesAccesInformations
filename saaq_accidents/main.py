import optparse
import os
import subprocess

from git import Repo

from core.logger.base import logger
from core.logger.base import LOG_LEVELS

MASTER_BRANCH = "main"


def increment_tag():
    """"""
    repo_path = os.path.dirname(__file__)
    repo = Repo(repo_path)
    latest_tag = sorted(repo.tags, key=lambda t: t.commit.committed_datetime)[-1]
    tag_number = float(latest_tag.name)
    new_tag = f"{int(tag_number + 1)}"
    tag = repo.create_tag(new_tag)
    return tag


def push(tag):
    """"""
    repo_path = os.path.dirname(__file__)
    repo = Repo(repo_path)
    repo.git.push()
    repo.remotes.origin.push(tag)


def checkout_to_latest_tag():
    """"""
    repo_path = os.path.dirname(__file__)
    repo = Repo(repo_path)

    try:
        logger.info("Stashing changes.")
        repo.git.stash()
        logger.info("Checking out {} branch.".format(MASTER_BRANCH))
        repo.git.checkout(MASTER_BRANCH)
        logger.info("Pulling latest changes from origin.")
        repo.git.pull()

        latest_tag = sorted(repo.tags, key=lambda t: float(t.name.lstrip("v")))[-1]
        logger.info("Latest Tag: {}".format(latest_tag))
        repo.git.checkout(latest_tag)
    except Exception as error:
        logger.error(error)


def log_subprocess_output(callback, pipe):
    source = u'{}'.format(pipe)

    for line in source.split("\\n"):
        if line:
            callback(line)


def update_requirements():
    """"""
    cur_dir = os.path.dirname(__file__)
    cmd = "python -m pip install -r"
    cmd += " {}/requirements.txt".format(cur_dir)

    process = subprocess.Popen(
        cmd,
        cwd=cur_dir,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate()

    log_subprocess_output(logger.debug, stdout)
    log_subprocess_output(logger.error, stderr)


if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option('-v', '--verbosity', default="2", dest='verbosity', help='change the logging level (0 - 6) default: 2')
    parser.add_option('', '--dry-run', default=False, action='store_true', dest='dry_run', help='')
    options, args = parser.parse_args()
    logger.setLevel(LOG_LEVELS[options.verbosity])

    checkout_to_latest_tag()
    update_requirements()
