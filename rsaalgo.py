from traffic import Traffic
import sys,numpy as np

# central= 284
"""This is a RSA algorithm class ,here we are trying to assign the frequencies to the demand obtained"""


class RsaAlgorithm():
    """these are called transponders cards which divide the demand into corresponding slots of 1000gig ,400gig,200gig,100gig"""

    def __init__(self,freq,split):
        self.trans = [1000, 400, 200, 100]
        self.Lambda = freq
        self.split = split
        self.trans_cards = {1000: {"chann_rate": 1000, "channel_spectrum": 150, "slots": 24},# channel spectrum or bandwidth 6.25 , roadms 12.5ghz
                            400: {"chann_rate": 400, "channel_spectrum": 75, "slots": 12},
                            200: {"chann_rate": 200, "channel_spectrum": 37.5, "slots": 10},
                            100: {"chann_rate": 100, "channel_spectrum": 37.5, "slots": 8}}


    def assignedspectrum(self):
        """this method is returned to the main class where the spectrum slots occupied are returned back """
        assigned,used_spec= self.reserve_slots(self.split)
        return assigned,used_spec

    def available_range(self,total_slot):
        '''here we are taking a window of starting and ending index for the required slots and finding them in the array '''

        count = 0
        begin_index = 0
        i = begin_index
        while count < total_slot and i < len(self.Lambda[1]):
            if self.Lambda[1][i] == 0:
                count += 1
            else:
                begin_index = i + 1
                count = 0
            i += 1
        if count == total_slot:
            end_index = i - 1
            return (begin_index , end_index)
        else:
            return (-1 ,-1)


    def reserve_slots(self,split):
        """here the demand is divided and the wavelenghts are assigned to it."""

        traffic = Traffic
        total_slots,total_spec= traffic.caluculate_total_Slots_spec(self,split)
        begin_id, end_id= self.available_range(total_slots)
        if begin_id == -1 or end_id == -1:
            sys.exit("Cannot allocate resource!!!!!")                   #otherwise slots are availble for use. So let's use them
        self.Lambda[1][begin_id:end_id]= 1
        freq_used = self.Lambda[0][begin_id:end_id]                     #we are using a window with the slots size of the requested demand
        # print("this is freq used",freq_used)
        assigned = []
        begin = begin_id
        slot=[]
        card=[]
        for key in self.trans_cards:
            slot.append(self.trans_cards[key]['slots'])
            card.append(self.trans_cards[key]['chann_rate'])
        for i, s in enumerate(split):
            for j in range(s):
                freq = self.Lambda[0][begin:begin + slot[i]]
                # mid = len(freq) // 2
                # central_freq = freq[mid]
                # central_index = begin + mid                   #NOT USING NOW (ASsume central freq is at central= 284)
                # print(freq[0],freq[-1])
                freq1 = []
                while freq[0] <= freq[-1]:                 # calculating the central frequency for each ghz @ 0.1 ghz
                    freq1.append(np.round((freq[0]), 4))
                    freq[0] += 0.0001
                freq1.append(freq[-1])
                print(freq1)
                # print(freq1[len(freq1)//2])
                data = {"transponder_card":card[i] ,"no of slots(m)": slot[i],"freq": freq, "cent_freq": freq1[len(freq1)//2]}
                assigned.append(data)
                begin += slot[i]
        # print(self.Lambda[1])
        return assigned,freq_used

    # def generate_demand_id(self,dem):       #demand and its index values
    #     pass
    #
    #
    # def release_slots(self):
    #     self.Lambda[1][1:10]= 0 #TODO spectrum release model ideas to be implemented
    #     print(self.Lambda[1])


