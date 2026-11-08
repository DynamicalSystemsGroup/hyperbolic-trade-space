/*
 * cubesat_tradespace.sysml -- WP4b: an ILLUSTRATIVE 12U-class cubesat configuration space.
 *
 * This is documentation of a demonstration, not an engineering model. Every number below is
 * illustrative: chosen for plausibility at cubesat scale (public component classes), never
 * calibrated to hardware, and never fitted to make a result appear. Each constant carries its
 * rationale in a `doc` comment beside it.
 *
 * What the model is for (spec section 3: configure -> model test -> measurements):
 *   - the abstract parts, the enumerations and the design-variable ranges are the configuration
 *     SPACE; the Python sampler (cubesat_model.py) reads them from here and holds no copy;
 *   - a concrete configuration is a `part ... : Cubesat` usage that fixes the design variables;
 *   - the mass and power/energy accounting are `calc def`s evaluated through the opensysml
 *     client; feasibility is `constraint def`s verified per concrete configuration;
 *   - the physics of the slew (the part SysML does not do) stays in Python: the existing
 *     simulator (adcs_sim.py) is called by `measure(configuration)`, and `analysis def ModelTest`
 *     documents that test: configuration in, attributes out.
 *
 * Couplings that reach the controls (the point of the case):
 *   panel span -> panel mass and generated power; span and mass -> slew-axis inertia;
 *   battery capacity -> battery mass -> bus mass -> inertia, and stored energy for the eclipse;
 *   available power (generation minus housekeeping and sensor loads) -> usable wheel torque;
 *   wheel class -> torque, momentum, mass; star-tracker grade -> pointing floor, mass, load.
 *
 * Optional tooling (not a dependency, nothing in tests or CI uses it), if the Rust toolchain
 * Open-MBEE/sysml-toolkit is installed:  sysmlv2 check|fmt|viz cubesat_tradespace.sysml
 */
