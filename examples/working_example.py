import realtimepose as rtp

video_input = rtp.new_input(type=rtp.REALSENSE, fps=60)
gui = rtp.new_gui(frontend=rtp.PYGAME)

activity = rtp.new_activity(input=video_input, gui=gui, backend=rtp.BLAZEPOSE)
activity.add_logger(rtp.Logger(type=rtp.CSV_LOGGER))

scene_1 = rtp.new_scene()
scene_1.add_component(rtp.Button(x=0, y=0, size=10, color="red", callback=callback_func))

activity.add_scene(scene_1)

activity.run()

def callback_func():
    print("Hello world!")