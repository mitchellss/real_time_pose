import realtimepose2 as rtp
from realtimepose2.core.displaying.components import button

def callback_func():
    print("Hello world!")

# Specify input
webcam: rtp.FrameInput = rtp.Webcam()
blazepose: rtp.CVModel = rtp.BlazePose()
webcam_pose: rtp.PoseGenerator = rtp.ComputerVisionPose(frame_input=webcam, model=blazepose)

# Specify GUI
ui: rtp.UserInterface = rtp.PyGame()
# ui: rtp.UserInterface = rtp.Pyglet()

# Create activity
activity = rtp.Activity(input=webcam_pose, frontend=ui)

# Add scene to activity
scene_1 = rtp.Scene()

button_1: rtp.Button = button(ui=ui, x=0.0, y=0.0)

scene_1.add_component(button_1)

# print(button_1.is_clicked(0, 0, 5))
print(button_1.render())

activity.add_scene(scene_1)

# Start
activity.run()
