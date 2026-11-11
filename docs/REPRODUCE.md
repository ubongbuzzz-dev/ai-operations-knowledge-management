# Reproduce the case-study examples

The A01 and B01 demonstrations use Python 3.10+ and its standard library. Both include fictional records and local automated tests.

From the repository root:

```bash
(cd demos/a01 && python -m unittest discover -s tests -v)
(cd demos/b01 && python -m unittest discover -s tests -v)
```

Explore the models and example outputs:

```bash
cd demos/a01
python src/a01_simulation.py fixtures/a01_fictional_scenario.json
python src/a01_simulation.py fixtures/a01_fictional_scenario.json --authorized --commit
python src/a01_simulation.py fixtures/a01_fictional_scenario.json --authorized --commit --write-fail

cd ../b01
python src/b01_reference_model.py fixtures/b01_synthetic_cases.json
```

The scripts evaluate fictional inputs locally and emit reproducible decision outputs. The separate historical case studies describe the real operational framework and its development.
