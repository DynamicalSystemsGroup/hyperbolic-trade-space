// Extended ADCS design space for the posynomial-invariant-form case study.
// Documentation only: this file is not parsed or executed by any code in this repository.
// Hardware values are illustrative, not calibrated to real products.
// Derived from the baseline satellite model of ADCS-lifecycle-demo (sysml/satellite.sysml).

package ExtendedDesignSpace {

    // --- Categorical choice 1: reaction-wheel class (maxTorque N.m, maxMomentum N.m.s, mass kg)
    part def WheelClass {
        attribute maxTorque;
        attribute maxMomentum;
        attribute mass;
    }
    part small  : WheelClass { attribute :>> maxTorque = 0.05; attribute :>> maxMomentum = 2; attribute :>> mass = 1.5; }
    part medium : WheelClass { attribute :>> maxTorque = 0.1;  attribute :>> maxMomentum = 4; attribute :>> mass = 2.5; }
    part large  : WheelClass { attribute :>> maxTorque = 0.2;  attribute :>> maxMomentum = 8; attribute :>> mass = 4.0; }

    // --- Categorical choice 2: star-tracker grade (accuracy arcsec 1-sigma, mass kg)
    part def StarTrackerGrade {
        attribute accuracyArcsec;
        attribute mass;
    }
    part coarse : StarTrackerGrade { attribute :>> accuracyArcsec = 15;  attribute :>> mass = 1.0; }
    part medium_st : StarTrackerGrade { attribute :>> accuracyArcsec = 5;   attribute :>> mass = 2.0; }
    part fine   : StarTrackerGrade { attribute :>> accuracyArcsec = 1.5; attribute :>> mass = 3.5; }

    // --- Continuous design variables
    part def ControlGains {
        attribute Kp;   // N.m/rad, log-uniform in [0.5, 16]
        attribute Kd;   // N.m.s/rad, log-uniform in [5, 60]
    }
    part def MassPerturbation {
        attribute panelMass;    // kg, baseline 30, ~10 % lognormal
        attribute antennaMass;  // kg, baseline 18, ~10 % lognormal
    }

    // --- Evaluation attributes (all to be minimised)
    attribute def settling_time_s;      // s, 1 % settling of a 10 deg X slew; censored at the horizon
    attribute def pointing_error_deg;   // deg, RSS(steady disturbance error, star-tracker floor)
    attribute def adcs_mass_kg;         // kg, 3 wheels + star tracker + IMU
    attribute def control_effort;       // N.m.s, integral of the control torque norm over the slew

    // Feasibility flags: settled, momentum_ok (peak wheel momentum <= maxMomentum), torque_saturated_frac.
}
