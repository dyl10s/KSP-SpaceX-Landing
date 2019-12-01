import krpc as ksp
import time

class Game:
    #Initialize out connection to the kRPC server and setup
    #some instance variables
    def __init__(self):
        self.conn = ksp.connect(address='127.0.0.1',rpc_port=5002, stream_port=5003)
        self.vessel = self.conn.space_center.active_vessel
        self.kerbin = self.conn.space_center.bodies['Kerbin']
        self.vessel.control.input_mode = self.vessel.control.input_mode.override
        self.StartRun()

    #Sets the pitch absolute value
    def Pitch(self, amount):
        self.vessel.control.pitch = amount

    #Sets the yaw absolute value
    def Yaw(self, amount):
        self.vessel.control.yaw = amount

    #Sets the roll absolute value
    def Roll(self, amount):
        self.vessel.control.roll = amount

    #Sets the throttle absolute value
    def Throttle(self, amount):
        self.vessel.control.throttle = amount

    #This loads the original save and launches the vessel to a set altitude
    #before making a new save and starting the main loop from that point
    def StartRun(self):

        self.playing = False
        
        #This save 'ailandersavelaunch' must exist for us to load
        #This save should just be the rocket flat on the launch pad
        self.conn.space_center.load('ailandersavelaunch')
        self.conn.space_center.physics_warp_factor = 3

        self.vessel.control.sas = True
        self.vessel.control.throttle = 1
        self.vessel.control.activate_next_stage()

        altitude = self.conn.add_stream(getattr, self.vessel.flight(self.kerbin.reference_frame), 'mean_altitude')
        
        #We pitch slightly so we land in an open area
        self.Pitch(.2)

        #This will wait till we are at a specific height before making the save point
        while altitude() < 1000:
            print('Launching')
        
        self.vessel.control.throttle = 0
        self.conn.space_center.save('ailandersave')
        self.FallRun()

    #This loads a save at a set altitude for quick training and testing
    def FallRun(self):
        
        #Load the save point made from the initial launch
        self.conn.space_center.load('ailandersave')

        self.playing = True
        self.vessel.control.throttle = 0
        self.conn.space_center.physics_warp_factor = 4

        #This will keep track of the original amount of parts on the vessel
        #if we do not equal that then we know there has been a crash
        self.partCount = len(self.vessel.parts.all)

        self.vessel.control.sas = False
        self.vessel.control.parachutes = True
        
    #This function lets us know if the ship has exploded or not
    def isDead(self):
        if(self.partCount != len(self.vessel.parts.all) and self.playing == True):
            return True
        return False

    #This will get the current state of the vessel
    #that we want to pass into the neural network
    def getState(self):
        results = [self.vessel.flight(self.kerbin.reference_frame).surface_altitude]
        return results 

    #This function is used to get the optimal velocity from a reference frame
    def getOptimalVelocity(self):
        curAlt = self.vessel.flight(self.kerbin.reference_frame).surface_altitude
        self.getOptimalVelocityFromHeight(curAlt)
        
    #This is the goal / fitness function of the neural network
    #The neural network will train to closely match this
    def getOptimalVelocityFromHeight(self, height):
        curAlt = height
        if(curAlt > 750):
            return 0
        elif(curAlt > 250):
            return .1
        elif(curAlt > 100):
            return .45
        elif(curAlt > 12):
            return .72
        else:
            return 0

    #Helper function to reset to the falling state
    def restart(self):
        self.FallRun()