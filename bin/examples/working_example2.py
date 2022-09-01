import realtimepose2 as rtp

def callback_func():
    print("Hello world!")

# Specify input
webcam: rtp.FrameInput = rtp.Webcam()
blazepose: rtp.CVModel = rtp.BlazePose()
webcam_pose: rtp.PoseGenerator = rtp.ComputerVisionPose()

# Specify GUI
pygame: rtp.UserInterface = rtp.PyGame()

# Create activity
activity = rtp.Activity(input=webcam_pose, frontend=pygame)

# Add scene to activity
scene_1 = rtp.Scene()
# scene_1.add_component(rtp.Button(x=0, y=0, size=10, color="red", callback=callback_func))
activity.add_scene(scene_1)

# Start
activity.run()
