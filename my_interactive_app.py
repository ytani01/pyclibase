
import sys

menu_items = ["Menu Item 1", "Menu Item 2", "Menu Item 3"]
selected_item = 0

def print_menu():
    for i, item in enumerate(menu_items):
        if i == selected_item:
            sys.stdout.write('> {}\n'.format(item))
        else:
            sys.stdout.write('  {}\n'.format(item))
    sys.stdout.flush()

print_menu()

while True:
    key = sys.stdin.read(1)
    if key == '\x1b':  # ANSI escape sequence
        key += sys.stdin.read(2)

    if key == '\n':  # Enter key
        sys.stdout.write('You selected {}\n'.format(menu_items[selected_item]))
        sys.stdout.flush()
        break
    elif key == '\x1b[A':  # Up arrow
        selected_item = (selected_item - 1) % len(menu_items)
    elif key == '\x1b[B':  # Down arrow
        selected_item = (selected_item + 1) % len(menu_items)

    # Clear previous menu and print new one
    sys.stdout.write('\033[F' * (len(menu_items) + 1)) # Move cursor up
    sys.stdout.write('\033[J') # Clear from cursor to end of screen
    print_menu()
