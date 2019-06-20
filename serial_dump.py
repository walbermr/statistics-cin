import serial
import sys

ser = serial.Serial('/dev/ttyACM0', 115200)

robot_id = int(sys.argv[1])
data_frame = []
while True:
    line = ser.readline()
    if '!' in line:
        break
    else:
        print(line)
        data_frame.append('[' + line[:-1] + ']')

with open('dump/robot-%d.dump' %(robot_id), 'w') as f:
    f.write(str(data_frame))
