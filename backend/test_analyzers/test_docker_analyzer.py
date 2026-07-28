from app.analyzers.docker_analyzer import (
    DockerAnalyzer,
)
from test_analyzers.utils import (
    select_repository,
)

repository = select_repository()

analyzer = DockerAnalyzer(repository)

print(analyzer.analyze())

# command to run from /backend directory

# python -m test_analyzers.test_docker_analyzer