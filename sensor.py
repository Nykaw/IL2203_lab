__author__ = 'lundh'
import serial   #importing libraries including methods using the serial port


class Wasa():

    def init(self):                                                     #init method that initialize the communication on the serial port
        self.ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=0.01)  #adress of serial port given,baudrate fixed to 115200, duration of the communication fixed (timeout of 1ms = 1 byte read or written)
        t = self.ser.write(b'at')                                       #it is asked to the Wasa board to pay attention to the next commands
        #for x in range(5):
        #    t = self.ser.write(b'\n')
        #self.ser.flushInput()

    def get_acc(self,):                 #method that returns the three different re-scaled values of the accelerometer
        t = self.ser.write(b's200?')    #asking for X acceleration value to the board
        #x = ser.readline()             # read up to ten bytes (fixed by timeout)

        t = self.ser.write(b's201?')    #asking for Y acceleration value to the board
        #y = ser.readline()             # read up to ten bytes (fixed by timeout)

        t = self.ser.write(b's202?')    #asking for Z acceleration value to the board
        r = self.ser.read(1024)         #read up to 1024 values
        #z = z.replace(b"\r\n", b"")
        x,y,z = r.split(b'\r\n\r\n')    #split the long result in order to separate the values so they correspond to one axis each
        x = x.replace(b"\r\n", b'')     #editing the x result so that we only keep the integer part of it (no more text)
        y = y.replace(b"\r\n", b'')     #editing the y result so that we only keep the integer part of it (no more text)
        z = z.replace(b"\r\n", b'')     #editing the z result so that we only keep the integer part of it (no more text)
        #print(z)

        return int(x)-2047, int(y)-2047, int(z)-2047    #Setting the zero (re-scaling) : the data is coded on 12 bits so the result vary from 0 to 4095
                                                        #because +g = 3000 and -g = -1000
                                                        #now we have a value nearly centered on 0 and going from -2047 to +2048
                                                        #interpreting the values is now quite more convenient (+g = 1000 and -g = -1000)
                                                        
    def get_light(self):                    #method that returns the value of the light sensor
        self.ser.write(b's203?')            #asking for light sensor's value to the board
        r = self.ser.read(1024)             #read up to 1024 values
        value = r.replace(b"\r\n", b'')     #editing the result so that we only keep the integer part of it (no more text)
        return int(r)                       #gives back the obtained value

    def close(self):                        #method supposed to stop the communication // doesn't work
        print("Closing")
        t = self.ser.write(b'\n')
        self.ser.close()


def calibrate_light(w):             #returns a reference value after reading from the sensor for a while
    sum = 0                         #this eliminates the factor of the ambient light !
    for x in range(100):
        sum += w.get_light()

    return sum/100                  #just returns the mean of the 100 values measured 


def determine_phone():              #this is the main method, testing the position of the phone and printing the corresponding state of the speaker
    w = Wasa()                      
    w.init()                        #initializing thecommunication with the board
    light_threshold = 1.5           #setting the light threshold
    acc_threshold = 0.4             #setting the acceleration threshold
    light_avg = calibrate_light(w)  #computing the ambiant light level
    counter = 0                     #reseting the variable named counter
    # state 0 is ON , and 1 is OFF
    state = 0                       #setting initial/default state as SPEAKER ON
    try:
        for i in range(10000):      #loop that's gonna print if the SPEAKER is ON or OFF 10000 times, evolving with the sensor's values
            x,y,z = w.get_acc()     #we get the values of the sensors and store it in viariables
            light = w.get_light()  
            #print("X,Y,Z: {0}, {1}, {2}".format(str(x),str(y),str(z))) #displaying the values of acceleration sensors
            #print("Light:{0}, Z:{1}".format(light, z))                 #displaying only light and z axis-acceleration (most useful)
            #print("Z:{0}".format(z))                                   #displaying only z axis-acceleration

            if(abs(z) < 1000*acc_threshold and light > light_avg*light_threshold): #testing if the phone is near the user's head
                if state == 0:              #this loop acts as a filter : the state mustn't be transient, we must obtain 20 times the same result to consider a real change in the state
                    counter += 1            #by incrementing the counter for each same successive step
                    if counter > 10:        #it may reach 10 and so the state can be changed
                        state = 1
                        counter = 0         #then we reset the counter
                else : 
                    counter = 0             #if two consecutives results are differents we reset the counter 
                #print("Speaker OFF")
            else:
                if state == 1:              #this loop acts as a filter : the state mustn't be transient, we must obtain 20 times the same result to consider a real change in the state
                    counter += 1            #by incrementing the counter for each same successive step
                    if counter > 10:        #it may reach 10 and so the state can be changed
                        state = 0
                        counter = 0         #then we reset the counter
                else : 
                    counter = 0             #if two consecutives results are differents we reset the counter
            if state == 0:
                print("Speaker ON")         #we finally inform the user of the current state of the SPEAKER
            else:
                print("Speaker OFF")        # ON(because the phone is on the table) or OFF(near the user's head)
            

    except KeyboardInterrupt:
        pass
        #w.close()
    finally:
        w.close()


if __name__ == "__main__":
    determine_phone()
    # w = Wasa()
    # w.init()
    # print(w.get_light())
    #
    # try:
    #     for i in range(10000):
    #         x,y,z = w.get_acc()
    #         light = w.get_light()
    #         #print("X,Y,Z: {0}, {1}, {2}".format(str(x),str(y),str(z)))
    #         print("Light:{0}, Z:{1}".format(light, z))
    # except KeyboardInterrupt:
    #     pass
    #     #w.close()
    # finally:
    #     w.close()
    # #w.close()
