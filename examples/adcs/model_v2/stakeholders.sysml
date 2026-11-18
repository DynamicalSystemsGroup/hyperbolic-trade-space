/*
 * stakeholders.sysml -- who cares about the cubesat of cubesat.sysml, and where the evidence is
 * (WP27). Its own file beside the model, applied after cubesat.sysml (and views.sysml) as one model,
 * so the model's bytes, and the hash the ledger records, do not move for it.
 *
 * Read top to bottom:
 *   1. who cares       three stakeholders, one for each objective of the decision: a sponsor (price:
 *                      the fleet cost and the launch budget), a manufacturer (the unit cost) and an
 *                      operator (performance in operation: the coverage probability and the pointing)
 *   2. their needs     concerns framing the cubesat, each held by its stakeholder and decomposed into
 *                      the engineers' requirements of cubesat.sysml that serve it; the verdict of
 *                      each named configuration on each of those requirements, engine-checked
 *   3. roll-ups        the sponsor's and the manufacturer's measures derived from the engineers':
 *                      the launch cost, the unit cost and the fleet cost (in the model, WP30), and
 *                      two ILLUSTRATIVE roll-ups, cost to build and effective life
 *   4. evidence        verification cases that verify the concerns' requirements and point at where
 *                      the evidence is logged and the environment that produced it
 *   5. coverage        the operator's measure of the fleet (WP56): the coverage probability, a
 *                      derived attribute of the fleet from its size and the pointing error, with its
 *                      two constants; the case's generator computes it beside the data of record
 *
 * The engineers' requirements, their thresholds and the tensions between them stay in
 * cubesat.sysml, at their own level; this file says which concern each serves. Nothing here is read
 * by the oracle, the coverage table, the view generator, the data or the contract; section 5's
 * coverage probability is computed by the case's generator (examples/adcs/case.py) from the data of
 * record, with the constants stated here, and a test holds the two to one value.
 */