package CubesatTradeSpace {
    private import ScalarValues::*;
    private import ISQ::*;
    private import SI::*;
    private import NumericalFunctions::min;

    // ------------------------------------------------------------------------------------------
    // Enumerations: the categorical design variables.
    // ------------------------------------------------------------------------------------------
    enum def WheelClass { small; medium; large; }
    enum def TrackerGrade { coarse; medium; fine; }

    // ------------------------------------------------------------------------------------------
    // Abstract parts and the alternatives that specialize them (attribute tables keyed by enum).
    // ------------------------------------------------------------------------------------------
    abstract part def ReactionWheel {
        attribute wheelClass : WheelClass;
        attribute maxTorque : TorqueValue;
        attribute maxMomentum : AngularMomentumValue;
        attribute mass : MassValue;
    }
    doc /* Public cubesat wheel classes (illustrative): small ~ 0.5 mN.m, medium ~ 2 mN.m,
           large ~ 10 mN.m peak torque; momentum storage 5, 20, 100 mN.m.s; mass 0.12, 0.25,
           0.60 kg. The set spans a factor of 20 in torque so that wheel class can trade agility
           against mass and power. */
    part def SmallWheel :> ReactionWheel {
        :>> wheelClass = WheelClass::small;
        :>> maxTorque = 0.0005 [N*m];
        :>> maxMomentum = 0.005 [N*m*s];
        :>> mass = 0.12 [kg];
    }
    part def MediumWheel :> ReactionWheel {
        :>> wheelClass = WheelClass::medium;
        :>> maxTorque = 0.002 [N*m];
        :>> maxMomentum = 0.020 [N*m*s];
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
        attribute accuracy : PlaneAngleValue;     // 1-sigma, arcsec
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

    // ------------------------------------------------------------------------------------------
    // Mission constants (one environment for every configuration).
    // ------------------------------------------------------------------------------------------
    part def Environment {
        doc /* LEO of about 95 minutes: orbital rate 1.13e-3 rad/s; eclipse 0.6 h; a battery
               may be cycled to 0.3 depth of discharge at most (cycle life). */
        attribute orbitalRate : AngularVelocityValue = 1.13e-3 [rad/s];
        attribute eclipseDuration : TimeValue = 0.6 [SI::h];
        attribute maxDepthOfDischarge : Real = 0.3;
        doc /* Solar chain (illustrative): flux 1361 W/m^2, cell efficiency 0.28, packing factor
               0.7, degradation 0.9, mean incidence factor 0.5; the product is about 120 W/m^2
               of panel, averaged over the sunlit arc. */
        attribute solarFlux : IrradianceValue = 1361.0 [W/m**2];
        attribute cellEfficiency : Real = 0.28;
        attribute packingFactor : Real = 0.7;
        attribute degradation : Real = 0.9;
        attribute incidenceFactor : Real = 0.5;
        doc /* Loads (illustrative): housekeeping and payload 12 W; idle power 0.3 W per wheel;
               wheel electrical loss coefficient c = 5e4 W/(N.m)^2, one value for every class,
               so a saturated large wheel (10 mN.m) draws 5 W and a saturated small one 12.5 mW. */
        attribute housekeepingLoad : PowerValue = 12.0 [W];
        attribute wheelIdlePower : PowerValue = 0.3 [W];
        attribute wheelLossCoefficient : Real = 5.0e4;   // W/(N.m)^2
        doc /* Disturbance and areal density (illustrative): constant LEO disturbance torque
               (aerodynamic plus solar) 2e-6 N.m; panel areal density 2.5 kg/m^2 per wing
               including cells and substrate; battery pack specific energy 140 Wh/kg. */
        attribute disturbanceTorque : TorqueValue = 2.0e-6 [N*m];
        attribute panelArealDensity : SurfaceDensityValue = 2.5 [kg/m**2];
        attribute batterySpecificEnergy : Real = 140.0;   // Wh/kg
    }
    part environment : Environment;

    // ------------------------------------------------------------------------------------------
    // The configuration space: bounds of every continuous design variable. Sampled log-uniformly.
    // ------------------------------------------------------------------------------------------
    part def DesignSpace {
        doc /* Ranges (illustrative): panel span 0.3 to 1.0 m per wing (two wings; chord 0.34 m
               so total area 0.2 to 0.68 m^2); battery 20 to 200 Wh; Kp 0.003 to 0.1 N.m/rad and
               Kd 0.03 to 1.0 N.m.s/rad, chosen so that settling times span tens to hundreds of
               seconds on this inertia. */
        attribute panelSpanMin : LengthValue = 0.3 [m];
        attribute panelSpanMax : LengthValue = 1.0 [m];
        attribute batteryCapacityMin : EnergyValue = 20.0 [W*h];
        attribute batteryCapacityMax : EnergyValue = 200.0 [W*h];
        attribute KpMin : Real = 0.003;     // N.m/rad
        attribute KpMax : Real = 0.1;
        attribute KdMin : Real = 0.03;      // N.m.s/rad
        attribute KdMax : Real = 1.0;
    }
    part designSpace : DesignSpace;

    // ------------------------------------------------------------------------------------------
    // The cubesat: composition of the abstract parts, with the design variables as attributes.
    // ------------------------------------------------------------------------------------------
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
    part def Imu { attribute mass : MassValue = 0.1 [kg]; }
    part def Controller {
        attribute Kp : Real default = 0.03;   // N.m/rad
        attribute Kd : Real default = 0.3;    // N.m.s/rad
    }
    part def SolarPanel {
        attribute span : LengthValue default = 0.6 [m];
        attribute chord : LengthValue = 0.34 [m];
        attribute area : AreaValue = span * chord;
        attribute mass : MassValue = PanelMass(span, chord);
    }
    part def Battery {
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
        // Accounting, evaluated by the calculations below.
        attribute totalMass : MassValue = MassAccounting(self);
        attribute structureMass : MassValue = StructureMass(self);
        attribute generatedPower : PowerValue = GeneratedPower(self);
        attribute availablePower : PowerValue = AvailablePower(self);
        attribute usableWheelTorque : TorqueValue = UsableWheelTorque(self);
        attribute sensorLoad : PowerValue = SensorLoad(self);
        attribute baseLoad : PowerValue = BaseLoad(self);
        // Feasibility constraints of this configuration (definitions below).
        constraint powerOk : PowerOK { in c default = self; }
        constraint dodOk : DepthOfDischargeOK { in c default = self; }
    }

    // ------------------------------------------------------------------------------------------
    // Mass accounting. Total = bus + battery + both panels + antenna + 3 wheels + tracker + IMU.
    // The structure mass is what the simulator's inertia model calls the body mass: the total
    // without the panels and the antenna, which the inertia model places by themselves.
    // ------------------------------------------------------------------------------------------
    calc def PanelMass {
        in span : LengthValue;
        in chord : LengthValue;
        return : MassValue = environment.panelArealDensity * span * chord;
    }
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

    // ------------------------------------------------------------------------------------------
    // Power accounting. Generation is proportional to panel area; the power left after the
    // housekeeping and sensor loads is what the wheels can use, and it caps the usable torque.
    // ------------------------------------------------------------------------------------------
    calc def GeneratedPower {
        in c : Cubesat;
        return : PowerValue = environment.solarFlux * environment.cellEfficiency
            * environment.packingFactor * environment.degradation * environment.incidenceFactor
            * (c.panelPlus.area + c.panelMinus.area);
    }
    calc def SensorLoad {
        in c : Cubesat;
        return : PowerValue = c.tracker.power;
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

    // ------------------------------------------------------------------------------------------
    // Slew-dependent energy accounting. The slew's wheel loss energy c * integral(|tau|^2 dt) is
    // measured by the simulator (Python) and passed in; the model does the budget.
    // ------------------------------------------------------------------------------------------
    // Wheel electrical loss energy over the slew: c times the integral of |tau|^2 dt, where the
    // integral (unit N^2.m^2.s) is measured by the simulator and passed in as a plain number.
    calc def SlewLossEnergy {
        in torqueSquaredIntegral : Real;
        return : EnergyValue = environment.wheelLossCoefficient * torqueSquaredIntegral
            * 1.0 [W*s];
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

    // ------------------------------------------------------------------------------------------
    // Feasibility constraints, verified per concrete configuration.
    // ------------------------------------------------------------------------------------------
    constraint def PowerOK {
        in c : Cubesat;
        AvailablePower(c) > 0.0 [W]
    }
    constraint def DepthOfDischargeOK {
        in c : Cubesat;
        in slewEnergy : EnergyValue;
        EclipseDemand(c, slewEnergy) <= environment.maxDepthOfDischarge * c.battery.capacity
    }

    // ------------------------------------------------------------------------------------------
    // The model test: documented, executed by cubesat_model.measure (Python), not by SysML.
    // ------------------------------------------------------------------------------------------
    analysis def ModelTest {
        doc /* Configuration in, attributes out. For a concrete Cubesat: (1) the model evaluates
               the mass and power accounting and the usable wheel torque; (2) Python runs the
               existing attitude simulator for a slew with that torque cap and the structure
               mass, panel span and panel mass in the inertia model; (3) the model evaluates the
               energy accounting and the constraints on the measured slew energy and peak
               torque. Attributes: settling time, pointing error, total mass, control effort,
               power margin, energy balance, eclipse reserve, peak slew power, eclipse depth of
               discharge; flags: settled, momentum_ok, torque_saturated_frac, power_ok, dod_ok. */
        subject cubesat : Cubesat;
        return totalMass : MassValue = cubesat.totalMass;
    }

    // ------------------------------------------------------------------------------------------
    // The baseline configuration: panel span 0.6 m, 80 Wh battery, medium wheels, medium tracker.
    // ------------------------------------------------------------------------------------------
    part cubesatBaseline : Cubesat {
        part :>> wheel : MediumWheel;
        part :>> tracker : MediumTracker;
    }
}
