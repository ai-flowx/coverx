from setuptools import setup, find_packages

setup(
    name="coverx",
    version="1.2.0",  # Placeholder. Will be replaced by dynamic versioning.
    description="Cover Agent Tool",
    author="QodoAI",
    author_email="tal.r@codium.ai",
    license="Apache 2.0",
    packages=find_packages(include=["cover_agent"]),
    install_requires=[
        "jinja2==3.1.3",
        "beautifulsoup4==4.12.3",
        "poetry-dynamic-versioning==1.3.0",
        "sqlalchemy==2.0.32",
        "diff-cover==9.1.1",
        "tenacity==9.0.0",
        "litellm==1.60.0",
        "openai==1.55.3",
        "tiktoken==0.8.0",
        "boto3==1.34.121",
        "google-cloud-aiplatform==1.54.0",
        "numpy==1.26.0",
        "dynaconf==3.2.4",
        "wandb==0.17.1",
        "grep_ast==0.3.3",
        "tree_sitter==0.21.3",
        "tree_sitter_languages==1.10.2",
        "jedi-language-server==0.41.1",
    ],
    extras_require={
        "dev": [
            "pytest==8.1.1",
            "pyinstaller==6.6.0",
            "pytest-mock==3.14.0",
            "pytest-cov==5.0.0",
            "pytest-asyncio==0.23.7",
            "pytest-timeout==2.3.1",
            "fastapi==0.111.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "cover-agent=cover_agent.main:main",
            "cover-agent-full-repo=cover_agent.main_full_repo:main",
            "generate-report=cover_agent.UnitTestDB:dump_to_report_cli",
        ]
    },
    python_requires=">=3.9,<3.13",
)
