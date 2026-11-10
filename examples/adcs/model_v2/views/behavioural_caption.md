Sources, verification and groups (read from the model by the views generator):

- The analysis `SlewExperiment` returns 8 of the 9 traded metrics. The settling time is read from `SlewMeasurement` and is not returned. The control effort is an input of the analysis that it returns unchanged, so its arrow starts at `SlewMeasurement`, where the value is measured.
- The pointing error and the total mass are computed from the configuration alone, with no slew; their requirements are verified in `ConfigurationVerification`, the others in `SlewVerification`.
- The groups are the analyst's grouping of the metrics (the model has no such structure); a requirement stands in the group of the metric it reads. The 3 requirements that read no traded metric stand apart here; the coupling table of `coverage.md` lists each under the group of the calc it reads.
- Not drawn: the coupling variables between the groups and the measured inputs the analysis takes. They are the cells of the coupling table of `coverage.md`.
