from app.analyzers.github_actions_analyzer import (
    GitHubActionsAnalyzer,
)
from test_analyzers.utils import (
    select_repository,
)

repository = select_repository()

analyzer = GitHubActionsAnalyzer(repository)

print(analyzer.analyze())

# command to run from /backend directory

# python -m test_analyzers.test_github_actions_analyzer