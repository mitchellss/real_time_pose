# Real Time Pose

**This repo is no longer maintained. For the package that is under active development go to [`cvgui`](https://github.com/mitchellss/cvgui).**

RealTimePose is a library for prototyping novel methods of
user feedback by creating body-interactive GUIs using computer
vison.

**RealTimePose is a prototype. No guarantees can
be made about the stability of the API or the library itself.**

## Installation

> pip install .

Requires Python 3.9 or later

## Working Example

This example creates a simple activity with a skeleton and a button.
When clicked, the buttton moves. Example programs can be found in the
`bin/examples` directory.

```python
import realtimepose as rtp

# Specify input as a webcam and computer vision model as blazepose
frame_input: rtp.FrameInput = rtp.Webcam(device_num=0, fps=30)
cv_model: rtp.CVModel = rtp.BlazePose()

# Create a pose generator based on a webcam + blazepose
pose_input: rtp.PoseGenerator = rtp.ComputerVisionPose(
    frame_input=frame_input, model=cv_model)

# Specify GUI to be pygame
ui: rtp.UserInterface = rtp.PyGameUI(width=1920//2, height=1080//2, fps=60)

# Create activity
activity = rtp.Activity(pose_input=pose_input, frontend=ui)

# Create a new scene
scene_1 = rtp.Scene()
activity.add_scene(scene_1)

# Create a button that can be clicked by the user's left or right hand
button_1: rtp.Button = rtp.button(gui=ui,
                                  x_coord=1920//2, y_coord=1080//2,
                                  activation_distance=100)
button_1.set_targets([cv_model.LEFT_HAND, cv_model.RIGHT_HAND])

# Define what the button should do when clicked
def callback(button: rtp.Button):
    button.x_coord = 0
    button.y_coord = 0

# Tie the callback method to the newly created button
button_1.set_callback(callback=lambda: callback(button_1))

# Create a skeleton to map pose points to
skeleton: rtp.Skeleton = rtp.skeleton(gui=ui, x_coord=200, y_coord=200)

# Add the skeleton and button to the scene  
scene_1.add_component(button_1)
scene_1.add_component(skeleton)

# Start activity
activity.run()
```
