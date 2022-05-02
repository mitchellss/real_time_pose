"""Dialog-Style application."""
import pathlib
import sys
import time
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QDialogButtonBox
from PyQt5.QtWidgets import QFormLayout
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QVBoxLayout, QComboBox, QLabel, QFileDialog, QPushButton, QCheckBox
import os
import multiprocessing as mp


class Dialog(QDialog):
    """Dialog."""

    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent)
        self.setWindowTitle('Visual Feedback Wizard')
        self.setFixedWidth(500)
        self.dlgLayout = QVBoxLayout()
        formLayout = QFormLayout()
        
        self.filepath = ""
        self.pose_service = None
        self.p = None
        self.td = None
        
        self.queueDropdown = QComboBox()
        self.queueDropdown.addItems(["redis", "rabbitmq"])
        formLayout.addRow('Message Queue:', self.queueDropdown)
        
        self.inputDropdown = QComboBox()
        self.inputDropdown.addItems(["video", "vicon"])
        self.inputDropdown.currentIndexChanged.connect(self.input_selection_changed)
        self.inputLabel = QLabel('Input:', parent=self.inputDropdown)
        formLayout.addRow(self.inputLabel, self.inputDropdown)
        
        self.videoSourceDropdown = QComboBox(parent=self.inputDropdown)
        self.videoSourceDropdown.addItems(["file", "webcam", "realsense"])
        self.videoSourceDropdown.currentIndexChanged.connect(self.input_selection_changed2)
        self.videoSourceLabel = QLabel('Video Source:', parent=self.videoSourceDropdown)
        formLayout.addRow(self.videoSourceLabel, self.videoSourceDropdown)
        
        self.filePushButton = QPushButton("Choose a file")
        self.fileLabel = QLabel("Video Source File:")
        self.filePushButton.clicked.connect(self.click_file_browser)
        formLayout.addRow(self.fileLabel, self.filePushButton)
        
        # Choose activity dropdown
        self.activityDropdown = QComboBox(parent=self.inputDropdown)
        self.activityDropdown.addItems(["game", "record_data", "vector_haptic", "vector_haptic_acc"])
        self.activityDropdown.currentIndexChanged.connect(self.input_selection_changed3)
        self.activityLabel = QLabel('Activity:', parent=self.activityDropdown)
        self.activityDescLabel = QLabel('Description:', parent=self.activityDropdown)
        self.activityDesc = QLabel('Connect to haptic glove and move hand to randomly appearing points.', parent=self.activityDropdown)
        formLayout.addRow(self.activityLabel, self.activityDropdown)
        formLayout.addRow(self.activityDescLabel, self.activityDesc)
        
        # Record video data checkbox
        self.record_checkbox = QCheckBox("Record video data")
        self.record_checkbox.clicked.connect(self.click_record_video_data)
        formLayout.addRow(self.record_checkbox)
        
        # self.mp4_name_field = QLineEdit(f"{int(time.time())}.mp4")
        # self.mp4_name_label = QLabel("Filename")
        # formLayout.addRow(self.mp4_name_label, self.mp4_name_field)
        # self.mp4_name_field.setHidden(True)
        # self.mp4_name_label.setHidden(True)

        # Record csv data checkbox
        self.record_skeleton = QCheckBox("Record skeleton data (CSV)")
        self.record_skeleton.clicked.connect(self.click_record_skeleton_data)
        formLayout.addRow(self.record_skeleton)
        
        # self.skeleton_csv_name_field = QLineEdit(f"{int(time.time())}.csv")
        # self.skeleton_csv_name_label = QLabel("Filename")
        # formLayout.addRow(self.skeleton_csv_name_label, self.skeleton_csv_name_field)
        # self.skeleton_csv_name_field.setHidden(True)
        # self.skeleton_csv_name_label.setHidden(True)
        
        # Record hdf5 data checkbox
        self.record_skeleton_hdf5 = QCheckBox("Record skeleton data (hdf5)")
        self.record_skeleton_hdf5.clicked.connect(self.click_record_skeleton_data_hdf5)
        formLayout.addRow(self.record_skeleton_hdf5)
        
        self.data_folder_name_field = QLineEdit(f"{int(time.time())}")
        self.data_folder_name_label = QLabel("Data Folder Name")
        formLayout.addRow(self.data_folder_name_label, self.data_folder_name_field)
        self.data_folder_name_field.setHidden(True)
        self.data_folder_name_label.setHidden(True)
        
        # Hide video output checkbox
        self.hide_video = QCheckBox("Hide video output")
        self.hide_video.clicked.connect(self.click_hide_video_output)
        formLayout.addRow(self.hide_video)


        self.dlgLayout.addLayout(formLayout)
        btns = QDialogButtonBox()
        btns.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.dlgLayout.addWidget(btns)
        
        btns.accepted.connect(self.click_ok_button)
        btns.rejected.connect(self.click_cancel_button)
        
        self.setLayout(self.dlgLayout)
        
    def input_selection_changed(self):
        if self.inputDropdown.currentText() == "video":
            self.videoSourceDropdown.setHidden(False)
            self.videoSourceLabel.setHidden(False)
            if self.videoSourceDropdown.currentText() == "file":
                self.filePushButton.setHidden(False)
                self.fileLabel.setHidden(False)

        elif self.inputDropdown.currentText() == "vicon":
            self.videoSourceDropdown.setHidden(True)
            self.videoSourceLabel.setHidden(True)
            self.filePushButton.setHidden(True)
            self.fileLabel.setHidden(True)
            
    def input_selection_changed2(self):
        if self.videoSourceDropdown.currentText() == "file":
            self.filePushButton.setHidden(False)
            self.fileLabel.setHidden(False)
        elif self.videoSourceDropdown.currentText() == "realsense":
            self.filePushButton.setHidden(True)
            self.fileLabel.setHidden(True)
        elif self.videoSourceDropdown.currentText() == "webcam":
            self.filePushButton.setHidden(True)
            self.fileLabel.setHidden(True)
            
    def input_selection_changed3(self):
        if self.videoSourceDropdown.currentText() == "file":
            self.filePushButton.setHidden(False)
            self.fileLabel.setHidden(False)
        elif self.videoSourceDropdown.currentText() == "realsense":
            self.filePushButton.setHidden(True)
            self.fileLabel.setHidden(True)
        elif self.videoSourceDropdown.currentText() == "webcam":
            self.filePushButton.setHidden(True)
            self.fileLabel.setHidden(True)
        
    def click_file_browser(self):
        path = QFileDialog.getOpenFileName(self, 'Open a file', '', 'All Files (*.*)')
        if path != ('', ''):
            self.filePushButton.setText(pathlib.Path(path[0]).name)
            self.filepath = pathlib.Path(path[0])
    
    def click_record_video_data(self):
        if self.record_checkbox.isChecked():
            self.data_folder_name_field.setHidden(False)
            self.data_folder_name_label.setHidden(False)
        elif not self.record_checkbox.isChecked() \
            and not self.record_skeleton.isChecked() \
                and not self.record_skeleton_hdf5.isChecked():
            self.data_folder_name_field.setHidden(True)
            self.data_folder_name_label.setHidden(True)
            
    def click_record_skeleton_data(self):
        if self.record_skeleton.isChecked():
            self.data_folder_name_field.setHidden(False)
            self.data_folder_name_label.setHidden(False)
        elif not self.record_checkbox.isChecked() \
            and not self.record_skeleton.isChecked() \
                and not self.record_skeleton_hdf5.isChecked():
            self.data_folder_name_field.setHidden(True)
            self.data_folder_name_label.setHidden(True)
            
    def click_record_skeleton_data_hdf5(self):
        if self.record_skeleton_hdf5.isChecked():
            self.data_folder_name_field.setHidden(False)
            self.data_folder_name_label.setHidden(False)
        elif not self.record_checkbox.isChecked() \
            and not self.record_skeleton.isChecked() \
                and not self.record_skeleton_hdf5.isChecked():
            self.data_folder_name_field.setHidden(True)
            self.data_folder_name_label.setHidden(True)
            
    def click_hide_video_output(self):
        pass
    
    def click_cancel_button(self):
        if self.pose_service != None:
            if self.pose_service.video_logger != None:
                print("Stop video logger")
                self.pose_service.video_logger.stop_logging()
                self.pose_service.video_logger.close()
            self.pose_service.stop()
        if self.p != None:
            self.p.terminate()
            
    def start_ui(self, **kwargs):
        from interface_service import InterfaceService
        self.td = InterfaceService(**kwargs)
        self.td.start()
        
    def click_ok_button(self):
        from pose_service import PoseService
        queue = self.queueDropdown.currentText()
        input = self.inputDropdown.currentText()
        record_video = self.record_checkbox.isChecked()
        hide_video = self.hide_video.isChecked()
        if input == "video":
            video_source = self.videoSourceDropdown.currentText()
            if video_source == "file":
                path = self.filepath
                self.pose_service = PoseService(input=input, record_video=record_video, 
                                                hide_video=hide_video, queue=queue, 
                                                video_input=video_source, path=path)
            else:
                self.pose_service = PoseService(input=input, record_video=record_video, 
                                                hide_video=hide_video, queue=queue, 
                                                video_input=video_source)
            
        elif input == "vicon":
            self.pose_service = PoseService(input=input, record_video=record_video, 
                                            hide_video=hide_video, queue=queue)
        
        kwargs = {
            "activity_name": self.activityDropdown.currentText(),
            "queue": self.queueDropdown.currentText(),
            "record_points": self.record_skeleton.isChecked(),
            "record_hdf5": self.record_skeleton_hdf5.isChecked(),
            "data_folder_name": self.data_folder_name_field.text()
            }
        self.p = mp.Process(target=self.start_ui, kwargs=kwargs)
        self.p.start()
        
        try:
            self.pose_service.start()
        except KeyboardInterrupt:
            print('Interrupted')
            if self.pose_service.video_logger != None:
                print("Stop video logger")
                self.pose_service.video_logger.stop_logging()
                self.pose_service.video_logger.close()
            
            if self.p != None:
                self.p.terminate()
        # try:
        #     sys.exit(0)
        # except SystemExit:
        #     os._exit(0)
        
    def closeEvent(self, event):
        if self.pose_service != None:
            if self.pose_service.video_logger != None:
                print("Stop video logger")
                self.pose_service.video_logger.stop_logging()
                self.pose_service.video_logger.close()
            self.pose_service.stop()
        if self.p != None:
            self.p.terminate()
        
        event.accept()
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    dlg = Dialog()
    dlg.show()
    sys.exit(app.exec_())