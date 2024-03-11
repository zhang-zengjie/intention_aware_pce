# Benchmark for PCE-Facilitated Intention-Aware Control

**Authors:** Zengjie Zhang

## Requirements
 - Python `3.10` (or lower)

- `conda install -c conda-forge matplotlib`
- `conda install -c anaconda scipy`
- `conda install -c anaconda numpy`
- `conda install -c conda-forge treelib`
- `conda install -c gurobi gurobi`
- `pip install importlib-metadata`
- `conda install -c conda-forge importlib_metadata`
- `conda install -c conda-forge numpoly`

## Toolbox stlpy

This benchmark is based on the `stlpy` toolbox (https://github.com/vincekurtz/stlpy/blob/main/README.md). Please cite the source when you develop your own benchmark.

## Running scripts

- Run `compare_statistics.py` to compare PCE and Monte Carlo statistics
- Go go `commons.py` to change variables of PCE basis and specifications
- Run `main.py` to solve the optimizer

## License

For the license of the `stlpy` toolbox, refer to `stlpy/LICENSE`.
