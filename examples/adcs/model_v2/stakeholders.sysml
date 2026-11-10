/*
 * stakeholders.sysml -- who cares about the cubesat of cubesat.sysml, and where the evidence is
 * (WP27). Its own file beside the model, applied after cubesat.sysml (and views.sysml) as one model,
 * so the model's bytes, and the hash the ledger records, do not move for it.
 *
 * Read top to bottom:
 *   1. who cares       two stakeholders: a sponsor (price) and an operator (performance in operation)
 *   2. their needs     concerns framing the cubesat, each held by its stakeholder and decomposed into
 *                      the engineers' requirements of cubesat.sysml that serve it; the verdict of
 *                      each named configuration on each of those requirements, engine-checked
 *   3. roll-ups        the sponsor's measures derived from the engineers': the launch cost (in the
 *                      model), and two ILLUSTRATIVE roll-ups, cost to build and effective life
 *   4. evidence        verification cases that verify the concerns' requirements and point at where
 *                      the evidence is logged and the environment that produced it
 *
 * The engineers' requirements, their thresholds and the tensions between them stay in
 * cubesat.sysml, at their own level; this file says which concern each serves. Nothing here is read
 * by the oracle, the coverage table, the view generator, the data or the contract.
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
        doc /* Pays for the mission and answers for it. Cares about price: what the cubesat costs to
               build and to launch (down), and how long it serves (up). Reads rolled-up measures,
               not the engineers' detail. */
    }
    part def Operator {
        doc /* Flies the cubesat. Cares about how it performs during its operational life: that it
               slews, settles and points as asked, and that its power and energy hold up. */
    }
    part sponsor : Sponsor;
    part operator : Operator;

    // ==========================================================================================
    // 2. THEIR NEEDS: concerns framing the cubesat, each decomposed into the engineers' requirements
    // ==========================================================================================
    concern def PriceConcern {
        doc /* A need of the sponsor about the price of the mission. */
        subject c : Cubesat;
        stakeholder s : Sponsor;
    }
    concern def PerformanceConcern {
        doc /* A need of the operator about the cubesat's performance during its operational life. */
        subject c : Cubesat;
        stakeholder s : Operator;
    }

    concern lowCost : PriceConcern {
        doc /* The cubesat costs little to build and to launch. The launch cost (the MoE on the
               total mass) is bounded by the launch budget requirement; the cost to build is an
               illustrative roll-up with no requirement on it (section 3). */
        subject :>> c;
        stakeholder :>> s = sponsor;
        requirement launchBudget : LaunchBudgetRequirement;
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
    // degree), so the operator's pointing concern is not met by it.
    satisfy lowCost.launchBudget by cubesatBaseline;
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
    // configuration fails the launch budget (93,960 against 90,643 USD), the control effort
    // (0.112 against 0.059 N.m.s) and the peak slew power (7.4 against 2.6 W): the sponsor's low
    // cost and two of the operator's requirements. The compact configuration fails the pointing
    // error (0.008533 against 0.008495 degree), the operator's pointing concern.
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
    part def UnitCosts {
        doc /* Illustrative unit costs (USD), chosen for plausibility at cubesat scale and never
               cited or calibrated: a bus 60,000; solar panels 150,000 per square metre of panel;
               a battery 50 per watt-hour; an antenna 15,000; an IMU 5,000; a reaction wheel 8,000
               plus 2,000,000 per N.m of peak torque (three wheels); a star tracker 5,000 plus
               300,000 arcsec over its accuracy. */
        attribute bus : Real = 60000.0;
        attribute panelPerArea : Real = 150000.0;        // USD/m^2
        attribute batteryPerEnergy : Real = 50.0;        // USD/(W.h)
        attribute antenna : Real = 15000.0;
        attribute imu : Real = 5000.0;
        attribute wheelBase : Real = 8000.0;
        attribute wheelPerTorque : Real = 2.0e6;         // USD/(N.m)
        attribute trackerBase : Real = 5000.0;
        attribute trackerPerFineness : Real = 300000.0;  // USD.arcsec
    }
    part unitCosts : UnitCosts;

    calc def CostToBuild {
        doc /* Illustrative roll-up for the sponsor's low cost: the sum of the unit costs of the
               configuration's parts (USD). It rolls up the parts the configuration swaps (wheel,
               tracker) and tunes (panel span, battery capacity); it is not a traded metric and no
               requirement reads it. */
        in c : Cubesat;
        return : Real = unitCosts.bus
            + unitCosts.panelPerArea * ((c.panelPlus.area + c.panelMinus.area) / 1.0 [m**2])
            + unitCosts.batteryPerEnergy * (c.battery.capacity / 1.0 [W*h])
            + unitCosts.antenna + unitCosts.imu
            + c.wheelCount * (unitCosts.wheelBase
                + unitCosts.wheelPerTorque * (c.wheel.maxTorque / 1.0 [N*m]))
            + unitCosts.trackerBase
            + unitCosts.trackerPerFineness / (c.tracker.accuracy / 1.0 [SI::arcsec]);
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
               budget, the pointing error and the power requirement, each as its concern holds it.
               Evidence: the primary dataset's verdicts, computed by the model's requirements in the
               oracle; the current entry is the close-out gate's container regression, which
               re-pinned the outputs in hts-paper. */
        objective {
            verify lowCost.launchBudget;
            verify pointingAndSlewing.pointingError;
            verify powerAndEnergy.power;
        }
        :>> ledgerEntry = "v2-primary@8";
        :>> recordEntry = "Container regression at the WP23 close-out gate (2026-11-10, image 877c42cc10e3, head 61cef31)";
        :>> testNode = "tests/test_cubesat_oracle.py::test_the_flags_come_from_the_requirements_not_from_python";
        :>> environment = "877c42cc10e3";
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
        :>> ledgerEntry = "v2-primary@8";
        :>> recordEntry = "Container regression at the WP23 close-out gate (2026-11-10, image 877c42cc10e3, head 61cef31)";
        :>> testNode = "tests/test_case.py::test_feasible_mask_counts_on_frozen_data";
        :>> environment = "877c42cc10e3";
    }
}
