#!/usr/bin/env python2
# coding=UTF8
# Author: Iñaki Ucar <i.ucar86@gmail.com>
# Description: Simple simulation core in Python and M/M/1 queueing example

from heapq import heappop, heappush

class Simulator(object):
    """Simulation environment"""
    
    def __init__(self):
        self.now = 0
        self.queue = []
        self.processes = []
    
    def reset(self):
        self.now = 0
        self.queue = []
        for p in self.processes:
            p.reset()
            p.activate()
    
    def schedule(self, delay, event):
        heappush(self.queue, (self.now + delay, event))
    
    def peek(self):
        return self.queue[0][0]
    
    def _step(self):
        self.now, event = heappop(self.queue)
        event()
        
    def step(self):
        if not self.queue:
            raise RuntimeError('no generators defined')
        self._step()
    
    def run(self, until=1000):
        if not self.queue:
            raise RuntimeError('no generators defined')
        while self.now < until:
            self._step()

class Process(object):
    """Abstract class"""
    
    def __init__(self, sim, dist, out):
        self.sim = sim
        self.sim.processes.append(self)
        if not callable(dist):
            raise TypeError('dist must be callable')
        self.dist = dist
        self.out = out
        self.reset()
        self.activate()
        
    def reset(self):
        pass
    
    def activate(self):
        raise NotImplementedError

class Monitor(object):
    """Statistics gathering"""
    
    def __init__(self, sim):
        self.sim = sim
        self.reset()
        
    def reset(self):
        self.last = 0
        self.dt = []
        self.Qt = []
        self.Ut = []
    
    def observe(self, queue, server):
        self.dt.append(self.sim.now - self.last)
        self.last = self.sim.now
        self.Qt.append(queue)
        self.Ut.append(server)

# Decorator for methods
def monitor(func):
    def new_func(self, *args, **kwargs):
        if self.mon:
            self.mon.observe(self.queue, self.busy)
        return func(self, *args, **kwargs)
    return new_func

class Generator(Process):
    """Generator of new entities"""
    
    def __init__(self, sim, dist, out=None):
        if not out or not isinstance(out, Resource):
            raise TypeError('no resource connected')
        super(Generator, self).__init__(sim, dist, out)
        
    def activate(self):
        delay = self.dist()
        sim.schedule(delay, self.out.seize)
        sim.schedule(delay, self.activate)

class Resource(Process):
    """Resource with variable capacity and queue size"""
    def __init__(self, sim, dist, capacity=1, queue_size=float('inf'), out=None, mon=None):
        if out and not isinstance(out, Resource):
            raise TypeError('no resource connected')
        self.queue_size = queue_size
        self.capacity = capacity
        self.mon = mon
        super(Resource, self).__init__(sim, dist, out)
    
    def reset(self):
        self.queue = 0
        self.busy = 0
        if self.mon:
            self.mon.reset()
    
    def activate(self):
        pass
    
    @monitor
    def seize(self):
        # Serve or enqueue
        if self.busy < self.capacity:
            self.busy += 1
            sim.schedule(self.dist(), self.release)
        elif self.queue < self.queue_size:
            self.queue += 1
    
    @monitor
    def release(self):
        if self.out:
            sim.schedule(0, self.out.seize)
        # Serve another or halt
        if self.queue:
            self.queue -= 1
            sim.schedule(self.dist(), self.release)
        else:
            self.busy -= 1

### M/M/1 queueing example
if __name__ == "__main__":
    import numpy as np
    import matplotlib.pyplot as plt
    from functools import partial
    
    la = 1.0
    mu = 2.0
    rho = la/mu
        
    exp_service = partial(np.random.exponential, 1.0/mu)
    exp_arrival = partial(np.random.exponential, 1.0/la)
    
    sim = Simulator()
    
    mon = Monitor(sim)
    server = Resource(sim, exp_service, mon=mon)
    gen = Generator(sim, exp_arrival, out=server)
    
    sim.run(until=1000)
    
    ### Figures
    dt = np.array(mon.dt)
    Ut = np.array(mon.Ut)
    Qt = np.array(mon.Qt)
    
    axis = plt.subplot()
    axis.set_title('M/M/1, $\lambda={}, \mu={}$'.format(la, mu))
    
    t = dt.cumsum()
    axis.step(t, Ut, label='Instantaneous server utilisation')
    axis.step(t, Qt, label='Instantaneous queue utilisation')
    N_average_t = ((Ut + Qt) * dt).cumsum() / t
    axis.plot(t, N_average_t, label='Average system utilisation')
    axis.axhline(rho/(1-rho), linewidth=2, color='black', ls='--', label='Theoretical average')
    
    axis.set_xlabel('time')
    axis.set_ylabel('# of customers')
    axis.legend()
    
    plt.show()
    