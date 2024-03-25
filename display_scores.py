import json
import csv
from collections import defaultdict

#jsonl_file = './ICP_Validation_Frames_prediction-ul-icp-2024-stratify_dist_sl_Update2-2024-03-20T15_42_28.417075Z_predictions_00001.jsonl'
jsonl_file = './validation.jsonl'

# Read JSONL file
with open(jsonl_file, 'r') as file:
    jsonl_data = [json.loads(line) for line in file]

results = []
for item in jsonl_data:
    content = item['instance']['content']
    prediction_data = item['prediction']

    confidences = defaultdict(float)

    # Extract the maximum confidence for each label
    for index, confidence in enumerate(prediction_data['confidences']):
        label = prediction_data['displayNames'][index]
        confidences[label] = max(confidences[label], confidence)

    # Sort the labels based on confidence
    sorted_labels = sorted(confidences, key=confidences.get, reverse=True)

    # Select the top 3 labels with their confidences
    top_labels = sorted_labels[:3]
    top_confidences = [confidences[label] for label in top_labels]

    result = [content] + top_labels + top_confidences
    results.append(result)

csv_file = './image_recognition_scores_output.csv'     

with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Validated Image', 'Component Name 1', 'Component Name 2', 'Component Name 3', 'Confidence Score 1', 'Confidence Score 2', 'Confidence Score 3'])
    writer.writerows(results)



