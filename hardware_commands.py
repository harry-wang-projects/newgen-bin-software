import serial

ser = serial.Serial('/dev/cu.usbserial-1410', 9600, timeout=1)
ser.flush()

def lock():
    ser.write('L')
    ser.flush()

def unlock():
    ser.write('U')
    ser.flush()

def lock_state():
    line = ''
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            break

        main = line.split("[", 1)

        lhs = main.split(" ", 2)
        return int(lhs)

def get_weight():
    line = ''
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            break
        
        main = line.split("[", 1)       
 
        lhs = main.split(" ", 1)
        return float(lhs)
