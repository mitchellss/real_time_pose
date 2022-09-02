# Real Time Pose

Real Time Pose is a library created by the wearable computing research
group, headed and advised by Dr. Jason Forsyth. The purpose of the 
library is to enable users to create body-interactive GUIs through
the use of computer vision. 

## Installation

> pip install realtimepose

Requires Python 3.9 or later

## Working Example

```python
import realtimepose as rtp

# Specify input
webcam: rtp.FrameInput = rtp.Webcam()
blazepose: rtp.CVModel = rtp.BlazePose()
webcam_pose: rtp.PoseGenerator = rtp.ComputerVisionPose(frame_input=webcam, model=blazepose)

# Specify GUI
ui: rtp.UserInterface = rtp.PyGameUI()

# Create activity
activity = rtp.Activity(pose_input=webcam_pose, frontend=ui)

# Create new scene
scene_1 = rtp.Scene()
scene_1.add_component(button(gui=ui, x_coord=0.0, y_coord=0.0))

# Add scene to activity
activity.add_scene(scene_1)

# Start
activity.run()
```