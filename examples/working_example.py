import realtimepose as rtp

def callback_func():
    print("Hello world!")

# Specify input
webcam: rtp.FrameInput = rtp.WebcamInput(type=rtp.WEBCAM, fps=60)
blazepose: rtp.CVModel = rtp.BlazePose()
webcam_pose: rtp.PoseGenerator = rtp.ComputerVisonPose(input=webcam, model=blazepose)

# Specify GUI
pygame: rtp.GUI = rtp.PyGame()

# Create activity
activity = rtp.Activity(input=webcam_pose, frontend=pygame)

# Attach logger to activity
activity.add_logger(rtp.CSVPointLogger("logger.csv"))

# Add scene to activity
scene_1 = rtp.Scene()
scene_1.add_component(rtp.Button(x=0, y=0, size=10, color="red", callback=callback_func))
activity.add_scene(scene_1)

# Start
activity.run()
