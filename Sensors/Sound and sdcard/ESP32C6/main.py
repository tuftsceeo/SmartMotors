from machine import I2S, Pin
import math
import time
import machine

import os
import ustruct


'''
LRC (Left/Right Clock)  D8
BCLK (Bit Clock) - D9
DIN (Data In) -D10

'''


# I2S Setup Function with Variable Rate
def setup_i2s(sample_rate, bit_depth,BUFFER_SIZE = 1024):
    i2s = I2S(
        0,
        sck=Pin(20),   # Serial Clock
        ws=Pin(19),    # Word Select / LR Clock
        sd=Pin(18),    # Serial Data
        mode=I2S.TX,
        bits=bit_depth,
        format=I2S.MONO,
        rate=sample_rate,
        ibuf=BUFFER_SIZE
    )
    return i2s

# Helper function to parse the .wav header and extract audio parameters
def parse_wav_header(file):
    file.seek(0)  # Ensure we're at the start of the file
    header = file.read(44)  # Standard .wav header size
    sample_rate = ustruct.unpack('<I', header[24:28])[0]
    bit_depth = ustruct.unpack('<H', header[34:36])[0]
    return sample_rate, bit_depth



def play_sound(path):
        # Open the .wav file from the SD card
    with open(path, "rb") as wav_file:
        sample_rate, bit_depth = parse_wav_header(wav_file)
        print(sample_rate, bit_depth)
        i2s = setup_i2s(sample_rate, bit_depth)

        # Skip the header and begin reading audio data
        wav_file.seek(44)  # Start of PCM data after 44-byte header

        # Buffer to hold PCM data read from the file
        buffer = bytearray(1024)
        
        while True:
            try:
                num_read = wav_file.readinto(buffer)
                if num_read == 0:
                    break  # End of file
                i2s.write(buffer[:num_read])  # Write to I2S in chunks
            except KeyboardInterrupt:
                print("CTRL C pressed")


try:
    play_sound("hello.wav")

    time.sleep(5)
    print('sleeping')

    
except Exception as e:
    print("An error occurred:", e)
finally:
    pass