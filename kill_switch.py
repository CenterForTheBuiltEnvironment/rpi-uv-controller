from gpiozero import Button
button = Button(2)

if __name__ == '__main__':

    button.wait_for_press()
    print('You pushed me')