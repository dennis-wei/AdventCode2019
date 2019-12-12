import math
import time

def parse_position(position_string):
    axes = position_string.strip()[1:-1].split(",")
    x = int(axes[0].split('=')[1])
    y = int(axes[1].split('=')[1])
    z = int(axes[2].split('=')[1])
    return (x, y, z)

def parse_input(filename):
    starting_positions = {}
    with open(filename, 'r') as f:
        for i, l in enumerate(f):
            starting_positions[i] = parse_position(l)
    return starting_positions

class MoonSystem:
    def __init__(self, starting_positions):
        self.positions = starting_positions
        self.velocities = { k: (0, 0, 0) for k in starting_positions.keys() }
        self.num_steps = 0
    
    def apply_gravity(self):
        all_changes = {}
        sign = lambda x: x and (1, -1)[x < 0]
        for moon1, moon1_position in self.positions.items():
            changes = [0, 0, 0]
            for moon2, moon2_position in self.positions.items():
                (x1, y1, z1) = moon1_position
                (x2, y2, z2) = moon2_position

                changes[0] += sign(x2 - x1)
                changes[1] += sign(y2 - y1)
                changes[2] += sign(z2 - z1)

            all_changes[moon1] = changes
        
        for k, v in self.velocities.items():
            (ix, iy, iz) = v
            (dx, dy, dz) = all_changes[k]
            self.velocities[k] = (ix + dx, iy + dy, iz + dz)
    
    def apply_velocity(self):
        for k, v in self.positions.items():
            (px, py, pz) = v
            (vx, vy, vz) = self.velocities[k]
            self.positions[k] = (px + vx, py + vy, pz + vz)
    
    def step(self):
        self.apply_gravity()
        self.apply_velocity()
        self.num_steps += 1

    def apply_gravity_dim(self, dim):
        all_changes = {}
        sign = lambda x: x and (1, -1)[x < 0]
        for moon1, moon1_position in self.positions.items():
            change = 0
            for moon2, moon2_position in self.positions.items():
                d1 = moon1_position[dim]
                d2 = moon2_position[dim]

                change += sign(d2 - d1)

            all_changes[moon1] = change
        
        for k, v in self.velocities.items():
            change = all_changes[k]
            velocities = list(v)
            velocities[dim] += change
            self.velocities[k] = tuple(velocities)
    
    def apply_velocity_dim(self, dim):
        for k, v in self.positions.items():
            initial_pos = list(v)
            change = self.velocities[k][dim]
            initial_pos[dim] += change
            self.positions[k] = tuple(initial_pos)
        
    def step_dim(self, dim):
        self.apply_gravity_dim(dim)
        self.apply_velocity_dim(dim)
        self.num_steps += 1
    
    def step_times(self, n):
        for i in range(1, n + 1):
            self.step()
            
            if i in set([10, 20, 30, 40, 50, 60, 70, 80, 90, 100]):
                print(f"After {i} steps:")
                for k, v in self.positions.items():
                    print(f"Moon {k}: pos = {v} | vel = {self.velocities[k]}")
                print()
    
    def get_energy_after_steps(self, n):
        self.step_times(n)
        energies = {}
        for k, v in self.positions.items():
            (x, y, z) = v
            (vx, vy, vz) = self.velocities[k]

            potential_energy = abs(x) + abs(y) + abs(z)
            kinetic_energy = abs(vx) + abs(vy) + abs(vz)
            total_energy = potential_energy * kinetic_energy
            
            print(f"Energies for moon {k}: potential={potential_energy}, kinetic={kinetic_energy}, total={total_energy}")

            energies[k] = total_energy
        
        return(sum(energies.values()))
    
    def get_state_tuple(self, dim):
        acc = []
        for moon, moon_position in self.positions.items():
            acc.append(moon_position[dim])
            acc.append(self.velocities[moon][dim])
        
        return tuple(acc)
    
    def step_until_previous_state(self, dim):
        prev_states = set()
        prev_states.add(self.get_state_tuple(dim))

        num_steps = 0
        while True:
            num_steps += 1
            self.step_dim(dim)
            new_state = self.get_state_tuple(dim)
            if new_state in prev_states:
                break
            
            prev_states.add(new_state)
        
        return num_steps

def lcm(n1, n2):
    return n1 * n2 // math.gcd(n1, n2)

def main():
    start = time.time()
    starting_positions = parse_input('input.txt')
    system = MoonSystem(starting_positions)
    answer1 = system.get_energy_after_steps(1000)
    print(f"Answer to Part 1: {answer1}")
    print(f"Took {time.time() - start} seconds")
    print()

    start = time.time()
    system2 = MoonSystem(starting_positions)
    period_x = system.step_until_previous_state(0)
    print(f"Period for x: {period_x}")
    period_y = system.step_until_previous_state(1)
    print(f"Period for y: {period_y}")
    period_z = system.step_until_previous_state(2)
    print(f"Period for z: {period_z}")
    answer2 = lcm(lcm(period_x, period_y), period_z)
    print(f"Answer to Part 2: Took {answer2} steps to return to previous state")
    print(f"Took {time.time() - start} seconds")
    
main()