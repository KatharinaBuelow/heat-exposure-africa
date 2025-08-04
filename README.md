#Changing Population Exposure to Extreme Heat Days in Africa


This repository documents the procedure used to develop maps of climate heat indicators for Africa based on [CORDEX AFR-22](https://cordex.org/experiment-guidelines/cordex-cmip5/cordex-core/cordex-core-simulations/) data.

We follow the workflow described in the paper:

**Weber, T., Bowyer, P., Rechid, D., Pfeifer, S., Raffaele, F., Remedio, A. R., et al. (2020). Analysis of compound climate extremes and exposed population in Africa under two different emission scenarios. Earth's Future, 8, e2019EF001473. https://doi.org/10.1029/2019EF001473**


##Ingredients:

### Climate Index

For the calculation of the Number of extrem heat days (maximum temperature > 40°C) we use the [index_calculator](https://github.com/climate-service-center/index_calculator). This is using [xclim](https://github.com/Ouranosinc/xclim)

### Future Population

The information about the [population](population.md) data source. 

With the following Notebook you can remap the population files and with the second Notebook you can calculate the country sum of the population for different time slices and compare their development.
(Katharina environment xesmv_env)

    Notebooks/remap_population_to_afr22.ipynb

## Plotting 


## Exposure

The change of population and the climate change signal for specific indicators are combined. [Literature] (exposure.md)

For the climate change signal, you can follow the steps as before and use the output of *climate_fact_data*. (environmet-Katharina: afrheat)

    Notebooks/horiplot-exposure-diff-robust-bulletin.ipynb
    Notebooks/plotting_tools_exposure.py


