/*
 * kitchenham.sysml -- the Kitchenham-CSC iron-triangle case as one SysML v2 model (WP76, G2).
 *
 * The method sees configurations -> attributes -> metrics. This case has no configuration space
 * and no simulator: the rows are 145 finished software projects of one company (Computer Sciences
 * Corporation, 1994 to 1999), published by Kitchenham, Pfleeger, McColl and Eagan (2002) and
 * uploaded to Zenodo as doi:10.5281/zenodo.268457 (CC BY 4.0). What the model records is every
 * decision the analysis makes before the fit, each with its rationale, so that the Python in
 * examples/kitchenham/run.py and variants.py copies nothing it cannot point to here:
 *
 *   1. the recorded project    the source columns, their units, and effort as the budget proxy
 *   2. the derived attributes  planned duration, the overrun ratios, the slack shares, scope
 *   3. the exclusion rule      which projects are kept (141 of 145)
 *   4. the metrics             orientation, the positivity shift, the scaler: the primary rule
 *   5. the alternatives        the one-change conditionings of the sensitivity ladder
 *   6. the fit                 the temperature rule, the seed, the two-term assessment
 *   7. the frontier band       the near-frontier rule and the band ladder
 *   8. the subsets and influence rules
 *   9. the question            the sign pattern the page states, as a constraint on the reading
 *
 * tests/test_wp76_kitchenham.py loads this file strictly through the opensysml client and holds
 * every constant of run.py and variants.py equal to its value here. Nothing below is a result:
 * results live in results.json and variants.json, and the page quotes them from there.
 */
