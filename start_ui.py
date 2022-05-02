import json
import os
import subprocess
import sys
import numpy as np
import argparse
import pika
import redis
from activities.activity_factory import ActivityFactory
from data_logging.hdf5_point_logger import Hdf5PointLogger
from data_logging.logger import Logger
from data_logging.csv_point_logger import CSVPointLogger
from data_logging.video_logger import VideoLogger
from data_logging.zarr_point_logger import ZarrPointLogger
from ui.pygame.pygame_ui import PyGameUI
from ui.pyqtgraph.pyqtgraph_ui import PyQtGraph
from constants.constants import *

class TwoDimensionGame():
    """
    Creates a 2-dimensional user interface displaying the results
    of a pose detection algorithm. Allows users to interact with
    said user interface using detected points on their body.
    """

    NUM_LANDMARKS = 33

    def __init__(self, activity_name="game", hide_demo=True, record_points=False, 
                 record_zarr=False, record_hdf5=False, queue="redis", gui_name="pygame", activity_playback_csv=".", data_folder_name=""):

        # Array of the 33 mapped points
        self.body_point_array = np.zeros((self.NUM_LANDMARKS, 4))

        if not hide_demo:
            subprocess.Popen(['python', 'play_demo.py', activity_name])

        if data_folder_name == "":
            self.data_folder_name = self.activity_name
        else:
            self.data_folder_name = data_folder_name

        # Init loggers
        self.loggers: list[Logger] = []
        if record_points:
            self.loggers.append(CSVPointLogger(self.data_folder_name))
        if record_zarr:
            self.loggers.append(ZarrPointLogger(self.data_folder_name))
        if record_hdf5:
            self.loggers.append(Hdf5PointLogger(self.data_folder_name))

        if queue == "rabbitmq":
            connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
            self.channel = connection.channel()
            self.channel.queue_declare(queue=QUEUE_NAME, durable=False, auto_delete=True, arguments={'x-max-length' : 10})
            self.channel.queue_purge(queue=QUEUE_NAME)
            self.channel.basic_qos(prefetch_count=1)
        elif queue == "redis":
            r = redis.Redis(host='localhost', port=6379, db=0)
            self.channel = r.pubsub()
            self.channel.subscribe(QUEUE_NAME)
                        
        self.gui_name = gui_name
        self.activity_name = activity_name
        self.activity_playback_csv = activity_playback_csv
        self.queue = queue
        
    def start(self):
        """Initializes the game's user interface and starts processing data"""
        # Initialize graphs and labels for the user interface
        self.init_ui()

        # Start processing images
        self.process()

    def init_ui(self):
        """Starts the ui and chooses the correct activity
        to play based on the command line arguments given.
        Registers functional arguments and passes those to
        the relevant activity."""

        if self.gui_name == "pygame":
            self.gui = PyGameUI()
        elif self.gui_name == "pyqtgraph":
            self.gui = PyQtGraph(lambda: self.persistant[TIMER].tick())

        self.gui.new_gui()

        '''Dict of functions to be given to the activity. This is done this way
        in order to allow for control of things like logging to be handled by
        the activity being played rather than by this main file. Moreso, this
        reduces the amount of coupling between the logger and the activity.
        Instead of having the activity import the logger and therefore have
        it be dependant on it, the activity just runs whatever functions are
        given to it at the times specified in the activity. This allows for
        very specific activity classes (as intended) but very general logging
        classes.'''
        funcs = {
            START_LOGGING:    [logger.start_logging   for logger in self.loggers],
            STOP_LOGGING:     [logger.stop_logging    for logger in self.loggers],
            NEW_LOG:          [logger.new_log         for logger in self.loggers],
            CLOSE:            [logger.close           for logger in self.loggers]
        }

        af = ActivityFactory(self.activity_name)
        self.activity_name = af.new_activity(self.body_point_array, self.gui_name, funcs, self.activity_playback_csv)

        if self.activity_name == None:
            sys.exit(1)

        # Dict of components persistant in the ui (don't change between stages)
        # i.e. the clock and the point skeleton components
        self.persistant = self.activity_name.get_persist()

        # Adds all components to the ui
        for stage in self.activity_name.get_stages():
            for component in stage:
                self.gui.add_component(stage[component])
                stage[component].hide() # hides all components

        for component in self.persistant:
            self.gui.add_component(self.persistant[component])

        # Call change activity initially to render components
        self.activity_name.change_stage()

    def process(self):
        """
        Infinitely loads skeletons from the queue until the program is 
        exited (esc). Updates the skeleton, handles any kind of activity 
        (i.e. button clicking), and calls the log function.
        """
        while True:
            if self.queue == "rabbitmq":
                _, _, body = self.channel.basic_get(queue=QUEUE_NAME)
            elif self.queue == "redis":
                data = self.channel.get_message()
                if data is not None:
                    body = data["data"]

            if body is not None:
                try:
                    self.body_point_array = np.array(json.loads(body))
                except:
                    pass

            # If global coords were successfully found
            if self.body_point_array is not None:
                scaled_array = np.array(self.body_point_array)
                scaled_array[:,0] = scaled_array[:,0]*PIXEL_SCALE+PIXEL_X_OFFSET
                scaled_array[:,1] = scaled_array[:,1]*PIXEL_SCALE+PIXEL_Y_OFFSET
                scaled_array[:,2] = scaled_array[:,2]*PIXEL_SCALE+PIXEL_Z_OFFSET
                self.persistant[SKELETON].set_pos(scaled_array)
                # log data
                self.log_data()
            
            # Handles the activity's logic at the end of a frame
            self.activity_name.handle_frame(surface=self.gui.window)

            self.gui.update()
            self.gui.clear()
            self.persistant[TIMER].tick()


    def log_data(self):
        """Calls the log method on any instantiated loggers"""
        for logger in self.loggers:
            if isinstance(logger, CSVPointLogger) or isinstance(logger, ZarrPointLogger) or isinstance(logger, Hdf5PointLogger):
                logger.log(self.body_point_array)
            if isinstance(logger, VideoLogger):
                logger.log(self.image)
                
    def quit(self):
        self.gui.quit()

if __name__ == "__main__":
    
    """Parses the arguments given to the program"""
    parser = argparse.ArgumentParser(description='''
    Recieves skeleton data from a queue and generates a user interface for the
    skeleton data to interact with. Is meant to consume data generated by start_pose.py''')
    parser.add_argument("--record_points", action="store_true", help="Record point data")
    parser.add_argument("--record_zarr", action="store_true", help="Record zarr data")
    parser.add_argument("--record_hdf5", action="store_true", help="Record hdf5 data")
    parser.add_argument("--activity", nargs="?", const="game", default="game", help="Activity to be recorded, default is game")
    parser.add_argument("--file", nargs="?", const=".", default=".", help="Path to the file to be used as the activity")
    parser.add_argument("--hide_demo", action="store_true", help="Set to hide demo video")
    parser.add_argument("--gui", choices=["pygame", "pyqtgraph"], default="pygame", help="The user interface to use")
    parser.add_argument("--queue", choices=["rabbitmq", "redis"], default="redis", help="The type of queue to use to accept skeleton data.")
    args = parser.parse_args()
    
    td = TwoDimensionGame(activity_name=args.activity, hide_demo=args.hide_demo, record_points=args.record_points,
                          record_zarr=args.record_zarr, record_hdf5=args.record_hdf5, queue=args.queue, gui_name=args.gui, activity_playback_csv=args.file)
    try:
        td.start()
    except KeyboardInterrupt:
        print('Interrupted')
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)
