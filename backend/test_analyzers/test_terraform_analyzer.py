from app.analyzers.terraform_analyzer import (
    TerraformAnalyzer,
)
from test_analyzers.utils import (
    select_repository,
)

repository = select_repository()

analyzer = TerraformAnalyzer(repository)

result = analyzer.analyze()

print(result)

# command to run from /backend directory

# python -m test_analyzers.test_terraform_analyzer