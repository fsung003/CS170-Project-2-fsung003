import math 
import time
import matplotlib.pyplot as plt # For data plot
from pathlib import Path # To properly open the file in the same path

def NearestNeighbor(data, features_to_evaluate):
  num_correctly_classified = 0
  data_len = len(data)
  for i in range(data_len):
    curr_obj = data[i]
    label_curr_obj = curr_obj[0] # Contains label of object
    nearest_neighbor_distance = math.inf
    nearest_neighbor_label = -1 

    for k in range(data_len):
      if k != i:
        next_obj = data[k]
        distance = 0
        for j in features_to_evaluate: # Get Euclidean Distance for the features being evaluated
          distance += (curr_obj[j] - next_obj[j])**2
          if distance > nearest_neighbor_distance: # Early abandon if distance is already bigger
            break
        if distance < nearest_neighbor_distance:
          nearest_neighbor_distance = distance
          nearest_neighbor_label = next_obj[0]
    if label_curr_obj == nearest_neighbor_label:
      num_correctly_classified += 1
  accuracy = num_correctly_classified / len(data)
  return accuracy

def SelectionAlgorithm(data, choice):
  num_features = len(data[0]) - 1 # Do not include class column
  if choice == 1: # Forward Selection
    curr_set_of_features = [] # Initialize an empty set of the recorded sets of features
  else: # Backward Elimination
    curr_set_of_features = [(i) for i in range(1, num_features + 1)] # Initialize an empty set of the recorded sets of features
  start_time = time.time()
  best_accuracy = NearestNeighbor(data, curr_set_of_features)
  best_features = curr_set_of_features.copy()
  print("Initial set being evaluated:", curr_set_of_features)
  print("Accuracy:", round(best_accuracy * 100, 1), "%\n")

  subsets_for_graph = [] # Keep track of tested subset and accuracy to plot
  accuracies_for_graph = []

  for i in range(num_features):
    print("On the", str(i + 1), "th level of the search tree.") 
    feature_to_evaluate = -1
    best_so_far_accuracy = 0
    
    for j in range(1, num_features + 1):
      if (choice == 1 and j not in curr_set_of_features) or (choice == 2 and j in curr_set_of_features):
        if choice == 1:
          curr_set_of_features.append(j)
        else:
          curr_set_of_features.remove(j)

        accuracy = NearestNeighbor(data, curr_set_of_features) # Test current set of features, with added/removed feature
        print("Using feature(s)", curr_set_of_features, "accuracy was", round(accuracy * 100, 1), "%\n")
        
        if accuracy > best_so_far_accuracy: # Update best accuracy
          best_so_far_accuracy = accuracy
          feature_to_evaluate = j
        # Revert back to original set of features
        if choice == 1:
          curr_set_of_features.pop()
        else:
          curr_set_of_features.append(j)
    if choice == 1:
      curr_set_of_features.append(feature_to_evaluate)
      print("At level", i + 1, ", I added feature", feature_to_evaluate, '\n')
    else:
      curr_set_of_features.remove(feature_to_evaluate)
      print("At level", i + 1, ", I removed feature", feature_to_evaluate, '\n')

    subsets_for_graph.append(curr_set_of_features.copy()) # Store the current subset of corresponding accuracy to create a graph
    accuracies_for_graph.append(best_so_far_accuracy * 100)

    if best_so_far_accuracy > best_accuracy: # Keep track of best accuracy and best set of features
      best_accuracy = best_so_far_accuracy
      best_features = curr_set_of_features.copy()

    print("Current set of features:", curr_set_of_features)
    print("Accuracy:", round(best_so_far_accuracy * 100, 1), "%\n")
  end_time = time.time()
  print("Finished Search! The best feature subset was", best_features, ", which has an accuracy of", round(best_accuracy * 100, 1), '%')
  print("Time elapsed:", round(end_time - start_time, 1), "seconds.")
  
  displayGraph(subsets_for_graph, accuracies_for_graph, choice)
  return

def displayGraph(subsets, accuracies, choice): # To visualize data for search algorithm
  x_axis = []
  for curr_set in subsets:
    x_axis.append(str(curr_set))
  plt.bar(x_axis, accuracies)
  if choice == 1:
    plt.xlabel("Current Feature Set: Forward Selection")
  else:
    plt.xlabel("Current Feature Set: Backward Elimination")
  plt.ylabel('Accuracy')
  plt.show()

  return

def convertFileToData(file_):
  # Convert input file into readable data
  # Order of Instances: Class, feature, feature, feature, ...
  data = []
  lines = file_.readlines()
  for instance in lines:
    row = instance.split()
    if row: # Check if a line is blank
      for i in range(len(row)):
        row[i] = float(row[i])
      data.append(row)
  return data

def main():
  print("Welcome to Francis Sunga's Feature Selection Algorithm.")
  print("Type in the name of the file to test: ")
  # Small Dataset: CS170_Small_DataSet__76.txt
  # Big Dataset: CS170_Large_DataSet__120.txt

  file_name = input() 
  # Read the file from the same directory
  ROOT_DIR = Path(__file__).parent
  TEXT_FILE = ROOT_DIR / file_name
  with open(TEXT_FILE, 'r') as file_:
    data = convertFileToData(file_)

  print("Type the number of the algorithm you want to run: ")
  print("1) Forward Selection")
  print("2) Backward Elimination")
  choice = 0
  while choice != 1 and choice != 2:
    choice = int(input())
    if choice == 1:
      print("Forward Selection search chosen...")
      SelectionAlgorithm(data, 1)
    elif choice == 2:
      print("Backward Elimination search chosen...")
      SelectionAlgorithm(data, 2)
    else:
      print("Invalid input. Please choose one of the options.")
      print("1) Forward Selection")
      print("2) Backward Elimination")
  return
  
main()