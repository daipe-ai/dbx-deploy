from argparse import ArgumentParser


def add_common_repos_args(argument_parser: ArgumentParser):
    argument_parser.add_argument("--repo-url", dest="repo_url", help="Project repo url")
    argument_parser.add_argument("--repo-name", dest="repo_name", help="Project repo name")
    argument_parser.add_argument("--branch", dest="branch", help="Branch to checkout")
    argument_parser.add_argument("--tag", dest="tag", help="Tag to checkout")
