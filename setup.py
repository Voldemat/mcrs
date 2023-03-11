import os
from pathlib import Path

from setuptools import setup  # type: ignore [import]


setup(
    name="mcrs",
    version=os.environ["GITHUB_REF_NAME"],
    description="Package for microservices",
    author="Vladimir Vojtenko",
    author_email="vladimirdev635@gmail.com",
    license="MIT",
    packages=["mcrs", "mcrs.lifespan", "mcrs.environment"],
    package_data={
        "mcrs": ["py.typed"],
        "mcrs.lifespan": ["py.typed"],
        "mcrs.environment": ["py.typed"],
    },
    long_description=(Path(__file__).parent / "README.md").read_text(),
    long_description_content_type="text/markdown",
)
