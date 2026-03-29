# Prompts History

Automatically captured prompt log. Entries are appended in chronological order (oldest first).

### 29-03-2026 13:00
- **Prompt**: I'm attempting to make a simple pygame app with randomly moving rectangles. I created a dataclass to store game configuration. I have a subclass of pygame rectangle with custom direction properties and methods for updating them and moving them randomly. Next I have: #sym:init_window to create a game window, #sym:handle_events to check if user has quit the game, #sym:create_moving_rects to initialize n amount of MovingRect objects and #sym:update_screen to move and display them.  Could you take a look at it and provide me with stubs and hint to improve it? Don't think about expanding the functionality yet, let's just make this code work for now. Additionally, please add simplistic typing annotations to it

### 29-03-2026 13:15
- **Prompt**: I think there's must be an error in my thinking, because right now nothing is going on when I launch the game. Can you analyze the square moving logic (functions like #sym:random_move #sym:randomize_dir #sym:update_screen)? I'm confused if we should update the rect's coordinates and then update the screen or is calling rect.move_ip() method enough

