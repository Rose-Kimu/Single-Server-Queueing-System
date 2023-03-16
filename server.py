import math
import random

class SingleServer():
    def __init__(self):
        self.Q_LIMIT =100
        self.BUSY = 1
        self.IDLE = 0

        self.next_event_type = 0
        self.num_custs_delayed = 0
        self.num_delays_required = 0
        self.num_events = 0
        self.num_in_q = 0
        self.server_status = self.IDLE

        self.area_num_in_q = 0.0
        self.area_server_status = 0.0 
        self.mean_interarrival = 0.0
        self.mean_service = 0.0
        self.sim_time = 0.0
        self.time_arrival = [0.0]*(self.Q_LIMIT + 1)
        self.time_last_event = 0.0
        self.total_of_delays = 0.0
        self.time_next_event = [0.0, 0.0 ,1.0e+30]

    def expon(self,mean):
        return -mean * math.log(random.random())

    def initialize(self):  #Initialization function
        self.sim_time = 0.0
        # Initialize the state variables
        self.server_status = self.IDLE
        self.num_in_q = 0
        self.time_last_event = 0.0

        # Initialize the statistical counters
        self.num_custs_delayed = 0
        self.total_of_delays = 0.0
        self.area_num_in_q = 0.0
        self.area_server_status = 0.0

        self.time_arrival = [0,0] * (self.Q_LIMIT+1)
        self.time_next_event = [0.0, 0.0, 1.0e+30]
        self.time_next_event[1] = self.sim_time + self.expon(self.mean_interarrival)


    def timing(self): #Timing function
        min_time_next_event = 1.0e+29
        self.next_event_type = 0

        # Determing the event type of the next event to occur
        for i in range (0, self.num_events):
            if self.time_next_event[i] < min_time_next_event:
                min_time_next_event = self.time_next_event[i]
                self.next_event_type = i+1

        # Check to see whether the event list is empty

        if (self.next_event_type == 0):
            # The event list is empty , so stop the simulation
            with open ("output.txt", 'w') as outfile:
                outfile.write(f"Event list empty at time {self.sim_time}") 
        # The event list is not empty, so advance the simulation clock
        self.sim_time = min_time_next_event


    def arrive(self):
        self.time_next_event[0] = self.sim_time + self.expon(self.mean_interarrival)

        if self.server_status == self.BUSY:
            self.num_in_q += 1

            if self.num_in_q > self.Q_LIMIT:
                with open("output.txt", 'w') as outfile:
                    outfile.write(f"Overflow of the array time_arrival at  {self.sim_time} and number = {self.num_in_q}")
            # Update the arrival time of the customer that just arrived in the queue
            self.time_arrival[self.num_in_q] = self.sim_time  
        else:
            delay = 0.0
            self.total_of_delays += delay
            self.num_custs_delayed += 1
            self.server_status = self.BUSY
            self.time_next_event[1] = self.sim_time + self.expon(self.mean_service)

    # Departure event function
    def depart(self):
        if self.num_in_q == 0:
            self.server_status = self.IDLE
            self.time_next_event[1] = 1.0e+30
        else:
            self.num_in_q -= 1
            delay = self.sim_time - self.time_arrival[1]
            self.total_of_delays += delay
            self.num_custs_delayed += 1
            self.time_next_event[1] = self.sim_time + self.expon(self.mean_service)

            for i in range(self.num_in_q):
                self.time_arrival[i] =self.time_arrival[i + 1]



    def update_time_avg_stats(self):
        time_since_last_event = self.sim_time - self.time_last_event
        
        self.area_num_in_q += (self.num_in_q * time_since_last_event)

        self.area_server_status += (self.server_status * time_since_last_event)
        self.time_last_event = self.sim_time


    def report(self): 
        with open("output.txt", 'w') as outfile:
            outfile.write(
                f"Single Server Queuing System\n\nMean interarrival time: {self.mean_interarrival}\nMean Service time: {self.mean_service}"
                f"\nNumber of Customers: {self.num_delays_required} ")
            outfile.write("\n\nAverage Delay in queue: {:.3f} minutes\n".format(self.total_of_delays/self.num_custs_delayed))
            outfile.write("Average number in queue: {:.3f}\n".format(self.area_num_in_q/self.sim_time))
            outfile.write("Server Utilization: {:.3f}\n ".format(self.area_server_status / self.sim_time) ) 
            outfile.write("Time Simulation Ended: {:.3f} minutes\n".format(self.sim_time))

    def main(self):
        self.num_events = 2

        with open ("input.txt", 'r') as infile:
            line = infile.read()
        
        listOfInputs = line.split()
        self.mean_interarrival = float(listOfInputs[0])
        self.mean_service = float(listOfInputs[1])
        self.num_delays_required = int(listOfInputs[2])

        
        with open ("output.txt", 'w')as outfile:
            outfile.write(
                "Single server queueing system"
                f"Mean interarrival time {self.mean_interarrival} minutes\n\n"
                f"Mean service time {self.mean_service} minutes"
                f"Number of customers {self.num_delays_required}"
            )

        # Initialize the simulation
        self.initialize()
        # Run the simulation while more delays are still needed
        while (self.num_custs_delayed < self.num_delays_required):
            # Determine the next event
            self.timing()
            # Update time-average statistical accumulators
            self.update_time_avg_stats()
            # Invoke the appropriate event function
            if self.next_event_type == 1:
                self.arrive()
            elif self.next_event_type == 2:
                self.depart()
        
        self.report()
print("Executing main function")
obj = SingleServer()
obj.main()
print("Finished testing main")
