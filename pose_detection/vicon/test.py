"""
    Minimal usage example
    Connects to QTM and streams 3D data forever
    (start QTM first, load file, Play->Play with Real-Time output)
"""

import asyncio
import sys
import qtm

# https://qualisys.github.io/qualisys_python_sdk/index.html


def on_packet(packet):
    """ Callback function that is called everytime a data packet arrives from QTM """
    print("Framenumber: {}".format(packet.framenumber))
    header, markers = packet.get_3d_markers_no_label()
    # type(packet.get_6d())
    # print("Component info: {}".format(header))
    for marker in markers:
        print("\t", marker)    


async def setup():
    """ Main function """
    connection = await qtm.connect(host="192.168.1.199", port="22223", version="1.22")
    if connection is None:
        return

    await connection.stream_frames(components=["3d"], on_packet=on_packet)


if __name__ == "__main__":
    asyncio.ensure_future(setup())
    asyncio.get_event_loop().run_forever()
