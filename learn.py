import serial
import re
import threading
import sys

from Config import config

import face
from Config import keyInput

MODE = input("test, train > ") #other使わない
is_new = input("renew or make new file > ")

def serial_loop():
    with serial.Serial('COM5', 9600, timeout=0.1) as ser:

        setPortCount = 0

        f = face.Face(MODE, config.sensor_nums)
        f.make_dir_train_or_test(is_new) #フォルダを作成する
        try:
            while True:
                s = ser.readline()
                m = None

                if setPortCount < 100:
                    print("waiting port now" + str(setPortCount))
                    ser.write(bytes(str(2), 'UTF-8'))

                try:
                    de = s.decode('utf-8')
                    m = re.match("\-*[\w]+", str(de))
                except Exception as e:
                    pass
                if(m != None):

                    setPortCount = setPortCount + 1

                    config.is_calibration, make_serial_flush = f.fetch_numbers(m.group())
                    if make_serial_flush:
                        ser.flushInput()
                else:
                    pass
        except:
             print("Unexpected error:", sys.exc_info()[0])
             raise
        ser.close()

ser_loop = threading.Thread(target=serial_loop,name="ser_loop",args=())
ser_loop.setDaemon(True)
ser_loop.start()

def main():
    keyInput.key_input()

if __name__ == "__main__":
    main()
