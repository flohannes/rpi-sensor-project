import RPi.GPIO as GPIO
import time
import socket
from datetime import datetime
#from mqtt_client import ServerCom
# change these as desired - they're the pins connected from the
# SPI port on the ADC to the Cobbler
SPICLK = 11
SPIMISO = 9
SPIMOSI = 10
SPICS = 8

# photoresistor connected to adc #0
photo_ch = 0
try:
    f = open('/home/pi/sensorlogs/light.csv', 'a+')
    if os.stat('/home/pi/sensorlogs/light.csv').st_size == 0:
        f.write('Date,Time,light,hostname\r\n')
except:
    pass

class WaterLevel:
    def __init__(self):
        GPIO.setwarnings(False)
        GPIO.cleanup()  # clean up at the end of your script
        GPIO.setmode(GPIO.BCM)  # to specify whilch pin numbering system
        # set up the SPI interface pins
        GPIO.setup(SPIMOSI, GPIO.OUT)
        GPIO.setup(SPIMISO, GPIO.IN)
        GPIO.setup(SPICLK, GPIO.OUT)
        GPIO.setup(SPICS, GPIO.OUT)
        #self.mqtt_client = ServerCom(server_host='ec2-3-122-180-139.eu-central-1.compute.amazonaws.com')
        self.collector()

    # read SPI data from MCP3008(or MCP3204) chip,8 possible adc's (0 thru 7)
    def readadc(self, adcnum, clockpin, mosipin, misopin, cspin):
        if (adcnum > 7) or (adcnum < 0):
            return -1
        GPIO.output(cspin, True)

        GPIO.output(clockpin, False)  # start clock low
        GPIO.output(cspin, False)  # bring CS low

        commandout = adcnum
        commandout |= 0x18  # start bit + single-ended bit
        commandout <<= 3  # we only need to send 5 bits here
        for i in range(5):
            if commandout & 0x80:
                GPIO.output(mosipin, True)
            else:
                GPIO.output(mosipin, False)
            commandout <<= 1
            GPIO.output(clockpin, True)
            GPIO.output(clockpin, False)

        adcout = 0
        # read in one empty bit, one null bit and 10 ADC bits
        for i in range(12):
            GPIO.output(clockpin, True)
            GPIO.output(clockpin, False)
            adcout <<= 1
            if (GPIO.input(misopin)):
                adcout |= 0x1

        GPIO.output(cspin, True)

        adcout >>= 1  # first bit is 'null' so drop it
        return adcout

    def collector(self):
        print('start collecting data')
        while True:
            adc_value = self.readadc(photo_ch, SPICLK, SPIMOSI, SPIMISO, SPICS)
            resultString = "light ",adc_value
            f.write('{0},{1},{2:0.1f},{3}%\r\n'.format(time.strftime('%m/%d/%y'), datetime.utcnow().strftime('%H:%M:%S.%f')[:-3], adc_value, socket.gethostname()))
            print(resultString)
            time.sleep(0.5)


if __name__ == '__main__':
    waterlevel = WaterLevel()
