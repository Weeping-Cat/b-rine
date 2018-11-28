class Character:
    def __init__(self, client):
        self.client = client
        self.name = None
        self.stats = {}

    def create(self):
        points = 50*len(stat_list)
        self._distribute_points(points)
        self._calculate_derivatives()
        #self.set_name()

    def _distribute_points(self, p):
        done = False
        while not done:
            for stat in stat_list:
                if p == 0:
                    break
                valid_input = False
                while not valid_input:
                    value = int(input('You have %d points left.\nHow many will you spend on %s?\n' % (p, stat.name)))     #Learn how to format
                    if value+stat.value > 100 or value > p:
                        print('Invalid input.')
                        continue
                    valid_input = True
                    p -= value
            if p > 0:
                continue
            done = True

    def _calculate_derivatives(self):   #replace with setter function for stats
        pass


class Stat:

    def __init__(self, name):
        self.name = name
        self.value = 0


stat_list = []
derivative_list = []        #change work on

def load_stats():
    for stat in ['STR', 'DEX', 'CON', 'INT', 'WIS', 'LCK']:
        stat_list.append(Stat(stat))
    for derivative in ['HP', 'MP']:
        derivative_list.append(Stat(derivative))


    
load_stats()
c = Character('debug')
c.create()