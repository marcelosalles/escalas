'''
Created on 8 de mar de 2016

@author: Frederico
https://www.youtube.com/watch?v=1Hqm0dYKUx4
'''
import math
import pyaudio

def sine_tone(freq=440, length=1, bitrate=16000):
    if freq > bitrate:
        bitrate = freq+100
    
    NUMBEROFFRAMES = int(bitrate * length)
    RESTFRAMES = NUMBEROFFRAMES % bitrate
    WAVEDATA = ''    
    
    for x in xrange(NUMBEROFFRAMES):
        WAVEDATA = WAVEDATA+chr(int(math.sin(x/((bitrate/freq)/math.pi))*127+128))    
    
    for x in xrange(RESTFRAMES):
        WAVEDATA = WAVEDATA+chr(128)
    
    p = pyaudio.PyAudio()
    stream = p.open(format = p.get_format_from_width(1), 
                    channels = 1, 
                    rate = bitrate, 
                    output = True)
    
    stream.write(WAVEDATA)
    stream.stop_stream()
    stream.close()
    p.terminate()

class Escala(list):
    NOTAS = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#' ]
    ESCALAS = { 'maior':[0, 2, 4, 5, 7, 9, 11],
                'menor':[0, 2, 3, 5, 7, 8, 10],
                'harmonica':[0, 2, 3, 5, 7, 8, 11],
                'melodica':[0, 2, 3, 5, 7, 9, 11],
                'pentatonica':[0, 3, 5, 7, 10],
                'diminuta':[0, 3, 6, 9],
                'cromatica':[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
                'pentatonica_blues':[0, 3, 5, 6, 7, 10],
                'fibonacci':[0, 1, 1, 2, 3, 5, 8],
                'ionian':[0, 2, 4, 5, 7, 9, 11],
                'dorian':[0, 2, 3, 5, 7, 9, 10],
                'phrygian':[0, 1, 3, 5, 7, 8, 10],
                'lydian':[0, 2, 4, 6, 7, 9, 11],
                'mixolydian':[0, 2, 4, 5, 7, 9, 10],
                'aeolian':[0, 2, 3, 5, 7, 8, 10],
                'locrian':[0, 1, 3, 5, 6, 8, 10] }
    FREQS = {'A':440.0,
             'A#':466.16,
             'B':493.88,
             'C':523.25,
             'C#':554.37,
             'D':587.33,
             'D#':622.25,
             'E':659.25,
             'F':698.46,
             'F#':739.99,
             'G':783.99,
             'G#':830.61 }
    INSTRUMENTS = { 'guitar':['E', 'B', 'G', 'D', 'A', 'E'],
                    'bass':['G', 'D', 'A', 'E'],
                    'bass5strings':['G', 'D', 'A', 'E', 'B'],
                    'ukulele':['A', 'E', 'C', 'G'] }

    def __init__(self, tonica, tipo_escala, *args):
        list.__init__(self, *args)
        self.tonica = tonica.upper()
        self.tipo_escala = tipo_escala.lower()
        self._make_escala()
        
    def __repr__(self, *args, **kwargs):
        return str(escala.tonica) + " " + str(escala.tipo_escala) + " = " + list.__repr__(self, *args, **kwargs)
        
    def _make_escala(self):
        index_tonica = self.NOTAS.index(self.tonica)
        del self[:]
        for dist_tonica in self.ESCALAS[self.tipo_escala]:
            self.append(self.NOTAS[(index_tonica+dist_tonica)%len(self.NOTAS)])
    
    def print_escala(self, instrument='guitar'):
        print('\n    1   2   3   4   5   6   7   8   9   10  11')
        for note in Escala.INSTRUMENTS[instrument]:
            self.print_string(Escala(note, 'cromatica'))
    
    def print_string(self, string):
        printed_string = string.tonica
        if string[0] in self:
            if string[0] == self[0]:
                printed_string += " O"
            else:
                printed_string += " X"
        else:
            printed_string += " |"
        for nota in string[1:]:
            if nota in self:
                if nota == self[0]:
                    printed_string += '-O-|'
                else:
                    printed_string += '-X-|'
            else:
                printed_string += '---|'
        print(printed_string)
        
    def play(self, length=1, oitavas=1):
        todas_freqs = []
        for i in range(oitavas):
            for note in self:
                freq = self.FREQS[note]
                if freq < Escala.FREQS[self[0]]:
                    freq *= 2
                todas_freqs.append(freq*(2**i))
        for note in todas_freqs:
            sine_tone(note, length)


escala = Escala('C', 'maior')

print(escala)
escala.print_escala()
escala.print_escala('ukulele')
escala.print_escala('bass')
escala.play(0.05)
