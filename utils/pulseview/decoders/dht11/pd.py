##
## This file is part of the libsigrokdecode project.
##
## Copyright (C) 2019 Marco Geisler <m-sigrok@mageis.de>
##
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program; if not, see <http://www.gnu.org/licenses/>.
##

import sigrokdecode as srd
class SamplerateError(Exception):
    pass
    
class Decoder(srd.Decoder):
    api_version = 3
    id = 'dht11'
    name = 'DHT11'
    longname = 'Digital Humidity Temperature-11 Sensor'
    desc = 'DHT11 temp/humidity sensor. single-wire'
    license = 'gplv2+'
    inputs = ['logic']
    outputs = []
    tags = ['IC', 'Sensor']
    annotations = (
        ('start', 'Start'),
        ('response', 'Response'),
        ('bit', 'Bit'),
        ('end', 'End'),
        ('byte', 'Byte'),
        ('humidity', 'Relative humidity'),
        ('temperature', 'Temperature'),
        ('checksum', 'Checksum'),
        ('wait', 'Wait'),
        ('calculated checksum', 'Calculated Checksum'),
        ('validity', 'Validity'),
    )
    annotation_rows = (
        ('bits', 'Bits', (0, 1, 2, 3, 8)),
        ('bytes', 'Bytes', (4, 7)),
        ('results', 'Results', (5, 6)),
        ('validation','Validation', (9, 10)),
    )
    channels = (
        {'id': 'sda', 'name': 'SDA', 'desc': 'Single wire serial data line'},
    )

    def metadata(self, key, value):
        if key == srd.SRD_CONF_SAMPLERATE:
            self.samplerate = value
    
    def __init__(self):
        self.reset()

    def reset(self):
        self.out_ann = None
        self.samplerate = None
    def start(self):
        self.out_ann = self.register(srd.OUTPUT_ANN)
        
    def procdata(self, bitlist, bytepos):
        if len(bitlist) == 40: #Decode for dht11 will have 40 valid bits
            humid = int(''.join(str(bit) for bit in bitlist[0:8]),2)  + (int(''.join(str(bit) for bit in bitlist[9:16]),2) / 10.0)
            temp = int(''.join(str(bit) for bit in bitlist[17:24]),2)  + (int(''.join(str(bit) for bit in bitlist[25:32]),2) / 10.0)
            cal_sum = int(''.join(str(bit) for bit in bitlist[0:8]),2) + int(''.join(str(bit) for bit in bitlist[9:16]),2) + int(''.join(str(bit) for bit in bitlist[17:24]),2) + int(''.join(str(bit) for bit in bitlist[25:32]),2)
            for i in range(0, len(bytepos), 2):
                strt_bit_index = (i // 2) * 8
                end_bit_index = strt_bit_index + 8
                sublist = bitlist[strt_bit_index:end_bit_index] 
                bit_string = int(''.join(str(bit) for bit in sublist),2)
                if i in [0, 2, 4, 6]:
                    self.put(bytepos[i], bytepos[i + 1], self.out_ann, [4, ['Byte: %#04x' % bit_string, '%#04x' % bit_string]])
                else:
                    self.put(bytepos[i], bytepos[i + 1], self.out_ann, [7, ['Checksum: %#04x' % bit_string, '%#04x' % bit_string]])
                    if bit_string == cal_sum:
                        self.put(bytepos[i], bytepos[i + 1], self.out_ann, [10, ['Checksum: %#04x: OK' % bit_string, '%#04x: OK' % bit_string]])
                    else:
                        self.put(bytepos[i], bytepos[i + 1], self.out_ann, [10, ['Checksum: %#04x: Error' % bit_string, '%#04x: Err' % bit_string]])
            self.put(bytepos[0], bytepos[3], self.out_ann, [5, ['Humidity: %.1f %%' % humid, 'RH = %.1f %%' % humid]])
            self.put(bytepos[4], bytepos[7], self.out_ann, [6, ['Temperature: %.1f °C' % temp, 'T = %.1f °C' % temp]])
            self.put(bytepos[0], bytepos[7], self.out_ann, [9, ['Calculated sum: %#04x' % cal_sum, '%#04x' % cal_sum]])
    def decode(self):
        state = 'IDLE'
        samp_pin = None
        start_samp = None
        prev_samp = None
        
        
        if not self.samplerate or self.samplerate < 200000:
            raise SamplerateError('Cannot decode without sample rate or sample rate lower than 200kHz.')
        pins = self.wait()
        samp_pin = pins[0]
        while True:
            if state == 'IDLE': #Wait for a logic low starting is communication
                #raise SamplerateError(str(self.samplenum) + ' ' + str(pins))
                if samp_pin == False:   #Checks if the logic level is low
                    start_samp = self.samplenum
                    state = 'START_COM'
                else:
                    pins = self.wait({0: 'f'})  #Since pin was logic high move to sample where it goes to a logic low
                    start_samp = self.samplenum
                    state = 'START_COM'
            elif state == 'START_COM': #Check if low meets start com_condition for sensor
                prev_samp = self.samplenum
                pins = self.wait({0: 'r'}) #Since we must be logic low look for the next rising edge.
                if (self.samplenum - prev_samp)  >= ((18000/1000000) * self.samplerate):
                    self.put(prev_samp, self.samplenum, self.out_ann, [0, ['start']])
                    prev_samp = self.samplenum
                    state = 'WAIT_RESP'
                else:
                    state = 'IDLE' #Look for the next possible valid pulse.
            elif state == 'WAIT_RESP': #Small wait before there is a response from the sensor
                pins = self.wait({0: 'e'}) #Look for the next edge
                if pins[0] == False and (((8/1000000) * self.samplerate)) <= (self.samplenum - prev_samp) <= (((40/1000000) * self.samplerate)):
                    self.put(prev_samp, self.samplenum, self.out_ann, [8, ['Wait', 'W']])
                    prev_samp = self.samplenum
                    state = 'RESP'           
                else:
                    state = 'IDLE'
            elif state == 'RESP': #Checking for the response signal.
                pins = self.wait({0: 'e'})
                if  pins[0] == True and (((80 * (1 - 0.10)/1000000) * self.samplerate)) <= (self.samplenum - prev_samp) <= (((80 * (1 + 0.10)/1000000) * self.samplerate)):
                    self.put(prev_samp, self.samplenum, self.out_ann, [1, ['Response', 'R']])
                    prev_samp = self.samplenum
                    state = 'WAIT_DATA'
                else:
                    state = 'IDLE'
            elif state == 'WAIT_DATA':
                pins = self.wait({0: 'e'}) #Wait before data response
                if pins[0] == False and (self.samplenum - prev_samp) >= ((75/1000000) * self.samplerate):    
                    self.put(prev_samp, self.samplenum, self.out_ann, [8, ['Wait', 'W']])
                    prev_samp = self.samplenum
                    state = 'COMS'
                else:
                    state = 'IDLE'
            elif state == 'COMS': #Data response
                data_bits = []
                byte_loc = []
                inter_samp = None
                diff = None
                #int(-(-x // 1)) used to round a number without importing the math module.
                end_lng = int(-(-((((70 + 1) * (1 + 0.13)/1000000) * self.samplerate)) + 1 // 1))
                while True:
                    pins = self.wait([{0: 'e'}, {'skip': end_lng}]) #Look for the next edge or longer than a '1' bit value
                    if pins[0] == True:
                        inter_samp = self.samplenum
                        if (inter_samp - prev_samp) > end_lng:
                            self.put(prev_samp, self.samplenum, self.out_ann, [3, ['End', 'E']])
                            state = 'IDLE'
                            self.procdata(data_bits, byte_loc) #Process the collected bits
                            break
                    elif pins[0] == False:
                        diff = self.samplenum - inter_samp
                        if (((25 * (1 - 0.20)/1000000) * self.samplerate)) <= diff <= (((25 * (1 + 0.20)/1000000) * self.samplerate)):
                            self.put(prev_samp, self.samplenum, self.out_ann, [2, ['Bit: 0','0']])
                            data_bits.append(0)
                        elif (((70 * (1 - 0.10)/1000000) * self.samplerate)) <= diff <= (((70 * (1 + 0.13)/1000000) * self.samplerate)):
                            self.put(prev_samp, self.samplenum, self.out_ann, [2, ['Bit: 1','1']])
                            data_bits.append(1)
                        else:
                            state = 'IDLE'
                            break
                        if len(data_bits) % 8 == 1: #For values 1, 9... to determine ending position of byte
                            byte_loc.append(prev_samp)
                        if len(data_bits) % 8 == 0: #For values 0, 8... to determine starting position of byte
                            byte_loc.append(self.samplenum)
                        prev_samp = self.samplenum
