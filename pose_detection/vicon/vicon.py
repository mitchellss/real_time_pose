
import asyncio
import qtm
from pose_detection.pose_detection import PoseDetection

# 192.168.1.199
# 22223

class Vicon(PoseDetection):

    def __init__(self, queue) -> None:
        asyncio.ensure_future(self.setup())
        super().__init__(queue)
        
    def add_pose_to_queue(self) -> bool:

        return super().add_pose_to_queue()
    

    def on_packet(self, packet):
        """ Callback function that is called everytime a data packet arrives from QTM """
        print("Framenumber: {}".format(packet.framenumber))
        header, markers = packet.get_3d_markers()
        print("Component info: {}".format(header))
        for marker in markers:
            print("\t", marker)


    async def setup(self, ):
        """ Main function """
        connection = await qtm.connect("127.0.0.1")
        if connection is None:
            return

        await connection.stream_frames(components=["3d"], on_packet=on_packet)