# L2IT Internship

## Testing general relativity with LISA gravitational waves

This repository brings together the code and analysis from my M2 internship at the **Laboratoire des 2 Infinis – Toulouse (L2IT)**, where I worked with **Sylvain Marsat** and **Manuel Piarulli**.

My project explored how non-GR deviations in the merger and ringdown of a massive black-hole binary (MBHB) could affect what we recover about its inspiral. The question was whether a signal with deviations from general relativity only in its late stages could lead us to recover an apparent deviation in the inspiral when analysing the full waveform with LISA.

## About the work

I generated waveforms with modified ringdown frequencies and damping times using `pSEOBNRv5HM`. To use these signals in the frequency-domain analysis, I applied the amplitude ratios and phase differences between the modified and GR waveforms, mode by mode, to `SEOBNRv5HMROM`. I then used `lisabeta` to calculate the LISA response.

For recovery, I used `SEOBNRv5HMROM` with Flexible Theory-Independent (FTI) phase corrections. Each run allowed one FTI parameter to vary alongside the usual source parameters. This let me study how a change introduced in the ringdown could shift the recovered inspiral parameters.

I estimated these shifts using the Cutler–Vallisneri (CV) bias calculation and used the Fisher matrix to estimate statistical uncertainties. I also carried out Bayesian parameter estimation with `ptemcee` through `lisabeta`, then compared the posterior distributions and median shifts with the CV predictions. The comparison helps assess where the linear bias estimate describes the recovery well and where it becomes less reliable.

The notebooks cover different deviation values, masses, and mass ratios. They also include a zero-deviation test, waveform alignment using Nelder–Mead minimization, and scans where either the ringdown frequency deviation or the damping-time deviation is held fixed. Many runs use a binary with total mass $10^6\,M_\odot$, mass ratio $q=4$, and spins $\chi_1=\chi_2=0.5$.

## What is in the repository?

| Folder | What you will find |
| --- | --- |
| [`Simulating_deviations/`](Simulating_deviations/) | Early waveform studies showing how ringdown deviations and FTI parameters change the signal. |
| [`pySEOBNR_deviation_2/`](pySEOBNR_deviation_2/) | Injection generation, waveform alignment, Fisher and CV calculations, and their plots and summary tables. |
| [`PE_for_my_work/`](PE_for_my_work/) | Bayesian recovery configurations, scripts for creating and submitting cluster jobs, and notebooks for analysing the posteriors and comparing them with the CV estimates. |

Within `pySEOBNR_deviation_2`, the folders `Dense scan`, `Mass ratio test`, `Null test corrected`, `domega fixed`, and `dtau fixed` contain the corresponding studies. The `Data` folder includes generation manifests and saved analysis outputs.

Within `PE_for_my_work`, the JSON configurations are in `config_files`, while `Analysis` and `Comparison` contain the posterior plots and comparisons. Several folders contain earlier or alternative versions of the notebooks that I kept during the project.

## Where to start

These files give a useful route through the main parts of the analysis:

| Task | File |
| --- | --- |
| Generate modified injections | [ROM_pSEOB_ratio_QNM_deviated_injection.ipynb](pySEOBNR_deviation_2/ROM_pSEOB_ratio_QNM_deviated_injection.ipynb) |
| Calculate Fisher uncertainties and CV biases | [CV_bias_recovery_with_FTI_parameters(3).ipynb](pySEOBNR_deviation_2/CV_bias_recovery_with_FTI_parameters%283%29.ipynb) |
| Create Bayesian recovery configurations | [json_config_creator_SEOBNRv5HMROM_params_PE_for_my_work_fixed.py](PE_for_my_work/json_config_creator_SEOBNRv5HMROM_params_PE_for_my_work_fixed.py) |
| Compare posteriors with CV predictions across injections | [PE_CV_grouped_multiple_inj_ids_violin_plots.ipynb](PE_for_my_work/Comparison/PE_CV_grouped_multiple_inj_ids_violin_plots.ipynb) |

## Running the notebooks

The main tools are Python, Jupyter, `lisabeta`, LALSuite, and `pySEOBNR`, together with NumPy, SciPy, Matplotlib, pandas, h5py, Astropy, and tqdm. Some notebooks also use seaborn. Bayesian runs use `ptemcee` and MPI, and the supplied cluster scripts use Slurm.

The analysis needs an FTI-enabled installation of `lisabeta` and LALSuite, as well as the external `SEOBNRv5HMROM` data file. The directory containing the ROM data should be set through `LAL_DATA_PATH`. A pinned software environment is not included here.

I ran the calculations at CC-IN2P3, so many notebooks and scripts still contain paths from that environment. Before running them elsewhere, update the data directories, output directories, and software paths. For Bayesian runs, also check the injection file, priors, active FTI parameter, and cluster settings in the configuration and submission scripts. **The Slurm creator scripts submit jobs as well as generate submission files.**

The usual order is to generate an injection, run its CV or Bayesian recovery, and then open the analysis notebooks with the matching outputs.

## A note on the data

Large `.h5` files are excluded from this repository. The injection arrays and posterior samples therefore need to be generated or supplied separately. The repository includes saved figures, CSV summaries, JSON manifests, and logs where available.

Injection IDs belong to individual scans. Check the corresponding `generation_manifest_*.json` and notebook settings to find the deviation values for a given ID. Some saved manifests reflect earlier settings, so make sure the configuration and data match the run you want to analyse.

## Acknowledgements

I thank Sylvain Marsat and Manuel Piarulli for their guidance during this work. The calculations use `lisabeta`, LALSuite, and `pySEOBNR`, with computing resources at CC-IN2P3.

**Asad Mahdi** · [GitHub](https://github.com/asadmahdi-phy)
