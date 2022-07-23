from kivy.uix.label import Label
import serial


def change_servo_position(device: serial, label: Label, servo_number: int, operation: str) -> None:
    current_value = 0
    if operation == "+":
        current_value = increment(label)
    elif operation == "-":
        current_value = decrement(label)
    move_servo(device, servo_number, current_value)


def increment(label: Label) -> int:
    current_value = label.text
    if int(current_value) >= 180:
        return 180
    new_value = int(current_value) + 20
    label.text = str(new_value)
    label.texture_update()
    return new_value


def decrement(label: Label) -> int:
    current_value = label.text
    if current_value == "0":
        return 0
    new_value = int(current_value) - 20
    label.text = str(new_value)
    label.texture_update()
    return new_value


def send_data(device: serial, line: str) -> None:
    line += "\r\n"
    device.write(line.encode())


def move_servo_old(device: serial, servo_number: int, new_value: int) -> None:
    send_data(device, f"s{servo_number}{new_value}")
    print(f"s{servo_number}{new_value}")


def move_servo(device: serial, servo_number: int, current_value: int, new_value: int):
    if current_value == new_value:
        return
    print(f"Moving servo {servo_number}")
    send_data(device, f"s{servo_number}{new_value}")
    print(f"s{servo_number}{new_value}")
    return 1
