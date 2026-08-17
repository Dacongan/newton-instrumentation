// =============================================================
//  config.h — compile-time configuration
//  newton-instrumentation · Bresser 130/650 · ESP32 DevKit V1
// =============================================================
//  Everything here is a constant of the *instrument*, not a
//  credential. Credentials live in secrets.h, which is ignored.
//
//  *** PIN ASSIGNMENTS ARE NOT FIXED YET. ***
//  They are marked TODO below and must be set against the real
//  expansion board when the hardware arrives. Do not trust them
//  until each one has been verified with a meter.
// =============================================================

#pragma once

// -------------------------------------------------------------
//  Pinout  — TODO: assign against the 30-pin expansion board
// -------------------------------------------------------------
//  Avoid GPIO 6-11 (SPI flash), GPIO 0/2/12/15 (strapping pins)
//  and remember GPIO 34-39 are input-only: no MOSFET gates there.
// -------------------------------------------------------------
#define PIN_ONEWIRE          -1   // TODO  DS18B20 bus (4 probes)
#define PIN_I2C_SDA          21   //       AHT20 + BMP280
#define PIN_I2C_SCL          22   //
#define PIN_HEATER_GATE      -1   // TODO  IRLZ44N, secondary heater
#define PIN_FAN_GATE         -1   // TODO  IRLZ44N, rear fan
#define PIN_FOCUSER_IN1      -1   // TODO  ULN2003 → 28BYJ-48
#define PIN_FOCUSER_IN2      -1   // TODO
#define PIN_FOCUSER_IN3      -1   // TODO
#define PIN_FOCUSER_IN4      -1   // TODO

// -------------------------------------------------------------
//  Thermal control
// -------------------------------------------------------------
//  The setpoint is NOT a temperature. It is an offset above the
//  dew point, because the dew point moves during the night and a
//  fixed temperature stops tracking it after an hour.
//
//  And the offset stays small on purpose: too much heat drives
//  convection inside the tube and destroys planetary detail
//  faster than the dew it was meant to prevent.
// -------------------------------------------------------------
#define HEATER_DEWPOINT_OFFSET_C   2.0f   // target = dew point + this
#define HEATER_HYSTERESIS_C        0.3f
#define HEATER_MAX_DUTY            255    // 1.50 W at 5 V, 16.7 ohm
#define HEATER_FAILSAFE_DUTY       0      // on sensor loss, heater off

#define SENSOR_POLL_MS             2000
#define DS18B20_COUNT              4      // primary edge, secondary,
                                          // tube air, spare

// -------------------------------------------------------------
//  Focuser  — 28BYJ-48 through an O-ring reduction
// -------------------------------------------------------------
//  Pinion pi x 8.50 = 26.7 mm per turn, reduced 33.3:16.0.
//  4096 half-steps x 2.08 = 8525 steps per pinion turn.
//    -> 3.13 um/step.  CFZ at f/5 is 27.5 um = 9 steps.
//
//  Precision is twelve times what is needed; speed is what is
//  short (50 mm of travel takes 32 s). Do not raise the ratio.
// -------------------------------------------------------------
#define FOCUSER_HALF_STEPS_PER_REV 4096
#define FOCUSER_REDUCTION          2.08f
#define FOCUSER_UM_PER_STEP        3.13f
#define FOCUSER_MAX_STEP_HZ        900     // 28BYJ-48 stalls above this
#define FOCUSER_IDLE_RELEASE_MS    500     // de-energise when stopped:
                                           // no holding current, no heat

// -------------------------------------------------------------
//  Network
// -------------------------------------------------------------
//  Try the home network, and if it is not there in 10 s raise our
//  own AP. Under a dark sky there is no router, so the AP is the
//  normal case. Serial stays available either way as a fallback
//  and for debugging.
// -------------------------------------------------------------
#define WIFI_STA_TIMEOUT_MS   10000
#define AP_IP_ADDRESS         "192.168.4.1"
#define HTTP_PORT             80
#define SERIAL_BAUD           115200

// -------------------------------------------------------------
//  Fail-safe
// -------------------------------------------------------------
//  The control loop runs HERE, inside the ESP32. The laptop is a
//  window onto it, never the thing that decides. If WiFi drops
//  mid-session the heater keeps holding the last setpoint.
// -------------------------------------------------------------
#define CONTROL_LOOP_LOCAL    1
