__author__ = 'lundh'
import serial


class Wasa():

    def init(self):
        self.ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=0.01)
        t = self.ser.write(b'at')
        #for x in range(5):
        #    t = self.ser.write(b'\n')
        #self.ser.flushInput()

    def get_acc(self,):
        t = self.ser.write(b's200?')

        #x = ser.readline()        # read up to ten bytes (timeout)

        t = self.ser.write(b's201?')
        #y = ser.readline()        # read up to ten bytes (timeout)

        t = self.ser.write(b's202?')
        r = self.ser.read(1024)        # read up to ten bytes (timeout)
        #z = z.replace(b"\r\n", b"")
        x,y,z = r.split(b'\r\n\r\n')
        x = x.replace(b"\r\n", b'')
        y = y.replace(b"\r\n", b'')
        z = z.replace(b"\r\n", b'')
        #print(z)

        return int(x)-2000, int(y)-2000, int(z)-2000

    def get_light(self):
        self.ser.write(b's203?')
        r = self.ser.read(1024)
        value = r.replace(b"\r\n", b'')
        return int(r)

    def close(self):
        print("Closing")
        t = self.ser.write(b'\n')
        self.ser.close()


def calibrate_light(w):
    #returns a reference value after reading from the sensor for a while
    sum = 0
    for x in range(100):
        sum += w.get_light()

    return sum/100


def determine_phone():
    w = Wasa()
    w.init()
    light_threshold = 1.5
    acc_threshold = 0.4
    light_avg = calibrate_light(w)
    counter = 0
    # state 0 is ON , and 1 is OFF
    state = 0
    try:
        for i in range(10000):
            x,y,z = w.get_acc()
            light = w.get_light()
            #print("X,Y,Z: {0}, {1}, {2}".format(str(x),str(y),str(z)))
            #print("Light:{0}, Z:{1}".format(light, z))
            #print("Z:{0}".format(z))

            if(abs(z) < 1000*acc_threshold and light > light_avg*light_threshold):
                if state == 0:
                    counter += 1
                    if counter > 20:
                        state = 1
                        counter = 0
                #print("Speaker OFF")
            else:
                if state == 1:
                    counter += 1
                    if counter > 20:
                        state = 0
                        counter = 0
            if state == 0:
                print("Speaker ON")
            else:
                print("Speaker OFF")


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