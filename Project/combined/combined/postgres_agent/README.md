# cbtsql Python Package

cbtsql is a package for building constrained SQL agents that generate, validate, and execute SQL queries, saving results as Parquet files.

## Installation

You can install cbtsql via pip (after publishing):

```bash
pip install cbtsql
```

Or directly from your GitLab repository:

```bash
pip install git+https://gitlab.nzminds.in/your-namespace/cbtsql.git
```

## Usage

Import and use cbtsql in your Python code:

```python
from cbtsql.cbtsql import create_constrained_sql_agent
from cbtsql.cbtsqltool import ConstrainedSQLToolkit

# Initialize your toolkit and language model (llm)
toolkit = ConstrainedSQLToolkit(...)
llm = ...  # Your language model instance

# Create the agent
agent = create_constrained_sql_agent(llm, toolkit)

# Use the agent to answer questions
result = agent.invoke({"input": "Your SQL question here"})
print(result)
```

## Project Structure
- cbtsql/: The main package directory
- pyproject.toml or setup.py: Dependency and project configuration

## Requirements
- Python >=3.11,<3.14
- See `pyproject.toml` or `requirements.txt` for all dependencies

## Development
To add new dependencies, use:
```bash
poetry add <package-name>
```

## License
Specify your license here.
