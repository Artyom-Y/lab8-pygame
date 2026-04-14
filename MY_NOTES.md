### Inital notes
I'm using a subclass of pygame.rect with custom properties, representing movement vectors. I also have 2 utility methods for moving in direction of vectors and for randomly updating them.

### Speed as a function of size
I need to come up with a formula where speed increases with size in a geometric progression. I also have to base it off max_speed and make sure it doesn't exceed that. It's also random, so the speed of n-sided square isn't predetermined

### Running away from squares
Each square should have its dir_x and dir_y modified based on size of nearby squares. We can calculate some sort of coefficient proportionate to nearby squares' sizes. Maybe the squares should have "force fields". the bigger the square, the larger the field. Each frame rect is in a field, it changes its direction slightly away from the field

### Lifecycle
I'm gonna change spawning squares to be a class method. Then I'll add a property which defines the life time of a square. At the end of each frame I subtract delta time from square's life. If it's less than zero, I remove this rect from rects list and delete the object. After, I add a new object to the list. Having rect's color change based on it's health would be a nice feature, but maybe a little complicated