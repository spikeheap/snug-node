import smbus
import time

# FIXME sensor classes should return a JSON object containing additional information, such as the sensor ID, timestamp.
class TempSensor:
  """ Temperature sensor reporting class for the TI TMP100NA Temperature Sensor on address 0x48 (e.g as included in http://shop.ciseco.co.uk/i-o-pod-rtc-eeprom-temp/)"""
  
  ADDRESS = 0x48
  
  def read(self):
    bus = smbus.SMBus(0)
    data = bus.read_i2c_block_data(self.ADDRESS, 0)
    msb = data[0]
    lsb = data[1]
    
    # Return the value in degrees Celsius
    return (((msb << 8) | lsb) >> 4) * 0.0625
