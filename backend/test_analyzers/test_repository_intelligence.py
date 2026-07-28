from pprint import pprint

from app.analyzers.repository_intelligence import (
    RepositoryIntelligence,
)
from test_analyzers.utils import (
    select_repository,
)

repository = select_repository()

analyzer = RepositoryIntelligence(repository)

result = analyzer.analyze()

pprint(result, sort_dicts=False)

# command to run from /backend directory

# python -m test_analyzers.test_repository_intelligence