# Import Pin and TouchPad classes from the machine module
# Pin is used for GPIO control, TouchPad is used for capacitive touch sensing
from machine import Pin, PWM, TouchPad

# Import time module to introduce delays
import time

# Create a TouchPad object using GPIO pin 4
# This pin will sense touch based on change in capacitance
my_touch_pin = TouchPad(Pin(14))
servo = PWM(Pin(13),freq=50)

# Create a Pin object for the LED
# GPIO pin 22 is configured as an OUTPUT pin


# Start an infinite loop
# The system continuously checks for touch input
while True:

    # Read the current touch sensor value
    # Lower values generally mean the sensor is being touched
    touch_pin_values = my_touch_pin.read()

    # Check if the touch value is below the threshold
    # This condition indicates that a touch has been detected
    # The threshold (100) is experimentally chosen
    if touch_pin_values < 200:

        # Turn the LED ON when touch is detected
        #my_led.on()
        servo.duty(35)
        time.sleep(0.75)
        servo.duty(110)
        time.sleep(0.75)

        # Print message indicating touch detection
        print("Touch Detected")

    else:
        # Turn the LED OFF when no touch is detected
        #my_led.off()

        # Print message indicating no touch
        print("No Touch")

    # Wait for 0.2 seconds before the next sensor reading
    time.sleep(0.2)