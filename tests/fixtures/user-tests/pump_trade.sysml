/*
 * pump_trade.sysml -- a small centrifugal-pump trade, written for the package-user tests.
 *
 * A pump is chosen by three numbers (impeller diameter, shaft speed, blade width ratio). Four
 * calculations turn a choice into the four numbers an engineer compares: the flow it delivers,
 * the head it lifts, the shaft power it draws and the mass of the unit. Every constant is
 * illustrative (affinity-law scaling with round coefficients), chosen for plausibility, not
 * calibrated to a catalogue.
 */
package PumpTrade {
    private import ScalarValues::*;
    private import OpenSysMLMathFunctions::exp;

    // Design ranges: impeller diameter 0.08 to 0.35 m, speed 900 to 3600 rpm, blade width ratio
    // 0.05 to 0.30 (blade width over diameter).

    // Flow in litres per second: affinity law, flow ~ speed * diameter^3, scaled by blade width.
    calc def Flow {
        in diameter : Real;
        in speed : Real;
        in width : Real;
        return : Real = 1.2 * (speed / 60.0) * diameter ** 3.0 * (width / 0.1) * 1000.0;
    }
    // Head in metres: head ~ (tip speed)^2 / g, less a loss that grows with the blade width ratio.
    calc def Head {
        in diameter : Real;
        in speed : Real;
        in width : Real;
        return : Real = 0.55 * ((3.14159265 * speed * diameter / 60.0) ** 2.0) / 9.81
            / (1.0 + 4.0 * width);
    }
    // Efficiency: best near a flow-to-head balance (specific speed), falling away on either side.
    calc def Efficiency {
        in diameter : Real;
        in speed : Real;
        in width : Real;
        return : Real = 0.82 * exp(-0.35 * (width / 0.15 - 1.0) ** 2.0);
    }
    // Shaft power in kilowatts: hydraulic power over efficiency.
    calc def ShaftPower {
        in diameter : Real;
        in speed : Real;
        in width : Real;
        return : Real = 9.81 * (Flow(diameter, speed, width) / 1000.0)
            * Head(diameter, speed, width) / Efficiency(diameter, speed, width);
    }
    // Mass in kilograms: casing and impeller scale with diameter squared and with blade width.
    calc def Mass {
        in diameter : Real;
        in speed : Real;
        in width : Real;
        return : Real = 6.0 + 180.0 * diameter ** 2.0 * (1.0 + 2.0 * width);
    }
}
