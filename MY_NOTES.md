### Current state
I'm using a subclass of pygame.rect with custom properties, representing movement vectors. I also have 2 utility methods for moving in direction of vectors and for randomly updating them.

### Speed as a function of size
I need to come up with a formula where speed increases with size in a geometric progression. I also have to base it off max_speed and make sure it doesn't exceed that. It's also random, so the speed of n-sided square isn't predetermined