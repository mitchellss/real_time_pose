import pyrealsense2 as rs
import numpy as np

from frame_input.frame_input import FrameInput

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
            self.width = 960
            self.height = 540
        else:
            config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
            self.width = 640
            self.height = 480

        # Start streaming
        self.pipeline.start(config)

    def get_video_frame(self) -> np.ndarray:
        # Wait for a coherent pair of frames: depth and color
        frames = self.pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()
        if not depth_frame or not color_frame:
            return None

        # Convert images to numpy arrays
        # depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())
        return color_image

    def get_frame_height(self) -> int:
        return self.height

    def get_frame_width(self) -> int:
        return self.width
    
    def close(self):
        # TODO: implement realsense close method
        print("UNIMPLEMENTED")
        pass
