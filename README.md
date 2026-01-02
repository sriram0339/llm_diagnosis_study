# Symptom and Prompt Generative Model and Analysis of LLM Responses

**Developers: ** Indira Sriram (CU Anschutz Medical School) and Sriram Sankaranarayanan (CU Boulder).

This repository contains the code, data and  results obtained from querying four different Large Language Models (LLMs).


- `src/` directory has all the code and data.
- `src/utils.py` contains all the useful code for querying LLMs and for parsing the results. This code is repeatedly used in the notebooks.
- `src/Generate-All-Model-Comparisons.ipynb` is a jupyter notebook that has all the analysis that was performed for this project. This is a "one stop" shop that can be run to generate all the figures, plots and data used in our analysis.
- `src/Run-More-Complex-Models-*-*.ipynb` are jupyter notebooks that were used to query the LLMs and generate responses. These notebooks should not be run since they require us to setup API keys on ChatGPT and Claude. It also requires us to setup payment on these platforms. Rather the results of running are already in the files under `data/` directory.



