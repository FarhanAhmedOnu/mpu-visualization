from vpython import *
import serial
import time

# Change this to match what you found in Step 2
# It is likely '/dev/ttyUSB0' or '/dev/ttyACM0'
PORT = '/dev/ttyACM0' 

try:
    ser = serial.Serial(PORT, 115200, timeout=1)
    print(f"Connected to {PORT}")
except:
    print(f"Could not open {PORT}. Is the Arduino plugged in or the Serial Monitor open?")
    exit()

# Create the 3D Scene
scene.title = "MPU6050 Real-Time Visualization (Linux Mint)"
scene.width = 1000
scene.height = 700

# Create a "Betaflight-style" board
# A thin box with a 'front' indicator
board = box(length=4, height=0.1, width=4, color=color.cyan)
front_arrow = arrow(axis=vector(1,0,0), color=color.red, shaftwidth=0.1, length=2)

def update_view():
    while True:
        rate(100) # Keep the loop smooth
        if ser.in_waiting > 0:
            try:
                line = ser.readline().decode('utf-8').strip()
                data = line.split(',')
                
                if len(data) == 3:
                    # Betaflight-style angles
                    roll = float(data[0])
                    pitch = float(data[1])
                    yaw = float(data[2])

                    # Convert to Radians
                    roll_rad = radians(roll)
                    pitch_rad = radians(-pitch)
                    yaw_rad = radians(yaw)

                    # Reset and re-apply rotations to prevent "spinning" glitches
                    board.axis = vector(1, 0, 0)
                    board.up = vector(0, 1, 0)
                    
                    board.rotate(angle=yaw_rad, axis=vector(0, 1, 0))
                    board.rotate(angle=pitch_rad, axis=vector(0, 0, 1))
                    board.rotate(angle=roll_rad, axis=vector(1, 0, 0))
                    
                    front_arrow.axis = board.axis * 2
                    front_arrow.up = board.up
            except:
                pass

update_view()