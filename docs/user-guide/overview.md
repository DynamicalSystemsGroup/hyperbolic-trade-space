# Overview

## The idea in use

You have evaluated many designs, and each came back with a handful of numbers: mass, power, settling
time, pointing error. You want the shape of the
trade: which numbers pull against each other, at what elasticity, where the evaluated designs
end, and where the table is empty.

The package answers with tensions, not variance. PCA finds the directions in which the data spread
([how the two compose](paper:sect-problem), [Appendix D.16](paper:sub-d-16));
this method finds the positive combination of the metrics along which the data stop, the binding
constraint among metrics that are all better when larger. The answer is one weight per metric, the
weights sum to one, and the metrics with positive weight in the exact-maximum fit (tau = inf)
are the ones that contend; a small weight at the fit temperature is weaker
participation. The data reveal them; you need not know in advance which dilemma or trilemma your problem holds.

The weights define a score V, a weighted geometric mean of the metrics. After a one-time
normalization V = 1 is the fitted reference surface, V below 1 is inside it and V above 1 is beyond
what the table reached.

## The pipeline

A study has five stages and the package covers the last three:

1. Sample configurations, by any scheme.
2. Evaluate each into attributes, with a simulator, a test or an assessment. The package never sees
   how: any table works, and a SysML v2 model's exported table is one source.
3. [Condition](conditioning.md) the attributes into metrics: positive, larger-is-better, comparable
   spread.
4. [Fit](fitting.md) `HyperbolicTradeSpace` to the metrics.
5. Read: the [tension report](tensions.md), the [chart](chart.md), a
   [prediction](prediction.md) from configuration.

## What you supply, what you get back

You supply a table of designs and the rule that turns attributes into metrics. You get back:

- the weights and the metrics that participate;
- the elasticities between contending metrics;
- for each design, its energy differential (level offset) to the fitted reference surface and its
  position along the surface;
- how much one metric alone would need to improve to reach the surface;
- a novelty score and candidate white space;
- the surface written back in your original attribute units;
- a stopping record, [`termination_` and `conditioning_`](termination.md), saying how far to trust
  the fit.

Where the method misleads is on the [limitations](limitations.md) page. Read it before acting on a
result.
