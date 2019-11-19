import krpc as ksp

class Game:
    def __init__(self):
        self.conn = ksp.connect(address='127.0.0.1',rpc_port=5002, stream_port=5003)
        self.vessel = self.conn.space_center.active_vessel
        self.StartRun()

    def Pitch(self, amount):
        self.vessel.control.pitch += amount

    def Yaw(self, amount):
        self.vessel.control.yaw += amount

    def Roll(self, amount):
        self.vessel.control.roll += amount

    def Throttle(self, amount):
        self.vessel.control.throttle += amount

    def StartRun(self):
        self.playing = False
        self.conn.space_center.load('ailandersavelaunch')
        self.conn.space_center.physics_warp_factor = 3

        self.vessel.control.sas = True
        self.vessel.control.throttle = 1
        self.vessel.control.activate_next_stage()

        altitude = self.conn.add_stream(getattr, self.vessel.flight(), 'mean_altitude')

        while altitude() < 1000:
            print('Launching')
        
        self.vessel.control.throttle = 0
        self.conn.space_center.save('ailandersave')
        self.FallRun()

    def FallRun(self):
        self.conn.space_center.load('ailandersave')
        self.playing = True
        self.vessel.control.throttle = 0
        self.conn.space_center.physics_warp_factor = 3
        self.partCount = len(self.vessel.parts.all)

        self.vessel.control.sas = False
        

    def isDead(self):
        if(self.partCount != len(self.vessel.parts.all) and self.playing == True):
            return True
        return False

    def isPlaying(self):
        if not self.isDead():
            return self.playing

    def getState(self):
        results = self.vessel.flight().direction + (self.vessel.flight().elevation,)
        return results 

    def getScore(self):
        score = self.vessel.flight().direction[0] #higher the better
        score += self.vessel.flight().direction[1] - 1 #lower is better
        score += self.vessel.flight().direction[1] - 1 #lower is better
        return score

    def restart(self):
        self.FallRun()