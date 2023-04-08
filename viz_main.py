# read data from a .yaml file and store data in a variable called mission_reader





import yaml
import visualizer as viz

class MissionReader:
    def __init__(self, filename):
        self.data = None
        with open(filename) as f:
            self.data = yaml.load(f, Loader=yaml.FullLoader)

    def get_flight_boundary(self):
        return self.data['flight_boundary']

    def get_altitude_limits(self):
        return self.data['altitude_limits']
      
    def get_search_boundary(self):
        return self.data['search_boundary']
    def get_land_position(self):
        return self.data['land_position']
    def get_air_drop_positions(self):
        return self.data['air_drop_positions']
    def get_mission_waypoints(self):
        return self.data['waypoints']
      
      # .... and so on
mission_reader = MissionReader('/home/ranguy/main/manas/image_pipeline/python_trials/test1a.yaml')
visualizer = viz.Visualizer(mission_reader)
visualizer.plot_mission()
visualizer.display()