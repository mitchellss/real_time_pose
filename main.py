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

class Dialog(QDialog):
    """Dialog."""

    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent)
        self.setWindowTitle('Visual Feedback Wizard')
        self.setFixedWidth(500)
        self.dlgLayout = QVBoxLayout()
        formLayout = QFormLayout()
        
        queueDropdown = QComboBox()
        queueDropdown.addItems(["redis (recommended)", "rabbitmq"])
        formLayout.addRow('Message Queue:', queueDropdown)
        
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
        self.activityDropdown.addItems(["haptic_glove"])
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
        
        self.mp4_name_field = QLineEdit(f"{int(time.time())}.mp4")
        self.mp4_name_label = QLabel("Filename")
        formLayout.addRow(self.mp4_name_label, self.mp4_name_field)
        self.mp4_name_field.setHidden(True)
        self.mp4_name_label.setHidden(True)

        # Record csv data checkbox
        self.record_skeleton = QCheckBox("Record skeleton data (CSV)")
        self.record_skeleton.clicked.connect(self.click_record_skeleton_data)
        formLayout.addRow(self.record_skeleton)
        
        self.skeleton_csv_name_field = QLineEdit(f"{int(time.time())}.csv")
        self.skeleton_csv_name_label = QLabel("Filename")
        formLayout.addRow(self.skeleton_csv_name_label, self.skeleton_csv_name_field)
        self.skeleton_csv_name_field.setHidden(True)
        self.skeleton_csv_name_label.setHidden(True)
        
        # Record hdf5 data checkbox
        self.record_skeleton_hdf5 = QCheckBox("Record skeleton data (hdf5)")
        self.record_skeleton_hdf5.clicked.connect(self.click_record_skeleton_data_hdf5)
        formLayout.addRow(self.record_skeleton_hdf5)
        
        self.skeleton_hdf5_name_field = QLineEdit(f"{int(time.time())}.hdf5")
        self.skeleton_hdf5_name_label = QLabel("Filename")
        formLayout.addRow(self.skeleton_hdf5_name_label, self.skeleton_hdf5_name_field)
        self.skeleton_hdf5_name_field.setHidden(True)
        self.skeleton_hdf5_name_label.setHidden(True)
        
        # Hide video output checkbox
        self.hide_video = QCheckBox("Hide video output")
        self.hide_video.clicked.connect(self.click_hide_video_output)
        formLayout.addRow(self.hide_video)


        self.dlgLayout.addLayout(formLayout)
        btns = QDialogButtonBox()
        btns.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.dlgLayout.addWidget(btns)
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
    
    def click_record_video_data(self):
        if self.record_checkbox.isChecked():
            self.mp4_name_field.setHidden(False)
            self.mp4_name_label.setHidden(False)
        elif not self.record_checkbox.isChecked():
            self.mp4_name_field.setHidden(True)
            self.mp4_name_label.setHidden(True)
            
    def click_record_skeleton_data(self):
        if self.record_skeleton.isChecked():
            self.skeleton_csv_name_field.setHidden(False)
            self.skeleton_csv_name_label.setHidden(False)
        elif not self.record_skeleton.isChecked():
            self.skeleton_csv_name_field.setHidden(True)
            self.skeleton_csv_name_label.setHidden(True)
            
    def click_record_skeleton_data_hdf5(self):
        if self.record_skeleton_hdf5.isChecked():
            self.skeleton_hdf5_name_field.setHidden(False)
            self.skeleton_hdf5_name_label.setHidden(False)
        elif not self.record_skeleton_hdf5.isChecked():
            self.skeleton_hdf5_name_field.setHidden(True)
            self.skeleton_hdf5_name_label.setHidden(True)
            
    def click_hide_video_output(self):
        pass
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    dlg = Dialog()
    dlg.show()
    sys.exit(app.exec_())