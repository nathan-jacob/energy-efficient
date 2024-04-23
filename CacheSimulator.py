import sys
from copy import deepcopy
from Cache import Cache
import csv
import statistics
import numpy as np


class CacheSimulator:
    def __init__(self, associativity=4):    

        self.l1_data = Cache()
        self.l1_instruction = Cache()
        self.l2_data = Cache()
        self.l2_data_instruction = Cache()
        self.dram = Cache()

        self.l1_data.set_values(
            active_consumption=1,
            idle_consumption=0.5,
            lower_access_time=0,
            access_time=5*10**-10,
            transfer_penalty=0,
            capacity=1<<15,
            associativity=1,
            DRAM=False
        )
        self.l1_instruction = deepcopy(self.l1_data)
        self.l2_data.set_values(
            active_consumption=2,
            idle_consumption=0.8,
            lower_access_time=5*10**-10,
            access_time=5*10**-9,
            transfer_penalty=5*10**-12,
            capacity=1<<18,
            associativity=associativity,
            DRAM=False
        )
        self.l2_data_instruction = deepcopy(self.l2_data)
        self.dram.set_values(
            access_time = 5*10**-8,
            idle_consumption = 0.8,
            active_consumption = 4,
            capacity=1<<18,
            associativity=4,
            transfer_penalty = 6.4*10**-10,
            lower_access_time = 5*10**-12, 
            DRAM=True
        )
                    
    def print_results(self, filename):
        true_filename = filename.strip('./Traces/Spec_Benchmark/')
        print("Cache Run (" + str(true_filename) + ")\n")

        l1_data_hits = self.l1_data.access_total() - self.l1_data.misses_total()
        l1_instruction_hits = self.l1_instruction.access_total() - self.l1_instruction.misses_total()
        l2_data_hits = self.l2_data.access_total() - self.l2_data.misses_total()

        l1_data_misses = self.l1_data.misses_total()
        l1_instruction_misses = self.l1_instruction.misses_total()
        l2_data_misses = self.l2_data.misses_total()

        l1_data_hit_rate = l1_data_hits / self.l1_data.access_total() if self.l1_data.access_total() > 0 else 0
        l1_instruction_hit_rate = l1_instruction_hits / self.l1_instruction.access_total() if self.l1_instruction.access_total() > 0 else 0
        l2_data_hit_rate = l2_data_hits / self.l2_data.access_total() if self.l2_data.access_total() > 0 else 0

        dram_accesses = self.dram.access_total()

        print("L1 Data Hits: " +  str(l1_data_hits))
        print("L1 Data Misses: " + str(l1_data_misses))
        print("L1 Data Hit Rate: {:.4f}".format(l1_data_hit_rate))
        print("L1 Instruction Hits: " + str(l1_instruction_hits))
        print("L1 Instruction Misses: " + str(l1_instruction_misses))
        print("L1 Instruction Hit Rate: {:.4f}".format(l1_instruction_hit_rate))
        print("L2 Hits: " + str(l2_data_hits))
        print("L2 Misses: " + str(l2_data_misses))
        print("L2 Hit Rate: {:.4f}".format(l2_data_hit_rate))
        
        print(f"DRAM Access Total: " + str(dram_accesses))
        
        factor = 10 ** 9
        total_time = (self.l1_data.time_sum() + self.l1_instruction.time_sum() + self.l2_data.time_sum() + self.dram.time_sum())
        l1_data_mem_energy = self.l1_data.idle_consump() * total_time + self.l1_data.total_watts()
        l1_instruction_mem_energy = self.l1_instruction.idle_consump() * total_time + self.l1_instruction.total_watts()
        l2_data_mem_energy = self.l2_data.idle_consump() * total_time + self.l2_data.total_watts()
        dram_mem_energy = self.dram.idle_consump() * total_time + self.dram.total_watts()

        l1_energy_consumption = (l1_data_mem_energy + l1_instruction_mem_energy)
        l2_energy_consumption = l2_data_mem_energy
        dram_energy_consumption = dram_mem_energy

        print("L1 Consumption: {:.3f} nJ".format(l1_energy_consumption * factor))
        print("L2 Consumption: {:.3f} nJ".format(l2_energy_consumption * factor))
        print("DRAM Consumption: {:.3f} nJ".format(dram_energy_consumption * factor))

        total_energy_consumption = (l1_energy_consumption + l2_energy_consumption + dram_energy_consumption)
        average_memory_access_time = (total_time * factor) / (self.l1_data.access_total() + self.l1_instruction.access_total() + self.l2_data.access_total() + self.dram.access_total())
        
        print("Total Consumption: {:.3f} nJ".format((total_energy_consumption * factor)))
        print("Total Time: {:.3f} ns".format(total_time * factor))
        print("AMAT: {:.3f} ns".format((average_memory_access_time)))
    
    def calc_stats(self):
        l1_data_hits = self.l1_data.access_total() - self.l1_data.misses_total()
        l1_instruction_hits = self.l1_instruction.access_total() - self.l1_instruction.misses_total()
        l2_data_hits = self.l2_data.access_total() - self.l2_data.misses_total()

        l1_data_misses = self.l1_data.misses_total()
        l1_instruction_misses = self.l1_instruction.misses_total()
        l2_data_misses = self.l2_data.misses_total()

        l1_data_hit_rate = l1_data_hits / self.l1_data.access_total() if self.l1_data.access_total() > 0 else 0
        l1_instruction_hit_rate = l1_instruction_hits / self.l1_instruction.access_total() if self.l1_instruction.access_total() > 0 else 0
        l2_data_hit_rate = l2_data_hits / self.l2_data.access_total() if self.l2_data.access_total() > 0 else 0

        dram_accesses = self.dram.access_total()

        factor = 10 ** 9
        total_time = (self.l1_data.time_sum() + self.l1_instruction.time_sum() + self.l2_data.time_sum() + self.dram.time_sum())
        l1_data_mem_energy = self.l1_data.idle_consump() * total_time + self.l1_data.total_watts()
        l1_instruction_mem_energy = self.l1_instruction.idle_consump() * total_time + self.l1_instruction.total_watts()
        l2_data_mem_energy = self.l2_data.idle_consump() * total_time + self.l2_data.total_watts()
        dram_mem_energy = self.dram.idle_consump() * total_time + self.dram.total_watts()
        
        l1_energy_consumption = (l1_data_mem_energy + l1_instruction_mem_energy)
        l2_energy_consumption = l2_data_mem_energy
        dram_energy_consumption = dram_mem_energy

        total_energy_consumption = (l1_energy_consumption + l2_energy_consumption + dram_energy_consumption)
        average_memory_access_time = (total_time * factor) / (self.l1_data.access_total() + self.l1_instruction.access_total() + self.l2_data.access_total() + self.dram.access_total())
        
        return l1_data_hits, l1_data_misses, l1_instruction_hits, l1_instruction_misses, l2_data_hits, l2_data_misses, l1_energy_consumption, l2_energy_consumption, total_energy_consumption, total_time, average_memory_access_time
    
    def run_cache(self, data): 
            for line in data:
                parts = line.split()
                code = int(parts[0], 16)
                address = int(parts[1], 16)

                cache = self.l1_instruction if code == 2 else self.l1_data
                evicted_address, evicted_index, l1_hit, l1_dirty = cache.try_access(code, address)

                if not l1_hit:
                    if l1_dirty:
                        self.l2_data.try_wb(evicted_address)
                    
                    evicted_address, evicted_index, l2_hit, l2_dirty = self.l2_data.try_access(code, address)
                    
                    if l2_hit:
                        self.l1_instruction.place_in_cache(address, evicted_index) if code == 2 else self.l1_data.place_in_cache(address, evicted_index)
                    else:
                        if l2_dirty:
                            self.dram.try_wb()
                            
                        self.dram.try_access()
                        
                        self.l2_data.place_in_cache(address, evicted_index)
                        self.l1_instruction.place_in_cache(address, 0) if code == 2 else self.l1_data.place_in_cache(address, 0)

    def csv_write():
        num_runs = 10
        results_list = []
        csv_write_list = []
        file_paths = ["008.espresso.din", "013.spice2g6.din", "015.doduc.din", "022.li.din", "023.eqntott.din", "026.compress.din", "034.mdljdp2.din", "039.wave5.din", "047.tomcatv.din", "048.ora.din", "085.gcc.din", "089.su2cor.din", "090.hydro2d.din", "093.nasa7.din", "094.fpppp.din"]
        for file_path in file_paths:
            filename = "./Traces/Spec_Benchmark/" + file_path
            run_results = []
            for a in (2,4,8):
                for _ in range(num_runs):
                    data = open(filename, 'r').readlines()
                    sim = CacheSimulator(associativity=a)
                    sim.run_cache(data)
                    l1_data_hits, l1_data_misses, l1_instruction_hits, l1_instruction_misses, \
                    l2_data_hits, l2_data_misses, l1_energy_consumption, l2_energy_consumption, total_energy_consumption, total_time, \
                    average_memory_access_time = sim.calc_stats()

                    run_results.append([
                        l1_data_hits, l1_data_misses, l1_instruction_hits,
                        l1_instruction_misses, l2_data_hits, l2_data_misses, l1_energy_consumption, l2_energy_consumption,
                        total_energy_consumption, total_time, average_memory_access_time
                    ])
                # print(run_results)
                # results_list.append(run_results)
                np_final = np.array(run_results)
                final_list = []
                for i in range(len(np_final[0])):
                    elements = np_final[:, i]
                    final_list.append(np.mean(elements))
                    final_list.append(np.std(elements))
                csv_write_list.append(final_list)
                # print("Results list: ", final_list)
        column_names = [
            'l1_data_hits mean', 'l1_data_hits std', 'l1_data_misses mean', 'l1_data_misses std',
            'l1_instruction_hits mean', 'l1_instruction_hits std', 'l1_instruction_misses mean',
            'l1_instruction_misses std', 'l2_hits mean', 'l2_hits std', 'l2_misses mean', 'l2_misses std',"l1_energy_consumption mean" , "l1_energy_consumption std", "l2_energy_consumption mean", "l2_energy_consumption std",
            'total_energy_consumption mean', 'total_energy_consumption std', 'total_time mean', 'total_time std',
            'average_memory_access_time mean', 'average_memory_access_time std'
        ]
        with open("results.csv", mode='w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(column_names)  # Write the column names as the header
            for row in csv_write_list:
                writer.writerow(row)
        print("Average statistics saved to results.csv")


def main():
    #run with: python3 CacheSimulator.py 008.espresso.din
    filename = "./Traces/Spec_Benchmark/" + sys.argv[1]
    data = open(filename, 'r').readlines()
    sim = CacheSimulator()
    sim.run_cache(data)
    sim.print_results(filename)

def test():
    CacheSimulator.csv_write()  

if __name__ == "__main__":
    main()