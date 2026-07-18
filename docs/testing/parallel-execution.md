# Parallel Test Execution

## Current Support

Framework unit tests may be executed with pytest-xdist.

API integration tests support limited parallel execution using:

```bash
pytest -m "api and regression" \
  --env=local \
  -n 2 \
  --dist loadscope