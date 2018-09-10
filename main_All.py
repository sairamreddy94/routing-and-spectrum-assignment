from traffic import Traffic
from Fiber import Fiber
from Kpathselection import Kpathselection
from traffic import Traffic
from rsaalgo import RsaAlgorithm
import sys
import itertools


def main():
    traffic1 = Traffic()                              # Traffic class
    s,t = traffic1.generate_s_t_pairs()                  # source and destination
    kpath = Kpathselection(s,t)                          #Kpath class
    path_list,graph=kpath.YenKpath()                     # disjoint path list and the topology graph
    path_value,value,cost,hops=kpath.getPath(path_list)     #only path path number distance and the number of hops segregated seperately
    print("this is the selected path",path_value)
    path_id = kpath.path_id(path_value['path'])  # assigning path id to the path
    updated = kpath.path_class()
    fiber=Fiber(graph,path_list)
    ids = fiber.initiateEdges()
    #print("edge ids:",ids)
    print("-"*80)
    for id in ids.values():
        pass
        # print("id:", id)

    fre_list = fiber.generateFreqWav()   # list of all the freq and its array
    kpath.updatepath(['id', 'route', 'source', 'destination', 'weight', 'cost', 'hops'],
                     [path_id, path_value["path"], s, t, value, cost,
                      hops])  # updating the path class with s,t,cost,hops etc
    # print("this is the selected path ", updated)
    # print("=" * 500)

    for x in itertools.count(0):
        dem = traffic1.demand_generation()
        # print("this is source {} destination {} and dem {}".format(s,t,dem))
        split = traffic1.segregateDataRates(dem,cost)
        slot, spec = traffic1.caluculate_total_Slots_spec(split)
        rsa = RsaAlgorithm(fre_list, split)
        # if slot <= 769 or spec <= 4850:
        assigned, used_spec = rsa.assignedspectrum()  # calling the assigned spectrum
        # pointer_count = []
        # pointer_count.append(pointer_ids)
        # print("in rsa testing x for 2 4 6 case", pointer_count, pointer_ids)
        # if x == 2:
        #     rsa.release_slots()

        for values in assigned:
            pass
            print(values)
        fiber_id = fiber.getCompleteedgeId(path_value['path'])

        for edge in fiber_id:
            fiber.updateSpectrum(edge, list(used_spec))
            fiber.updateLink1(edge, ['slots_occupied', 'spec_occupied'], [slot, spec])
            fiber.updateLink2(edge, ["slots_sum", "total_spec"], [slot, spec])
            fiber.updateLink4(edge, ["unused_spec", "unused_slots"], [spec, slot], [4850, 769])
            # fiber.updateLink3(edge, ["array"],1)
        for k, v in ids.items():
            print(k, v)
        print("=" * 500)
        if x ==1:
            break
    else:

        sys.exit('no slots are available')
if __name__ == '__main__':
    main()