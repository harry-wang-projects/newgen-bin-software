import serial
from time import sleep

ser = serial.Serial('/dev/cu.usbserial-1420', 9600, timeout=1)
ser.flush()

ser.write(b'R')

def unlock():
    ser.write(b'U')
    ser.flush()
    sleep(0.1)
    triggered = False
    while True:
        if ser.in_waiting > 0:
            while ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').rstrip()

            main = line.split("[", 3)
            print(main)
 
            lhs = (main[len(main) - 1].split(" ", 3))
            rhs = (main[len(main) - 1].split(" ", 3))
            print('point2')
            print(lhs)
            print('point3')
            if int(lhs[1]) == 0:
                print('true!!')
                return
                 
        

def lock_state():
    line = ''
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            break

        main = line.split("[", 2)

        lhs = main[0].split(" ", 3)
        return int(lhs[1])

def get_weight():
    line = ''
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            break
        
        main = line.split("[", 1)       
 
        lhs = main.split(" ", 1)
        return float(lhs)


print(get_weight)

print(lock_state)

unlock()
