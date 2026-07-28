from app.analyzers.helm_analyzer import (
    HelmAnalyzer,
)
from test_analyzers.utils import (
    select_repository,
)

repository = select_repository()

analyzer = HelmAnalyzer(repository)

print(analyzer.analyze())

# command to run from /backend directory

# python -m test_analyzers.test_helm_analyzer