Module 1 Overview: DHT11 Sensor Communication

**1. Objective:

    Develop a script to interface with the DHT11 sensor using a Raspberry Pi. The module focuses on reading data from the sensor, processing it, and formatting it appropriately.

**2. Steps to Achieve:

a. Sensor Initialization:

    Pin Configuration: Set up the GPIO pins on the Raspberry Pi for communication with the DHT11 sensor.
    Communication Start: Implement the procedure to initiate communication with the DHT11 sensor, which involves pulling the data line low for at least 18ms to start the data transmission.

b. Data Reading:

    Data Collection: Read the sensor's output by polling the GPIO pin to capture the high and low pulses that encode the data.
    Pulse Measurement: Measure the duration of the high and low pulses to decode the transmitted data.
    Data Parsing: Convert the measured pulse lengths into a meaningful format (e.g., bits representing temperature and humidity values).

c. Data Processing:

    Bit Shifting: Implement logic to shift the decoded bits into a byte array.
    Data Conversion: Convert the byte array into readable temperature and humidity values.
    Error Handling: Include basic error handling for cases where the data transmission might fail or be corrupted.

d. Output:

    Debugging: Print the raw pulse lengths and the decoded byte array to verify correct data interpretation.
    Data Display: Format and display the temperature and humidity values for verification.

e. Testing and Validation:

    Testing: Run the script to ensure that the sensor readings are accurate and that the script handles various scenarios correctly.
    Validation: Verify the correctness of the temperature and humidity readings against known values or expected ranges.

**3. Deliverables:

    A working Python script that interfaces with the DHT11 sensor, reads data, and processes it.
    Debug outputs showing the raw pulse lengths, byte array contents, and final temperature and humidity values.

**4. Goals:

    Successfully read and interpret data from the DHT11 sensor using the Raspberry Pi GPIO pins.
    Convert raw sensor data into useful temperature and humidity readings.
    Ensure that the communication and data processing are reliable and accurate.

**5. Considerations:

    Timing Accuracy: Ensure that timing measurements for pulse lengths are precise and consistent.
    GPIO Handling: Properly manage GPIO pin configurations and state changes.
    Sensor Communication Protocol: Follow the DHT11 communication protocol as described in the datasheet for accurate data interpretation.
