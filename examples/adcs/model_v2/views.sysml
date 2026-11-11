/*
 * views.sysml -- the views of cubesat.sysml that a SysML v2 view editor draws (WP26). Its own file
 * beside the model, so the model's bytes (and the hash the ledger records) do not move for a view.
 * Load it after cubesat.sysml, as one applied model. Each view exposes the model's own elements
 * and names, in its `doc`, the intent it shows, quoted from the supervisor's recorded words
 * (WP22-decisions.md, WP23-decisions.md, WP27-decisions.md). The stakeholder view exposes
 * stakeholders.sysml, so the three files are applied together: cubesat.sysml, stakeholders.sysml,
 * views.sysml.
 */
package CubesatViews {
    private import StandardViewDefinitions::*;
    private import CubesatTradeSpaceV2::*;

    // ------------------------------------------------------------------------------------------
    // The configuration space: how a configuration is constructed
    // ------------------------------------------------------------------------------------------
    view assembly : InterconnectionView {
        doc /* The configuration space, one side of "a space of configs on one side (how its
               constructed) and a space of metrics on the other (how its evaluated)" (WP22): the
               parts of the baseline configuration, the wheel and the tracker that a configuration
               swaps, and the panels and battery whose span and capacity it tunes. */
        expose CubesatTradeSpaceV2::Cubesat;
    }
    view alternatives : GeneralView {
        doc /* The swaps and tunes of the configuration space: the two categorical design variables
               (the swaps `wheelClass` and `grade`, whose enumerations WheelClass and TrackerGrade
               name the concrete wheel and tracker each literal selects), and the ranges and gain
               boxes of the four continuous ones. */
        filter @SysML::PartDefinition or @SysML::EnumerationDefinition;
        expose CubesatTradeSpaceV2::WheelClass;
        expose CubesatTradeSpaceV2::TrackerGrade;
        expose CubesatTradeSpaceV2::ReactionWheel;
        expose CubesatTradeSpaceV2::SmallWheel;
        expose CubesatTradeSpaceV2::MediumWheel;
        expose CubesatTradeSpaceV2::LargeWheel;
        expose CubesatTradeSpaceV2::StarTracker;
        expose CubesatTradeSpaceV2::CoarseTracker;
        expose CubesatTradeSpaceV2::MediumTracker;
        expose CubesatTradeSpaceV2::FineTracker;
        expose CubesatTradeSpaceV2::DesignRanges;
        expose CubesatTradeSpaceV2::GainBox;
    }
    view configurations : GeneralView {
        doc /* The three named configurations of the configuration space: the baseline and the two
               contrasts at its corners (agile, compact), each a Cubesat with its wheel and tracker
               swapped and its span, capacity and gains tuned. */
        expose CubesatTradeSpaceV2::cubesatBaseline;
        expose CubesatTradeSpaceV2::cubesatBaseline::*;
        expose CubesatTradeSpaceV2::cubesatAgile;
        expose CubesatTradeSpaceV2::cubesatAgile::*;
        expose CubesatTradeSpaceV2::cubesatCompact;
        expose CubesatTradeSpaceV2::cubesatCompact::*;
    }

    // ------------------------------------------------------------------------------------------
    // The metric space: how a configuration is evaluated
    // ------------------------------------------------------------------------------------------
    view metrics : GeneralView {
        doc /* The metric space, "how its evaluated" (WP22): the calcs that take a configuration to
               its metrics, each traded metric's element marked MoE or MoP in its doc ("MoE on
               mass, no new column", WP23), and the experiment that returns them. The calcs are
               the subsystem calculations of "the coupling variables between subsystems in the
               MDAO lit" (WP23). */
        filter @SysML::CalculationDefinition;
        expose CubesatTradeSpaceV2::*;
    }
    view requirements : GeneralView {
        doc /* The requirements the metrics are read against, "a bunch more metrics explicitly
               included but tied to our actual requirements" (WP22): one requirement on each traded
               metric's own quantity at the supervisor's thresholds, and the baseline's
               requirements with their satisfy statements (the pointing-error one not satisfied). */
        filter @SysML::RequirementDefinition or @SysML::RequirementUsage;
        expose CubesatTradeSpaceV2::*;
    }
    view metricCarriers : GeneralView {
        doc /* Where the nine traded metrics live, each marked MoE or MoP in the doc of its
               element: the configuration's own accounting (total mass, with the launch cost its
               MoE), the measured slew (settling time, control effort), and the thresholds the
               requirements read them against. */
        expose CubesatTradeSpaceV2::Cubesat::totalMass;
        expose CubesatTradeSpaceV2::Cubesat::launchCost;
        expose CubesatTradeSpaceV2::SlewMeasurement;
        expose CubesatTradeSpaceV2::SlewMeasurement::*;
        expose CubesatTradeSpaceV2::Budgets;
        expose CubesatTradeSpaceV2::Budgets::*;
    }

    // ------------------------------------------------------------------------------------------
    // Who cares: the stakeholders, their concerns and the evidence (stakeholders.sysml)
    // ------------------------------------------------------------------------------------------
    view stakeholders : GeneralView {
        doc /* "who cares" (WP27, the supervisor: "to trace all the back to "who cares" via this
               tool"): the sponsor and the operator, the concerns each holds, the engineers'
               requirements each concern is decomposed into, the verification cases that verify
               them with the pointers to their evidence, and the sponsor's roll-ups. */
        expose CubesatStakeholders::sponsor;
        expose CubesatStakeholders::operator;
        expose CubesatStakeholders::lowCost;
        expose CubesatStakeholders::lowCost::*;
        expose CubesatStakeholders::longLife;
        expose CubesatStakeholders::longLife::*;
        expose CubesatStakeholders::pointingAndSlewing;
        expose CubesatStakeholders::pointingAndSlewing::*;
        expose CubesatStakeholders::powerAndEnergy;
        expose CubesatStakeholders::powerAndEnergy::*;
        expose CubesatStakeholders::configurationEvidence;
        expose CubesatStakeholders::configurationEvidence::*;
        expose CubesatStakeholders::slewEvidence;
        expose CubesatStakeholders::slewEvidence::*;
        expose CubesatStakeholders::CostToBuild;
        expose CubesatStakeholders::EffectiveLife;
    }
}