package KitchenhamIronTriangle {
    private import ScalarValues::*;
    private import ISQ::*;
    private import SI::*;

    // ==========================================================================================
    // 1. THE RECORDED PROJECT: the source's columns
    // ==========================================================================================
    doc /* One row of the table is one finished project. The table records a first estimate and an
           actual for effort, an actual start date, an estimated completion date and an actual
           duration, and the delivered size in adjusted function points. It records no quality
           measure, so this case has the three sides of the triangle and nothing more. */

    enum def ProjectType {
        doc /* The source's project-type code. D is development, P perfective maintenance; A, C,
               Pr and U are the remaining codes, too few rows each to read apart (4, 2, 1, 1). */
        A; C; D; P; Pr; U;
    }

    enum def EstimateMethod {
        doc /* The source's code for how the first estimate was made; carried, not used. */
        A; C; CAE; D; EO; W;
    }

    part def RecordedProject {
        doc /* The columns read from kitchenham.arff, in the source's units. Effort stands for the
               budget: the table records hours and no money, and in this company's accounting the
               estimate and the actual are both in hours (the memo: "effort as the budget proxy"). */
        attribute project : Integer;
        attribute client : Integer;
        attribute kind : ProjectType;
        attribute actualStart : String { doc /* ISO date, YYYY-MM-DD */ }
        attribute estimatedCompletion : String { doc /* ISO date; missing in three rows */ }
        attribute actualDuration : DurationValue { doc /* days */ }
        attribute firstEstimate : DurationValue { doc /* hours of effort, the budget planned */ }
        attribute actualEffort : DurationValue { doc /* hours of effort, the budget spent */ }
        attribute adjustedFunctionPoints : Real { doc /* the delivered size: scope */ }
        attribute estimateMethod : EstimateMethod;
    }

    // ==========================================================================================
    // 2. THE DERIVED ATTRIBUTES: plans, actuals, the three sides
    // ==========================================================================================
    calc def PlannedDuration {
        doc /* The estimated completion date minus the actual start date, in days. The source gives
               no planned start, so the plan is read from the start the project actually had. */
        in estimatedCompletion : DurationValue;
        in actualStart : DurationValue;
        return planned : DurationValue = estimatedCompletion - actualStart;
    }

    calc def OverrunRatio {
        doc /* Actual over plan: 1 is on plan, above 1 an overrun. The same calc serves duration
               (actual duration over planned duration) and effort (actual effort over the first
               estimate). */
        in actual : Real;
        in plan : Real;
        return ratio : Real = actual / plan;
    }

    calc def SlackShare {
        doc /* The share of the plan left over, 1 - actual / plan: zero on plan, negative for an
               overrun. Larger is better. The two slacks of the triangle (time, money) are this
               quantity on duration and on effort. */
        in actual : Real;
        in plan : Real;
        return share : Real = 1.0 - actual / plan;
    }

    attribute def Scope :> Real {
        doc /* Adjusted function points delivered, as recorded; larger is better; not shifted. */
    }

    // ==========================================================================================
    // 3. THE EXCLUSION RULE: which projects are kept
    // ==========================================================================================
    attribute plannedDurationBound : Real = 0.0 {
        doc /* A project is kept when its planned duration is a positive number of days. Three
               rows have no estimated completion date and one row's estimated completion precedes
               its start; those four cannot carry a schedule slack and are dropped. 141 of 145 are
               kept (manifest.toml, kept_rows). */
    }

    constraint def KeptProject {
        in plannedDuration : Real;
        plannedDuration > plannedDurationBound
    }

    // ==========================================================================================
    // 4. THE METRICS: orientation, the positivity shift, the scaler (the primary rule)
    // ==========================================================================================
    enum def Orientation {
        doc /* +1: larger is better as recorded; -1: a cost, inverted by the conditioning. */
        largerIsBetter; smallerIsBetter;
    }

    enum def Scaler {
        doc /* The scaler of the log-metrics: standard (unit standard deviation), robust (unit
               interquartile range) or none (the pure logs). */
        standard; robust; none;
    }

    part def Conditioning {
        doc /* One conditioning of the three attributes into strictly positive, larger-is-better
               metrics: a shift added to both slack shares (scope is never shifted), an optional cap
               on each overrun ratio before the share is taken, the plan-over-actual alternative
               (the overrun's reciprocal, which needs no shift), and the scaler of the logs. */
        attribute shift : Real;
        attribute capOverrunAt : Real { doc /* 0 means no cap */ }
        attribute planOverActual : Boolean;
        attribute scaler : Scaler;
    }

    attribute scheduleOrientation : Orientation = Orientation::largerIsBetter {
        doc /* More schedule slack is better. */
    }
    attribute budgetOrientation : Orientation = Orientation::largerIsBetter {
        doc /* More budget slack is better. */
    }
    attribute scopeOrientation : Orientation = Orientation::largerIsBetter {
        doc /* More delivered scope is better. */
    }

    part primary : Conditioning {
        doc /* The primary rule: share of plan for both slacks with shift 10, scope unshifted,
               standard scaler of the logs. */
        attribute :>> shift = 10.0 {
            doc /* The fit needs every metric strictly positive and an overrun gives a negative
                   share. The worst overruns in the table are 8.9 times the planned duration and
                   5.9 times the first estimate, so 10, the round number above the worst, keeps
                   every shifted share positive; the smallest shifted value is 2.1. The shift bends
                   the scale (the WP70 synthetic run showed a planted exponent moving with it),
                   which is why the ladder varies it. */
        }
        attribute :>> capOverrunAt = 0.0;
        attribute :>> planOverActual = false;
        attribute :>> scaler = Scaler::standard {
            doc /* Each log-metric at unit spread, so one fit temperature means the same for the
                   three; without it scope's log-spread (about 1.1) is ten times the shifted slacks'
                   (0.14 and 0.07) and the fit reads the scale, not the projects. */
        }
    }

    calc def ShiftedSlack {
        doc /* The metric from a slack share: share + shift, strictly positive by the choice of
               shift. */
        in share : Real;
        in shift : Real;
        return metric : Real = share + shift;
    }

    constraint def StrictlyPositive {
        doc /* Every metric the fit receives is strictly positive (the package rejects negatives). */
        in metric : Real;
        metric > 0.0
    }

    // ==========================================================================================
    // 5. THE ALTERNATIVES: one change each from the primary rule (the conditioning ladder)
    // ==========================================================================================
    doc /* The ladder of WP70, kept as the sensitivity check of G3: each part changes one thing. */

    part robustScaler : Conditioning {
        doc /* The robust scaler (unit interquartile range) in place of the standard one. */
        attribute :>> shift = 10.0;
        attribute :>> capOverrunAt = 0.0;
        attribute :>> planOverActual = false;
        attribute :>> scaler = Scaler::robust;
    }
    part noScaler : Conditioning {
        doc /* No scaler: the pure logs, where scope's spread is ten times the slacks'. */
        attribute :>> shift = 10.0;
        attribute :>> capOverrunAt = 0.0;
        attribute :>> planOverActual = false;
        attribute :>> scaler = Scaler::none;
    }
    part shift20 : Conditioning {
        doc /* Twice the primary shift, to see what the shift does to the exponents. */
        attribute :>> shift = 20.0;
        attribute :>> capOverrunAt = 0.0;
        attribute :>> planOverActual = false;
        attribute :>> scaler = Scaler::standard;
    }
    part shift40 : Conditioning {
        doc /* Four times the primary shift. */
        attribute :>> shift = 40.0;
        attribute :>> capOverrunAt = 0.0;
        attribute :>> planOverActual = false;
        attribute :>> scaler = Scaler::standard;
    }
    part cap3Shift3 : Conditioning {
        doc /* Each overrun ratio capped at 3 before the share is taken, so the worst overruns no
               longer set the shift; shift 3 then clears the worst capped share (-2). */
        attribute :>> shift = 3.0;
        attribute :>> capOverrunAt = 3.0;
        attribute :>> planOverActual = false;
        attribute :>> scaler = Scaler::standard;
    }
    part planOverActualRule : Conditioning {
        doc /* Plan over actual for both slacks, no shift: the log is the overrun's log with its
               sign turned, the one form in which a planted monomial stays a monomial (WP70). */
        attribute :>> shift = 0.0;
        attribute :>> capOverrunAt = 0.0;
        attribute :>> planOverActual = true;
        attribute :>> scaler = Scaler::standard;
    }

    // ==========================================================================================
    // 6. THE FIT: the temperature rule, the seed, the two-term assessment
    // ==========================================================================================
    part fitRule {
        doc /* The one-term fit at the temperature that puts a tenth of the projects above V = 1,
               as the other example pages fit; the two-term fit at the same temperature with five
               restarts, read for whether a second term holds any near-frontier project. */
        attribute targetFractionAbove : Real = 0.10 {
            doc /* The share of projects the fitted surface leaves above it; the rule every
                   example page uses, so the temperatures compare across cases. */
        }
        attribute temperatureLowerBound : Real = 3.0 {
            doc /* The search bounds of select_temperature, the example pages' (3, 10^4). */
        }
        attribute temperatureUpperBound : Real = 10000.0 {
            doc /* The upper search bound; a fit at it would be the exact maximum in all but name. */
        }
        attribute seed : Integer = 0 {
            doc /* The random state of the fits, the example pages' 0, so a rerun is the run. */
        }
        attribute twoTermRestarts : Integer = 5 {
            doc /* Restarts of the two-term fit, the example pages' five; the best of them is kept. */
        }
    }

    // ==========================================================================================
    // 7. THE FRONTIER BAND: the near-frontier rule and the band ladder
    // ==========================================================================================
    part bandRule {
        doc /* Near the frontier means |log V| below the band. The package's default band is 1 / tau,
               which at 141 projects can hold fewer rows than an association can be read from; the
               rule widens it to the smallest band holding minNearFrontier projects and records the
               widening. The band ladder reads the association at 1 / tau and at the bands holding
               10, 15, 20 and 25 projects, so a reader sees how the reading moves with the band. */
        attribute minNearFrontier : Integer = 15 {
            doc /* Fifteen: enough rows for a sign to be read, few enough to stay near the surface
                   (a tenth of 141 is 14). The WP70 probe's rule. */
        }
        attribute reportGuard : Integer = 10 {
            doc /* The package's own guard: trade_off_report refuses an association from fewer
                   rows; left at its default. */
        }
        attribute ladderCounts : Integer[4] = (10, 15, 20, 25) {
            doc /* The band ladder: the report's guard (10), the rule (15), and two wider bands. */
        }
    }

    calc def NearFrontierBand {
        doc /* max(1 / tau, the smallest band holding minNearFrontier rows). */
        in tau : Real;
        in bandHoldingMinRows : Real;
        return band : Real = if 1.0 / tau > bandHoldingMinRows ? 1.0 / tau else bandHoldingMinRows;
    }

    constraint def NearFrontier {
        in logV : Real;
        in band : Real;
        logV < band and logV > -band
    }

    // ==========================================================================================
    // 8. THE SUBSETS AND THE INFLUENCE RULES
    // ==========================================================================================
    part def Subset {
        doc /* The primary rule refitted on one part of the portfolio; the contrast WP70 ran and the
               memo keeps ("Retain the project-type and client subset contrasts"). */
        attribute selection : String;
    }
    part developmentOnly : Subset {
        doc /* The 50 development projects: new systems, the type the triangle is usually told about. */
        attribute :>> selection = "kind == ProjectType::D";
    }
    part perfectiveOnly : Subset {
        doc /* The 73 perfective-maintenance projects, the table's largest type. */
        attribute :>> selection = "kind == ProjectType::P";
    }
    part largestClientOnly : Subset {
        doc /* Client 2, 113 of the 141 projects: one client's portfolio inside the company's. */
        attribute :>> selection = "client == 2";
    }

    part influenceRule {
        doc /* Every project left out in turn, the temperature held at the primary's so the change
               is the row's; a project is influential when its removal changes a sign of the
               near-frontier association or moves an exponent by the threshold or more. The named
               extremes (the largest project, the worst schedule overrun, the worst budget overrun)
               are also removed one at a time with the temperature reselected, as a reader would. */
        attribute exponentMoveThreshold : Real = 0.05 {
            doc /* A move of 0.05 on the simplex is about the spread of exponents across the
                   ladder's neighbouring rungs; smaller moves are the fit's own. */
        }
    }

    // ==========================================================================================
    // 9. THE QUESTION: the sign pattern the page states
    // ==========================================================================================
    constraint def HeadlinePattern {
        doc /* The memo's question as a reading of the near-frontier association: did greater
               delivered scope accompany less schedule and budget slack (both associations with
               scope negative), and did the two slacks move together (their association positive)?
               The page states the pattern only on the rows of the ladders where it holds. */
        in scheduleScope : Real;
        in budgetScope : Real;
        in scheduleBudget : Real;
        scheduleScope < 0.0 and budgetScope < 0.0 and scheduleBudget > 0.0
    }
}
