import math
import random
    
class Cache():
    def __init__(self):
        pass

    def set_values(self, active_consumption, idle_consumption, lower_access_time,access_time, transfer_penalty, capacity, associativity, DRAM):
        self.acc_total, self.write_total = 0, 0
        self.miss_total = 0
        self.energy_active = active_consumption
        self.energy_idle = idle_consumption
        self.acc_lower = lower_access_time
        self.acc_time = access_time
        self.penalty = transfer_penalty
        self.DRAM = DRAM
        self.associativity = associativity

        self.x1 = (self.energy_active * self.acc_time + self.penalty)
        self.x2 = (self.energy_active * (self.acc_time - self.acc_lower) + (self.penalty))

        self.cacheVals = [[-1, False, False] for _ in range(capacity // 64)]
        self.mask = (capacity // (64 * associativity)) - 1
        self.offset = int(6 + math.log2(capacity // (64 * associativity)))
        self.accesses = {access: 0 for access in range(capacity // (64 * associativity))}

    def idle_consump(self):
        return self.energy_idle
    
    def access_total(self):
        return self.acc_total

    def misses_total(self):
        return self.miss_total
    
    def total_watts(self):
        return self.x1 * self.acc_total + self.x2 * self.write_total

    def time_sum(self):
        return self.write_total * (self.acc_time - self.acc_lower) + self.acc_time * self.acc_total

    def try_access(self, access_type=None, address=None):
        if self.DRAM:
            self.acc_total += 1
            return
        
        tag = (address >> self.offset) & ((1 << (32 - self.offset)) - 1)
        
        block_start = ((address >> 6) & self.mask) * self.associativity
        block_end = block_start + self.associativity
        curr_cache = self.cacheVals[block_start:block_end]
        
        dirty = False
        hit = False
        invalid = -1
        
        for i, (tag_c, valid_c, _) in enumerate(curr_cache):
            if not valid_c:
                invalid = i
                continue
            
            if tag == tag_c:
                hit = True
                curr_cache[i][2] |= access_type == 1
                break
        
        evicted_address = 0
        index = -1
        
        if not hit:
            self.miss_total += 1
            
            if invalid != -1:
                index = invalid
            else:
                index = random.randint(0, self.associativity - 1)
                dirty = curr_cache[index][2]
                
                if dirty:
                    evicted_address = (curr_cache[index][0] << self.offset) | (((address >> 6) & self.mask) << 6)
                    
            curr_cache[index] = [tag, True, access_type == 1]
        
        self.acc_total += 1
        self.accesses[((address >> 6) & self.mask)] += 1
        self.cacheVals[block_start:block_end] = curr_cache
        
        return evicted_address, index, hit, dirty

    
    def try_wb(self, address=None):
        if self.DRAM:
            self.write_total += 1
            return
        
        tag = (address >> self.offset) & ((1 << (32 - self.offset)) - 1)
        
        block_start = ((address >> 6) & self.mask) * self.associativity
        block_end = block_start + self.associativity
        
        for block_index in range(block_start, block_end):
            tag_c, valid_c, dirty_c = self.cacheVals[block_index]
            if tag == tag_c and valid_c:
                self.cacheVals[block_index] = [tag, True, True]
                self.write_total += 1
                break

    def place_in_cache(self, address, index):
        self.cacheVals[((address >> 6) & self.mask) * self.associativity  + index] = [((address >> self.offset) & ((1 << (32 - self.offset)) - 1)), True, False]

    
    
