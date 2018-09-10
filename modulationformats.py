import numpy as np


class ModulationFormats():


    def __init__(self):

        self.modulation_formats = { PM-Qpsk: {"bit_rate_sym": 4, "reach": 3000,"getrequiredSNRdb":0},
                                    PM -Qam8: {"bit_rate_sym": 6, "reach": 1500,"getrequiredSNRdb":9.03},
                                    PM -Qam16: {"bit_rate_sym": 8, "reach": 700,"getrequiredSNRdb":10.52},
                                    PM -Qam32: {"bit_rate_sym": 10, "reach": 350,"getrequiredSNRdb":12.57},
                                    PM -Qam64: {"bit_rate_sym": 12, "reach": 350,"getrequiredSNRdb":14.77}}


    def createRequiredOSNR(self):
        osnr = (bitrate * getrequiredSNRdb)/(2.0 *slotwidth)
        nslots = (bitrate/noofbitspersymbol)/slotwidth


        l = 145.741 +(n - 14.0344)(60.2196 np.log(BR)-465.83)

