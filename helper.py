
from traffic import Traffic
from Fiber import Fiber
import numpy as  np
import math
import itertools
from traffic import Traffic

class Helper():
    def __init__(self):

        demand = Traffic()
        demand.generate_s_t_pairs()


        fibre = Fiber(self.graph, self.dist_path)  # fiber class
        ids = fibre.initiateEdges()
        path_get, value, path_cost = fibre.getPath
        print("This is the selected k-path:", path_get)  # printing the path
        path_id = fibre.getCompletePathId(path_get['path'])  # edge from path
        seg = Traffic()  # demand class
        seg.generateFreqWav()
        for x in itertools.count(0):
            if slot_sum <= 769:

                seg.segregateDataRates(self.dem)
                slot, spec = seg.AssignSlots()
                used_spectrum, len_unsed = seg.AssignedSpectrum(self.dem)
                for edge in path_id:
                    # fibre.updateSpectrum(edge, used_spectrum)
                    fibre.updateLink1(edge, ['demand', 'slots_occupied', 'spec_occupied', 'used_spec'],
                                      [self.dem, slot, spec, used_spectrum])
                    fibre.updateLink2(edge, ['demand_sum', "slots_sum", 'cost', 'unused_slots'],
                                      [self.dem, slot, path_cost, len_unsed])
                    fibre.updateLink3(edge, ['cost', 'weight'], [path_cost, value])
                # print("\n")
                # print("fiber class with each path values")
                # for k, v in ids.items():
                #     print(k, v)
                # print("=" * 500)
                # print("=" * 100)
                slot_sum += slot
                if x == 3:
                    break
            else:
                break

        print(slot_sum)



