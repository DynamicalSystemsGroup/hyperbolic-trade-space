
package CubesatTradeSpaceV2 {
    private import ScalarValues::*;
    private import ISQ::*;
    private import SI::*;
    private import NumericalFunctions::min;
    private import NumericalFunctions::max;
    private import NumericalFunctions::abs;
    private import OpenSysMLMathFunctions::ln;

    doc /* The seven design variables. */
    enum def WheelClass { small; medium; large; }
    enum def TrackerGrade { coarse; medium; fine; }

    abstract part def ReactionWheel {
        attribute wheelClass : WheelClass;
        attribute maxTorque : TorqueValue;
        attribute maxMomentum : AngularMomentumValue;
        attribute mass : MassValue;
    }
    doc /* Public cubesat wheel classes (illustrative): small ~ 0.3 mN.m, medium ~ 2 mN.m, large ~ 10 mN.m peak torque; */
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
        attribute accuracy : PlaneAngleValue;
        attribute mass : MassValue;
        attribute power : PowerValue;
    }
    doc /* Star-tracker grades (illustrative): coarse 30 arcsec / 0.15 kg / 0.4 W, medium 10 arcsec / 0.35 kg / 0.9 W, fine 2 arcsec / 0.90 kg / 1.5 W. */
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
        doc /* Ranges (illustrative): panel span 0.3 to 1.0 m per wing (two wings; */
        attribute panelSpanMin : LengthValue = 0.3 [m];
        attribute panelSpanMax : LengthValue = 1.0 [m];
        attribute batteryCapacityMin : EnergyValue = 20.0 [W*h];
        attribute batteryCapacityMax : EnergyValue = 200.0 [W*h];
        doc /* The fleet size (WP30): 1 to 30 identical satellites, a real number in the model (the pricing curves of section 3 are posynomials in it, which need real exponents) and read as a count. */
        attribute fleetSizeMin : Real = 1.0;
        attribute fleetSizeMax : Real = 30.0;
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
        doc /* Baseline box: Kp 0.03 to 1.0 and Kd 0.3 to 1.5, a stiff attitude loop that asks for more torque than a cubesat wheel gives on a large slew, so the wheel class binds. */
        :>> KpMin = 0.03;
        :>> KpMax = 1.0;
        :>> KdMin = 0.3;
        :>> KdMax = 1.5;
    }
    part aggressiveGains : GainBox {
        doc /* Aggressive box (the primary dataset): Kp 0.2 to 2.0, Kd 0.3 to 1.5, with Kd/Kp mostly at or below 5, where the wheel class separates the slew time. */
        :>> KpMin = 0.2;
        :>> KpMax = 2.0;
        :>> KdMin = 0.3;
        :>> KdMax = 1.5;
    }

    doc /* The cubesat is a composition of fixed parts (bus, antenna, IMU) and of the parts the design variables select (two solar panels of one span, a battery of one capacity, three identical orthogonal wheels, a tracker, the controller gains). */
    part def Environment {
        doc /* LEO of about 95 minutes: orbital rate 1.13e-3 rad/s; */
        attribute orbitalRate : AngularVelocityValue = 1.13e-3 [rad/s];
        attribute eclipseDuration : TimeValue = 0.6 [h];
        attribute maxDepthOfDischarge : Real = 0.3;
        doc /* Solar chain (illustrative): flux 1361 W/m^2, cell efficiency 0.28, packing factor 0.7, degradation 0.9, mean incidence factor 0.5; */
        attribute solarFlux : IrradianceValue = 1361.0 [W/m**2];
        attribute cellEfficiency : Real = 0.28;
        attribute packingFactor : Real = 0.7;
        attribute degradation : Real = 0.9;
        attribute incidenceFactor : Real = 0.5;
        doc /* Loads (illustrative): housekeeping and payload 12 W; */
        attribute housekeepingLoad : PowerValue = 12.0 [W];
        attribute wheelIdlePower : PowerValue = 0.3 [W];
        attribute wheelLossCoefficient : Real = 5.0e4;
        doc /* Disturbance and areal density (illustrative): constant LEO disturbance torque (aerodynamic plus solar) 2e-6 N.m; */
        attribute disturbanceTorque : TorqueValue = 2.0e-6 [N*m];
        attribute gravityGradientOffset : PlaneAngleValue = 1.7453292519943296e-3 [rad];
        attribute panelArealDensity : SurfaceDensityValue = 2.5 [kg/m**2];
        attribute batterySpecificEnergy : Real = 140.0;
        doc /* Battery rating (illustrative, WP23 round 2): a continuous discharge rating of 1 C, the pack delivering its capacity in one hour, the plain rating of a small-satellite lithium-ion pack; */
        attribute batteryDischargeRate : Real = 1.0;
        doc /* Launch (WP30, spike D section 3, D-1; */
        attribute launchRate : Real = 7000.0;
    }
    part environment : Environment;

    part def Bus {
        doc /* 12U-class body 0.226 x 0.226 x 0.340 m; */
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
        doc /* PD attitude law tau = -Kp/2 q - Kd omega per axis, clipped at the usable torque. */
        attribute Kp : Real default = 0.03;
        attribute Kd : Real default = 0.3;
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
        attribute panelSpan : LengthValue default = 0.6 [m];
        attribute batteryCapacity : EnergyValue default = 80.0 [W*h];
        attribute fleetSize : Real default = 1.0;
        part bus : Bus;
        part panelPlus : SolarPanel { :>> span = Cubesat::panelSpan; }
        part panelMinus : SolarPanel { :>> span = Cubesat::panelSpan; }
        part battery : Battery { :>> capacity = Cubesat::batteryCapacity; }
        part antenna : Antenna;
        part imu : Imu;
        part wheel : ReactionWheel;
        part tracker : StarTracker;
        part controller : Controller;
        attribute wheelCount : Integer = 3;
        attribute totalMass : MassValue = MassAccounting(self) {
            doc /* MoP: the launch mass of the configuration (the traded metric `total mass`); */
        }
        attribute launchCost : Real = LaunchCost(self);
        attribute structureMass : MassValue = StructureMass(self);
        attribute adcsMass : MassValue = AdcsMass(self);
        attribute momentumCapacity : AngularMomentumValue = wheel.maxMomentum;
        attribute generatedPower : PowerValue = GeneratedPower(self);
        attribute availablePower : PowerValue = AvailablePower(self);
        attribute usableWheelTorque : TorqueValue = UsableWheelTorque(self);
    }

    doc /* Mass: total = bus + battery + both panels + antenna + 3 wheels + tracker + IMU. */
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
        doc /* MoE: the cost to launch the configuration, the launch rate times the total mass (USD); */
        in c : Cubesat;
        return : Real = environment.launchRate * (c.totalMass / 1.0 [kg]);
    }
    doc /* The cost model prices the manufacturing and launch of a fleet of identical satellites, per unit: the fleet enters only as the variable `fleetSize` and the fleet cost. */
    part def Prices {
        doc /* Single-unit prices (USD), n = 1, at the 2026 listings of spike D2 (WP23-rounds/spikes/spike-D2-prices-2026, pages opened 2026-11-11). */
        attribute bus : Real = 60000.0;
        attribute antenna : Real = 15000.0;
        attribute imu : Real = 5000.0;
        attribute panelPerArea : Real = 340000.0;
        attribute batteryPerEnergy : Real = 70.0;
        attribute wheelBase : Real = 4000.0;
        attribute wheelPerTorque : Real = 2.0e6;
        attribute trackerBase : Real = 5000.0;
        attribute trackerPerFineness : Real = 150000.0;
        attribute assembly : Real = 100000.0;
    }
    part prices : Prices;
    part def PricingCurves {
        doc /* The fixed share f_p and the learning slope s_p of each part's curve (spike D, section 3; */
        attribute busShare : Real = 0.30;
        attribute busSlope : Real = 0.90;
        attribute panelShare : Real = 0.15;
        attribute panelSlope : Real = 0.90;
        attribute batteryShare : Real = 0.10;
        attribute batterySlope : Real = 0.90;
        attribute wheelShare : Real = 0.15;
        attribute wheelSlope : Real = 0.95;
        attribute trackerShare : Real = 0.20;
        attribute trackerSlope : Real = 0.95;
        attribute assemblyShare : Real = 0.50;
        attribute assemblySlope : Real = 0.90;
    }
    part pricing : PricingCurves;

    calc def PartTotal {
        doc /* The total price (USD) of a part for a fleet of n: the single-unit price times the fixed share plus the learning share times n^(1 - b), b = -log2(slope), written with the natural logarithm (ln 2 = 0.6931471805599453). */
        in unitPrice : Real;
        in fixedShare : Real;
        in slope : Real;
        in n : Real;
        return : Real = unitPrice * (fixedShare
            + (1.0 - fixedShare) * n ** (1.0 + ln(slope) / 0.6931471805599453));
    }
    calc def PanelPrice {
        in c : Cubesat;
        return : Real = prices.panelPerArea
            * ((c.panelPlus.area + c.panelMinus.area) / 1.0 [m**2]);
    }
    calc def BatteryPrice {
        in c : Cubesat;
        return : Real = prices.batteryPerEnergy * (c.battery.capacity / 1.0 [W*h]);
    }
    calc def WheelPrice {
        in c : Cubesat;
        return : Real = c.wheelCount * (prices.wheelBase
            + prices.wheelPerTorque * (c.wheel.maxTorque / 1.0 [N*m]));
    }
    calc def TrackerPrice {
        in c : Cubesat;
        return : Real = prices.trackerBase
            + prices.trackerPerFineness / (c.tracker.accuracy / 1.0 [SI::arcsec]);
    }
    calc def BusTotal {
        in c : Cubesat;
        return : Real = PartTotal(prices.bus + prices.antenna + prices.imu, pricing.busShare,
            pricing.busSlope, c.fleetSize);
    }
    calc def PanelTotal {
        in c : Cubesat;
        return : Real = PartTotal(PanelPrice(c), pricing.panelShare, pricing.panelSlope,
            c.fleetSize);
    }
    calc def BatteryTotal {
        in c : Cubesat;
        return : Real = PartTotal(BatteryPrice(c), pricing.batteryShare, pricing.batterySlope,
            c.fleetSize);
    }
    calc def WheelTotal {
        in c : Cubesat;
        return : Real = PartTotal(WheelPrice(c), pricing.wheelShare, pricing.wheelSlope,
            c.fleetSize);
    }
    calc def TrackerTotal {
        in c : Cubesat;
        return : Real = PartTotal(TrackerPrice(c), pricing.trackerShare, pricing.trackerSlope,
            c.fleetSize);
    }
    calc def AssemblyTotal {
        doc /* Assembly, integration and test: a line of its own, 100,000 USD for one satellite (unsourced), half of it fixed (procedures, fixtures, the test campaign). */
        in c : Cubesat;
        return : Real = PartTotal(prices.assembly, pricing.assemblyShare, pricing.assemblySlope,
            c.fleetSize);
    }
    calc def FleetBuildCost {
        doc /* The cost to build the fleet (USD): the parts and the assembly line, without the launch. */
        in c : Cubesat;
        return : Real = BusTotal(c) + PanelTotal(c) + BatteryTotal(c) + WheelTotal(c)
            + TrackerTotal(c) + AssemblyTotal(c);
    }
    calc def FleetCost {
        doc /* MoE: the cost to build and launch the fleet (USD), the traded metric `fleet cost`: the build cost of the parts and the assembly line plus the launch of every satellite at the launch rate times its mass. */
        in c : Cubesat;
        return : Real = FleetBuildCost(c) + c.fleetSize * c.launchCost;
    }
    calc def UnitCost {
        doc /* MoE: the cost per satellite to build and launch the fleet (USD), the traded metric `unit cost`: the fleet cost over the fleet size, read at the configuration's own fleet size. */
        in c : Cubesat;
        return : Real = FleetCost(c) / c.fleetSize;
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
        doc /* MoP: the generated power left after the housekeeping load and the tracker (the traded metric `available power`), positive wherever the power requirement holds. */
        in c : Cubesat;
        return : PowerValue = GeneratedPower(c) - environment.housekeepingLoad - c.tracker.power;
    }
    calc def UsableWheelTorque {
        in c : Cubesat;
        return : TorqueValue = if AvailablePower(c) > 0.0 [W]
            ? min(c.wheel.maxTorque / 1.0 [N*m],
                  QuantityCalculations::sqrt(AvailablePower(c)
                      / (c.wheelCount * environment.wheelLossCoefficient * 1.0 [W/(N*m)**2]))
                  / 1.0 [N*m]) * 1.0 [N*m]
            else 0.01 * c.wheel.maxTorque;
    }
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
        doc /* MoP: the eclipse depth of discharge, the eclipse demand with the slew loss energy over the battery capacity (the traded metric `depth of discharge`). */
        in c : Cubesat;
        in slewEnergy : EnergyValue;
        return : Real = EclipseDemand(c, slewEnergy) / c.battery.capacity;
    }
    calc def OrbitPeriod {
        return : TimeValue = 2.0 * 3.141592653589793 [rad] / environment.orbitalRate;
    }
    calc def EnergyBalance {
        doc /* MoP: over one orbit, the energy the panels supply in sunlight less the base load over the orbit and the slew loss energy (the traded metric `energy balance`). */
        in c : Cubesat;
        in slewEnergy : EnergyValue;
        return : EnergyValue = GeneratedPower(c) * (OrbitPeriod() - environment.eclipseDuration)
            - BaseLoad(c) * OrbitPeriod() - slewEnergy;
    }
    calc def PeakSlewPower {
        doc /* MoP: the electrical power drawn at the peak of the slew, the tracker and idle wheel loads plus the wheel loss at the measured peak torque (the traded metric `peak slew power`). */
        in c : Cubesat;
        in peakTorque : TorqueValue;
        return : PowerValue = c.tracker.power + c.wheelCount * environment.wheelIdlePower
            + environment.wheelLossCoefficient * 1.0 [W/(N*m)**2] * peakTorque * peakTorque;
    }
    calc def PowerMargin {
        doc /* MoP: the generated power left after the housekeeping load and the peak slew power (the traded metric `power margin`). */
        in c : Cubesat;
        in peakTorque : TorqueValue;
        return : PowerValue = GeneratedPower(c) - environment.housekeepingLoad
            - PeakSlewPower(c, peakTorque);
    }
    calc def MomentumHeadroom {
        doc /* MoP: the wheel's momentum capacity over the peak wheel momentum of the slew (the traded metric `momentum headroom`), 1 where the peak momentum just reaches the capacity and above 1 where the wheel keeps reserve; */
        in c : Cubesat;
        in peakMomentum : AngularMomentumValue;
        return : Real = c.momentumCapacity / peakMomentum;
    }
    calc def BatteryPeakPowerRatio {
        doc /* MoP: the pack's peak power over the eclipse peak load (the traded metric `battery peak power ratio`), 1 where the pack just carries the slew in eclipse and above 1 where it keeps reserve. */
        in c : Cubesat;
        in peakTorque : TorqueValue;
        return : Real = BatteryPeakPower(c) / EclipsePeakLoad(c, peakTorque);
    }
    calc def BatteryPeakPower {
        doc /* The power the pack can deliver at its continuous discharge rating: the discharge rate times the capacity (W). */
        in c : Cubesat;
        return : PowerValue = environment.batteryDischargeRate * c.battery.capacity / 1.0 [h];
    }
    calc def EclipsePeakLoad {
        doc /* The load the battery alone carries at the peak of a slew in eclipse, where the panels give nothing: the housekeeping load plus the peak slew power. */
        in c : Cubesat;
        in peakTorque : TorqueValue;
        return : PowerValue = environment.housekeepingLoad + PeakSlewPower(c, peakTorque);
    }
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
    calc def GravityGradientTorque {
        in c : Cubesat;
        return : TorqueValue = 3.0 * (environment.orbitalRate / 1.0 [rad/s]) ** 2
            * max(abs((InertiaZ(c) - InertiaY(c)) / 1.0 [kg*m**2]),
                  abs((InertiaZ(c) - InertiaX(c)) / 1.0 [kg*m**2]))
            * (environment.gravityGradientOffset / 1.0 [rad]) * 1.0 [N*m];
    }
    calc def PointingError {
        doc /* MoE: how well the payload points, the root-sum-square of the steady attitude error under the disturbance and gravity-gradient torques and the star tracker's accuracy (the traded metric `pointing error`); */
        in c : Cubesat;
        return : PlaneAngleValue = QuantityCalculations::sqrt(
            (4.0 * ((GravityGradientTorque(c) + environment.disturbanceTorque) / 1.0 [N*m])
                / c.controller.Kp * 180.0 / 3.141592653589793) ** 2
            + (c.tracker.accuracy / 1.0 [SI::arcsec] / 3600.0) ** 2) * 1.0 [SI::degree];
    }

    doc /* A scenario is a named part of numbers: the slew the experiment simulates and the band that reads the response. */
    part def Scenario {
        doc /* Nominal slew (illustrative): 30 degrees about the body X axis from rest, simulated over a 600 s horizon at a 0.5 s step. */
        attribute slewAngle : PlaneAngleValue = 30.0 [SI::degree];
        attribute horizon : TimeValue = 600.0 [s];
        attribute timeStep : TimeValue = 0.5 [s];
        attribute slewBand : PlaneAngleValue = 1.0 [SI::degree];
        attribute settlingFraction : Real = 0.01;
    }
    part nominalSlew : Scenario;

    doc /* Closed-form time to the band, for the single slew axis (small-angle PD law, torque cap T = the usable wheel torque, inertia J, stiffness Kp/4 on the angle, damping Kd): torque-limited regime: bang-bang, accelerate at T/J then brake, which enters a band b of an angle a at sqrt(J/T) (2 sqrt(a) - sqrt(2 b)); */
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

    doc /* The four feasibility flags (settled, momentum_ok, power_ok, dod_ok) as named requirements, one requirement on every traded metric's own quantity, the four thresholds, `satisfy` statements tying each requirement to the baseline, `verification def`s naming what each verifies, and claims over every in-range configuration. */
    doc /* Feasibility is stated here and verified, not computed in Python. */
    part def SlewMeasurement {
        doc /* A measurement of one slew: the quantities the requirements and the experiment read. */
        attribute settlingTime : TimeValue {
            doc /* MoP: the settling time (the traded metric `settling time`): the hold time, the first time after which the pointing error stays inside the settling band, computed by event detection as the last exit from the band. */
        }
        attribute peakTorque : TorqueValue;
        attribute peakMomentum : AngularMomentumValue;
        attribute controlEffort : AngularMomentumValue {
            doc /* MoP: the control effort (the traded metric `control effort`), the integral of |tau| over the slew, N.m.s: what the slew asks of the wheels. */
        }
        attribute torqueSquaredIntegral : Real;
    }
    part baselineMeasurement : SlewMeasurement {
        doc /* The baseline's slew integrated by adcs_sim.simulate_adcs (600 s horizon, 0.5 s step, 30 degree slew), recorded to reproduce the verdicts below. */
        :>> settlingTime = 180.1904772571943 [s];
        :>> peakTorque = 0.002 [N*m];
        :>> peakMomentum = 0.00466041037173962 [N*m*s];
        :>> controlEffort = 0.009490621914197469 [N*m*s];
        :>> torqueSquaredIntegral = 7.70613052023095e-06;
    }
    part def Budgets {
        doc /* The cost limits of WP30 (the unit cost and the fleet cost) are the supervisor's values (WP30-decisions.md, 2026-11-11); */
        attribute pointingErrorLimit : PlaneAngleValue = 0.008495 [degree] {
            doc /* 0.0085 degree, the row that admits 95 % of the primary regime (95.0 % / 63.7 %), kept knowing that the baseline configuration (0.015535 degree) fails it ("Keep 0.0085 deg", 2026-11-10, 08:55). */
        }
        attribute controlEffortLimit : AngularMomentumValue = 0.05922 [N*m*s] {
            doc /* 0.059 N.m.s, the row that admits 90 % of the baseline regime (58.9 % / 90.0 %). */
        }
        attribute peakSlewPowerLimit : PowerValue = 2.6 [W] {
            doc /* 2.6 W, the row that admits every small and medium wheel (62.2 % / 67.3 %). */
        }
        attribute launchBudget : Real = 105770.0 {
            doc /* 105,770 USD, 15.11 kg at the 7,000 USD/kg of WP30 (D-1): the supervisor's budget was the mass of the row that admits 95 % (94.9 % / 95.6 %), 15.107 kg, stated in USD at the earlier 6,000 USD/kg as 90,643; */
        }
        attribute unitCostLimit : Real = 350000.0 {
            doc /* 350,000 USD per satellite on the covered cost, read at the design's own fleet size (the supervisor's value, WP30-decisions.md, 2026-11-11: "i want to lean smaller and its fine that no single satellite clears it"; */
        }
        attribute fleetCostLimit : Real = 6.0e6 {
            doc /* 6,000,000 USD on the covered fleet cost, build and launch, the fleet size free from 1 to 30 (the supervisor's value, WP30-decisions.md, 2026-11-11). */
        }
    }
    part budgets : Budgets;

    requirement def SettledRequirement {
        doc /* The attitude error settles inside the horizon (the flag `settled`): the settling time (the traded metric `settling time`, measured) is below the horizon of the nominal slew. */
        subject c : Cubesat;
        in settlingTime : TimeValue default = baselineMeasurement.settlingTime;
        require constraint { settlingTime < nominalSlew.horizon }
    }
    requirement def MomentumRequirement {
        doc /* The peak wheel momentum stays within the wheel class capacity (`momentum_ok`): the momentum headroom (the traded metric `momentum headroom`, measured peak momentum against the wheel class capacity) is at least 1. */
        subject c : Cubesat;
        in peakMomentum : AngularMomentumValue default = baselineMeasurement.peakMomentum;
        require constraint { MomentumHeadroom(c, peakMomentum) >= 1.0 }
    }
    requirement def PowerRequirement {
        doc /* The panels cover the housekeeping and tracker loads (`power_ok`): the available power (the traded metric `available power`) is positive. */
        subject c : Cubesat;
        require constraint { AvailablePower(c) > 0.0 [W] }
    }
    requirement def DepthOfDischargeRequirement {
        doc /* The depth of discharge, the eclipse demand with the slew loss energy over the battery capacity (the traded metric `depth of discharge`), stays within the allowed depth of discharge of the environment (`dod_ok`). */
        subject c : Cubesat;
        in torqueSquaredIntegral : Real default = baselineMeasurement.torqueSquaredIntegral;
        require constraint {
            DepthOfDischarge(c, SlewLossEnergy(torqueSquaredIntegral))
                <= environment.maxDepthOfDischarge
        }
    }
    requirement def PointingErrorRequirement {
        doc /* The payload points within the pointing limit: the pointing error (the traded metric `pointing error`, an MoE) is within budgets.pointingErrorLimit. */
        subject c : Cubesat;
        require constraint { PointingError(c) <= budgets.pointingErrorLimit }
    }
    requirement def ControlEffortRequirement {
        doc /* The slew asks no more of the wheels than the effort budget: the control effort (the traded metric `control effort`, measured) is within budgets.controlEffortLimit. */
        subject c : Cubesat;
        in controlEffort : AngularMomentumValue default = baselineMeasurement.controlEffort;
        require constraint { controlEffort <= budgets.controlEffortLimit }
    }
    requirement def PeakSlewPowerRequirement {
        doc /* The slew draws no more than the power budget at its peak: the peak slew power (the traded metric `peak slew power`) is within budgets.peakSlewPowerLimit. */
        subject c : Cubesat;
        in peakTorque : TorqueValue default = baselineMeasurement.peakTorque;
        require constraint { PeakSlewPower(c, peakTorque) <= budgets.peakSlewPowerLimit }
    }
    requirement def BatteryPeakPowerRequirement {
        doc /* The pack can carry a slew in eclipse: the eclipse peak load (the housekeeping load plus the peak slew power) is within the battery's peak power, its discharge rating times its capacity (WP23 round 2: the battery's own rating ties the capacity to the slew's peak draw); */
        subject c : Cubesat;
        in peakTorque : TorqueValue default = baselineMeasurement.peakTorque;
        require constraint { BatteryPeakPowerRatio(c, peakTorque) >= 1.0 }
    }
    requirement def LaunchBudgetRequirement {
        doc /* The configuration launches within the launch budget: the launch cost (the MoE on the traded metric `total mass`) is within budgets.launchBudget. */
        subject c : Cubesat;
        require constraint { c.launchCost <= budgets.launchBudget }
    }
    requirement def UnitCostRequirement {
        doc /* The configuration costs within the unit cost limit to build and launch, per satellite, at its own fleet size: the unit cost (the traded metric `unit cost`, an MoE) is within budgets.unitCostLimit, 350,000 USD. */
        subject c : Cubesat;
        require constraint { UnitCost(c) <= budgets.unitCostLimit }
    }
    requirement def FleetCostRequirement {
        doc /* The fleet costs within the fleet cost limit to build and launch, with its size free: the fleet cost (the traded metric `fleet cost`, an MoE) is within budgets.fleetCostLimit, 6,000,000 USD. */
        subject c : Cubesat;
        require constraint { FleetCost(c) <= budgets.fleetCostLimit }
    }
    requirement def PowerMarginRequirement {
        doc /* The panels cover the loads at the peak of the slew: the power margin (the traded metric `power margin`) is not negative. */
        subject c : Cubesat;
        in peakTorque : TorqueValue default = baselineMeasurement.peakTorque;
        require constraint { PowerMargin(c, peakTorque) >= 0.0 [W] }
    }
    requirement def EnergyBalanceRequirement {
        doc /* Over an orbit the panels supply what the loads and the slew consume: the energy balance (the traded metric `energy balance`) is not negative. */
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
    requirement baselineUnitCost : UnitCostRequirement;
    requirement baselineFleetCost : FleetCostRequirement;
    requirement baselinePowerMargin : PowerMarginRequirement;
    requirement baselineEnergyBalance : EnergyBalanceRequirement;
    satisfy baselineSettled by cubesatBaseline;
    satisfy baselineMomentum by cubesatBaseline;
    satisfy baselinePower by cubesatBaseline;
    satisfy baselineDepthOfDischarge by cubesatBaseline;
    not satisfy baselinePointingError by cubesatBaseline;
    satisfy baselineControlEffort by cubesatBaseline;
    satisfy baselinePeakSlewPower by cubesatBaseline;
    satisfy baselineBatteryPeakPower by cubesatBaseline;
    satisfy baselineLaunchBudget by cubesatBaseline;
    not satisfy baselineUnitCost by cubesatBaseline;
    satisfy baselineFleetCost by cubesatBaseline;
    satisfy baselinePowerMargin by cubesatBaseline;
    satisfy baselineEnergyBalance by cubesatBaseline;

    verification def ConfigurationVerification {
        doc /* Before simulation: what the configuration alone decides. */
        subject c : Cubesat;
        objective {
            verify requirement power : PowerRequirement;
            verify requirement pointingError : PointingErrorRequirement;
            verify requirement launchBudget : LaunchBudgetRequirement;
            verify requirement unitCost : UnitCostRequirement;
            verify requirement fleetCost : FleetCostRequirement;
        }
    }
    verification def SlewVerification {
        doc /* After the slew is measured: what needs the measured quantities. */
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

    doc /* Claims over every in-range configuration. */
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
        doc /* Over the whole span and tracker range the available power is positive: `power_ok` is true for every in-range configuration. */
        in s : LengthValue;
        in t : PowerValue;
        (s >= 0.3 [m] and s <= 1.0 [m] and t >= 0.4 [W] and t <= 1.5 [W])
            implies (81.627336 [W/m] * s - 12.0 [W] - t > 0.0 [W])
    }
    constraint def BatteryPeakPowerRequirementHoldsInRange {
        doc /* Over the whole battery, tracker and wheel-torque range the pack's rated power covers the eclipse peak load (housekeeping, tracker, three idle wheels and the wheel loss at the peak torque, at most 0.010 N.m): `BatteryPeakPowerRequirement` holds for every in-range configuration, 20 W against at most 19.4 W. */
        in cap : EnergyValue;
        in t : PowerValue;
        in tau : TorqueValue;
        (cap >= 20.0 [W*h] and t >= 0.4 [W] and t <= 1.5 [W] and tau >= 0.0 [N*m]
            and tau <= 0.010 [N*m])
            implies (1.0 * cap / 1.0 [h] >= 12.0 [W] + t + 3.0 * 0.3 [W]
                + 5.0e4 [W/(N*m)**2] * tau * tau)
    }
    constraint def SmallBatteryViolatesDepthOfDischarge {
        doc /* A battery below the eclipse base load floor (26.6 Wh at the coarse tracker) fails `dod_ok` for every tracker and every non-negative slew energy. */
        in cap : EnergyValue;
        in t : PowerValue;
        in e : EnergyValue;
        (cap >= 20.0 [W*h] and cap <= 26.5 [W*h] and t >= 0.4 [W] and t <= 1.5 [W] and e >= 0.0 [W*h])
            implies ((12.0 [W] + t + 0.9 [W]) * 0.6 [h] + e > 0.3 * cap)
    }

    doc /* The model test of the method's first stage. */
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
            DepthOfDischarge(cubesat, SlewLossEnergy(torqueSquaredIntegral)),
            MomentumHeadroom(cubesat, peakMomentum),
            AvailablePower(cubesat),
            BatteryPeakPowerRatio(cubesat, peakTorque));
    }
    analysis def UnitCostExperiment {
        doc /* The traded metric `unit cost` (MoE): the cost per satellite to build and launch the configuration's fleet, at its own fleet size. */
        subject cubesat : Cubesat;
        return attributes = (UnitCost(cubesat));
    }
    analysis def FleetCostExperiment {
        doc /* The traded metric `fleet cost` (MoE): the cost to build and launch the configuration's fleet, at its own fleet size. */
        subject cubesat : Cubesat;
        return attributes = (FleetCost(cubesat));
    }

    doc /* The baseline: panel span 0.6 m, 80 Wh battery, medium wheels, medium tracker, the lower corner of the baseline gain box. */
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


