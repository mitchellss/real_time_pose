from frame_input.frame_input import FrameInput
import pyrealsense2 as rs
import numpy as np

class Realsense(FrameInput):
    """FrameInput implementation representing an intel realsense camera"""

    def __init__(self) -> None:
        # Configure depth and color streams 
        self.pipeline = rs.pipeline()
        config = rs.config()

        # Get device product line for setting a supporting resolution
        pipeline_wrapper = rs.pipeline_wrapper(self.pipeline)
        pipeline_profile = config.resolve(pipeline_wrapper)
        device = pipeline_profile.get_device()
        device_product_line = str(device.get_info(rs.camera_info.product_line))

        # Tries to find the rgb camera
        found_rgb = False
        for s in device.sensors:
            if s.get_info(rs.camera_info.name) == 'RGB Camera':
                found_rgb = True
                break
        if not found_rgb:
            print("The demo requires Depth camera with Color sensor")
            exit(0)

        config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

        if device_product_line == 'L500':
            config.enable_stream(rs.stream.color, 960, 540, rs.format.bgr8, 30)
        else:
            config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
        # Start streaming
        pipe_profile = self.pipeline.start(config)

        depth_sensor = pipe_profile.get_device().first_depth_sensor()

        # preset_range = depth_sensor.get_option_range(rs.option.visual_preset)
        # for i in range(int(preset_range.max)):
        #     visulpreset = depth_sensor.get_option_value_description(rs.option.visual_preset,i)
        #     print('%02d: %s'%(i,visulpreset))
        '''
        00: Custom
        01: Default
        02: Hand
        03: High Accuracy
        04: High Density
        '''

        depth_sensor.set_option(rs.option.visual_preset, 3)

        self.depth_image = None

        align_to = rs.stream.color
        self.align = rs.align(align_to)

    def get_frame(self) -> np.ndarray:
        # Wait for a coherent pair of frames: depth and color
        frames = self.pipeline.wait_for_frames()
        aligned_frames = self.align.process(frames)

        self.depth_frame = aligned_frames.get_depth_frame()
        color_frame = aligned_frames.get_color_frame()
        if not self.depth_frame or not color_frame:
            return None
        
        # print(depth_frame.get_distance(depth_frame.width//2,depth_frame.height//2), end="\r")

        colorizer = rs.colorizer()
        self.depth_image = np.asanyarray(colorizer.colorize(self.depth_frame).get_data())

        # Convert images to numpy arrays
        # self.depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())
        return color_image

    def get_frame_height(self) -> int:
        # TODO
        return super().get_frame_height()

    def get_frame_width(self) -> int:
        # TODO
        return super().get_frame_width()

    def get_depth_image(self) -> np.ndarray:
        return self.depth_image

    def get_distance(self, x: int, y: int) -> float:
        return self.depth_frame.get_distance(x, y)
