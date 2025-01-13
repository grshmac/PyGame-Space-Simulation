#1. imports libraries and modules
import pygame
import math

#2. initialize pygame
pygame.init()

#3. set up window i.e square
WIDTH, HEIGHT = 650, 650
#4. pygame surface and we need to have access
WIN= pygame.display.set_mode((WIDTH,HEIGHT))  #takes coordin for win
#5. put caption for win
pygame.display.set_caption("My planet simulation")

#9. color to fill whole screen and each planet
WHITE=(255,255,255)
YELLOW=(255,255,0)
BLUE= (100,140,239)
RED=(180,40,50)
DARK_GREY=(90,70,80)
GREY=(200,140,69)

#6. you would like to create a pygame infinite loop so that your simulation run entire time
#this is just like when you play game that is always looping keeping track of events

#here, so the event in the loop is moving of different planets around the sun
#7. define main function
def main():
    run= True
    #lets set a clock so the frame rate regulates to synchronize
    clock= pygame.time.Clock() 

    #14. now lets draw planets
    sun = Planet(0,0,30,YELLOW,1.9891 * 10**30) #in kg, for expo **
    sun.sun= True #so we dont mistake sun as planet  

    earth= Planet(-1*Planet.AU,0,16 ,BLUE,5.9742 * 10**24) #-1 so it goes to left else right
    earth.y_vel= 29.783*1000
    mars= Planet(-1.524*Planet.AU,0,12,RED,6.39* 10**23)
    mars.y_vel= 24.077*1000
    mercury= Planet(0.387*Planet.AU,0,8,DARK_GREY,3.30*10**23)
    mercury.y_vel=47.4*1000
    venus= Planet(0.723*Planet.AU,0,14,GREY, 4.8685*10**24)
    venus.y_vel= -35.02*1000

    planets =[sun,earth,mars,mercury,venus]


    while run:  #this loop runs when "run" variable is true
         clock.tick(60)   #update this loop at max 60 times per second
         #now is time to draw something on the screen
         WIN.fill((0,0,0)) 
         #pygame.display.update() #takes all of the actions done since last update so in every loop fill bg with white


         for event in pygame.event.get():   
              #we only need to close the window when user clicks X close button so,
              if event.type == pygame.QUIT:
                   run = False

        #15. loop for drawing planets
         for planet in planets:
          #17.
              planet.update_pos(planets)
              planet.draw(WIN)

         pygame.display.update()

    pygame.quit()

#10. now lets implem planets
class Planet:
     #these are basically physics param
     #12. dew const we gonna use 
     #const for planet class is Astronomical units and 1 au approx equal to distn btwm earth and sun
     AU= (149.6e6)*1000 #149 mil and 600K km
     #const for planet class is gravitational constant for force of attrac
     G= 6.67428e-11
     #what 1 meter repre in pixels in our window
     SCALE= 190/AU  #1au= 100pixels
     #evrytime we update the frame look at planet orbit in timestep
     TIMESTEP= 3600*24 #in one day

     def __init__(self,x,y,radius,color,mass):  #11. x,y is position we want for planets to be on the screen with radius
         #now initiale the values we have
         self.x=x
         self.y=y
         self.radius=radius
         self.color=color
         self.mass=mass  #in kg and needed to calc the attraction between diff planets and orbit physics

         self.sun=0 #to make sure planet is not sun
         self.dist_to_sun=0  #we will update these values later
         self.orbit=[] #this list will help display orbit points planet has traveled along


        # to generate movement in circles we need x dirn and y dirn at a constant speed
         self.x_vel=0
         self.y_vel=0

     #13. method to draw each planet on the screen in center
     def draw(self,win):
          x= self.x * self.SCALE + WIDTH / 2 #meters in scale of our pixel
          y= self.y * self.SCALE + HEIGHT /2

          if len(self.orbit) > 2:
          #17. okay now we draw orbit line with the orbit[] list help 
               updated_points=[]
               for point in self.orbit:
                    x,y=point
                    x=x*self.SCALE+WIDTH/2
                    y=y*self.SCALE+HEIGHT/2
                    updated_points.append((x,y))

               pygame.draw.lines(win,self.color,False,updated_points,2)

          pygame.draw.circle(win, self.color, (x,y), self.radius)

     #15. now we define a method that calculates force of planets with each other
     def attract(self,other):
          other_x,other_y=other.x,other.y
          #then calculate distance
          distance_x=other_x - self.x
          distance_y=other_y- self.y
          distance= math.sqrt(distance_x**2 + distance_y**2)

          if other.sun:
               self.distance_to_sun=distance
          
          #calc fore of attraction ie st line force
          force= self.G* self.mass * other.mass / distance**2
          #now break into x and y comp, so calc angle theta
          theta= math.atan2(distance_y,distance_x) #atan2 gets the y over x and gives angle
          force_x= math.cos(theta)*force
          force_y=math.sin(theta)*force

          return force_x, force_y

      #16. Now we update the position of planets
     def update_pos(self,planets):
          total_fx=total_fy=0
          for planet in planets:
               if self==planet:    #to avoid div by self i.e 0
                    continue
               fx,fy=self.attract(planet)
               total_fx += fx
               total_fy+= fy
          
          #calc velocity, f=m/a where a=f/m
          # we take timestep i.e 1 day
          #constantly add this since we need to change in dirn
          self.x_vel+=total_fx/self.mass*self.TIMESTEP
          self.y_vel+=total_fy/self.mass*self.TIMESTEP

          self.x+= self.x_vel * self.TIMESTEP
          self.y+= self.y_vel * self.TIMESTEP
          self.orbit.append((self.x,self.y))

 
#8. calling the main function
main()