package CubesatStakeholders {
    private import ScalarValues::*;
    private import ISQ::*;
    private import SI::*;
    private import CubesatTradeSpaceV2::*;

    // ==========================================================================================
    // 1. WHO CARES
    // ==========================================================================================
    part def Sponsor {
        doc /* Pays for the mission and answers for it. Cares about price: what the fleet costs to
               build and to launch, within the launch budget (down), and how long it serves (up).
               Reads rolled-up measures, not the engineers' detail. */
    }
    part def Manufacturer {
        doc /* Builds the satellites. Cares about the unit cost: the cost of one satellite, built and
               launched, at the fleet size it is built in (down). */
    }
    part def Operator {
        doc /* Flies the cubesat. Cares about how it performs during its operational life: that it
               slews, settles and points as asked, and that its power and energy hold up. */
    }
    part sponsor : Sponsor;
    part manufacturer : Manufacturer;
    part operator : Operator;

    // ==========================================================================================
    // 2. THEIR NEEDS: concerns framing the cubesat, each decomposed into the engineers' requirements
    // ==========================================================================================
    concern def PriceConcern {
        doc /* A need of the sponsor about the price of the mission. */
        subject c : Cubesat;
        stakeholder s : Sponsor;
    }
    concern def ManufacturingConcern {
        doc /* A need of the manufacturer about the cost of building the satellites. */
        subject c : Cubesat;
        stakeholder s : Manufacturer;
    }
    concern def PerformanceConcern {
        doc /* A need of the operator about the cubesat's performance during its operational life. */
        subject c : Cubesat;
        stakeholder s : Operator;
    }

    concern lowCost : PriceConcern {
        doc /* The fleet costs little to build and to launch. The launch cost (the MoE on the total
               mass) is bounded by the launch budget requirement; the fleet cost (a traded cost
               metric of the cost model, WP30) by the fleet cost requirement, 6,000,000 USD a fleet;
               the unit cost, the other traded cost metric, is the manufacturer's (lowUnitCost); the
               cost to build is an illustrative roll-up with no requirement on it (section 3).
               The sponsor's full fleet budget is 8,000,000 USD. The two cost limits, on the fleet
               and on the unit, are on the covered cost, a lower bound on a full costing: the bus block (structure, power, radios
               and computer), the attitude-control parts, assembly, integration and test, and
               wholesale launch. The covered cost is held under 6,000,000 USD, and the remaining
               2,000,000 USD is the allowance for what the assessment does not scope, in this order:
               the payload and its instruments; communications and the payload interface; flight
               software; environmental testing beyond the assembly line; licensing; a ground station
               network and operations; the launch slot minimum and broker fees. The figures are for
               this 12U class: a 1U series can sit below 40,000 USD a unit, larger series are
               dearer. */
        subject :>> c;
        stakeholder :>> s = sponsor;
        requirement launchBudget : LaunchBudgetRequirement;
        requirement fleetCost : FleetCostRequirement;
    }
    concern lowUnitCost : ManufacturingConcern {
        doc /* Each satellite costs little to build and to launch at the fleet size it is built in:
               the unit cost (a traded cost metric of the cost model, WP30, the fleet cost over the
               fleet size) is bounded by the unit cost requirement, 350,000 USD a satellite, on the
               covered cost as lowCost states it. It falls as the fleet grows. */
        subject :>> c;
        stakeholder :>> s = manufacturer;
        requirement unitCost : UnitCostRequirement;
    }
    concern longLife : PriceConcern {
        doc /* The cubesat serves long. The battery's cycle life falls as its eclipse depth of
               discharge grows, so the depth-of-discharge requirement serves it; the effective life
               is an illustrative roll-up of it (section 3). */
        subject :>> c;
        stakeholder :>> s = sponsor;
        requirement depthOfDischarge : DepthOfDischargeRequirement;
    }
    concern pointingAndSlewing : PerformanceConcern {
        doc /* The cubesat points the payload accurately and slews and settles in time, within what
               its wheels can store and give. */
        subject :>> c;
        stakeholder :>> s = operator;
        requirement pointingError : PointingErrorRequirement;
        requirement settled : SettledRequirement;
        requirement controlEffort : ControlEffortRequirement;
        requirement momentum : MomentumRequirement;
    }
    concern powerAndEnergy : PerformanceConcern {
        doc /* The cubesat's power and energy hold up through an orbit and through a slew in
               eclipse. The depth-of-discharge requirement serves this concern (as the eclipse
               depth of discharge) and the sponsor's long life both: the trace says so, not the
               requirement. */
        subject :>> c;
        stakeholder :>> s = operator;
        requirement power : PowerRequirement;
        requirement powerMargin : PowerMarginRequirement;
        requirement energyBalance : EnergyBalanceRequirement;
        requirement peakSlewPower : PeakSlewPowerRequirement;
        requirement batteryPeakPower : BatteryPeakPowerRequirement;
        requirement eclipseDepthOfDischarge : DepthOfDischargeRequirement;
    }

    // The baseline configuration's verdict on each concern's requirements, as the model computes them
    // (the toolkit's engine checks each statement; they restate, per concern, the satisfy statements
    // of cubesat.sysml): the baseline fails the pointing-error requirement (0.0155 against 0.0085
    // degree), so the operator's pointing concern is not met by it, and, as a single satellite,
    // the unit cost limit (461,360 against 350,000 USD), so the manufacturer's is not met either.
    satisfy lowCost.launchBudget by cubesatBaseline;
    not satisfy lowUnitCost.unitCost by cubesatBaseline;
    satisfy lowCost.fleetCost by cubesatBaseline;
    satisfy longLife.depthOfDischarge by cubesatBaseline;
    not satisfy pointingAndSlewing.pointingError by cubesatBaseline;
    satisfy pointingAndSlewing.settled by cubesatBaseline;
    satisfy pointingAndSlewing.controlEffort by cubesatBaseline;
    satisfy pointingAndSlewing.momentum by cubesatBaseline;
    satisfy powerAndEnergy.power by cubesatBaseline;
    satisfy powerAndEnergy.powerMargin by cubesatBaseline;
    satisfy powerAndEnergy.energyBalance by cubesatBaseline;
    satisfy powerAndEnergy.peakSlewPower by cubesatBaseline;
    satisfy powerAndEnergy.batteryPeakPower by cubesatBaseline;
    satisfy powerAndEnergy.eclipseDepthOfDischarge by cubesatBaseline;

    // The two contrasts' verdicts on the same requirements, as the model computes them on each
    // configuration's own slew (the engine checks each statement). A requirement that reads a
    // measured quantity has the baseline's measurement as its default, so each such statement
    // binds the `in` parameter to the configuration's recorded measurement below. The agile
    // configuration fails the launch budget (109,620 against 105,770 USD), the control effort
    // (0.112 against 0.059 N.m.s) and the peak slew power (7.4 against 2.6 W): the sponsor's low
    // cost and two of the operator's requirements. The compact configuration fails the pointing
    // error (0.008533 against 0.008495 degree), the operator's pointing concern.
    // Each of the three, as a single satellite, fails the unit cost limit (461,360, 371,455 and
    // 636,380 USD against 350,000), the manufacturer's low unit cost; the limit is read at a
    // design's own fleet size, and a fleet brings the baseline under it.
    part agileMeasurement : SlewMeasurement {
        doc /* The agile configuration's slew integrated by adcs_sim.simulate_adcs (600 s horizon,
               0.5 s step, 30 degree slew), recorded as the baseline's is in cubesat.sysml, to
               reproduce the verdicts below. A test re-measures it. */
        :>> settlingTime = 14.035843742103072 [s];
        :>> peakTorque = 0.01 [N*m];
        :>> peakMomentum = 0.055687526518579916 [N*m*s];
        :>> controlEffort = 0.1117208500927503 [N*m*s];
        :>> torqueSquaredIntegral = 0.0010405792882731359;
    }
    part compactMeasurement : SlewMeasurement {
        doc /* The compact configuration's slew, integrated and recorded as the agile one's. */
        :>> settlingTime = 71.5888092670763 [s];
        :>> peakTorque = 0.0003 [N*m];
        :>> peakMomentum = 0.006933607071907376 [N*m*s];
        :>> controlEffort = 0.020091285377954803 [N*m*s];
        :>> torqueSquaredIntegral = 5.839661452972206e-06;
    }
    not satisfy lowCost.launchBudget by cubesatAgile;
    not satisfy lowUnitCost.unitCost by cubesatAgile;
    satisfy lowCost.fleetCost by cubesatAgile;
    satisfy longLife.depthOfDischarge by cubesatAgile {
        in torqueSquaredIntegral = agileMeasurement.torqueSquaredIntegral;
    }
    satisfy pointingAndSlewing.pointingError by cubesatAgile;
    satisfy pointingAndSlewing.settled by cubesatAgile {
        in settlingTime = agileMeasurement.settlingTime;
    }
    not satisfy pointingAndSlewing.controlEffort by cubesatAgile {
        in controlEffort = agileMeasurement.controlEffort;
    }
    satisfy pointingAndSlewing.momentum by cubesatAgile {
        in peakMomentum = agileMeasurement.peakMomentum;
    }
    satisfy powerAndEnergy.power by cubesatAgile;
    satisfy powerAndEnergy.powerMargin by cubesatAgile {
        in peakTorque = agileMeasurement.peakTorque;
    }
    satisfy powerAndEnergy.energyBalance by cubesatAgile {
        in torqueSquaredIntegral = agileMeasurement.torqueSquaredIntegral;
    }
    not satisfy powerAndEnergy.peakSlewPower by cubesatAgile {
        in peakTorque = agileMeasurement.peakTorque;
    }
    satisfy powerAndEnergy.batteryPeakPower by cubesatAgile {
        in peakTorque = agileMeasurement.peakTorque;
    }
    satisfy powerAndEnergy.eclipseDepthOfDischarge by cubesatAgile {
        in torqueSquaredIntegral = agileMeasurement.torqueSquaredIntegral;
    }
    satisfy lowCost.launchBudget by cubesatCompact;
    not satisfy lowUnitCost.unitCost by cubesatCompact;
    satisfy lowCost.fleetCost by cubesatCompact;
    satisfy longLife.depthOfDischarge by cubesatCompact {
        in torqueSquaredIntegral = compactMeasurement.torqueSquaredIntegral;
    }
    not satisfy pointingAndSlewing.pointingError by cubesatCompact;
    satisfy pointingAndSlewing.settled by cubesatCompact {
        in settlingTime = compactMeasurement.settlingTime;
    }
    satisfy pointingAndSlewing.controlEffort by cubesatCompact {
        in controlEffort = compactMeasurement.controlEffort;
    }
    satisfy pointingAndSlewing.momentum by cubesatCompact {
        in peakMomentum = compactMeasurement.peakMomentum;
    }
    satisfy powerAndEnergy.power by cubesatCompact;
    satisfy powerAndEnergy.powerMargin by cubesatCompact {
        in peakTorque = compactMeasurement.peakTorque;
    }
    satisfy powerAndEnergy.energyBalance by cubesatCompact {
        in torqueSquaredIntegral = compactMeasurement.torqueSquaredIntegral;
    }
    satisfy powerAndEnergy.peakSlewPower by cubesatCompact {
        in peakTorque = compactMeasurement.peakTorque;
    }
    satisfy powerAndEnergy.batteryPeakPower by cubesatCompact {
        in peakTorque = compactMeasurement.peakTorque;
    }
    satisfy powerAndEnergy.eclipseDepthOfDischarge by cubesatCompact {
        in torqueSquaredIntegral = compactMeasurement.torqueSquaredIntegral;
    }

    // ==========================================================================================
    // 3. ROLL-UPS: the sponsor's measures from the engineers' (illustrative, read by no output)
    // ==========================================================================================
    calc def CostToBuild {
        doc /* Illustrative roll-up for the sponsor's low cost: the cost to build one satellite of
               the configuration's fleet (USD), the parts and the assembly line of the cost model
               (cubesat.sysml, section 3, WP30) over the fleet size, without the launch. It is not
               a traded metric and no requirement reads it: the traded cost metrics add the launch
               (the unit cost, the fleet cost). */
        in c : Cubesat;
        return : Real = FleetBuildCost(c) / c.fleetSize;
    }

    part def BatteryLife {
        doc /* Illustrative cycle-life rule for the battery: a reference cycle life of 10,000
               cycles at the environment's maximum depth of discharge (0.3), inversely
               proportional to the depth of discharge, one cycle per orbit. Not a cited life. */
        attribute referenceCycles : Real = 10000.0;
        attribute hoursPerYear : Real = 8766.0;
    }
    part batteryLife : BatteryLife;

    calc def EffectiveLife {
        doc /* Illustrative roll-up for the sponsor's long life: the years until the battery's cycle
               life is spent, from its eclipse depth of discharge (the traded metric, the calc
               DepthOfDischarge) by the cycle-life rule of BatteryLife, one cycle per orbit. It is
               not a traded metric and no requirement reads it. */
        in c : Cubesat;
        in slewEnergy : EnergyValue;
        attribute dod : Real = DepthOfDischarge(c, slewEnergy);
        attribute cycles : Real = batteryLife.referenceCycles * (environment.maxDepthOfDischarge / dod);
        return : Real = cycles * (OrbitPeriod() / 1.0 [h]) / batteryLife.hoursPerYear;
    }

    // ==========================================================================================
    // 4. EVIDENCE: verification cases pointing at where the evidence is and what produced it
    // ==========================================================================================
    verification def EvidenceCase {
        doc /* A verification case that names its evidence: the ledger entry whose output carries
               the verdicts (examples/adcs/experiments/ledger/ledger.jsonl), the entry of the
               environment's record (paper/container/RECORD.md), the test that reads the evidence,
               and the environment that produced it (an hts-paper image id, or "host" when the
               entry was run on the host and its platform field names the machine). The model
               carries the pointer; the repository carries the evidence. */
        subject c : Cubesat;
        attribute ledgerEntry : String;
        attribute recordEntry : String;
        attribute testNode : String;
        attribute environment : String;
    }

    verification configurationEvidence : EvidenceCase {
        doc /* What the configuration alone decides (as ConfigurationVerification): the launch
               budget, the unit cost and the fleet cost, the pointing error and the power
               requirement, each as its concern holds it.
               Evidence: the primary dataset's verdicts, computed by the model's requirements in the
               oracle; the current entry is the WP30 data gate's container regression
               (v2-primary@12), the data of record. */
        objective {
            verify lowCost.launchBudget;
            verify lowCost.fleetCost;
            verify lowUnitCost.unitCost;
            verify pointingAndSlewing.pointingError;
            verify powerAndEnergy.power;
        }
        :>> ledgerEntry = "v2-primary@12";
        :>> recordEntry = "Container regression at the WP30 data gate (2026-11-11, image 27add815d66c, head c64430e)";
        :>> testNode = "tests/test_cubesat_oracle.py::test_the_flags_come_from_the_requirements_not_from_python";
        :>> environment = "27add815d66c";
    }
    verification slewEvidence : EvidenceCase {
        doc /* What needs the measured slew (as SlewVerification): settling, control effort,
               momentum, power margin, energy balance, peak slew power, battery peak power and depth
               of discharge, each as its concern holds it. Evidence and environment as for
               configurationEvidence; the test reads the primary and baseline datasets' feasible
               counts. */
        objective {
            verify longLife.depthOfDischarge;
            verify pointingAndSlewing.settled;
            verify pointingAndSlewing.controlEffort;
            verify pointingAndSlewing.momentum;
            verify powerAndEnergy.powerMargin;
            verify powerAndEnergy.energyBalance;
            verify powerAndEnergy.peakSlewPower;
            verify powerAndEnergy.batteryPeakPower;
            verify powerAndEnergy.eclipseDepthOfDischarge;
        }
        :>> ledgerEntry = "v2-primary@12";
        :>> recordEntry = "Container regression at the WP30 data gate (2026-11-11, image 27add815d66c, head c64430e)";
        :>> testNode = "tests/test_case.py::test_feasible_mask_counts_on_frozen_data";
        :>> environment = "27add815d66c";
    }

    // ==========================================================================================
    // 5. COVERAGE: the operator's measure of the fleet (WP56)
    // ==========================================================================================
    part def CoverageAssumptions {
        doc /* The two constants of the coverage probability. They are mission assumptions the data
               of record do not carry; the operator supplies them for a real mission.
               singleSatelliteCoverage (p0 = 0.2, a probability): the chance that one satellite
               pointing without error covers the target set in the planning period.
               errorScale (e0, an angle): the pointing error at which that chance falls to 1/e of
               p0, set to the pointing-error limit of the requirement (budgets.pointingErrorLimit,
               0.008495 degree), so a design at the limit keeps 1/e of the single-satellite chance. */
        attribute singleSatelliteCoverage : Real = 0.2;
        attribute errorScale : PlaneAngleValue = budgets.pointingErrorLimit;
    }
    part coverageAssumptions : CoverageAssumptions;

    calc def CoverageProbability {
        doc /* MoE: how well the fleet does its job, the operator's measure of the fleet and the
               performance objective of the decision-maker's ternary (WP56). A derived attribute of
               the fleet of `fleetSize` identical satellites of the configuration: the probability
               that a target is covered by at least one satellite in the planning period,
               P = 1 - (1 - p(e))^n, with p(e) = p0 exp(-e / e0), n the fleet size, e the pointing
               error (the calc PointingError) and p0, e0 the constants of CoverageAssumptions.
               Dimensionless, from 0 to 1; it rises with the fleet size at a falling rate and falls
               with the pointing error. It takes the satellites as independent and the target set
               as one, and it models nothing of orbits, revisit or communication.
               Why this measure: the brief was an aggregate an executive reads as how well the fleet
               does its job, rising with fleet size with diminishing returns and falling with
               pointing error, with little new detail. Of the three definitions the WP56 spike
               compared (this one, an observation capacity with a ceiling, a refresh rate), it is the
               quantity an operator holds for a coverage problem; it needs the fewest constants, each
               with an operational reading, and one of them is the requirement already in the model;
               it is bounded, so it is not read as a count. It saturates: a fleet of 30 satellites at
               small pointing error comes close to 1. The comparison, the decision's stability across
               the three definitions and across a factor of two in each constant, and what the data
               cannot settle are recorded in work-packages/WP56-rounds/ternary/readout.md. */
        in c : Cubesat;
        attribute p : Real = coverageAssumptions.singleSatelliteCoverage
            * OpenSysMLMathFunctions::exp(-(PointingError(c) / coverageAssumptions.errorScale));
        return : Real = 1.0 - (1.0 - p) ** c.fleetSize;
    }
}
