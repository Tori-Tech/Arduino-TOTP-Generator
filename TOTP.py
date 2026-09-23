import serial
import time
import pyotp
import threading

# secret key used between this and the arduino
SHARED_SECRET = "JBSWY3DPEHPK3PXP" 
totp = pyotp.TOTP(SHARED_SECRET)

# establish connection
arduino = serial.Serial(port='COM6', baudrate=9600, timeout=1)
time.sleep(2) # allow Arduino to stabilize

print("Python TOTP Server is running... Listening for Arduino requests.")

def file_cleanup_loop():
    """Background task to ensure active_totp.txt matches the real-time active OTP."""
    last_written_otp = ""
    while True:
        current_otp = totp.now()
        # update text file when code changes
        if current_otp != last_written_otp:
            with open("active_totp.txt", "w") as f:
                f.write(current_otp)
            last_written_otp = current_otp
        time.sleep(0.5)

# start the text file daemon thing in a background thread
cleanup_thread = threading.Thread(target=file_cleanup_loop, daemon=True)
cleanup_thread.start()
#it basically wipes out the content form the old archive_totp.txt whenever a new code is made

try:
    while True:
        if arduino.in_waiting > 0:
            # read incoming message from Arduino
            incoming_line = arduino.readline().decode('utf-8').strip()
            
            if incoming_line == "REQ_TOTP":
                current_otp = totp.now()
                
                # calculate how many seconds are left for this code globally
                time_remaining = int(totp.interval - (time.time() % totp.interval))
                
                print(f"Request received. Generated TOTP: {current_otp} (Valid for {time_remaining}s)")
                
                # send the OTP to the Arduino
                arduino.write(f"{current_otp}\n".encode('utf-8'))
                
        time.sleep(0.05) # small loop delay to prevent high CPU usage

except KeyboardInterrupt:
    print("\nStopping Python server...")
finally:
    arduino.close()
    print("Serial port closed.")
