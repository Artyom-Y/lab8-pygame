### Inital notes
I'm using a subclass of pygame.rect with custom properties, representing movement vectors. I also have 2 utility methods for moving in direction of vectors and for randomly updating them.

### Speed as a function of size
I need to come up with a formula where speed increases with size in a geometric progression. I also have to base it off max_speed and make sure it doesn't exceed that. It's also random, so the speed of n-sided square isn't predetermined

### Running away from squares
Each square should have its dir_x and dir_y modified based on size of nearby squares. We can calculate some sort of coefficient proportionate to nearby squares' sizes. Maybe the squares should have "force fields". the bigger the square, the larger the field. Each frame rect is in a field, it changes its direction slightly away from the field

### Lifecycle
I'm gonna change spawning squares to be a class method. Then I'll add a property which defines the life time of a square. At the end of each frame I subtract delta time from square's life. If it's less than zero, I remove this rect from rects list and delete the object. After, I add a new object to the list. Having rect's color change based on it's health would be a nice feature, but maybe a little complicated

### Chase feature
Each loop, the vector of every rect but one (the biggest) gets updated. So the easiest (albeit not super optmized) approach which won't require much rewriting is
1. For each square, find the threat (already implemented: find_threat function)
2. Then find prey for each square (to implement: find_prey function. Or repurpose find_threat to be find_threat_and_prey)
3. Update the vector
I have two optimization concerns. Firstly, we don't want to iterate through rectangles twice in search of threat and prey. This is more cost-heavy of the two. The other concern is us having to adjust the vector two times: to escape and to chase. This is less computation heavy. But also there's a logical concern: do we prioritze chasing or escaping? Can we do it at the same time? And will it involve three point linear interpolation?

Current algorithm: find a desired vector, compute the coefficient, "lerp" rect's vector based on the coefficient. But now we need to take more rectangles into account