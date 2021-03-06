import time

import board
import busio
from anyleaf import PhSensor, CalPt, CalSlot, OnBoard, OffBoard
from anyleaf import OrpSensor, CalPtOrp


def main():
    i2c = busio.I2C(board.SCL, board.SDA)
    delay = 1  # Time between measurements, in seconds

    ph_sensor = PhSensor(i2c, delay)

    # If you connect multiple AnyLeaf modules on the same I²C bus, set one's
    # jumper to the `0x49` position, and specify this as below:
    # orp_sensor = OrpSensor(i2c, delay, address=0x49)

    # 2 or 3 pt calibration both give acceptable results.
    # Calibrate with known values. (voltage, pH, temp in °C).
    # You can find voltage and temperature with `ph_sensor.read_voltage()` and
    # `ph_sensor.read_temp()` respectively. Or skip this to use default calibration.
    # For 3 pt calibration, pass a third argument to `calibrate_all`.
    ph_sensor.calibrate_all(
        CalPt(0., 7., 25.), CalPt(0.18, 4., 25.)
    )

    # Or, call these with the sensor in the appropriate buffer solution.
    # This will automatically use voltage and temperature.
    # Voltage and Temp are returned, but calibration occurs
    # without using the return values.
    # V, T = ph_sensor.calibrate(CalSlot.ONE, 7., OnBoard(())
    # ph_sensor.calibrate(CalSlot.TWO, 4., OffBoard(23.)

    # ORP setup is simpler: There's only 1 calibration point, and no
    # temperature compensation:
    # orp_sensor.calibrate_all(CalPtOrp(0.4, 400.0))

    # Ideally, store the calibration parameters somewhere, so they persist
    # between program runs.



    while True:
        pH = ph_sensor.read(OnBoard())
        # ORP = orp_sensor.read()
        # To use an offboard temperature measurement `ph_sensor.read(OffBoard(30.))`
        print(f"pH: {pH}")
        # print(f"ORP: {ORP}")

        time.sleep(delay)


if __name__ == "__main__":
    main()