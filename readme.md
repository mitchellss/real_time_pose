# Real Time Pose

Real Time Pose is a tool created by the wearable computing research group. Headed and advised by Dr. Jason Forsyth. The purpose of the tool is to provide a modular video feedback mechanism that can take a variety of input, process that input with a pose detection model, display the results of the model, and allow researchers to manipulate the displayed results for the purposes of feedback and direction.

### Example Usage:
> `python main.py --help`

> `python main.py webcam --activity game`

> `python main.py video --video_file ./activities/jumping_jacks/demo.mp4 --activity game_mk2 --file ./data/looped/jumping_jacks.csv --hide_demo --hide_video`

### Currently Working Activities:
* **game** - Two floating buttons that move around randomly.
* **game_mk2** - Actively moving buttons make user replicate dynamic motion. Complete with score tracking and name entering. (requires --file to define motion)
* **bread_crumb** - Buttons that move from one spot to another to guide a user into a defined motion. (requires --file to define motion)
* **haptic** - A single button moving around when clicked. Connects to the haptic golf glove to deliver feedback based on the button direction.
* **shapes** - Six triangles followed by six rectangles followed by six circles

## Project Layout
The project is laid out in seperate modules in an attempt to achieve the lowest amount of [coupling](https://en.wikipedia.org/wiki/Coupling_%28computer_programming%29) possible. Allowing frame inputs, pose detection algorithms, and frontends to be swapped seamlessly. This design choice was made in an effort to future-proof the tool in the event that new algorithms or approaches are released.

A basic flow of data can be seen below. 

![Basic layout of the real time pose project.](https://i.imgur.com/BrLD8xj.png)

### Modules

The following are main modules that comprise the project. Each can be found in a seperate folder in the project.

* frame_input
* pose_detection
* ui
* data_logging
* activities
* utils
* constants