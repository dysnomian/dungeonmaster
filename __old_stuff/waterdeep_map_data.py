import networkx as nx
from collections import defaultdict
import matplotlib.pyplot as plt

street_data = {
    "The High Road": [
        "North Gate",
        "Northyard",
        "The Fieldway/Chop Street/Gawenknife Street",
        "North Trollwall gate",
        "Trollkill Street",
        "Skulls Street",
        "Thunderstaff Way",
        "Chasso’s Trot",
        "Sashtar Street",
        "Vondil Street",
        "Tower March",
        "Delzorin Street",
        "Sidle Street",
        "Sulmor Street",
        "Hassantyr’s Street",
        "Julthoon Street",
        "Trader’s Way/Suldown Street",
        "Bazaar Street/Andamar’s Street",
        "Lamp Street",
        "Selduth Street",
        "Buckle Alley/The Coffinmarch",
        "Winter Path/Burnt Wagon Way",
        "Spendthrift Alley",
        "Waterdeep Way/Snail Street",
        "The Street of the Tusks/Quaff Alley",
        "Scroll Street",
        "The Way of the Dragon",
        "Slipstone Street",
        "Lathin’s Cut",
        "River Street",
        "Shoor Street",
        "Sahtyra’s Lane",
        "Telshambra’s Street",
        "The Street of the Smiths",
        "Rising Ride",
        "Brian’s Street",
        "The Forcebar",
        "The Specterwalk",
        "Coach Street",
        "The Waymoot",
        "Smuggler’s Run",
        "South Gate",
    ],
    "Way of the Dragon": [
        "The High Road",
        "Simple’s Street",
        "Soothsayer’s Way",
        "Drakiir Street",
        "Telshambra’s Street",
        "Street of Smiths",
        "Candle Lane",
        "Zastrow Street",
        "Fillet Lane",
        "Net Street",
        "Spices Street",
        "Hog Street",
        "Nag Street",
        "Sambril Lane",
        "The Waymoot",
    ],
    "Trader’s Way": [
        "Julthoon Street",
        "Courtyard of the Spires of the Morning",
        "Gothal Street",
        "Mel shares Street",
        "Tchozal’s Race",
        "The Sutherlane",
        "Mendever’s Street",
        "Sul Street",
        "Shield Street",
        "Copper Street",
        "The High Road",
    ],
    "Bazaar Street": [
        "The Street of Silks/Calamastyr Lane/The Sutherlane",
        "Tharleon Street/The Street of Silver",
        "Alnether Street",
        "Warrior’s Way",
        "The Street of the Sword",
        "The Street of Bells",
        "The High Road",
    ],
    "Street of the Singing Dolphin": [
        "Trollyard",
        "Old Trollwall Gate",
        "Trollkill Street",
        "Street of Lances",
        "Aurenaar Street",
        "Breeze’s Cut",
        "Street of Glances",
        "Telchar Lane",
        "Gorl Street",
        "Ivory Street",
        "Sighing Maiden’s Walk",
        "Grimwald’s Way",
        "Shark Street/Delzorin Street",
        "Diamond Street",
        "Dob’s Loss",
        "Darselune Street",
    ],
    "Snail Street": [
        "Waterdeep Way/The High Road",
        "Niles Way",
        "Scroll Street",
        "Crossbow Lane",
        "Soothsayer’s Way",
        "Unnamed alley",
        "Shesstra’s Street",
        "Blackstar Lane",
        "Street of Curtains",
        "Spiderweb Alley",
        "Trollcrook Alley",
        "Fish Street",
        "Shrimp Alley",
        "Fillet Lane",
    ],
    "Belnimbra's Street": [
        "Sail Street",
        "Crook Street",
        "The Slide",
        "Eel Street",
        "Sekiir’s Street",
        "Ward’s Way",
        "Wastrel Alley",
        "Redcloak lane",
        "Lackpurse Lane",
        "Gut Alley",
        "Unnamed Alley",
        "Rainrun Street",
        "Soothsayer’s Way",
    ],
    "Fish Street": [
        "Dock street",
        "Wastrel Alley",
        "Ship Street",
        "Adder Lane",
        "Snail Street",
    ],
    "Ship Street": [
        "Fish Street",
        "Odd Street",
        "Siren Street",
        "Sternpost Street",
        "Presper Street",
        "Shrimp Alley",
        "Dar Alley",
        "Keel Alley",
        "Aline’s Way",
        "Dock Street",
    ],
    "Net Street": ["Dock Street", "Keel Alley", "Pressbow Lane", "Way of the Dragon"],
    "Dock Street": [
        "Sail street",
        "Lackpurse Lane",
        "Sail Street",
        "Fish Street",
        "Wastrel Alley",
        "Odd Street",
        "Sternpost Street",
        "Asterii’s Way",
        "Cod Lane",
        "Ship Street",
        "Net Street",
        "Spices Street",
        "Wharf Street",
        "Cedar Street",
        "Hog Street",
    ],
    "Gut Alley": [
        "Belnimbra’s Street",
        "Shesstra’s Street",
        "Watchrun Way",
        "Leera’s Alley",
        "Blackstar Lane",
        "Adder Lane",
    ],
    "Sail Street": [
        "Coin Alley",
        "Sea Lion Street",
        "Dock Street",
        "Tarnished Silver Alley",
        "Lackpurse Lane",
        "Belnimbra’s Street",
        "Dock Street",
    ],
    "Wastrel Alley": [
        "Belnimbra’s Street",
        "Nelnuk’s Walk",
        "Adder Lane",
        "Fish Street",
        "Dock Street",
    ],
    "Lackpurse Lane": [
        "Dock Street",
        "Sail street",
        "The Reach",
        "Crock Street",
        "Dretch Lane",
        "Eel Street",
        "Sakiir’s Street",
        "Ward’s Way",
        "Cook Street",
        "Belnimbra’s Street",
    ],
    "Coin Alley": ["Tarnished Silver Alley", "Dock Street"],
    "Ward’s Way": [
        "Castle Waterdeep",
        "Rainrun Street",
        "Lackpurse Lane",
        "Arun’s Alley",
    ],
    "Sakiir’s Street": [
        "Lackpurse Lane",
        "Belnimbra’s Street",
        "The Slide",
        "Fishgut Court",
        "Dock Street",
    ],
    "Trollcrook Alley": ["Snail Street", "Zastrow Street"],
    "Zastrow Street": [
        "Way of the Dragon",
        "Trollcrook Alley",
        "Pearl Alley",
        "Fillet Lane",
    ],
    "Fillet Lane": ["Snail Street", "Zastrow Street", "Way of the Dragon"],
    "Dar Alley": ["Ship Street", "Pressbow Lane"],
    "Presper Street": [
        "Ship Street",
        "Troll Flask Alley",
        "Street of Six Casks",
        "Pressbow Lane",
        "Shrimp Alley",
    ],
    "Pressbow Lane": ["Shrimp Alley", "Dar Alley", "Snail Street", "Net Street"],
    "Sea Lion Street": ["Sail Street", "Tarnished Silver Alley"],
    "Book Street": [
        "Soothsayer’s way",
        "Seestra’s Street",
        "Drakiir Street",
        "Black Wagon Alley",
        "Candle Lane",
        "Trollcrook Alley",
    ],
    "Adder Lane": [
        "Sakiir’s street",
        "Fishgut Court",
        "Wastrel Alley",
        "Gut Alley",
        "Picklock Alley",
        "Fish Street",
    ],
    "Redcloak Lane": [
        "Belnimbra’s Street",
        "Watchrun Alley",
        "Leera’s Alley",
        "Nelnuk’s Walk",
        "Gut Alley",
    ],
    "Dust Alley": ["Blackstar Lane"],
    "Aline’s Way": ["Ship Street"],
    "Picklock Alley": ["Adder Lane", "Julbuck Alley"],
    "Fishgut Court": ["Sekiir’s Street", "Adder Lane"],
    "Smuggler’s Run": ["High Road"],
    "Wharf Street": ["Spices Street", "Dock Street"],
    "Spices Street": [
        "Dock Street",
        "Fishgut Alley",
        "Wharf Street",
        "The Way of the Dragon",
    ],
    "Fishgut Alley": ["Spices Street"],
    "Nelnuk’s Walk": ["Wastrel Alley", "Watchrun Alley", "Redcloak Lane"],
    "Watchrun Alley": ["Nelnuk’s Walk", "Redcloak Lane", "Gut Alley"],
}

