__author__ = 'lundh'
import serial


class Wasa():

    def init(self,):
        self.ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=0.1)
        t = self.ser.write(b'at')


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

        return x,y,z

    def get_light(self):
        pass

    def close(self):
        t = self.ser.write(b'\n')
        self.ser.close()


if __name__ == "__main__":
    w = Wasa()
    print(w.get_light())

    for i in range(1000):
        x,y,z = w.get_acc()
        print("X,Y,Z: {0}, {1}, {2}".format(str(x),str(y),str(z)))
    w.close()