from time import sleep

#set mode = 0 to disable reading serial
mode = 1
weightmode = 1

if mode == 1:
    import serial
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
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
            while ser.in_waiting > 0:
                line = ser.readline().decode().rstrip()
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
        return 0.5
    line = ''
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            if len(line) < 7:
                continue
            print("line: ", line, ";")       
            main = line.split("[", 1)       
            print("newline:", line) 
            lhs = main[len(main) - 1].split(" ", 2)
            print("lhs:", lhs)
            return float(lhs[0])
        else:
            continue


print(get_weight())