# Initialize a dictionary to keep track of intersections (nodes)
intersections = defaultdict(set)

# Populate the intersections dictionary with streets meeting at each intersection
for street, crossing_streets in street_data.items():
    for i in range(len(crossing_streets) - 1):
        # For each pair of consecutive intersections, add each other as connected
        intersection_from = crossing_streets[i]
        intersection_to = crossing_streets[i + 1]

        # Adding each street segment as a bidirectional connection
        intersections[intersection_from].add((intersection_to, street))
        intersections[intersection_to].add((intersection_from, street))

edges = []
for intersection, connections in intersections.items():
    for connection, street in connections:
        edges.append((intersection, connection, {"street": street}))

# Initialize a directed graph
G = nx.DiGraph()


# A function to add edges between consecutive points on a street to the graph
# and label those edges with the street name
def add_streets_with_labels(graph, streets):
    for street, locations in streets.items():
        for i in range(len(locations) - 1):
            start_location = locations[i]
            end_location = locations[i + 1]
            graph.add_edge(start_location, end_location, label=street)


# Adding the streets to the graph
add_streets_with_labels(G, street_data)

# Position nodes using the spring layout
pos = nx.spring_layout(G, seed=42)

plt.figure(figsize=(20, 15), dpi=300)

# Draw the graph
nx.draw(G, pos, with_labels=False, node_size=20, font_size=8, node_color="lightblue")

