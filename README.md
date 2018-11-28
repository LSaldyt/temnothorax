# Temnothorax Decision Models
Overview of several python models of ant decision making

This repository contains (at time of writing) 5 models:
 - Granivoskiy 2012, agent based
 - Pratt 2002, ordinary differential equations
 - Pratt 2005, agent based
 - Saldyt 2018, ordinary differential equations
 - Saldyt 2018, agent-based

The Pratt 2005 model is largely superseded by the Granivoskiy 2012 model, and the Pratt 2002 model is improved in the Saldyt 2018 differential equation model. The Saldyt 2018 agent-based model only models the core dynamics of Granivoskiy 2012 and Pratt 2005. 

The following plot shows convergence times based on nest distance:
![Image](https://github.com/LSaldyt/temnothorax/blob/master/saldyt_2018/distance_convergance_times_t_over_10.png)

The following plot shows convergence times based on nest quality:
![Image](https://github.com/LSaldyt/temnothorax/blob/master/saldyt_2018/convergance_times.png)
