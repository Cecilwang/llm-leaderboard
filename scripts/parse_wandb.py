import os
import json
import argparse
import csv

def find_and_read_leaderboard(directory):
    prefix = "leaderboard_table"
    suffix = ".table.json"
    
    leaderboard = None

    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.startswith(prefix) and filename.endswith(suffix):
                leaderboard = os.path.join(root, filename)
    
    if leaderboard:
        print(f"found leaderboard table file {leaderboard}")
        try:
            with open(leaderboard, 'r', encoding='utf-8') as file:
                json_data = json.load(file)
                return json_data
        except json.JSONDecodeError as e:
            print(f"failed to parse leaderboard json file: {e}")
        except Exception as e:
            print(f"error: {e}")
    else:
        assert False, f"cannot find leaderboard_table in {directory}"


def json_to_csv(data, output):
    columns = data['columns']
    values = data['data'][0]

    with open(output, mode='w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(columns)
        csv_writer.writerow(values)

    print(f'saved leaderboard to {output}')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("run", type=str, help="wandb run")
    parser.add_argument("csv", type=str, help="output csv file")
    args = parser.parse_args()

    json_to_csv(find_and_read_leaderboard(args.run), args.csv) 