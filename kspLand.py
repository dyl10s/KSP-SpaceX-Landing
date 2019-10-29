import krpc
conn = krpc.connect(
    address='127.0.0.1',
    rpc_port=5002, stream_port=5003)

while True:
    vessel = conn.space_center.active_vessel
    conn.space_center.physics_warp_factor = 3
    conn.space_center.save('ailandersavelaunch')

    partCount = len(vessel.parts.all)

    conn.space_center.physics_warp_factor = 3
    altitude = conn.add_stream(getattr, vessel.flight(), 'mean_altitude')
    situation = conn.add_stream(getattr, vessel, 'situation')
    ref_frame = vessel.orbit.body.reference_frame
    speed = conn.add_stream(getattr, vessel.flight(ref_frame), 'speed')

    vessel.control.sas = True
    vessel.control.throttle = 1
    vessel.control.activate_next_stage()

    while altitude() < 1000:
        print('Launching')

    vessel.control.sas = False
    vessel.control.throttle = 0

    while partCount == len(vessel.parts.all):
        print('AI Land')

    print('Crashed Restarting')
    conn.space_center.load('ailandersave')
