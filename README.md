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



```