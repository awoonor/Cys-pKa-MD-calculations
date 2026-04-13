# Cys-pKa-MD-calculations

This repository contains a suite of automated scripts designed to streamline **Replica-Exchange Thermodynamic Integration Molecular Dynamics (RETI-MD)** calculations for predicting Cysteine pK<sub>a</sub> values. The workflow is optimized for use with the **GROMACS** molecular dynamics engine and is managed via the **PBS job scheduler**.

## 📁 Repository Structure

* **`scripts/`** Contains the core Python and Bash scripts used to set up, automate, and analyze the RETI-MD calculations.
* **`mdp_templates/`** Standard GROMACS `.mdp` parameter files required for running the minimization, equilibration, and RETI-MD production phases.
* **`example_PDB/`** Sample input files and directory structures to help users test the workflow and run their first calculation.

## ⚙️ Dependencies & Requirements

To successfully utilize these scripts, you will need the following installed in your environment:
* **GROMACS** (Compatible version for RETI calculations)
* **Python** (version 3.x recommended)
* A computing cluster running the **PBS job scheduler**

## 📝 Citations

The methodologies employed and automated within these scripts were developed and utilized in the following publications. If you use these scripts in your research, please cite:

> **Awoonor-Williams, E., and Rowley, C. N.** Evaluation of Methods for the Calculation of the pK<sub>a</sub> of Cysteine Residues in Proteins. *Journal of Chemical Theory and Computation (JCTC)*, **2016**, 12(9), 4662-4673.  
> **DOI:** [10.1021/acs.jctc.6b00631](https://pubs.acs.org/doi/10.1021/acs.jctc.6b00631)

> **Awoonor-Williams, E., and Rowley, C. N.** Molecular Simulation of the pK<sub>a</sub> of Cysteine Residues in Proteins Using a Generalized Born Model. *Journal of Chemical Information and Modeling (JCIM)*, **2018**, 58(9), 1935-1946.  
> **DOI:** [10.1021/acs.jcim.8b00454](https://pubs.acs.org/doi/10.1021/acs.jcim.8b00454)
