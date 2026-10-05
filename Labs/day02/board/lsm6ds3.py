# lsm6ds3.py - MicroPython driver for the IMU of the XIAOML Kit
#
# Sensor:  LSM6DS3TR-C (3-axis accelerometer, 3-axis gyroscope), I2C address 0x6A
# Board:   XIAOML Kit (XIAO ESP32S3 Sense with the expansion board)
# Runs on: MicroPython v1.29.0 for SEEED_XIAO_ESP32S3
#
# Credits: the register addresses, the bit values, and the scale factors come
# from the Arduino library "Seeed Arduino LSM6DS3" 2.0.7 (files LSM6DS3.h and
# LSM6DS3.cpp, github.com/Seeed-Studio/Seeed_Arduino_LSM6DS3, MIT licence).
# The I2C address comes from the sketch imu_test.ino of "XIAO ESP32S3 Sense"
# by Marcelo Rovai (github.com/Mjrovai/XIAO-ESP32S3-Sense, Apache-2.0).
#
# The driver needs only an I2C object with the methods readfrom_mem,
# readfrom_mem_into, and writeto_mem. It does not import "machine".

import struct

# Register addresses (LSM6DS3.h, lines 212 to 240).
WHO_AM_I = 0x0F
CTRL1_XL = 0x10   # accelerometer: output data rate and range
CTRL2_G = 0x11    # gyroscope: output data rate and range
CTRL3_C = 0x12    # block data update, address increment, reset
STATUS_REG = 0x1E
OUTX_L_G = 0x22   # first of 12 data bytes: gyroscope x, y, z, then accelerometer x, y, z

# Identity values (LSM6DS3.h, lines 194 and 195).
ID_LSM6DS3 = 0x69
ID_LSM6DS3_C = 0x6A   # LSM6DS3-C and LSM6DS3TR-C

# CTRL3_C bits (LSM6DS3.h: SW_RESET, IF_INC, BDU).
SW_RESET = 0x01
IF_INC = 0x04   # the register address goes up by one after each byte
BDU = 0x40      # the sensor holds one sample until both bytes are read

# Output data rate in Hz -> bits 7 to 4 of CTRL1_XL and of CTRL2_G
# (LSM6DS3.h: LSM6DS3_ACC_GYRO_ODR_XL_t and LSM6DS3_ACC_GYRO_ODR_G_t).
_ODR = {13: 0x10, 26: 0x20, 52: 0x30, 104: 0x40,
        208: 0x50, 416: 0x60, 833: 0x70, 1660: 0x80}

# Accelerometer range in g -> bits 3 and 2 of CTRL1_XL
# (LSM6DS3.h: LSM6DS3_ACC_GYRO_FS_XL_t). The order is not monotonic.
_FS_XL = {2: 0x00, 16: 0x04, 4: 0x08, 8: 0x0C}

# Gyroscope range in degrees per second -> bits 3 to 1 of CTRL2_G
# (LSM6DS3.h: LSM6DS3_ACC_GYRO_FS_G_t and LSM6DS3_ACC_GYRO_FS_125_t).
_FS_G = {125: 0x02, 245: 0x00, 500: 0x04, 1000: 0x08, 2000: 0x0C}

# Scale factors (LSM6DS3.cpp, functions calcAccel and calcGyro).
_ACCEL_MG_PER_LSB_AT_2G = 0.061      # milli-g for each count at the 2 g range
_GYRO_MDPS_PER_LSB_AT_125 = 4.375    # milli-degrees per second for each count


class LSM6DS3:
    """Read the accelerometer and the gyroscope of the XIAOML Kit.

    The default values are the default values of the Arduino library:
    16 g, 2000 degrees per second, 416 Hz. The Day 3 sketch uses that
    library. The training data and the inference then use the same
    sensor configuration.
    """

    def __init__(self, i2c, address=0x6A, accel_range=16, gyro_range=2000,
                 odr=416):
        if accel_range not in _FS_XL:
            raise ValueError("accel_range must be 2, 4, 8, or 16")
        if gyro_range not in _FS_G:
            raise ValueError("gyro_range must be 125, 245, 500, 1000, or 2000")
        if odr not in _ODR:
            raise ValueError("odr must be one of %s" % sorted(_ODR))

        self.i2c = i2c
        self.address = address
        self.accel_range = accel_range
        self.gyro_range = gyro_range
        self.odr = odr
        self._buf = bytearray(12)

        self.chip_id = self._read_u8(WHO_AM_I)
        if self.chip_id not in (ID_LSM6DS3, ID_LSM6DS3_C):
            raise OSError("no LSM6DS3 at address 0x%02X (WHO_AM_I = 0x%02X)"
                          % (address, self.chip_id))

        # g for each count, and degrees per second for each count.
        self.accel_scale = _ACCEL_MG_PER_LSB_AT_2G * (accel_range >> 1) / 1000
        divisor = 2 if gyro_range == 245 else gyro_range // 125
        self.gyro_scale = _GYRO_MDPS_PER_LSB_AT_125 * divisor / 1000

        self._write_u8(CTRL3_C, BDU | IF_INC)
        self._write_u8(CTRL1_XL, _ODR[odr] | _FS_XL[accel_range])
        self._write_u8(CTRL2_G, _ODR[odr] | _FS_G[gyro_range])

    def _read_u8(self, register):
        return self.i2c.readfrom_mem(self.address, register, 1)[0]

    def _write_u8(self, register, value):
        self.i2c.writeto_mem(self.address, register, bytes([value]))

    def reset(self):
        """Start the sensor again with the reset values of all registers."""
        self._write_u8(CTRL3_C, SW_RESET)

    def data_ready(self):
        """Return True when a new accelerometer sample is available."""
        return bool(self._read_u8(STATUS_REG) & 0x01)

    def read_raw(self):
        """Return (gx, gy, gz, ax, ay, az) as signed 16-bit counts."""
        self.i2c.readfrom_mem_into(self.address, OUTX_L_G, self._buf)
        return struct.unpack("<hhhhhh", self._buf)

    def read(self):
        """Return (ax, ay, az, gx, gy, gz): g and degrees per second."""
        gx, gy, gz, ax, ay, az = self.read_raw()
        a = self.accel_scale
        g = self.gyro_scale
        return (ax * a, ay * a, az * a, gx * g, gy * g, gz * g)

    def accel(self):
        """Return (ax, ay, az) in g."""
        return self.read()[0:3]

    def gyro(self):
        """Return (gx, gy, gz) in degrees per second."""
        return self.read()[3:6]

    def power_down(self):
        """Stop both sensors. Make a new object to start them again."""
        self._write_u8(CTRL1_XL, 0x00)
        self._write_u8(CTRL2_G, 0x00)