package CubesatStakeholders {
    private import ScalarValues::*;
    private import ISQ::*;
    private import SI::*;
    private import CubesatTradeSpaceV2::*;

    part def Sponsor {
        doc /* Pays for the mission and answers for it. */
    }
    part def Manufacturer {
        doc /* Builds the satellites. */
    }
    part def Operator {
        doc /* Flies the cubesat. */
    }
    part sponsor : Sponsor;
    part manufacturer : Manufacturer;
    part operator : Operator;

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
        doc /* The fleet costs little to build and to launch. */
        subject :>> c;
        stakeholder :>> s = sponsor;
        requirement launchBudget : LaunchBudgetRequirement;
        requirement fleetCost : FleetCostRequirement;
    }
    concern lowUnitCost : ManufacturingConcern {
        doc /* Each satellite costs little to build and to launch at the fleet size it is built in: the unit cost (a traded cost metric of the cost model, WP30, the fleet cost over the fleet size) is bounded by the unit cost requirement, 350,000 USD a satellite, on the covered cost as lowCost states it. */
        subject :>> c;
        stakeholder :>> s = manufacturer;
        requirement unitCost : UnitCostRequirement;
    }
    concern longLife : PriceConcern {
        doc /* The cubesat serves long. */
        subject :>> c;
        stakeholder :>> s = sponsor;
        requirement depthOfDischarge : DepthOfDischargeRequirement;
    }
    concern pointingAndSlewing : PerformanceConcern {
        doc /* The cubesat points the payload accurately and slews and settles in time, within what its wheels can store and give. */
        subject :>> c;
        stakeholder :>> s = operator;
        requirement pointingError : PointingErrorRequirement;
        requirement settled : SettledRequirement;
        requirement controlEffort : ControlEffortRequirement;
        requirement momentum : MomentumRequirement;
    }
    concern powerAndEnergy : PerformanceConcern {
        doc /* The cubesat's power and energy hold up through an orbit and through a slew in eclipse. */
        subject :>> c;
        stakeholder :>> s = operator;
        requirement power : PowerRequirement;
        requirement powerMargin : PowerMarginRequirement;
        requirement energyBalance : EnergyBalanceRequirement;
        requirement peakSlewPower : PeakSlewPowerRequirement;
        requirement batteryPeakPower : BatteryPeakPowerRequirement;
        requirement eclipseDepthOfDischarge : DepthOfDischargeRequirement;
    }

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

    part agileMeasurement : SlewMeasurement {
        doc /* The agile configuration's slew integrated by adcs_sim.simulate_adcs (600 s horizon, 0.5 s step, 30 degree slew), recorded as the baseline's is in cubesat.sysml, to reproduce the verdicts below. */
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

    calc def CostToBuild {
        doc /* Illustrative roll-up for the sponsor's low cost: the cost to build one satellite of the configuration's fleet (USD), the parts and the assembly line of the cost model (cubesat.sysml, section 3, WP30) over the fleet size, without the launch. */
        in c : Cubesat;
        return : Real = FleetBuildCost(c) / c.fleetSize;
    }

    part def BatteryLife {
        doc /* Illustrative cycle-life rule for the battery: a reference cycle life of 10,000 cycles at the environment's maximum depth of discharge (0.3), inversely proportional to the depth of discharge, one cycle per orbit. */
        attribute referenceCycles : Real = 10000.0;
        attribute hoursPerYear : Real = 8766.0;
    }
    part batteryLife : BatteryLife;

    calc def EffectiveLife {
        doc /* Illustrative roll-up for the sponsor's long life: the years until the battery's cycle life is spent, from its eclipse depth of discharge (the traded metric, the calc DepthOfDischarge) by the cycle-life rule of BatteryLife, one cycle per orbit. */
        in c : Cubesat;
        in slewEnergy : EnergyValue;
        attribute dod : Real = DepthOfDischarge(c, slewEnergy);
        attribute cycles : Real = batteryLife.referenceCycles * (environment.maxDepthOfDischarge / dod);
        return : Real = cycles * (OrbitPeriod() / 1.0 [h]) / batteryLife.hoursPerYear;
    }

    verification def EvidenceCase {
        doc /* A verification case that names its evidence: the ledger entry whose output carries the verdicts (examples/adcs/experiments/ledger/ledger.jsonl), the entry of the environment's record (paper/container/RECORD.md), the test that reads the evidence, and the environment that produced it (an hts-paper image id, or "host" when the entry was run on the host and its platform field names the machine). */
        subject c : Cubesat;
        attribute ledgerEntry : String;
        attribute recordEntry : String;
        attribute testNode : String;
        attribute environment : String;
    }

    verification configurationEvidence : EvidenceCase {
        doc /* What the configuration alone decides (as ConfigurationVerification): the launch budget, the unit cost and the fleet cost, the pointing error and the power requirement, each as its concern holds it. */
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
        doc /* What needs the measured slew (as SlewVerification): settling, control effort, momentum, power margin, energy balance, peak slew power, battery peak power and depth of discharge, each as its concern holds it. */
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

    part def CoverageAssumptions {
        doc /* The two constants of the coverage probability. */
        attribute singleSatelliteCoverage : Real = 0.2;
        attribute errorScale : PlaneAngleValue = budgets.pointingErrorLimit;
    }
    part coverageAssumptions : CoverageAssumptions;

    calc def CoverageProbability {
        doc /* MoE: how well the fleet does its job, the operator's measure of the fleet and the performance objective of the decision-maker's ternary (WP56). */
        in c : Cubesat;
        attribute p : Real = coverageAssumptions.singleSatelliteCoverage
            * OpenSysMLMathFunctions::exp(-(PointingError(c) / coverageAssumptions.errorScale));
        return : Real = 1.0 - (1.0 - p) ** c.fleetSize;
    }
}


package CubesatViews {
    private import StandardViewDefinitions::*;
    private import CubesatTradeSpaceV2::*;

    view assembly : InterconnectionView {
        doc /* The configuration space, one side of "a space of configs on one side (how its constructed) and a space of metrics on the other (how its evaluated)" (WP22): the parts of the baseline configuration, the wheel and the tracker that a configuration swaps, and the panels and battery whose span and capacity it tunes. */
        expose CubesatTradeSpaceV2::Cubesat;
    }
    view alternatives : GeneralView {
        doc /* The swaps and tunes of the configuration space: the two categorical design variables (the swaps `wheelClass` and `grade`, whose enumerations WheelClass and TrackerGrade name the concrete wheel and tracker each literal selects), and the ranges and gain boxes of the four continuous ones. */
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
        doc /* The three named configurations of the configuration space: the baseline and the two contrasts at its corners (agile, compact), each a Cubesat with its wheel and tracker swapped and its span, capacity and gains tuned. */
        expose CubesatTradeSpaceV2::cubesatBaseline;
        expose CubesatTradeSpaceV2::cubesatBaseline::*;
        expose CubesatTradeSpaceV2::cubesatAgile;
        expose CubesatTradeSpaceV2::cubesatAgile::*;
        expose CubesatTradeSpaceV2::cubesatCompact;
        expose CubesatTradeSpaceV2::cubesatCompact::*;
    }

    view metrics : GeneralView {
        doc /* The metric space, "how its evaluated" (WP22): the calcs that take a configuration to its metrics, each traded metric's element marked MoE or MoP in its doc ("MoE on mass, no new column", WP23), and the experiment that returns them. */
        filter @SysML::CalculationDefinition;
        expose CubesatTradeSpaceV2::*;
    }
    view requirements : GeneralView {
        doc /* The requirements the metrics are read against, "a bunch more metrics explicitly included but tied to our actual requirements" (WP22): one requirement on each traded metric's own quantity at the supervisor's thresholds, and the baseline's requirements with their satisfy statements (the pointing-error one not satisfied). */
        filter @SysML::RequirementDefinition or @SysML::RequirementUsage;
        expose CubesatTradeSpaceV2::*;
    }
    view metricCarriers : GeneralView {
        doc /* Where the thirteen traded metrics live, each marked MoE or MoP in the doc of its element: the configuration's own accounting (total mass, with the launch cost its MoE), the measured slew (settling time, control effort), the cost model (the unit cost and the fleet cost, with the prices and the pricing curves they are computed from), and the thresholds the requirements read them against. */
        expose CubesatTradeSpaceV2::Cubesat::totalMass;
        expose CubesatTradeSpaceV2::Cubesat::launchCost;
        expose CubesatTradeSpaceV2::Cubesat::fleetSize;
        expose CubesatTradeSpaceV2::UnitCost;
        expose CubesatTradeSpaceV2::FleetCost;
        expose CubesatTradeSpaceV2::prices;
        expose CubesatTradeSpaceV2::pricing;
        expose CubesatTradeSpaceV2::SlewMeasurement;
        expose CubesatTradeSpaceV2::SlewMeasurement::*;
        expose CubesatTradeSpaceV2::Budgets;
        expose CubesatTradeSpaceV2::Budgets::*;
    }

    view stakeholders : GeneralView {
        doc /* "who cares" (WP27, the supervisor: "to trace all the back to "who cares" via this tool"): the sponsor, the manufacturer and the operator, the concerns each holds, the engineers' requirements each concern is decomposed into, the verification cases that verify them with the pointers to their evidence, and the roll-ups. */
        expose CubesatStakeholders::sponsor;
        expose CubesatStakeholders::manufacturer;
        expose CubesatStakeholders::operator;
        expose CubesatStakeholders::lowCost;
        expose CubesatStakeholders::lowCost::*;
        expose CubesatStakeholders::lowUnitCost;
        expose CubesatStakeholders::lowUnitCost::*;
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
