# docs-user-guide-prediction

## Q1. What the page conveys

It shows how to use `TradeSpaceRegressor` to predict where a configuration that has not been evaluated would fall: its metrics, its chart coordinates and its novelty (V - 1) relative to the fitted reference surface. It also says that such a prediction is a proposal for the next evaluation, not a result.

## Q2. The story sentence it serves

Home page: "The workflow serves design optimization and configuration management: choosing among configurations, and tracking a configuration's evaluation against the fitted reference surface." It also serves the Home page's "User guide: one page per task", with prediction as one of those tasks.

## Q3. Verdict

advances. The Home page promises a workflow for choosing among configurations, and only this page goes from configuration to the trade space. Every other part of the story starts from a table of metrics that has already been evaluated. Going by the unit list, no other unit carries the regressor or prediction from configuration.

## Q4. If "repeats"

Not applicable.

## Q8. Judged three ways

- Against the Home page: it fits the "choosing among configurations" sentence and the one-page-per-task guide. The Home page never says the package predicts from configuration, though. It lists only fit, transform, inverse_transform and score_samples, so a reader who starts from the Home page does not expect this page's estimator or its `predict`.
- Against the root page: the root page frames the method as unsupervised learning beside PCA. This page adds a supervised step on top of that, and the root page does not mention it. The page does not contradict the root page, but the root page does not lead the reader here.
- Against its own opening sentence: the opening sentence promises an answer to "where would a configuration without measurements fall?" and says the estimator composes two fits. The example and the Methods list deliver that. The example prints output, but the page does not show what it prints, and it does not explain the arguments `300, 3, 2` or the `info` value.
- A paragraph that serves none of the three: the last paragraph, "The package returns positions in the metrics. Turning a predicted or reference level into a bounded outcome…". None of the Home page, the root page or the opening question about predicting a configuration's position leads to it.

## Q9. Read twice and still could not place

- "it can leave the quantity's admissible range while the certificate holds": the page never says what "the certificate" is.
- "a breach fraction or a probability": I could not tell which outcome is meant, or why it belongs on this page.
- "predict_novelty(X_config): V - 1": V is not defined on this page. I could not tell whether V is the energy differential named on the root page or something else.
- "the pair (Z, log_v)": Z and log_v are not introduced here.
- "The regressor declares positive_only targets": I could not tell whether "declares" refers to an estimator tag or to something the user does.
