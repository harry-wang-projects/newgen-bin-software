from time import sleep
import serial

#set mode = 0 to disable reading serial
mode = 1
weightmode = 0

ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=5)
ser.flush()

ser.write(b'R')


def unlock():
    if mode == 0:
        sleep(1)
        return;
    ser.write(b'U')
    ser.flush()
    sleep(0.5)
    triggered = False
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            for i in range(len(line)):
                if line[i] == 'C':
                    return

def lock_state():
    if mode == 0:
        return 1

    line = ''
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            break
        main = line.split("[", 2)
        lhs = main[0].split(" ", 3)
        return int(lhs[1])

def get_weight():
    if mode == 0 or weightmode == 0:
        return 5
    line = ''
    ser.write(b'W')
    ser.flush()
    while True:
        if ser.in_waiting > 0:
            print("hi")
            line = ser.readline().decode('utf-8').rstrip()
            if len(line) < 2:
                continue
            print("line: ", line, ";")       
            main = line.split("[", 1)       
            print("newline:", line) 
            lhs = main[len(main) - 1].split("]", 2)
            print("lhs:", lhs)
            return int(lhs[0])
        else:
            continue

def get_button():
    if mode == 0:
        return 0
    ser.write(b'B')
    ser.flush()
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip() 
            main = line.split("[", 1)
            lhs = main[len(main) - 1].split("]", 1)
            return int(lhs[0])

print(get_weight())

