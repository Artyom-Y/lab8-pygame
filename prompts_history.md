# Prompts History

Automatically captured prompt log. Entries are appended in chronological order (oldest first).

### 29-03-2026 13:00
- **Prompt**: I'm attempting to make a simple pygame app with randomly moving rectangles. I created a dataclass to store game configuration. I have a subclass of pygame rectangle with custom direction properties and methods for updating them and moving them randomly. Next I have: #sym:init_window to create a game window, #sym:handle_events to check if user has quit the game, #sym:create_moving_rects to initialize n amount of MovingRect objects and #sym:update_screen to move and display them.  Could you take a look at it and provide me with stubs and hint to improve it? Don't think about expanding the functionality yet, let's just make this code work for now. Additionally, please add simplistic typing annotations to it

### 29-03-2026 13:15
- **Prompt**: I think there's must be an error in my thinking, because right now nothing is going on when I launch the game. Can you analyze the square moving logic (functions like #sym:random_move #sym:randomize_dir #sym:update_screen)? I'm confused if we should update the rect's coordinates and then update the screen or is calling rect.move_ip() method enough

### 30-03-2026 11:05
- **Prompt**: Could you update #file:README.md for this project? Keep in mind that I just started and the app will be updated, but the general idea involves moving squares with pygame. Include overview, setup and usage.

### 09-04-2026 20:52
- **Prompt**: Hey, I want smaller rectangles to run away from bigger ones. Currently, I find the threat for each rectangle (except the biggest one) and change rectangles vector based on threats vector. It doesn't work very well. Can you give me hints with explanations about how could I do that? The bigger the threat rectangle, the stronger it affects the other rectangle. The bigger the distance between them, the less it affects the other vector. The problem is that in my code, the vector is always normalized, so we can't directly sum vectors. Vector represents direction, speed represents speed of movement. So the question is how do we smoothly change vector's direction based on aforementioned factors

### 09-04-2026 21:05
- **Prompt**: Let's focus on formulas you suggested. First one, why do you turn d into a unit vector? Second what is k and epsilon? Fourth, what exactly are lambda and delta t? Is delta t delta time? And what is this formula used for? Maybe explain your idea as a whole

### 13-04-2026 11:23
- **Prompt**: activate the journal logger

### 13-04-2026 11:27
- **Prompt**: generate the code explorer site for this project

