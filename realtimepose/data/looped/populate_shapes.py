import math


file = open("shapes.csv", "w")

file.writelines("timestamp,x00,y00,x01,y01,x02,y02,x03,y03,x04,y04,x05,y05,x06,y06,x07,y07,x08,y08,x09,y09,x10,y10,x11,y11,x12,y12,x13,y13,x14,y14,x15,y15,x16,y16,x17,y17,x18,y18,x19,y19,x20,y20,x21,y21,x22,y22,x23,y23,x24,y24,x25,y25,x26,y26,x27,y27,x28,y28,x29,y29,x30,y30,x31,y31,x32,y32\n")

def get_triangle_pt(coords: tuple[int, int], width: int, height: int, speed: int, frame: int):
    a = (frame % (speed / 3))
    if frame % speed < speed / 3:
        starting_pt = (coords[0], (coords[1] - height / 2))
        return (starting_pt[0] + (a * ((width/2) / (speed / 3))), starting_pt[1] + (a) * height / (speed / 3))
    if frame % speed < speed * 2 / 3:
        starting_pt = (coords[0] + width / 2, (coords[1] + height / 2))
        return (starting_pt[0] - (a * width) / (speed / 3), starting_pt[1])
    if frame % speed < speed:
        starting_pt = (coords[0] - width / 2, (coords[1] + height / 2))
        return (starting_pt[0] + (a * width/2) / (speed / 3), starting_pt[1] - (a) * height / (speed / 3))

def get_rect_pt(coords: tuple[int, int], width: int, height: int, speed: int, frame: int):
    a = (frame % (speed / 4))
    if frame % speed < speed / 4:
        starting_pt = (coords[0] - width / 2, (coords[1] - height / 2))
        return (starting_pt[0] + (a * ((width) / (speed / 4))), starting_pt[1])
    if frame % speed < speed / 4 * 2:
        starting_pt = (coords[0] + width / 2, (coords[1] - height / 2))
        return (starting_pt[0], starting_pt[1] + (a) * height / (speed / 4))
    if frame % speed < speed / 4 * 3:
        starting_pt = (coords[0] + width / 2, (coords[1] + height / 2))
        return (starting_pt[0] - (a * ((width) / (speed / 4))), starting_pt[1])
    if frame % speed < speed:
        starting_pt = (coords[0] - width / 2, (coords[1] + height / 2))
        return (starting_pt[0], starting_pt[1] - (a) * height / (speed / 4))

def get_circle_pt(coords: tuple[int, int], radius: int, speed: int, frame: int):
    deg_per_frame = 360 / speed
    current_deg = (frame % speed) * deg_per_frame
    starting_pt = (coords[0], coords[1])
    return (starting_pt[0] + math.sin(math.radians(current_deg)) / 5, starting_pt[1] - math.cos(math.radians(current_deg)) / 5)


for i in range(0,300):
    x, y = get_triangle_pt((0,-0.6), 0.5, 0.5, 60, i)
    file.write("0.0,"*31 + f"{round(x,3)},{round(y,3)}," + "0.0," * 33 + "0.0\n")


for i in range(0,300):
    x, y = get_rect_pt((0,-0.6), 0.5, 0.5, 60, i)
    file.write("0.0,"*31 + f"{round(x,3)},{round(y,3)}," + "0.0," * 33 + "0.0\n")


for i in range(0,300):
    x, y = get_circle_pt((0,-0.6), 0.25, 60, i)
    file.write("0.0,"*31 + f"{round(x,3)},{round(y,3)}," + "0.0," * 33 + "0.0\n")

file.close()