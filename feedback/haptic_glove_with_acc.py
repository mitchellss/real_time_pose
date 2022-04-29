
import math
import socket
import numpy as np
from feedback.feedback_device import FeedbackDevice


class HapticGloveAcc(FeedbackDevice):

    MOTORS = np.array([np.array([0.0,0.0,1.0]), np.array([0.0,0.0,-1.0]), np.array([0.0,-1.0,0.0]), np.array([0.0,1.0,0.0])]) #array of motor positions
    MOTORS_UD = np.array([np.array([0.0,0.0,-1.0]), np.array([0.0,0.0,1.0]), np.array([0.0,1.0,0.0]), np.array([0.0,-1.0,0.0])])
    MOTORS_R = np.array([np.array([0.0,-1.0,0.0]), np.array([0.0,1.0,0.0]), np.array([0.0,0.0,-1.0]), np.array([0.0,0.0,1.0])])
    MOTORS_L = np.array([np.array([0.0,1.0,0.0]), np.array([0.0,-1.0,0.0]), np.array([0.0,0.0,1.0]), np.array([0.0,0.0,-1.0])])
    CURRENT_MOTORS = MOTORS

    TIMEOUT = 10 # seconds
    MINIMUM_INTENSITY_MESSAGE = "/150/150/150/150"

    def __init__(self, tcp_ip: str, tcp_port: int, direction: str = "pull") -> None:
        super().__init__()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(self.TIMEOUT)
        self.tcp_ip = tcp_ip
        self.tcp_port = tcp_port
        self.direction = direction
        self.accel_data = np.array([1.0,1.0,1.0])      
        self.accel_norm = np.array([1.0,1.0,1.0])      
        #self.accel_mapped = np.array([0,0,0])
          
    
    def connect(self) -> None:
        self.socket.connect((self.tcp_ip, self.tcp_port))
        self.socket.settimeout(None)

    def disconnect(self) -> None:
        self.socket.close()
    
    def send_push_feedback(self, message: np.array) -> None:
        for _ in range(0,10):
            self.socket.send(f'{message}\n'.encode('ascii'))

    def send_pull_feedback(self, current_pt: np.array, goal_pt: np.array):
        self.get_acceleration()
        
        if (self.accel_norm[1] > 0.7):
            self.CURRENT_MOTORS = self.MOTORS
        elif (self.accel_norm[1] < -0.7):
            self.CURRENT_MOTORS = self.MOTORS_UD
        elif (self.accel_norm[0] > 0.7 ):
            self.CURRENT_MOTORS = self.MOTORS_L
        elif (self.accel_norm[0] < -0.7 ):
            self.CURRENT_MOTORS = self.MOTORS_R
        goal = goal_pt# - self.accel_data
        intensity = self.find_intensity_array(current_pt, goal, self.CURRENT_MOTORS, norm=True)

        # print(goal, intensity)
        message = self.make_message(intensity)

        for _ in range(0,2):
            self.socket.send(message.encode('ascii'))
    
    def stop_feedback(self) -> None:
        for _ in range(0,10):
            self.socket.send(f'{self.MINIMUM_INTENSITY_MESSAGE}\n'.encode('ascii'))

    def make_message(self, vect) -> str:
        return f'/{vect[1]}/{vect[0]}/{vect[2]}/{vect[3]}\n'

    def find_distance(self, vector1, vector2, normalized=False):
        if normalized:
            vector1 = vector1 / np.linalg.norm(vector1)
            vector2 = vector2 / np.linalg.norm(vector2)
        diff = vector1 - vector2
        distance = np.linalg.norm(diff)
        return distance

    def map_to_range(self, x, in_min, in_max, out_min, out_max, bounded=False):
        output = (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
        if bounded:
            if output < out_min:
                output = out_min
            if output > out_max:
                output = out_max
        return output

    def reverse_map_to_range(self, x, in_min, in_max, out_min, out_max, bounded=False):
        output = (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
        if bounded:
            if output > out_min:
                output = out_min
            if output < out_max:
                output = out_max
        return output

    def find_intensity_array(self, current_pos, goal_pos, motor_positions, norm=True) -> np.array:
        
        if norm:
            if ( np.linalg.norm(current_pos) != 0):
                current_pos = current_pos / np.linalg.norm(current_pos)
            if ( np.linalg.norm(goal_pos) != 0):
                goal_pos = goal_pos / np.linalg.norm(goal_pos)
        
        U = goal_pos - current_pos
        #print(f'Displacement vector: {U}')

        D = np.linalg.norm(U)
        #print(f'Distance from goal: {D}')

        I = self.map_to_range(D, 0, 0.6, 150, 255,  bounded=True)
        #print(f'Distance adjusted to range: {I}')

        motor_distance = [0.0,0.0,0.0,0.0]
        mapped = [0.0,0.0,0.0,0.0]

        for i in range(0, len(motor_positions)):
            motor_distance[i] = self.find_distance(U, motor_positions[i], normalized=True)
            mapped[i] = self.reverse_map_to_range(motor_distance[i], 0.0, math.sqrt(2), 1, .59, bounded=True)

        mapped = np.array(mapped)

        #print(f'Motor distances : {motor_distance}')
        #print(f'Motor intensity proportions: {mapped}')

        intensity = np.array(I * mapped).astype(int)
        #print(f'Motor intensity array: {intensity}')
        return intensity
    
    def get_acceleration(self):
        self.socket.send('accel\n'.encode('ascii'))
        msg = self.socket.recv(4096).decode("ascii").split('\r')[0].split('\n')[0]
        try: 
            msg_split = msg.split(',')
            msg_split = np.array(msg_split)
            msg_split = msg_split.astype(float)
            self.accel_data = msg_split
            self.accel_norm = self.accel_data / np.linalg.norm(self.accel_data)
            self.accel_norm[0] = round(self.accel_norm[0],2)
            self.accel_norm[1] = round(self.accel_norm[1],2)
            self.accel_norm[2] = round(self.accel_norm[2],2)                    
            print(self.accel_norm)
        except:
            None

if __name__ == "__main__":
    glove = HapticGloveAcc("172.16.1.4", 8888)
    glove.connect()