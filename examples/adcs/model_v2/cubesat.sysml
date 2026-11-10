/*
 * cubesat.sysml -- the ILLUSTRATIVE 12U-class cubesat trade space, as one readable model with two
 * views (WP22), revised in WP23 (the model-realism loop, rounds 1 and 2) and adopted at WP23's
 * data gate (WP23-decisions.md). The WP22 version it replaced is in history at d3018ba, the WP15
 * version at 2d13465; every accounting calculation of them is kept here as it was. What WP23
 * changes: every traded metric is marked as a measure of effectiveness (MoE)
 * or a measure of performance (MoP) in a `doc` on its element; a launch cost (a calc of the total
 * mass, increasing in mass) is the MoE that ties the total mass to a launch-budget requirement;
 * the four metrics that had no requirement (pointing error, control effort, peak slew power, total
 * mass through the launch cost) each have one, at the threshold the supervisor chose from the
 * loop's ladder (part `budgets`; WP23-decisions.md, "The four thresholds"); the slew time leaves
 * (one time metric, the settling time; WP16's decision), its requirements folding into
 * SettledRequirement; the measurement states the inputs the simulator
 * reads. Round 2 (the coupling check): the battery's own rating enters, a continuous discharge
 * rate whose product with the capacity is the pack's peak power, and a requirement reads it
 * against the eclipse peak load (housekeeping plus the peak slew power), so the battery capacity
 * is tied to the slew's peak draw through the model's own calcs; no new configuration variable.
 * The close-out (WP23-closeout-scope-of-work.md): the eclipse reserve leaves, its calc and its
 * requirement with it, because its requirement was the depth-of-discharge requirement restated
 * (0.3 C - D >= 0 is D / C <= 0.3); the depth of discharge is the one metric and the one
 * requirement on the eclipse energy, and eight metrics are traded. The baseline configuration
 * fails the pointing-error requirement: its pointing error is 0.0155 degree against a limit of
 * 0.0085 degree, so section 5 states `not satisfy` for it; 63.7 % of the baseline regime's feasible
 * designs pass that requirement.
 *
 * This is documentation of a demonstration, not an engineering model. Every number is
 * illustrative: chosen for plausibility at cubesat scale (public component classes), never
 * calibrated to hardware and never fitted to make a result appear. Each constant carries its
 * rationale in a `doc` comment beside it. The model covers the cubesat only; the geostationary
 * variant of WP4 is retired to the record (its modules and data stay frozen, see WP15 OD1).
 *
 * The file is read top to bottom (the method sees only configuration -> attributes):
 *   1. configuration space   what can be chosen: enumerations, alternatives, ranges, gain boxes
 *   2. the cubesat           its composition and its environment
 *   3. accounting            mass, power, energy, inertia, pointing: `calc def`s
 *   4. scenarios             the slew, and a closed-form approximation of it
 *   5. requirements          feasibility as requirements, `satisfy`, verification cases, claims
 *   6. the experiment        an `analysis def`: configuration and measured slew in, attributes out
 *   7. named configurations  the baseline and two contrasts
 *
 * One model, two views (WP22). The CONFIGURATION view is sections 1, 2 and 7: the parts, the
 * alternatives (categorical variables), the parameters (continuous variables), the named
 * configurations. The ASSESSMENT view is sections 3 to 6: the calculations, the scenario, the
 * requirements and verification cases, and the experiment, that say how a configuration is
 * assessed and how each traded metric (the eight of the case study) traces back to this model.
 * Each section header below carries the name of its view. The chain read from the elements: a
 * configuration variable feeds a calc def or the measured slew; the experiment returns the calc as
 * the metric, or the measurement passes it on; a requirement def states the bound on the same calc
 * or measured quantity (or, for the total mass, on the launch cost computed from it); a
 * verification case verifies the requirement. The eight traded metrics: settling time, pointing
 * error, total mass, control effort, power margin, energy balance, peak slew power, depth of
 * discharge. Each is marked MoE or MoP in the `doc` of its element (the first word
 * of the doc): an MoE is a measure a stakeholder states without knowing the design (how well the
 * payload points; what the launch costs); an MoP is a measure of the system's performance under
 * the scenario the engineer states. Every one has a requirement that reads its own quantity.
 * The slew itself is integrated in Python (adcs_sim.simulate_adcs, the measurement of record);
 * SysML v2 cannot integrate the ODE, so the measured quantities enter the experiment as `in`
 * parameters. Section 4 carries a closed-form approximation for model checking.
 *
 * The views a SysML v2 view editor draws (the assembly, the alternatives, the named
 * configurations, the calcs, where the metrics live, the requirements with their satisfy and
 * verify links) are declared in views.sysml beside this file and applied after it as one model.
 *
 * How a Python caller reads this model (opensysml client; `m = conn.load_from_content(text,
 * strict=True)`; P = "CubesatTradeSpaceV2"). No number below is copied into Python:
 *   ranges, gain boxes, scenario numbers, constants
 *       m.eval(f"{P}::designRanges.panelSpanMin")           -> Quantity; .in_unit(unit)
 *       m.eval(f"{P}::aggressiveGains.KpMax")               -> float
 *       m.eval(f"{P}::nominalSlew.horizon")                 -> Quantity
 *       unit = m.eval("1.0 [SI::W*SI::h]").unit             (units built by the model itself)
 *   enumeration literals              [c.name for c in m.find(f"{P}::WheelClass").children()]
 *   alternatives (attribute tables)   m.query(scope=[P], where={"property": "@type",
 *       "operator": "=", "value": "PartDefinition"}) then, for each hit, `m.find(hit.id)
 *       .specializations` names its abstract part def and `m.instantiate(hit.id).get("wheelClass")`
 *       its literal; `m.instantiate(hit.id).get("maxTorque")` reads the table entry
 *   a configuration                   a `part x : Cubesat { ... }` appended in a second package of
 *       the same loaded text (the runtime cannot import across separately loaded files)
 *   the experiment                    m.run_analysis(f"{P}::SlewExperiment", subject=<part>,
 *       named_arguments={...}) -> outputs["attributes"], in the order stated in its `doc`
 */
