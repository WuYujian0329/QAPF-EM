# QAPF-EM reproducibility archive

This archive accompanies the manuscript *Quantum annealing penalized fusion expectation-maximization for Gaussian mixture estimation* by Yujian Wu and Weigang Wang.

## Repository contents

- `data/simulation_results.csv`: complete results for five methods in nine simulation settings (45 method-setting rows).
- `data/real_data_results.csv`: complete results for Iris, Wine, and Seeds (15 method-data rows).
- `data/thesis_experiment_datasets.xlsx`: source workbook for the three benchmark data sets and their standardized forms.
- `docs/supplementary.pdf`: generating parameters, algorithm settings, full numerical tables, and proof details.
- `src/qapf_em/`: callable complete-observation QAPF-EM implementation and CEM, DAEM, SEM, and SAEM baselines.
- `run_demo.py`: deterministic deletion sanity check that starts from four components for two-component synthetic data and prints estimated and generating parameters.
- `validate_archive.py`: dependency-free integrity check for the two archived CSV files.

## Benchmark data workbook

`data/thesis_experiment_datasets.xlsx` contains the six sheets used by the accompanying manuscript:

- `Iris_Raw` and `Iris_Standardized` (150 observations, four features).
- `Wine_Raw` and `Wine_Standardized` (178 observations, 13 features).
- `Seeds_Raw` and `Seeds_Standardized` (210 observations, seven features).

## Code status

The complete-observation core is callable: it implements Gaussian-mixture likelihoods, quantum responsibilities, both penalties, component deletion, mean fusion, covariance regularization, joint BIC-style tuning, and the five comparison estimators. The minimal example starts from four separated quantile initial centres for data generated from two components and uses a demonstration-only weight penalty (lambda = 0.01) to make the deletion step observable. It is not one of the manuscript's nine simulation settings and does not replace the manuscript parameter lambda = 0.0004. Run it with:

```bash
pip install -r requirements.txt
python run_demo.py
```

The archived data and numerical results can be checked with:

```bash
python validate_archive.py
```

The repository does not yet include a scripted end-to-end regeneration of every manuscript table from fixed seeds; do not claim exact numerical reproduction from this archive alone.

## Data dictionary

Both CSV files use one row per method and experimental setting. Columns ending in `_mean` and `_sd` report the mean and standard deviation over 30 runs. Deterministic methods can have a standard deviation of zero. Accuracy and ARI are larger-is-better; NLL and the three parameter MSE measures are smaller-is-better.

Simulation fields:

- `dimension`: feature dimension (1, 2, or 3).
- `model`: simulation-model index (1, 2, or 3).
- `components`: generating component count (2, 4, or 6).
- `method`: CEM, DAEM, SEM, SAEM, or QAPF-EM.

Real-data fields:

- `data`: Iris, Wine, or Seeds.
- `method`: CEM, DAEM, SEM, SAEM, or QAPF-EM.

## Recommended public-release steps

1. Add automated unit tests for responsibility normalization, limiting cases, deletion/reordering, covariance regularization, and metric calculations.
2. Add one command that regenerates the CSV files from fixed seeds.
3. Compare regenerated values with `data/*.csv` within documented numerical tolerances.
4. Add an open-source license chosen by the authors, then create a tagged GitHub release and archive it with Zenodo to obtain a permanent DOI.

## Citation

Please cite the accompanying article. Bibliographic details and a DOI should be added here after acceptance.
