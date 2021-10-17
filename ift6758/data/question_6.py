import numpy as np 
import pandas as pd 
import pickle    
import matplotlib
import matplotlib.pyplot as plt
color_map = plt.cm.winter
from matplotlib.patches import RegularPolygon
import math
from PIL import Image
from matplotlib.colors import ListedColormap,LinearSegmentedColormap
import matplotlib.colors as mcolors




def get_league_all_shoots_coordinates(df):
    # To keep the aspect ration correct we use a square figure size
    x_bound = np.array([0,100])
    y_bound = np.array([-42.5,42.5])
    extent = [x_bound[0],x_bound[1],y_bound[0],y_bound[1]]
    # We are going to bin in 30 unit increments.  It is fun to play with this!  
    gridsize= 20;mincnt=0

    # First concatenate the arrays for x and y league data
    league_coordinate_x_all_shots = df['Shooter/Scorer X Coordinate'].replace(np.NAN,0)
    league_coordiantes_y_all_shots = df['Shooter/Scorer Y Coordinate'].replace(np.NAN,0)
 
    # Perform the coordinate flipping!
    league_coordinate_x_all_shots_normalized = [];
    league_coordiantes_y_all_shots_normalized = []

    # Enumerate the list so we can use the index for y also
    for i,s in enumerate(league_coordinate_x_all_shots):
        if league_coordinate_x_all_shots[i] <0:
            league_coordinate_x_all_shots_normalized.append(-league_coordinate_x_all_shots[i])
            league_coordiantes_y_all_shots_normalized.append(-league_coordiantes_y_all_shots[i])
        else:
            league_coordinate_x_all_shots_normalized.append(league_coordinate_x_all_shots[i])
            league_coordiantes_y_all_shots_normalized.append(league_coordiantes_y_all_shots[i])


   
    # First we will used the hexbin function to simply bucket our shot data into basically a 2D histogram
    hex_data = plt.hexbin(league_coordinate_x_all_shots_normalized,
                                 league_coordiantes_y_all_shots_normalized,gridsize=gridsize,
                                 extent=extent,mincnt=mincnt,alpha=0.0)

    # Now we extract the bin coordinates and counts
    bin_coordinates= hex_data.get_offsets()
    shot_frequency = hex_data.get_array()
    plt.close()
    return bin_coordinates, shot_frequency

def get_shoots_coordinates(df):
    # To keep the aspect ration correct we use a square figure size
    x_bound = np.array([0,100])
    y_bound = np.array([-42.5,42.5])
    extent = [x_bound[0],x_bound[1],y_bound[0],y_bound[1]]
    # We are going to bin in 30 unit increments.  It is fun to play with this!  
    gridsize= 20;mincnt=0

    # First concatenate the arrays for x and y league data
    coordinate_x_all_shots = df['Shooter/Scorer X Coordinate'].replace(np.NAN,0)
    coordiantes_y_all_shots = df['Shooter/Scorer Y Coordinate'].replace(np.NAN,0)
 
    xy_coordinates =list(zip(coordinate_x_all_shots,coordiantes_y_all_shots))

    # Perform the coordinate flipping!
    coordinates_x_all_shots_normalized = []
    coordinates_y_all_shots_normalized = []

    for i,j in enumerate(xy_coordinates):
        if xy_coordinates[i][0] <0:
            coordinates_x_all_shots_normalized.append(-xy_coordinates[i][0])
            coordinates_y_all_shots_normalized.append(-xy_coordinates[i][1])
        else:
            coordinates_x_all_shots_normalized.append(xy_coordinates[i][0])
            coordinates_y_all_shots_normalized.append(xy_coordinates[i][1])

   
    # First we will used the hexbin function to simply bucket our shot data into basically a 2D histogram
    hex_data = plt.hexbin(coordinates_x_all_shots_normalized,
                                 coordinates_y_all_shots_normalized,gridsize=gridsize,
                                 extent=extent,mincnt=mincnt,alpha=0.0)

    # Now we extract the bin coordinates and counts
    bin_coordinates= hex_data.get_offsets()
    shot_frequency = hex_data.get_array()
    plt.close()
    return bin_coordinates, shot_frequency


def plot_shoots_map(df1,df2, team, season):
    positive_cm = ListedColormap(["lightcoral", "red"])
    negative_cm = ListedColormap(["lightblue", "blue"]) 
    league_bin_coordinates, league_shot_frequency=get_league_all_shoots_coordinates(df1)
    team_bin_coordinates, team_shot_frequency=get_shoots_coordinates(df2)
    
    I = Image.open('../figures/nhl_rink -half.png')
    width, height = I.size
    
    # Using matplotlib we create a new figure for plotting
    fig=plt.figure(figsize=(10,10))
    ax = fig.add_subplot(111)
    # Clean up the figure to be completely blank
    ax.set_facecolor("white")
    ax.set_title(''+ team +' Shoots per season '+ season, color='black')
    fig.patch.set_facecolor("white")
    fig.patch.set_alpha(0.0)
    
    # Calculate the scaling factor and offset (trial and error)
    scalingx=width/100-0.6;
    scalingy=height/100+0.5;
    x_trans=33;
    y_trans=height/2
    # We will want to scale the size of our hex bins with the image so we calculate a "radius" scaling factor here
    S = 3.8*scalingx;
    # Loop over the locations and draw the hex
    
    
    for i,v in enumerate(team_bin_coordinates):
        # Here we will only include locations where the team made at
    
        if team_shot_frequency[i] < 1:continue
    
        # Scaling the frequencies
        scaled_league_shot_frequency = league_shot_frequency[i]/max(league_shot_frequency)
        scaled_team_shot_frequency = team_shot_frequency[i]/max(team_shot_frequency)
    
   
        relative_efficiency=scaled_team_shot_frequency-scaled_league_shot_frequency
        # Calculate a radius of the hex
        radius = S*math.sqrt(scaled_team_shot_frequency)
         
       # Since there can be positive and negative efficiencies
        if relative_efficiency >0:
            colour = positive_cm(math.pow(relative_efficiency,0.1))
        else:
            colour = negative_cm(math.pow(-relative_efficiency,0.1))
   
       # And finally we plot!    
        hex = RegularPolygon((x_trans+v[0]*scalingx,y_trans-v[1]*scalingy),numVertices=6, radius=radius,orientation=np.radians(0),facecolor=colour,alpha=1,edgecolor=None)
        ax.add_patch(hex)   
    
    im =ax.imshow(I, vmin = min(league_shot_frequency), vmax =max(league_shot_frequency))
    cb = plt.colorbar(im, shrink=0.5)
    cb.set_label('Number of all shoots per season', color='black')
    # set colorbar tick color
    cb.ax.yaxis.set_tick_params(color='black')
    # set colorbar edgecolor
    cb.outline.set_edgecolor('black')
    


