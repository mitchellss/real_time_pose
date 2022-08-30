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

video_input = rtp.new_input()
gui = rtp.new_gui()

activity = rtp.new_activity(input=video_input, gui=gui, backend=rtp.BLAZEPOSE)

scene_1 = rtp.new_scene()
scene_1.add_component(rtp.Button(x=0, y=0, size=10, color="red", callback=callback_func))

activity.run()

def callback_func() {
    print("Hello world!")
}
```