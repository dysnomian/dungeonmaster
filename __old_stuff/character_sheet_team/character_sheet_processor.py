import json

# Function to read character data from characterSheet.json file
# Function to update character data based on requests
def update_character_data(character_data, update_request):
    for key, value in update_request.items():
        if key in character_data:
            character_data[key] += value

# Function to write updated character data back to characterSheet.json file
def write_character_data(character_data):
    with open('characterSheet.json', 'w') as file:
        json.dump(character_data, file, indent=4)

# Main function to orchestrate the process
def main():
    character_data = read_character_data()
    
    # Example update request
    update_request = {'level': 1, 'experience': 100}
    
    update_character_data(character_data, update_request)
    
    write_character_data(character_data)