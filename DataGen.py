import time

from pynput.keyboard import Key, Listener

# Keys whose presses are not recorded as part of the password timing.
IGNORED_KEYS = {
    Key.backspace, Key.caps_lock, Key.shift, Key.shift_l, Key.shift_r,
    Key.up, Key.down, Key.right, Key.left, Key.enter,
}

samples = []
time_list = []


def on_press(key):
    if key in IGNORED_KEYS:
        return
    time_list.append(time.time())


password = input("Enter the password: ")

while True:
    answer = input("Do you want to train more? (y/n) ")
    if answer.strip().lower() == "n":
        break

    time_list = []
    # Record key-press timestamps while the user types the password into
    # input(), so the typed characters are consumed and don't leak into the
    # next prompt.
    with Listener(on_press=on_press):
        attempt = input("Type the password and press ENTER: ")

    if attempt != password or len(time_list) != len(password):
        print("Mistyped, sample discarded.")
        continue

    samples.append(tuple(time_list))
    print(samples)
