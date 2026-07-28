from app.analyzers.kubernetes_analyzer import (
    KubernetesAnalyzer,
)
from test_analyzers.utils import (
    select_repository,
)

repository = select_repository()

analyzer = KubernetesAnalyzer(repository)

print(analyzer.analyze())

# command to run from /backend directory

# python -m test_analyzers.test_kubernetes_analyzer