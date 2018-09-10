import numpy as np,sys,math

class Traffic():

    def __init__(self):
        self.trans = [1000,400,200,100]
        self.trans_cards = {1000: {"chann_rate": 1000, "channel_spectrum": 150, "slots": 24},
                            400: {"chann_rate": 400, "channel_spectrum": 75, "slots": 12},
                            200: {"chann_rate": 200, "channel_spectrum": 37.5, "slots": 10},
                            100: {"chann_rate": 100, "channel_spectrum": 37.5, "slots": 8}}
    def generate_s_t_pairs(self):
        s = 1 #np.random.randint(1,14)      #s = 1  # int(input('Insert the source node: '))
        t = 12 #np.random.randint(1,14)                      #t = 14  # int(input('Insert the destination node: '))
        return s, t

    def demand_generation(self):
        self.dem = np.random.randint(0,3146)
        self.dem = math.ceil(self.dem / 100) * 100
        print(self.dem)
        return self.dem


    def segregateDataRates(self, dem,cost):
        if dem == 0:
            sys.exit('"demand cannot be provisioned"')
        else:
            split = [0, 0, 0, 0]
            self.dem = dem
            i = 0
            while self.dem > 0:  # dividing the demand into 1tb 400gig and 100gig
                split[i] = (self.dem // self.trans[i])
                self.dem = self.dem % self.trans[i]
                i += 1
            print(split)
            return split

    def caluculate_total_Slots_spec(self, split):
        slot = split[0] * self.trans_cards[1000]['slots'] + split[1] * self.trans_cards[400]['slots'] + split[2] * \
               self.trans_cards[200]['slots'] + split[3] * self.trans_cards[100]['slots']
        spec1 = split[0] * float(self.trans_cards[1000]['channel_spectrum']) + split[1] * float(
            self.trans_cards[400]['channel_spectrum']) + split[2] * float(self.trans_cards[200]['channel_spectrum']) + \
               split[3] * float(self.trans_cards[100]['channel_spectrum'])
        spec = math.ceil(spec1/ 12.5) * 12.5
        return slot, spec
