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
        ('start', 'Start of Communication'),
    )
    annotation_rows = (
        ('control', 'Control Signals', (0,)),  # Shows the 'start' annotation in a row called 'Control Signals'
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
            if state == 'IDLE': #Wait for a logic low
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
                    self.put(prev_samp, self.samplenum, self.out_ann, [0, ['start ' + str(self.samplenum) + ' ' + str(self.samplerate)]])
                    prev_samp = self.samplenum
                    state = 'WAIT_RESP'
                else:
                    state = 'IDLE' #Look for the next possible valid pulse.
            elif state == 'WAIT_RESP': #Small wait before there is a response from the sensor
                pins = self.wait({0: 'e'}) #Look for the next edge
                if pins[0] == False and (((8/1000000) * self.samplerate)) <= (self.samplenum - prev_samp) <= (((40/1000000) * self.samplerate)):
                    self.put(prev_samp, self.samplenum, self.out_ann, [0, ['wait']])
                    prev_samp = self.samplenum
                    state = 'RESP'           
                else:
                    state = 'IDLE'
            elif state == 'RESP': #Checking for the response signal.
                pins = self.wait({0: 'e'})
                if  pins[0] == True and (((80 * (1 - 0.10)/1000000) * self.samplerate)) <= (self.samplenum - prev_samp) <= (((80 * (1 + 0.10)/1000000) * self.samplerate)):
                    self.put(prev_samp, self.samplenum, self.out_ann, [0, ['Reponse']])
                    prev_samp = self.samplenum
                    state = 'WAIT_DATA'
                else:
                    state = 'IDLE'
            elif state == 'WAIT_DATA':
                pins = self.wait({0: 'e'}) #Wait before data response
                if pins[0] == False and (self.samplenum - prev_samp) >= ((75/1000000) * self.samplerate):    
                    self.put(prev_samp, self.samplenum, self.out_ann, [0, ['Wait']])
                    prev_samp = self.samplenum
                    state = 'COMS'
                else:
                    state = 'IDLE'
            elif state == 'COMS':
                data_bits = []
                int_samp = None
                while len(data_bits) < 40:
                    pins = self.wait({0: 'e'})
                    if pins[0] == True:
                        int_samp = self.samplenum
                    elif pins[0] == False:
                        self.put(prev_samp, self.samplenum, self.out_ann, [0, ['Bit']])
                        prev_samp = self.samplenum
                        data_bits.append(1)
                state = 'IDLE'