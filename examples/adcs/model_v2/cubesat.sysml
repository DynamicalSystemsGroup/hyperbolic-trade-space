/*
 * cubesat.sysml -- the ILLUSTRATIVE 12U-class cubesat trade space, as one readable model with two
 * views (WP22). It replaced the WP15 model at the recorded gate (9c444e3); that version is in
 * history at 2d13465, and every number and calculation of it is kept here as it was.
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
 * assessed and how each traded metric (the ten of the case study) traces back to this model.
 * Each section header below carries the name of its view. The chain read from the elements: a
 * configuration variable feeds a calc def or the measured slew; the experiment returns the calc as
 * the metric, or the measurement passes it on; a requirement def states the bound on the same calc
 * or measured quantity; a verification case verifies the requirement. Six metrics are covered
 * (settling time, slew time, power margin, energy balance, eclipse reserve, depth of discharge);
 * four are traded with no requirement on them and are named as such in the verification cases.
 * The slew itself is integrated in Python (adcs_sim.simulate_adcs, the measurement of record);
 * SysML v2 cannot integrate the ODE, so the measured quantities enter the experiment as `in`
 * parameters. Section 4 carries a closed-form approximation for model checking.
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
        attribute totalMass : MassValue = MassAccounting(self);
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
           base load over the eclipse; depth of discharge is demand over capacity. */
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
        in c : Cubesat;
        in slewEnergy : EnergyValue;
        return : Real = EclipseDemand(c, slewEnergy) / c.battery.capacity;
    }
    calc def EclipseReserve {
        in c : Cubesat;
        in slewEnergy : EnergyValue;
        return : EnergyValue = environment.maxDepthOfDischarge * c.battery.capacity
            - EclipseDemand(c, slewEnergy);
    }
    calc def OrbitPeriod {
        return : TimeValue = 2.0 * 3.141592653589793 [rad] / environment.orbitalRate;
    }
    calc def EnergyBalance {
        in c : Cubesat;
        in slewEnergy : EnergyValue;
        return : EnergyValue = GeneratedPower(c) * (OrbitPeriod() - environment.eclipseDuration)
            - BaseLoad(c) * OrbitPeriod() - slewEnergy;
    }
    calc def PeakSlewPower {
        in c : Cubesat;
        in peakTorque : TorqueValue;
        return : PowerValue = c.tracker.power + c.wheelCount * environment.wheelIdlePower
            + environment.wheelLossCoefficient * 1.0 [W/(N*m)**2] * peakTorque * peakTorque;
    }
    calc def PowerMargin {
        in c : Cubesat;
        in peakTorque : TorqueValue;
        return : PowerValue = GeneratedPower(c) - environment.housekeepingLoad
            - PeakSlewPower(c, peakTorque);
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
        in c : Cubesat;
        return : PlaneAngleValue = QuantityCalculations::sqrt(
            (4.0 * ((GravityGradientTorque(c) + environment.disturbanceTorque) / 1.0 [N*m])
                / c.controller.Kp * 180.0 / 3.141592653589793) ** 2
            + (c.tracker.accuracy / 1.0 [SI::arcsec] / 3600.0) ** 2) * 1.0 [SI::degree];
    }

    // ==========================================================================================
    // 4. SCENARIOS (assessment view): the slew, and a closed-form approximation of it
    // ==========================================================================================
    doc /* A scenario is a named part of numbers: the slew the experiment simulates and the
           bands that read the response. The ODE (adcs_sim.simulate_adcs) is the measurement of
           record; the closed-form calcs below approximate its slew time, to say something about
           agility over the whole space (model checking) without simulating. */
    part def Scenario {
        doc /* Nominal slew (illustrative): 30 degrees about the body X axis from rest, simulated
               over a 600 s horizon at a 0.5 s step. The slew time is the first time the attitude
               error falls below a 1 degree band (a 0.5 degree band is recorded for sensitivity);
               the settling time is the last time the error exceeds 1 % of its start. */
        attribute slewAngle : PlaneAngleValue = 30.0 [SI::degree];
        attribute horizon : TimeValue = 600.0 [s];
        attribute timeStep : TimeValue = 0.5 [s];
        attribute slewBand : PlaneAngleValue = 1.0 [SI::degree];
        attribute slewBandSensitivity : PlaneAngleValue = 0.5 [SI::degree];
        attribute settlingFraction : Real = 0.01;
    }
    part nominalSlew : Scenario;

    doc /* Closed-form slew time to the band, for the single slew axis (small-angle PD law, torque
           cap T = the usable wheel torque, inertia J, stiffness Kp/4 on the angle, damping Kd):
           torque-limited regime: bang-bang, accelerate at T/J then brake, which enters a band b
           of an angle a at sqrt(J/T) (2 sqrt(a) - sqrt(2 b));
           linear regime: the dominant pole of J th'' + Kd th' + (Kp/4) th = 0 (rate Kd/(2J) when
           underdamped, wn (z - sqrt(z^2 - 1)) when overdamped, wn = sqrt(Kp/(4J)), z =
           Kd/sqrt(J Kp)), entering the band at ln(a/b) / rate.
           The estimate is the larger of the two; the regime is torque-limited when the first
           binds. Against the ODE it is a model-checking approximation, not a replacement. */
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
           requirements, `satisfy` statements tying them to the baseline, `verification def`s
           naming what each verifies, and claims over every in-range configuration. */
    // BEGIN 15.2
    doc /* Feasibility is stated here and verified, not computed in Python. Four requirements, one
           per flag the experiment reports: settled, momentum_ok, power_ok, dod_ok. A requirement
           takes a Cubesat as its subject and, where it needs a measured quantity of the slew, an
           `in` parameter that the runner binds by name (a Quantity, or a Real for the integral of
           |tau|^2). The defaults of those parameters are the recorded measurement of the baseline
           (below), so the `satisfy` statements are checkable without a runner. A fifth requirement
           (the slew band was entered) reads the censoring of the slew time; it is not a flag.
           WP22 round 1 adds four requirements, each over the metric's own quantity (the measured
           slew time, or the calc the experiment returns as the metric), so that the line from a
           requirement to a traded metric is an element of the model and not a sentence: slew time,
           eclipse reserve, power margin, energy balance. The depth-of-discharge requirement is
           restated over the calc that is the metric. Every threshold is a value this model
           already states: zero for a margin, a balance or a reserve, the maximum depth of
           discharge of the environment, the horizon of the nominal slew. */
    part def SlewMeasurement {
        doc /* A measurement of one slew: the quantities the feasibility requirements read. */
        attribute settlingTime : TimeValue;
        attribute slewTime : TimeValue;   // first time the attitude error is inside the slew band
        attribute peakTorque : TorqueValue;
        attribute peakMomentum : AngularMomentumValue;
        attribute controlEffort : AngularMomentumValue;   // integral of |tau| over the slew, N.m.s
        attribute torqueSquaredIntegral : Real;   // N^2 m^2 s
        attribute censored : Boolean;
    }
    part baselineMeasurement : SlewMeasurement {
        doc /* The baseline's slew integrated by adcs_sim.simulate_adcs (600 s horizon, 0.5 s step,
               30 degree slew), recorded to reproduce the verdicts below. A test re-measures it. */
        :>> settlingTime = 180.1904772571943 [s];
        :>> slewTime = 133.6904772571943 [s];
        :>> peakTorque = 0.002 [N*m];
        :>> peakMomentum = 0.00466041037173962 [N*m*s];
        :>> controlEffort = 0.009490621914197469 [N*m*s];
        :>> torqueSquaredIntegral = 7.70613052023095e-06;
        :>> censored = false;
    }

    requirement def SettledRequirement {
        doc /* The attitude error settles inside the horizon (the flag `settled`). */
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
    requirement def SlewTimeRequirement {
        doc /* The slew completes inside the horizon: the slew time (the traded metric `slew time`,
               measured) is below the horizon of the nominal slew. A slew that never enters the
               band has the horizon as its slew time, so this is the same statement as the slew
               band requirement, made over the metric's own quantity. */
        subject c : Cubesat;
        in slewTime : TimeValue default = baselineMeasurement.slewTime;
        require constraint { slewTime < nominalSlew.horizon }
    }
    requirement def EclipseReserveRequirement {
        doc /* The battery keeps a reserve through the eclipse: the eclipse reserve (the traded
               metric `eclipse reserve`) is not negative. */
        subject c : Cubesat;
        in torqueSquaredIntegral : Real default = baselineMeasurement.torqueSquaredIntegral;
        require constraint {
            EclipseReserve(c, SlewLossEnergy(torqueSquaredIntegral)) >= 0.0 [W*h]
        }
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
    requirement def SlewBandRequirement {
        doc /* The slew entered the pointing band within the horizon (the slew time is not
               censored). Not a flag: it qualifies the slew-time attribute. */
        subject c : Cubesat;
        in censored : Boolean default = baselineMeasurement.censored;
        require constraint { censored == false }
    }

    requirement baselineSettled : SettledRequirement;
    requirement baselineMomentum : MomentumRequirement;
    requirement baselinePower : PowerRequirement;
    requirement baselineDepthOfDischarge : DepthOfDischargeRequirement;
    requirement baselineSlewBand : SlewBandRequirement;
    requirement baselineSlewTime : SlewTimeRequirement;
    requirement baselineEclipseReserve : EclipseReserveRequirement;
    requirement baselinePowerMargin : PowerMarginRequirement;
    requirement baselineEnergyBalance : EnergyBalanceRequirement;
    satisfy baselineSettled by cubesatBaseline;
    satisfy baselineMomentum by cubesatBaseline;
    satisfy baselinePower by cubesatBaseline;
    satisfy baselineDepthOfDischarge by cubesatBaseline;
    satisfy baselineSlewBand by cubesatBaseline;
    satisfy baselineSlewTime by cubesatBaseline;
    satisfy baselineEclipseReserve by cubesatBaseline;
    satisfy baselinePowerMargin by cubesatBaseline;
    satisfy baselineEnergyBalance by cubesatBaseline;

    verification def ConfigurationVerification {
        doc /* Before simulation: what the configuration alone decides. Traded metrics with no
               requirement in this model, because it states no bound for them (open, WP22b): the
               pointing error and the total mass, which depend on the configuration only. */
        subject c : Cubesat;
        objective { verify requirement power : PowerRequirement; }
    }
    verification def SlewVerification {
        doc /* After the slew is measured: what needs the measured quantities. Each objective below
               verifies the requirement on a traded metric's own quantity: settling time, slew
               time, eclipse reserve, power margin, energy balance, depth of discharge. Traded
               metrics with no requirement in this model, because it states no bound for them
               (open, WP22b): control effort and peak slew power, which need the measured slew;
               with pointing error and total mass in ConfigurationVerification, these four each need
               a bound the configuration does not state (an angle, a mass, an effort, a power). */
        subject c : Cubesat;
        objective {
            verify requirement settled : SettledRequirement;
            verify requirement momentum : MomentumRequirement;
            verify requirement depthOfDischarge : DepthOfDischargeRequirement;
            verify requirement slewBand : SlewBandRequirement;
            verify requirement slewTime : SlewTimeRequirement;
            verify requirement eclipseReserve : EclipseReserveRequirement;
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
           peak torque, the peak wheel momentum, the control effort (integral of |tau|, N.m.s) and
           whether the slew band was never entered (censored). The analysis returns the eight
           attributes the model computes, in this order: pointing error, total mass, control
           effort, power margin, energy balance, eclipse reserve, peak slew power, eclipse depth
           of discharge. The settling time and the slew time are measured, not computed: they go
           from the measurement into the output row unchanged (the settling time is also the input
           of the settled requirement of section 5), so they are neither inputs nor entries of
           this return tuple (the runtime refuses a return tuple whose entries are equal, and
           a stiff loop makes the two times equal). Measured quantities not used by an attribute
           (peak momentum, censored) are the inputs of those requirements. Flags are not returned
           here. */
    analysis def SlewExperiment {
        subject cubesat : Cubesat;
        in torqueSquaredIntegral : Real;
        in peakTorque : TorqueValue;
        in peakMomentum : AngularMomentumValue;
        in controlEffort : AngularMomentumValue default = baselineMeasurement.controlEffort;
        in censored : Boolean;
        return attributes = (
            PointingError(cubesat), cubesat.totalMass, controlEffort,
            PowerMargin(cubesat, peakTorque),
            EnergyBalance(cubesat, SlewLossEnergy(torqueSquaredIntegral)),
            EclipseReserve(cubesat, SlewLossEnergy(torqueSquaredIntegral)),
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