# Draw edge labels
edge_labels = nx.get_edge_attributes(G, "label")
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

plt.title("Map of Waterdeep with Street Names on Edges")
plt.axis("off")  # Turn off the axis
output_path = "waterdeep_map_large.png"

plt.savefig(output_path, bbox_inches="tight")  # Save the figure as a PNG file


plt.close()  # Close the plot to free up memory

special_locations = [
    {
        "Name": "The Yawning Portal",
        "Address Type": "Streetside",
        "Location Details": "Between Cook Street and Belnimbra’s Street on Rainrun Street",
        "Ward": "Castle Ward",
    },
    {
        "Name": "The Honorable Knight",
        "Note": "One of the Walking Statues of Waterdeep",
        "Address Type": "Intersection",
        "Location Details": "Intersection of Shesstra’s Street and Book Street",
        "Ward": "N/A",
    },
    {
        "Name": "Mistshore",
        "Address Type": "Intersection",
        "Location Details": "Intersection of Sail Street and Coin Alley",
        "Ward": "N/A",
    },
    {
        "Name": "Cassalanter Villa",
        "Address Type": "Intersection",
        "Location Details": "Intersection of Diamond Street and Delzorin Street",
        "Ward": "Sea Ward",
    },
    {
        "Name": "Hospice of St. Laupsenn",
        "Address Type": "Intersection",
        "Location Details": "Intersection of Andamar’s Street and Lamp Street",
        "Ward": "North Ward",
    },
    {
        "Name": "The Great Drunkard",
        "Note": "One of the Walking Statues of Waterdeep",
        "Address Type": "Streetside",
        "Location Details": "On Bazaar Street between The Street of Swords and the Street of Bells",
        "Ward": "Castle Ward",
    },
    {
        "Name": "The Market",
        "Address Type": "Streetside",
        "Location Details": "Between Trader’s Way, the Sutherlane, and Bazaar Street",
        "Ward": "Castle Ward",
    },
]