package CubesatTradeSpaceV2 {
    private import ScalarValues::*;
    private import ISQ::*;
    private import SI::*;
    private import NumericalFunctions::min;
    private import NumericalFunctions::max;
    private import NumericalFunctions::abs;
    private import OpenSysMLMathFunctions::ln;   // OpenSysML extension: the KerML library has no ln

    // ==========================================================================================
    // 1. CONFIGURATION SPACE (configuration view): what can be chosen
    // ==========================================================================================
    doc /* The six design variables. Two are categorical (WheelClass, TrackerGrade), each an
           enumeration whose literals select a concrete alternative of an abstract part with its
           attribute table. Four are continuous (panel span, battery capacity, gains Kp and Kd),
           each with a range sampled log-uniformly; the gains have two boxes, baseline and
           aggressive. Ranges are the model's; the sampler in Python reads them from here. */
    enum def WheelClass { small; medium; large; }
    enum def TrackerGrade { coarse; medium; fine; }

    abstract part def ReactionWheel {
        attribute wheelClass : WheelClass;
        attribute maxTorque : TorqueValue;
        attribute maxMomentum : AngularMomentumValue;   // the momentum capacity
        attribute mass : MassValue;
    }
    doc /* Public cubesat wheel classes (illustrative): small ~ 0.3 mN.m, medium ~ 2 mN.m,
           large ~ 10 mN.m peak torque; momentum storage 10, 30, 100 mN.m.s (momentum-to-torque
           ratios of 33, 15 and 10 s); mass 0.12, 0.25, 0.60 kg. The set spans a factor of 20 in
           torque so that the wheel class trades agility against mass and power. */
    part def SmallWheel :> ReactionWheel {
        :>> wheelClass = WheelClass::small;
        :>> maxTorque = 0.0003 [N*m];
        :>> maxMomentum = 0.010 [N*m*s];
        :>> mass = 0.12 [kg];
    }
    part def MediumWheel :> ReactionWheel {
        :>> wheelClass = WheelClass::medium;
        :>> maxTorque = 0.002 [N*m];
        :>> maxMomentum = 0.030 [N*m*s];
        :>> mass = 0.25 [kg];
    }
    part def LargeWheel :> ReactionWheel {
        :>> wheelClass = WheelClass::large;
        :>> maxTorque = 0.010 [N*m];
        :>> maxMomentum = 0.100 [N*m*s];
        :>> mass = 0.60 [kg];
    }

    abstract part def StarTracker {
        attribute grade : TrackerGrade;
        attribute accuracy : PlaneAngleValue;     // 1-sigma
        attribute mass : MassValue;
        attribute power : PowerValue;
    }
    doc /* Star-tracker grades (illustrative): coarse 30 arcsec / 0.15 kg / 0.4 W, medium
           10 arcsec / 0.35 kg / 0.9 W, fine 2 arcsec / 0.90 kg / 1.5 W. A finer sensor points
           better, weighs more and draws more. */
    part def CoarseTracker :> StarTracker {
        :>> grade = TrackerGrade::coarse;
        :>> accuracy = 30.0 [SI::arcsec];
        :>> mass = 0.15 [kg];
        :>> power = 0.4 [W];
    }
    part def MediumTracker :> StarTracker {
        :>> grade = TrackerGrade::medium;
        :>> accuracy = 10.0 [SI::arcsec];
        :>> mass = 0.35 [kg];
        :>> power = 0.9 [W];
    }
    part def FineTracker :> StarTracker {
        :>> grade = TrackerGrade::fine;
        :>> accuracy = 2.0 [SI::arcsec];
        :>> mass = 0.90 [kg];
        :>> power = 1.5 [W];
    }

    part def DesignRanges {
        doc /* Ranges (illustrative): panel span 0.3 to 1.0 m per wing (two wings; chord 0.34 m
               so total area 0.2 to 0.68 m^2); battery 20 to 200 Wh. */
        attribute panelSpanMin : LengthValue = 0.3 [m];
        attribute panelSpanMax : LengthValue = 1.0 [m];
        attribute batteryCapacityMin : EnergyValue = 20.0 [W*h];
        attribute batteryCapacityMax : EnergyValue = 200.0 [W*h];
    }
    part designRanges : DesignRanges;

    part def GainBox {
        doc /* Attitude-loop gains, units N.m/rad (Kp) and N.m.s/rad (Kd). */
        attribute KpMin : Real;
        attribute KpMax : Real;
        attribute KdMin : Real;
        attribute KdMax : Real;
    }
    part baselineGains : GainBox {
        doc /* Baseline box: Kp 0.03 to 1.0 and Kd 0.3 to 1.5, a stiff attitude loop that asks for
               more torque than a cubesat wheel gives on a large slew, so the wheel class binds. */
        :>> KpMin = 0.03;
        :>> KpMax = 1.0;
        :>> KdMin = 0.3;
        :>> KdMax = 1.5;
    }
    part aggressiveGains : GainBox {
        doc /* Aggressive box (the primary dataset): Kp 0.2 to 2.0, Kd 0.3 to 1.5, with Kd/Kp
               mostly at or below 5, where the wheel class separates the slew time. */
        :>> KpMin = 0.2;
        :>> KpMax = 2.0;
        :>> KdMin = 0.3;
        :>> KdMax = 1.5;
    }

    // ==========================================================================================
    // 2. THE CUBESAT (configuration view): composition and environment
    // ==========================================================================================
    doc /* The cubesat is a composition of fixed parts (bus, antenna, IMU) and of the parts the
           design variables select (two solar panels of one span, a battery of one capacity, three
           identical orthogonal wheels, a tracker, the controller gains). The environment is one
           set of mission constants shared by every configuration. */
    part def Environment {
        doc /* LEO of about 95 minutes: orbital rate 1.13e-3 rad/s; eclipse 0.6 h; a battery may be
               cycled to 0.3 depth of discharge at most (cycle life). */
        attribute orbitalRate : AngularVelocityValue = 1.13e-3 [rad/s];
        attribute eclipseDuration : TimeValue = 0.6 [h];
        attribute maxDepthOfDischarge : Real = 0.3;
        doc /* Solar chain (illustrative): flux 1361 W/m^2, cell efficiency 0.28, packing factor
               0.7, degradation 0.9, mean incidence factor 0.5; the product is about 120 W/m^2 of
               panel, averaged over the sunlit arc. */
        attribute solarFlux : IrradianceValue = 1361.0 [W/m**2];
        attribute cellEfficiency : Real = 0.28;
        attribute packingFactor : Real = 0.7;
        attribute degradation : Real = 0.9;
        attribute incidenceFactor : Real = 0.5;
        doc /* Loads (illustrative): housekeeping and payload 12 W; idle power 0.3 W per wheel;
               wheel electrical loss coefficient c = 5e4 W/(N.m)^2, one value for every class, so
               a saturated large wheel (10 mN.m) draws 5 W and a saturated small one 12.5 mW. */
        attribute housekeepingLoad : PowerValue = 12.0 [W];
        attribute wheelIdlePower : PowerValue = 0.3 [W];
        attribute wheelLossCoefficient : Real = 5.0e4;   // W/(N.m)^2
        doc /* Disturbance and areal density (illustrative): constant LEO disturbance torque
               (aerodynamic plus solar) 2e-6 N.m; worst-case attitude offset 0.1 degree (1.745e-3 rad) for
               the gravity-gradient bound; panel areal density 2.5 kg/m^2 per wing including cells and
               substrate; battery pack specific energy 140 Wh/kg. */
        attribute disturbanceTorque : TorqueValue = 2.0e-6 [N*m];
        attribute gravityGradientOffset : PlaneAngleValue = 1.7453292519943296e-3 [rad];   // 0.1 degree
        attribute panelArealDensity : SurfaceDensityValue = 2.5 [kg/m**2];
        attribute batterySpecificEnergy : Real = 140.0;   // Wh/kg
        doc /* Battery rating (illustrative, WP23 round 2): a continuous discharge rating of 1 C,
               the pack delivering its capacity in one hour, the plain rating of a small-satellite
               lithium-ion pack; the pack's peak power is this rate times its capacity, so an 80 Wh
               pack delivers 80 W and a 20 Wh pack 20 W. Not a cited rating. */
        attribute batteryDischargeRate : Real = 1.0;   // 1/h (C-rate)
        doc /* Launch (illustrative): a launch price of 6000 USD per kilogram to low Earth orbit, a
               round figure at the order of magnitude of published small-satellite rideshare list
               prices; not a cited price (WP23 OD1). The launch cost is this rate times the total
               mass, so a lighter configuration is cheaper to launch and a heavier one dearer. */
        attribute launchRate : Real = 6000.0;   // USD/kg
    }
    part environment : Environment;

    part def Bus {
        doc /* 12U-class body 0.226 x 0.226 x 0.340 m; bus structure, avionics, harness: 10 kg. */
        attribute bodyLength : LengthValue = 0.226 [m];
        attribute bodyWidth : LengthValue = 0.226 [m];
        attribute bodyHeight : LengthValue = 0.340 [m];
        attribute mass : MassValue = 10.0 [kg];
    }
    part def Antenna {
        doc /* Payload antenna: disc of 0.2 m diameter at 0.25 m offset, 0.5 kg (fixed). */
        attribute diameter : LengthValue = 0.2 [m];
        attribute offset : LengthValue = 0.25 [m];
        attribute mass : MassValue = 0.5 [kg];
    }
    part def Imu {
        doc /* Inertial measurement unit, 0.1 kg (fixed). */
        attribute mass : MassValue = 0.1 [kg];
    }
    part def Controller {
        doc /* PD attitude law tau = -Kp/2 q - Kd omega per axis, clipped at the usable torque.
               Defaults are the lower corner of the baseline gain box. */
        attribute Kp : Real default = 0.03;   // N.m/rad
        attribute Kd : Real default = 0.3;    // N.m.s/rad
    }
    part def SolarPanel {
        doc /* One wing: span (a design variable) by a fixed chord of 0.34 m. */
        attribute span : LengthValue default = 0.6 [m];
        attribute chord : LengthValue = 0.34 [m];
        attribute area : AreaValue = span * chord;
        attribute mass : MassValue = environment.panelArealDensity * span * chord;
    }
    part def Battery {
        doc /* Pack mass follows from the capacity (a design variable) and the specific energy. */
        attribute capacity : EnergyValue default = 80.0 [W*h];
        attribute mass : MassValue = capacity / (environment.batterySpecificEnergy * 1.0 [W*h/kg]);
    }

    part def Cubesat {
        // Design variables (defaults are the baseline configuration).
        attribute panelSpan : LengthValue default = 0.6 [m];
        attribute batteryCapacity : EnergyValue default = 80.0 [W*h];
        part bus : Bus;
        part panelPlus : SolarPanel { :>> span = Cubesat::panelSpan; }
        part panelMinus : SolarPanel { :>> span = Cubesat::panelSpan; }
        part battery : Battery { :>> capacity = Cubesat::batteryCapacity; }
        part antenna : Antenna;
        part imu : Imu;
        part wheel : ReactionWheel;        // the three identical orthogonal wheels
        part tracker : StarTracker;
        part controller : Controller;
        attribute wheelCount : Integer = 3;
        // Accounting, evaluated by the calculations of section 3.
        attribute totalMass : MassValue = MassAccounting(self) {
            doc /* MoP: the launch mass of the configuration (the traded metric `total mass`); the
                   launch cost, the MoE on it, is LaunchCost below. */
        }
        attribute launchCost : Real = LaunchCost(self);   // USD; the MoE on the total mass
        attribute structureMass : MassValue = StructureMass(self);
        attribute adcsMass : MassValue = AdcsMass(self);
        attribute momentumCapacity : AngularMomentumValue = wheel.maxMomentum;
        attribute generatedPower : PowerValue = GeneratedPower(self);
        attribute availablePower : PowerValue = AvailablePower(self);
        attribute usableWheelTorque : TorqueValue = UsableWheelTorque(self);
    }

    // ==========================================================================================
    // 3. ACCOUNTING (assessment view): mass, power, energy, inertia, pointing
    // ==========================================================================================
    doc /* Mass: total = bus + battery + both panels + antenna + 3 wheels + tracker + IMU. The
           structure mass is what the inertia model calls the body: the total without the panels
           and the antenna, which the inertia model places by themselves. Power: generation is
           proportional to panel area; the power left after the housekeeping and tracker loads is
           what the wheels can use, and it caps the usable torque. Energy: the slew loss energy is
           c times the integral of |tau|^2 dt (measured, section 6); the eclipse demand adds the
           base load over the eclipse; depth of discharge is demand over capacity; the pack's
           peak power is its discharge rating times its capacity, read against the eclipse peak
           load. Cost: the launch cost is the launch rate times the total mass. Each calc that is
           a traded metric carries its MoE or MoP mark in its own doc. */
    calc def MassAccounting {
        in c : Cubesat;
        return : MassValue = c.bus.mass + c.battery.mass + c.panelPlus.mass + c.panelMinus.mass
            + c.antenna.mass + c.wheelCount * c.wheel.mass + c.tracker.mass + c.imu.mass;
    }
    calc def StructureMass {
        in c : Cubesat;
        return : MassValue = c.bus.mass + c.battery.mass + c.wheelCount * c.wheel.mass
            + c.tracker.mass + c.imu.mass;
    }
    calc def AdcsMass {
        in c : Cubesat;
        return : MassValue = c.wheelCount * c.wheel.mass + c.tracker.mass + c.imu.mass;
    }
    calc def LaunchCost {
        doc /* MoE: the cost to launch the configuration, the launch rate times the total mass
               (USD); increasing in mass. It is not itself a traded metric: the total mass is, and
               the launch budget requirement reads this cost. */
        in c : Cubesat;
        return : Real = environment.launchRate * (c.totalMass / 1.0 [kg]);
    }
    calc def GeneratedPower {
        in c : Cubesat;
        return : PowerValue = environment.solarFlux * environment.cellEfficiency
            * environment.packingFactor * environment.degradation * environment.incidenceFactor
            * (c.panelPlus.area + c.panelMinus.area);
    }
    calc def BaseLoad {
        in c : Cubesat;
        return : PowerValue = environment.housekeepingLoad + c.tracker.power
            + c.wheelCount * environment.wheelIdlePower;
    }
    calc def AvailablePower {
        in c : Cubesat;
        return : PowerValue = GeneratedPower(c) - environment.housekeepingLoad - c.tracker.power;
    }
    // Usable torque = min(maxTorque, sqrt(P_avail / (3 c))): all three wheels at the cap draw
    // P_avail. A non-positive available power gives a minimal cap of 1 % of the class maximum.
    calc def UsableWheelTorque {
        in c : Cubesat;
        return : TorqueValue = if AvailablePower(c) > 0.0 [W]
            ? min(c.wheel.maxTorque / 1.0 [N*m],
                  QuantityCalculations::sqrt(AvailablePower(c)
                      / (c.wheelCount * environment.wheelLossCoefficient * 1.0 [W/(N*m)**2]))
                  / 1.0 [N*m]) * 1.0 [N*m]
            else 0.01 * c.wheel.maxTorque;
    }
    // Wheel electrical loss energy over the slew: c times the integral of |tau|^2 dt, whose value
    // (unit N^2.m^2.s) the simulator measures and the experiment hands in as a plain number.
    calc def SlewLossEnergy {
        in torqueSquaredIntegral : Real;
        return : EnergyValue = environment.wheelLossCoefficient * torqueSquaredIntegral * 1.0 [W*s];
    }
    calc def EclipseDemand {
        in c : Cubesat;
        in slewEnergy : EnergyValue;
        return : EnergyValue = BaseLoad(c) * environment.eclipseDuration + slewEnergy;
    }
    calc def DepthOfDischarge {
        doc /* MoP: the eclipse depth of discharge, the eclipse demand with the slew loss energy over
               the battery capacity (the traded metric `depth of discharge`). */
        in c : Cubesat;
        in slewEnergy : EnergyValue;
        return : Real = EclipseDemand(c, slewEnergy) / c.battery.capacity;
    }
    calc def OrbitPeriod {
        return : TimeValue = 2.0 * 3.141592653589793 [rad] / environment.orbitalRate;
    }
    calc def EnergyBalance {
        doc /* MoP: over one orbit, the energy the panels supply in sunlight less the base load over
               the orbit and the slew loss energy (the traded metric `energy balance`). */
        in c : Cubesat;
        in slewEnergy : EnergyValue;
        return : EnergyValue = GeneratedPower(c) * (OrbitPeriod() - environment.eclipseDuration)
            - BaseLoad(c) * OrbitPeriod() - slewEnergy;
    }
    calc def PeakSlewPower {
        doc /* MoP: the electrical power drawn at the peak of the slew, the tracker and idle wheel
               loads plus the wheel loss at the measured peak torque (the traded metric `peak slew
               power`). */
        in c : Cubesat;
        in peakTorque : TorqueValue;
        return : PowerValue = c.tracker.power + c.wheelCount * environment.wheelIdlePower
            + environment.wheelLossCoefficient * 1.0 [W/(N*m)**2] * peakTorque * peakTorque;
    }
    calc def PowerMargin {
        doc /* MoP: the generated power left after the housekeeping load and the peak slew power
               (the traded metric `power margin`). */
        in c : Cubesat;
        in peakTorque : TorqueValue;
        return : PowerValue = GeneratedPower(c) - environment.housekeepingLoad
            - PeakSlewPower(c, peakTorque);
    }
    calc def BatteryPeakPower {
        doc /* The power the pack can deliver at its continuous discharge rating: the discharge rate
               times the capacity (W). Not a traded metric: the battery peak power requirement
               reads it against the eclipse peak load. */
        in c : Cubesat;
        return : PowerValue = environment.batteryDischargeRate * c.battery.capacity / 1.0 [h];
    }
    calc def EclipsePeakLoad {
        doc /* The load the battery alone carries at the peak of a slew in eclipse, where the panels
               give nothing: the housekeeping load plus the peak slew power. Not a traded metric. */
        in c : Cubesat;
        in peakTorque : TorqueValue;
        return : PowerValue = environment.housekeepingLoad + PeakSlewPower(c, peakTorque);
    }
    // Principal inertia (kg m^2) of the box bus, two thin-plate panels offset along Y (centre at
    // Ly/2 + span/2) and a disc antenna offset along Z, by the parallel-axis theorem.
    calc def InertiaX {
        in c : Cubesat;
        return : MomentOfInertiaValue =
            (c.bus.bodyWidth ** 2 + c.bus.bodyHeight ** 2) * StructureMass(c) / 12.0
            + 2.0 * c.panelPlus.mass * (c.panelPlus.span ** 2 / 12.0
                + (c.bus.bodyWidth / 2.0 + c.panelPlus.span / 2.0) ** 2)
            + c.antenna.mass * (c.antenna.diameter ** 2 / 16.0 + c.antenna.offset ** 2);
    }
    calc def InertiaY {
        in c : Cubesat;
        return : MomentOfInertiaValue =
            (c.bus.bodyLength ** 2 + c.bus.bodyHeight ** 2) * StructureMass(c) / 12.0
            + 2.0 * c.panelPlus.mass * c.panelPlus.chord ** 2 / 12.0
            + c.antenna.mass * (c.antenna.diameter ** 2 / 16.0 + c.antenna.offset ** 2);
    }
    calc def InertiaZ {
        in c : Cubesat;
        return : MomentOfInertiaValue =
            (c.bus.bodyLength ** 2 + c.bus.bodyWidth ** 2) * StructureMass(c) / 12.0
            + 2.0 * c.panelPlus.mass * ((c.panelPlus.span ** 2 + c.panelPlus.chord ** 2) / 12.0
                + (c.bus.bodyWidth / 2.0 + c.panelPlus.span / 2.0) ** 2)
            + c.antenna.mass * c.antenna.diameter ** 2 / 8.0;
    }
    // Pointing error: root-sum-square of the steady error 4 (tau_gg + tau_dist) / Kp and the
    // star-tracker floor; tau_gg = 3 n^2 max(|Jz - Jy|, |Jz - Jx|) times the offset angle.
    calc def GravityGradientTorque {
        in c : Cubesat;
        return : TorqueValue = 3.0 * (environment.orbitalRate / 1.0 [rad/s]) ** 2
            * max(abs((InertiaZ(c) - InertiaY(c)) / 1.0 [kg*m**2]),
                  abs((InertiaZ(c) - InertiaX(c)) / 1.0 [kg*m**2]))
            * (environment.gravityGradientOffset / 1.0 [rad]) * 1.0 [N*m];
    }
    calc def PointingError {
        doc /* MoE: how well the payload points, the root-sum-square of the steady attitude error
               under the disturbance and gravity-gradient torques and the star tracker's accuracy
               (the traded metric `pointing error`); the payload's need, stated without knowing the
               design. */
        in c : Cubesat;
        return : PlaneAngleValue = QuantityCalculations::sqrt(
            (4.0 * ((GravityGradientTorque(c) + environment.disturbanceTorque) / 1.0 [N*m])
                / c.controller.Kp * 180.0 / 3.141592653589793) ** 2
            + (c.tracker.accuracy / 1.0 [SI::arcsec] / 3600.0) ** 2) * 1.0 [SI::degree];
    }

    // ==========================================================================================
    // 4. SCENARIOS (assessment view): the slew, and a closed-form approximation of it
    // ==========================================================================================
    doc /* A scenario is a named part of numbers: the slew the experiment simulates and the band
           that reads the response. The ODE (adcs_sim.simulate_adcs) is the measurement of record;
           the closed-form calcs below approximate the time its attitude error takes to enter a
           band, to say something about agility over the whole space (model checking) without
           simulating. */
    part def Scenario {
        doc /* Nominal slew (illustrative): 30 degrees about the body X axis from rest, simulated
               over a 600 s horizon at a 0.5 s step. The settling time is the hold time: the first
               time after which the pointing error stays inside the settling band, 1 % of the slew
               angle, computed by event detection as the last exit from that band (WP16). The
               1 degree band is the band of the closed-form approximation below; no traded metric
               reads it. */
        attribute slewAngle : PlaneAngleValue = 30.0 [SI::degree];
        attribute horizon : TimeValue = 600.0 [s];
        attribute timeStep : TimeValue = 0.5 [s];
        attribute slewBand : PlaneAngleValue = 1.0 [SI::degree];
        attribute settlingFraction : Real = 0.01;
    }
    part nominalSlew : Scenario;

    doc /* Closed-form time to the band, for the single slew axis (small-angle PD law, torque
           cap T = the usable wheel torque, inertia J, stiffness Kp/4 on the angle, damping Kd):
           torque-limited regime: bang-bang, accelerate at T/J then brake, which enters a band b
           of an angle a at sqrt(J/T) (2 sqrt(a) - sqrt(2 b));
           linear regime: the dominant pole of J th'' + Kd th' + (Kp/4) th = 0 (rate Kd/(2J) when
           underdamped, wn (z - sqrt(z^2 - 1)) when overdamped, wn = sqrt(Kp/(4J)), z =
           Kd/sqrt(J Kp)), entering the band at ln(a/b) / rate.
           The estimate is the larger of the two; the regime is torque-limited when the first
           binds. Against the ODE it is a model-checking approximation, not a replacement; the
           calcs keep their WP15 names (SlewTimeEstimate and its parts), which the comparison code
           reads. */
    calc def TorqueLimitedSlewTime {
        in c : Cubesat;
        in scenario : Scenario;
        return : TimeValue = QuantityCalculations::sqrt(
                (InertiaX(c) / 1.0 [kg*m**2]) / (UsableWheelTorque(c) / 1.0 [N*m]))
            * (2.0 * QuantityCalculations::sqrt(scenario.slewAngle / 1.0 [rad])
               - QuantityCalculations::sqrt(2.0 * scenario.slewBand / 1.0 [rad])) * 1.0 [s];
    }
    calc def NaturalFrequency {
        in c : Cubesat;
        return : Real = RealFunctions::sqrt(
            c.controller.Kp / (4.0 * (InertiaX(c) / 1.0 [kg*m**2])));
    }
    calc def DampingRatio {
        in c : Cubesat;
        return : Real = c.controller.Kd
            / RealFunctions::sqrt((InertiaX(c) / 1.0 [kg*m**2]) * c.controller.Kp);
    }
    calc def DominantPoleRate {
        in c : Cubesat;
        return : Real = if DampingRatio(c) > 1.0
            ? NaturalFrequency(c) * (DampingRatio(c)
                - RealFunctions::sqrt(DampingRatio(c) * DampingRatio(c) - 1.0))
            else DampingRatio(c) * NaturalFrequency(c);
    }
    calc def LinearSlewTime {
        in c : Cubesat;
        in scenario : Scenario;
        return : TimeValue = ln(scenario.slewAngle / scenario.slewBand) / DominantPoleRate(c) * 1.0 [s];
    }
    calc def SlewTimeEstimate {
        in c : Cubesat;
        in scenario : Scenario;
        return : TimeValue = if TorqueLimitedSlewTime(c, scenario) > LinearSlewTime(c, scenario)
            ? TorqueLimitedSlewTime(c, scenario) else LinearSlewTime(c, scenario);
    }
    calc def IsTorqueLimited {
        in c : Cubesat;
        in scenario : Scenario;
        return : Boolean = TorqueLimitedSlewTime(c, scenario) > LinearSlewTime(c, scenario);
    }

    // ==========================================================================================
    // 5. REQUIREMENTS, SATISFACTION AND VERIFICATION (assessment view; 15.2, WP22)
    // ==========================================================================================
    doc /* The four feasibility flags (settled, momentum_ok, power_ok, dod_ok) as named
           requirements, one requirement on every traded metric's own quantity, the four
           thresholds, `satisfy` statements tying each requirement to the baseline, `verification
           def`s naming what each verifies, and claims over every in-range configuration. */
    // BEGIN 15.2
    doc /* Feasibility is stated here and verified, not computed in Python. Eleven requirements.
           Four are the flags the experiment reports: settled, momentum_ok, power_ok, dod_ok; the
           settled and depth-of-discharge ones read the settling time and the depth of discharge.
           Six more each read a traded metric's own quantity: pointing error, control effort, peak
           slew power, power margin, energy balance, and the total mass through the launch cost;
           so every one of the eight traded metrics has a requirement. The eleventh, the battery
           peak power requirement, reads the pack's rating against the eclipse peak load. A
           requirement takes a Cubesat as its subject and, where it needs a measured quantity of
           the slew, an `in` parameter that the runner binds by name (a Quantity, or a Real for
           the integral of |tau|^2). The defaults of those parameters are the recorded measurement
           of the baseline (below), so the `satisfy` statements are checkable without a runner.
           Every threshold is a value this model states: zero for a margin or a balance, the
           maximum depth of discharge of the environment, the horizon of the nominal slew, a
           limit in `budgets`, or the pack's own rated power. */
    part def SlewMeasurement {
        doc /* A measurement of one slew: the quantities the requirements and the experiment read.
               The simulator (adcs_sim.simulate_adcs) reads these inputs of the configuration:
               structureMass, bus.bodyLength, bus.bodyWidth, bus.bodyHeight, panelPlus.span,
               panelPlus.chord, panelPlus.mass, antenna.diameter, antenna.offset, antenna.mass,
               usableWheelTorque, momentumCapacity, controller.Kp, controller.Kd; of the
               environment: orbitalRate; of the scenario: slewAngle, horizon, timeStep,
               settlingFraction. Every measured quantity below depends on all of them. */
        attribute settlingTime : TimeValue {
            doc /* MoP: the settling time (the traded metric `settling time`): the hold time, the
                   first time after which the pointing error stays inside the settling band,
                   computed by event detection as the last exit from the band. */
        }
        attribute peakTorque : TorqueValue;
        attribute peakMomentum : AngularMomentumValue;
        attribute controlEffort : AngularMomentumValue {
            doc /* MoP: the control effort (the traded metric `control effort`), the integral of
                   |tau| over the slew, N.m.s: what the slew asks of the wheels. */
        }
        attribute torqueSquaredIntegral : Real;   // N^2 m^2 s
    }
    part baselineMeasurement : SlewMeasurement {
        doc /* The baseline's slew integrated by adcs_sim.simulate_adcs (600 s horizon, 0.5 s step,
               30 degree slew), recorded to reproduce the verdicts below. A test re-measures it. */
        :>> settlingTime = 180.1904772571943 [s];
        :>> peakTorque = 0.002 [N*m];
        :>> peakMomentum = 0.00466041037173962 [N*m*s];
        :>> controlEffort = 0.009490621914197469 [N*m*s];
        :>> torqueSquaredIntegral = 7.70613052023095e-06;
    }
    part def Budgets {
        doc /* The four thresholds, the supervisor's choice from the loop's ladder (WP23-decisions.md,
               "The four thresholds", 2026-11-10; the ladder is WP23-review.md, "Proposed
               thresholds, revised for the gate popup"). Each limit is a literal; its doc names the
               ladder row and the share of the feasible designs it admits (primary / baseline
               regime). The baseline configuration's own values stay the record of the baseline:
               pointing error 0.015535 degree, control effort 0.0094906 N.m.s, peak slew power
               2.0 W, launch cost 79,749 USD (13.291 kg). */
        attribute pointingErrorLimit : PlaneAngleValue = 0.008495 [degree] {
            doc /* 0.0085 degree, the row that admits 95 % of the primary regime (95.0 % / 63.7 %),
                   kept knowing that the baseline configuration (0.015535 degree) fails it ("Keep
                   0.0085 deg", 2026-11-10, 08:55). */
        }
        attribute controlEffortLimit : AngularMomentumValue = 0.05922 [N*m*s] {
            doc /* 0.059 N.m.s, the row that admits 90 % of the baseline regime (58.9 % / 90.0 %). */
        }
        attribute peakSlewPowerLimit : PowerValue = 2.6 [W] {
            doc /* 2.6 W, the row that admits every small and medium wheel (62.2 % / 67.3 %). */
        }
        attribute launchBudget : Real = 90643.0 {   // USD
            doc /* 90,643 USD, 15.107 kg at the illustrative 6,000 USD/kg, the row that admits 95 %
                   (94.9 % / 95.6 %). */
        }
    }
    part budgets : Budgets;

    requirement def SettledRequirement {
        doc /* The attitude error settles inside the horizon (the flag `settled`): the settling
               time (the traded metric `settling time`, measured) is below the horizon of the
               nominal slew. A slew that never holds inside the band has the horizon as its
               settling time, so this one statement also says that the band was entered and held;
               the slew-time and slew-band requirements of WP22 fold into it (WP23). */
        subject c : Cubesat;
        in settlingTime : TimeValue default = baselineMeasurement.settlingTime;
        require constraint { settlingTime < nominalSlew.horizon }
    }
    requirement def MomentumRequirement {
        doc /* The peak wheel momentum stays within the wheel class capacity (`momentum_ok`). */
        subject c : Cubesat;
        in peakMomentum : AngularMomentumValue default = baselineMeasurement.peakMomentum;
        require constraint { peakMomentum <= c.momentumCapacity }
    }
    requirement def PowerRequirement {
        doc /* The panels cover the housekeeping and tracker loads (`power_ok`); it reads the
               configuration only, so it can be checked before any simulation. */
        subject c : Cubesat;
        require constraint { c.availablePower > 0.0 [W] }
    }
    requirement def DepthOfDischargeRequirement {
        doc /* The depth of discharge, the eclipse demand with the slew loss energy over the battery
               capacity (the traded metric `depth of discharge`), stays within the allowed depth
               of discharge of the environment (`dod_ok`). */
        subject c : Cubesat;
        in torqueSquaredIntegral : Real default = baselineMeasurement.torqueSquaredIntegral;
        require constraint {
            DepthOfDischarge(c, SlewLossEnergy(torqueSquaredIntegral))
                <= environment.maxDepthOfDischarge
        }
    }
    requirement def PointingErrorRequirement {
        doc /* The payload points within the pointing limit: the pointing error (the traded metric
               `pointing error`, an MoE) is within budgets.pointingErrorLimit. It reads the
               configuration only. The baseline configuration fails it (0.0155 against 0.0085
               degree). */
        subject c : Cubesat;
        require constraint { PointingError(c) <= budgets.pointingErrorLimit }
    }
    requirement def ControlEffortRequirement {
        doc /* The slew asks no more of the wheels than the effort budget: the control
               effort (the traded metric `control effort`, measured) is within
               budgets.controlEffortLimit. */
        subject c : Cubesat;
        in controlEffort : AngularMomentumValue default = baselineMeasurement.controlEffort;
        require constraint { controlEffort <= budgets.controlEffortLimit }
    }
    requirement def PeakSlewPowerRequirement {
        doc /* The slew draws no more than the power budget at its peak: the peak slew
               power (the traded metric `peak slew power`) is within budgets.peakSlewPowerLimit.
               It needs the measured peak torque. */
        subject c : Cubesat;
        in peakTorque : TorqueValue default = baselineMeasurement.peakTorque;
        require constraint { PeakSlewPower(c, peakTorque) <= budgets.peakSlewPowerLimit }
    }
    requirement def BatteryPeakPowerRequirement {
        doc /* The pack can carry a slew in eclipse: the eclipse peak load (the housekeeping load plus
               the peak slew power) is within the battery's peak power, its discharge rating times
               its capacity (WP23 round 2: the battery's own rating ties the capacity to the slew's
               peak draw). It needs the measured peak torque and bounds no traded metric by itself,
               so the behavioural view draws it with no line, like the power requirement. */
        subject c : Cubesat;
        in peakTorque : TorqueValue default = baselineMeasurement.peakTorque;
        require constraint { EclipsePeakLoad(c, peakTorque) <= BatteryPeakPower(c) }
    }
    requirement def LaunchBudgetRequirement {
        doc /* The configuration launches within the launch budget: the launch cost (the MoE on
               the traded metric `total mass`) is within budgets.launchBudget. It reads the
               configuration only. */
        subject c : Cubesat;
        require constraint { c.launchCost <= budgets.launchBudget }
    }
    requirement def PowerMarginRequirement {
        doc /* The panels cover the loads at the peak of the slew: the power margin (the traded
               metric `power margin`) is not negative. It needs the measured peak torque. */
        subject c : Cubesat;
        in peakTorque : TorqueValue default = baselineMeasurement.peakTorque;
        require constraint { PowerMargin(c, peakTorque) >= 0.0 [W] }
    }
    requirement def EnergyBalanceRequirement {
        doc /* Over an orbit the panels supply what the loads and the slew consume: the energy
               balance (the traded metric `energy balance`) is not negative. */
        subject c : Cubesat;
        in torqueSquaredIntegral : Real default = baselineMeasurement.torqueSquaredIntegral;
        require constraint {
            EnergyBalance(c, SlewLossEnergy(torqueSquaredIntegral)) >= 0.0 [W*h]
        }
    }

    requirement baselineSettled : SettledRequirement;
    requirement baselineMomentum : MomentumRequirement;
    requirement baselinePower : PowerRequirement;
    requirement baselineDepthOfDischarge : DepthOfDischargeRequirement;
    requirement baselinePointingError : PointingErrorRequirement;
    requirement baselineControlEffort : ControlEffortRequirement;
    requirement baselinePeakSlewPower : PeakSlewPowerRequirement;
    requirement baselineBatteryPeakPower : BatteryPeakPowerRequirement;
    requirement baselineLaunchBudget : LaunchBudgetRequirement;
    requirement baselinePowerMargin : PowerMarginRequirement;
    requirement baselineEnergyBalance : EnergyBalanceRequirement;
    satisfy baselineSettled by cubesatBaseline;
    satisfy baselineMomentum by cubesatBaseline;
    satisfy baselinePower by cubesatBaseline;
    satisfy baselineDepthOfDischarge by cubesatBaseline;
    // the baseline configuration fails the pointing-error requirement (0.0155 against 0.0085 degree)
    not satisfy baselinePointingError by cubesatBaseline;
    satisfy baselineControlEffort by cubesatBaseline;
    satisfy baselinePeakSlewPower by cubesatBaseline;
    satisfy baselineBatteryPeakPower by cubesatBaseline;
    satisfy baselineLaunchBudget by cubesatBaseline;
    satisfy baselinePowerMargin by cubesatBaseline;
    satisfy baselineEnergyBalance by cubesatBaseline;

    verification def ConfigurationVerification {
        doc /* Before simulation: what the configuration alone decides. The power requirement, and
               the requirements on the two traded metrics that depend on the configuration only:
               the pointing error, and the total mass through the launch cost. */
        subject c : Cubesat;
        objective {
            verify requirement power : PowerRequirement;
            verify requirement pointingError : PointingErrorRequirement;
            verify requirement launchBudget : LaunchBudgetRequirement;
        }
    }
    verification def SlewVerification {
        doc /* After the slew is measured: what needs the measured quantities. Each objective below
               verifies the requirement on a traded metric's own quantity: settling time, control
               effort, power margin, energy balance, peak slew power, depth of discharge; the
               momentum requirement reads the measured peak momentum, and the battery peak power
               requirement the pack's rating against the eclipse peak load, neither traded. With
               ConfigurationVerification, every traded metric has a requirement. */
        subject c : Cubesat;
        objective {
            verify requirement settled : SettledRequirement;
            verify requirement momentum : MomentumRequirement;
            verify requirement depthOfDischarge : DepthOfDischargeRequirement;
            verify requirement controlEffort : ControlEffortRequirement;
            verify requirement peakSlewPower : PeakSlewPowerRequirement;
            verify requirement batteryPeakPower : BatteryPeakPowerRequirement;
            verify requirement powerMargin : PowerMarginRequirement;
            verify requirement energyBalance : EnergyBalanceRequirement;
        }
    }

    doc /* Claims over every in-range configuration. The solver (engine `solve`, answer `holds`,
           evidence `proved`) reads arithmetic, comparisons and scalar features, not `calc def`
           invocations; so each claim restates the accounting of section 3 over scalar features,
           with the model's constants as literals (a test ties each literal to its source).
           Constants: generated power per metre of span 81.627336 W/m (flux 1361 W/m^2 times the
           efficiency product 0.08820 times two wings of chord 0.34 m); housekeeping 12 W; idle
           wheels 3 x 0.3 W; eclipse 0.6 h; depth of discharge 0.3; span 0.3 to 1.0 m; tracker power
           0.4 to 1.5 W; battery 20 to 200 Wh. */
    constraint def MassAccountingIdentity {
        doc /* The total mass less the structure mass is the panels plus the antenna. */
        in c : Cubesat;
        (c.bus.mass + c.battery.mass + c.panelPlus.mass + c.panelMinus.mass + c.antenna.mass
            + 3.0 * c.wheel.mass + c.tracker.mass + c.imu.mass)
        - (c.bus.mass + c.battery.mass + 3.0 * c.wheel.mass + c.tracker.mass + c.imu.mass)
            == c.panelPlus.mass + c.panelMinus.mass + c.antenna.mass
    }
    constraint def GeneratedPowerMonotoneInSpan {
        doc /* A longer panel never generates less. */
        in s1 : LengthValue;
        in s2 : LengthValue;
        (s1 <= s2) implies (81.627336 [W/m] * s1 <= 81.627336 [W/m] * s2)
    }
    constraint def PowerRequirementHoldsInRange {
        doc /* Over the whole span and tracker range the available power is positive: `power_ok`
               is true for every in-range configuration. */
        in s : LengthValue;
        in t : PowerValue;
        (s >= 0.3 [m] and s <= 1.0 [m] and t >= 0.4 [W] and t <= 1.5 [W])
            implies (81.627336 [W/m] * s - 12.0 [W] - t > 0.0 [W])
    }
    constraint def SmallBatteryViolatesDepthOfDischarge {
        doc /* A battery below the eclipse base load floor (26.6 Wh at the coarse tracker) fails
               `dod_ok` for every tracker and every non-negative slew energy. */
        in cap : EnergyValue;
        in t : PowerValue;
        in e : EnergyValue;
        (cap >= 20.0 [W*h] and cap <= 26.5 [W*h] and t >= 0.4 [W] and t <= 1.5 [W] and e >= 0.0 [W*h])
            implies ((12.0 [W] + t + 0.9 [W]) * 0.6 [h] + e > 0.3 * cap)
    }
    // END 15.2

    // ==========================================================================================
    // 6. THE EXPERIMENT (assessment view): configuration and measured slew in, attributes out
    // ==========================================================================================
    doc /* The model test of the method's first stage. The subject is a concrete Cubesat (the six
           design variables are its features). The Python runner integrates the slew and hands in
           the measured quantities the accounting needs: the integral of |tau|^2 (N^2.m^2.s), the
           peak torque, the peak wheel momentum and the control effort (integral of |tau|, N.m.s).
           The eight traded metrics are the settling time and the seven attributes this analysis
           returns, in this order: pointing error, total mass, control effort, power margin,
           energy balance, peak slew power, eclipse depth of discharge. The
           settling time is measured, not computed: it goes from the measurement into the output
           row unchanged (it is also the input of the settled requirement of section 5), so it is
           neither an input nor an entry of this return tuple. The peak momentum, measured and not
           used by an attribute, is the input of the momentum requirement. The launch cost is not
           returned: it is the MoE on the total mass, read by its requirement. Flags are not
           returned here. */
    analysis def SlewExperiment {
        subject cubesat : Cubesat;
        in torqueSquaredIntegral : Real;
        in peakTorque : TorqueValue;
        in peakMomentum : AngularMomentumValue;
        in controlEffort : AngularMomentumValue default = baselineMeasurement.controlEffort;
        return attributes = (
            PointingError(cubesat), cubesat.totalMass, controlEffort,
            PowerMargin(cubesat, peakTorque),
            EnergyBalance(cubesat, SlewLossEnergy(torqueSquaredIntegral)),
            PeakSlewPower(cubesat, peakTorque),
            DepthOfDischarge(cubesat, SlewLossEnergy(torqueSquaredIntegral)));
    }

    // ==========================================================================================
    // 7. NAMED CONFIGURATIONS (configuration view)
    // ==========================================================================================
    doc /* The baseline: panel span 0.6 m, 80 Wh battery, medium wheels, medium tracker, the
           lower corner of the baseline gain box. Two contrasts at the corners of the space: the
           agile configuration (large wheels, fine tracker, aggressive gains) and the compact one
           (small wheels, coarse tracker, small panels and battery, gentle gains). */
    part cubesatBaseline : Cubesat {
        part :>> wheel : MediumWheel;
        part :>> tracker : MediumTracker;
    }
    part cubesatAgile : Cubesat {
        :>> panelSpan default = 0.8 [m];
        :>> batteryCapacity default = 140.0 [W*h];
        part :>> wheel : LargeWheel;
        part :>> tracker : FineTracker;
        part :>> controller { :>> Kp default = 1.5; :>> Kd default = 1.2; }
    }
    part cubesatCompact : Cubesat {
        :>> panelSpan default = 0.35 [m];
        :>> batteryCapacity default = 40.0 [W*h];
        part :>> wheel : SmallWheel;
        part :>> tracker : CoarseTracker;
        part :>> controller { :>> Kp default = 0.25; :>> Kd default = 0.4; }
    }
}
