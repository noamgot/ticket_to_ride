from game.classes import *
from game.board import *
import numpy as np

class GraphTopology:
    claimants = dict()
    city_to_i = dict()
    Laplacian = None
    Degree = None
    Adjacency = None
    cities = list()
    routes = None
    self.enemy_cities = list()
    def __init__(self):
        pass
    """
    #Set edge weights based on who has claimed them
    def set_claim_value(self,claimant,value):
        self.claimants[claimant] = value

    def route_weight(self,route):
        #print self.claimants
        #print route
        #print self.routes.get(route) or 'unclaimed'
        #print self.claimants.get(self.routes.get(route,'unclaimed'))
        #return self.claimants[self.routes.get(route,'unclaimed')]
        return self.claimants[self.routes.get(route) or 'unclaimed' ]
        
    def initialize_matrices(self,n):
        #self.laplacian = [[0 for i in range(40)] for j in range(40)]
        self.degree = [[0 for i in range(n)] for j in range(n)]
        self.adjacency =  [[0 for i in range(n)] for j in range(n)]
        self.cities = list()
        self.city_to_i = dict()
    """
    def get_2d_list_slice(self, matrix, start_row, end_row, start_col, end_col):
        return [row[start_col:end_col] for row in matrix[start_row:end_row]]


    def get_adacent_cities(self,city,routes,player):
        cities = list()
        for route in routes:
            if(route.city1 is city):
                cities.append(city2)
            if(route.city2 is city):
                cities.append(city1)

        pass

    def brushfire_from(self,start_city,depth,player,return_on_fork,routes):
        actual_depth = 0
        burned_cities = list()
        buringing_cities = list()
        burning_cities.append([start_city,actual_depth])
        routes = game.get_edge_claims()
        while depth > actual_depth:
            burn_city = burning_cities.pop_front()
            actual_depth = actual_depth + 1
            for city in self.get_adjacent_cities(routes,player):
                if(city not in burned_cities):
                    burning_cities.append([city, actual_depth])
            if(len(burning_cities) >  1 & return_on_fork):
                depth = actual_depth
                return burning_cities
        depth = actual_depth

        return burned_cities




    def get_possible_edges(self,player,city,depth):
        actual_depth = 0
        burned_cities = list()
        buringing_cities = list()
        burning_cities.append([start_city,actual_depth])
        routes = game.get_edge_claims()
        while depth > actual_depth:
            burn_city = burning_cities.pop_front()
            actual_depth = actual_depth + 1

            for city_edge in self.get_adjacent_cities(routes,player):
                if(city_edge[0] not in burned_cities):
                    burning_cities.append([city_edge[0], actual_depth])
                if(city in enemy_cities):
                    harmful_edges.append(city_edge[1])
        depth = actual_depth
        return harmful_edges

    def get_unfilled_enemy_edges(self,player,depth):
        self.routes = game.get_edge_claims()
        unfillled_enemy_edge = list()
        # get list of cities which opponent has edges which connect to it
        self.enemy_cities = list()
        for route in self.routes:
            if route.city1 not in enemy_cities:
                self.enemy_cities.append(route.city1)
            if route.city2 not in enemy_cities:
                self.enemy_cities.append(route.city2)
        # for each enemy city
        for city in enemy_cities:
            #search for beginings of other paths at depth
            for edge_group in self.get_possible_edges(player,city,depth): #correct?
                unfilled_enemy_edges.append(edge_group)
        return unfilled_enemy_edges

    def get_most_harmful_edge(self,player):
        return self.get_unfilled_enemy_edges(player,1)


"""
    #Create a new adjacency matrix based on claims
    def getLaplacian(self,game):
        self.routes = game.get_edge_claims()
        self.initialize_matrices(len(self.routes))

        for route in self.routes:
            for route in self.routes:
                #city_weight;
                if()


                A[i][j] =


    def update_game_board(self,game):
        self.initialize_matrices()
        self.routes = game.get_edge_claims()
        i=0;
        for route in self.routes:
            if self.route_weight(route) > 0:
                if route.city1 not in self.cities:
                    self.cities.append(route.city1)
                    self.city_to_i[route.city1]=i
                    i=i+1
                if route.city2 not in self.cities:
                    self.cities.append(route.city2)
                    self.city_to_i[route.city2]=i
                    i=i+1
                city1 = self.city_to_i[route.city1]
                city2 = self.city_to_i[route.city2]
                self.adjacency[city1][city2] = self.route_weight(route)
                self.degree [city1][city1] =  self.degree [city1][city1] +1;
                self.degree [city2][city2] =  self.degree [city2][city2] +1;
        #print self.degree
        #print i
        #np.delete.adjacency(
    
        #self.adjacency2 = numpy.array(self.adjacency)[[0:i-1],[0:i-1]]
        #self.degree2 = numpy.array(self.degree)[[0:i-1][0:i-1]]
        
        self.adjacency = self.get_2d_list_slice(self.adjacency,0,i,0,i)
        self.degree = self.get_2d_list_slice(self.degree,0,i,0,i)

        #print self.degree
        self.laplacian = np.subtract(self.degree, self.adjacency)
        #print len(self.laplacian)
        #print self.laplacian

    def get_most_harmful_edge(self):

        w,v = np.linalg.eig(self.laplacian)
        print v
        i = 0
        j = 0
        #for city1 in self.cities:
        #    for city2 in self.cities:
        return 0
        #return edge

"""
