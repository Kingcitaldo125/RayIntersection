import pygame
import time

def check_intersect(o, d, u, c, rad_squared, interval = 10):	
	x = o + d*u

	svec_prod = x - c

	dprod = svec_prod.dot(svec_prod)
	
	# TBD: Better way to check the dot product against rad_squared?
	# Many valid intersection points were omitted without the interval
	if dprod >= rad_squared - interval and dprod <= rad_squared + interval:
		#print("o",o)
		#print("d",d)
		#print("u",u)
		#print("c",c)
		#print("x",x)
		#print("dprod",dprod)
		#print("")
		return x

	return None

def calc_intersect_sphere(o, u, c, rad):
	points = []
	d = 1

	while d < c.length() + rad:
		point = check_intersect(o, d, u, c, rad**2)

		if point:
			points.append(point)

		d += 0.25

	return points

pygame.display.init()

winx = 400
winy = 400

screen = pygame.display.set_mode((winx, winy))

sphere_rad = 30

sphere_x, sphere_y = winx//2, winy//2
sphere_vec = pygame.Vector2(sphere_x, sphere_y)

ray_start = pygame.Vector2(0,0)

ray_dir = pygame.Vector2(winx, winy//2) - ray_start
ray_dir = ray_dir.normalize()

ray_dir_draw = pygame.Vector2(ray_dir.x, ray_dir.y)
ray_dir_draw.scale_to_length(winx * winy)

points = None

done = False

while not done:
	events = pygame.event.get()
	for e in events:
		if e.type == pygame.QUIT:
			done = True
		elif e.type == pygame.KEYDOWN:
			if e.key == pygame.K_ESCAPE:
				done = True
		elif e.type == pygame.MOUSEBUTTONUP:
			mpos = pygame.mouse.get_pos()
			mx = mpos[0]
			my = mpos[1]

			mouse_vec = pygame.Vector2(mx, my)
			ray_dir = mouse_vec - ray_start
			ray_dir = ray_dir.normalize()

			ray_dir_draw = pygame.Vector2(ray_dir.x, ray_dir.y)
			ray_dir_draw.scale_to_length(winx * winy)

			points = calc_intersect_sphere(ray_start, ray_dir, sphere_vec, sphere_rad)
			if len(points) > 2:
				points = [points[0],points[-1]]

	screen.fill((0,0,0))

	pygame.draw.circle(screen, (255,0,0), (int(ray_start.x), int(ray_start.y)), 5)
	pygame.draw.circle(screen, (255,0,0), (sphere_x, sphere_y), sphere_rad, 1)

	pygame.draw.line(screen, (255,0,0), (int(ray_start.x), int(ray_start.y)), (int(ray_dir_draw.x), int(ray_dir_draw.y)))

	if points:
		for p in points:
			pygame.draw.circle(screen, (255,255,255), (int(p.x), int(p.y)), 3)

	pygame.display.flip()
	time.sleep(0.05)

pygame.display.quit()
