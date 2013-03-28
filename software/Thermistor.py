
# Import PyBBIO library:
import bbio as io
import numpy as np
import time 

# Import the temp chart. 
from temp_chart import *
from threading import Lock

''' Represents a thermistor '''
class Thermistor: 

    mutex = Lock()

    ''' Init '''
    def __init__(self, pin, name, chart_name="B57560G104F"):
        self.pin = pin
        self.name = name
        # Get the chart and transpose it
        self.temp_table = map(list, zip(*temp_chart[chart_name]))    
        self.debug = 0
	
    ''' Return the temperature in degrees celcius '''
    def getTemperature(self):	
        #print "Getting Temp"
        Thermistor.mutex.acquire()                        # Get the mutex
        #print "Mutex acquired"
        try:
            time.sleep(1)
            #print "Delay done"
            adc_val = io.analogRead(self.pin)        # Read the value 		
            time.sleep(1)
            print "Got adc value: "+str(adc_val)
        except:
            print "Unexpected error:", sys.exc_info()[0]          
        finally:
            #print "Releasing mutex"
            Thermistor.mutex.release()                    # Release the mutex
        voltage = io.inVolts(adc_val)                     # Convert to voltage
        res_val = self.voltage_to_resistance(voltage)     # Convert to resistance  
        temperature = self.resistance_to_degrees(res_val) # Convert to degrees
        if self.debug > 1:  
            print self.name+": ADC: %i - voltage: %f"%(adc_val, voltage), 
            print " - thermistor res: %f - Temperature: %f deg."%(res_val, temperature)
        return temperature	
		
    ''' Return the temperature nearest to the resistor value '''
    def resistance_to_degrees(self, resistor_val):
        idx = (np.abs(np.array(self.temp_table[1])-resistor_val)).argmin()
        return self.temp_table[0][idx]

    ''' Convert the voltage to a resistance value '''
    def voltage_to_resistance(self, v_sense):
        if v_sense == 0:
            return 10000000.0
        return  4700.0/((1.8/v_sense)-1.0)

    ''' Set the deuglevel '''
    def setDebugLevel(self, val):
        self.debug = val

