import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

class Visualizer():
    
    def __init__(self, mission_reader, way_points = None):
        
        self.fig = plt.figure()
        self.ax = plt.axes(projection='3d')
        
        self.mission = mission_reader # Data from mission_file
        self.way_points = way_points # All Waypoints from planner

        self.fig.set_figwidth(100)
        self.fig.set_figheight(100)
        plt.title("Mission Visualiztion")
        self.ax.set_proj_type('ortho')
        self.ax.set_xlabel('Latitude')
        self.ax.set_ylabel('Longitude')
        self.ax.set_zlabel('Altitude(AGL)(in feet)')
    
    def data_for_cylinder_along_z(self, center_x, center_y, radius, height_z):
        z = np.linspace(0, height_z, 50)
        theta = np.linspace(0, 2*np.pi, 50)
        theta_grid, z_grid = np.meshgrid(theta, z)
        x_grid = radius*np.cos(theta_grid) + center_x
        y_grid = radius*np.sin(theta_grid) + center_y
        return x_grid, y_grid, z_grid

    def scatter_points(self, points, colour='r', s=10):
        x = []
        y = []
        z = []
        for point in points:
            x.append(point[0])
            y.append(point[1])
            z.append(point[2])
        self.ax.scatter(x, y, z, alpha=1.0, c=colour, s =s)

    def scatter_cylinders(self, cylinders):

        for cylinder in cylinders:
            x, y, z = self.data_for_cylinder_along_z(   cylinder[0],
                                                        cylinder[1],
                                                        cylinder[2] * 0.3048 /111320,
                                                        cylinder[3]
                                                    )
            self.ax.plot_surface(x, y, z, alpha=0.3, color='cyan')

    def plot_bounds(self, bounds, altmax, altmin, colour='b'):
        
        if len(bounds) < 3:
            return

        bounds.append(bounds[0])
        for i, point in enumerate(bounds):
            if i > 0:
                vertices = [(prev[0], prev[1], altmin),
                            (point[0], point[1], altmin),
                            (point[0], point[1], altmax),
                            (prev[0], prev[1], altmax)]

                x = [vertex[0] for vertex in vertices]
                y = [vertex[1] for vertex in vertices]
                z = [vertex[2] for vertex in vertices]

                vertices = [list(zip(x, y, z))]
                poly = mplot3d.art3d.Poly3DCollection(
                    vertices, alpha=0.2, linewidths=0.01, edgecolors='k', facecolors=colour)
                self.ax.add_collection(poly)
            prev = point

    def plot_lines(self, points, colour='r'):
        x = []
        y = []
        z = []
        i=0
        for point in points:
            i+=1
            x.append(point[0])
            y.append(point[1])
            z.append(point[2])
            self.ax.text(point[0],point[1],point[2],  '%s' % (str(i)), size=10, zorder=1,  
    color='k') 

        self.ax.plot(x, y, z, alpha=0.8, c=colour)
    
    def plot_waypoints(self, waypoints):
        
        fly_through_points = []
        drop_points = []
        coverage_points = []
        path = []#[(p.lat, p.lon, p.alt) for p in waypoints]

        terminal = [waypoints[0], waypoints[-1]]
        terminal_point = []

        for waypoint in waypoints:
        
            point = [waypoint.lat, waypoint.lon, waypoint.alt ]
            # print(point)
            
            if waypoint in terminal:
                terminal_point.append(point)
                path.append(point)
                continue


            if waypoint.behaviour == 1:
                fly_through_points.append(point)
            
            if waypoint.behaviour == 2:
                drop_points.append(point)
            
            if waypoint.behaviour == 3:
                coverage_points.append(point)

            # TODO: 4 IS Coverage END, 5 IS Mission End
            
            path.append(point)

        self.scatter_points(fly_through_points, colour='turquoise')
        self.scatter_points(coverage_points, colour='purple')
        
        self.scatter_points(drop_points, colour='navy', s=15)

        # # Start and End Points
        self.scatter_points([terminal_point[0]], colour='green', s=25)
        self.scatter_points([terminal_point[-1]], colour='red', s=25)

        self.plot_lines(path, colour='lime')



    def plot_mission(self):
        
        if self.way_points is not None:
            self.plot_waypoints(self.way_points)
            self.adjust_plot()
        
        
        # TODO: communcations lost point, what is the altitude?
        # lost_comms = self.mission.get_land_position()
        # lost_comms.append(100)
        # self.scatter_points([lost_comms], colour='black')

        # air_drops = self.mission.get_air_drop_positions()
        # [point.append(95) for point in air_drops]
        # self.scatter_points(air_drops, colour='navy')

        self.scatter_points(self.mission.get_mission_waypoints(), 
                            colour='#e68e35')
        self.plot_lines(self.mission.get_mission_waypoints(),colour='#e68e35')

        # self.scatter_cylinders(self.mission.get_obstacles())

        # # Flight Boundary 
        # self.plot_bounds(self.mission.get_flight_boundary(), 
        #                  *self.mission.get_altitude_limits(), '#dd517e')
        
        # # Search Grid
        # self.plot_bounds(self.mission.get_search_boundary(),
        #                  *self.mission.get_altitude_limits(), '#481d52')

        

    def adjust_plot(self):
        """
            Adjusts the graph such that it occupies around 75% of graph volume
        """
        
        pad = 0.00045

        waypoints = np.array([(p.lat, p.lon, p.alt ) for p in self.way_points])

        x_begin = min(waypoints[:, 0]) - pad
        x_end = max(waypoints[:, 0]) + pad

        y_begin = min(waypoints[:, 1]) - pad
        y_end = max(waypoints[:, 1]) + pad

        z_begin = min(waypoints[:, 2]) - pad
        z_end = max(waypoints[:, 2]) + pad

        self.ax.set_xlim(x_begin, x_end)
        self.ax.set_ylim(y_begin, y_end)
        # self.ax.set_zlim(z_begin, z_end)

    def display(self):
        # self.ax.set_aspect('equalxy')
        plt.show()


