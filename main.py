import requests
import json
import os


class MakeDir:
    def __init__(self):
        self.dir_name = "BountyData"
        self.files = ["wildscope.txt", "all-targets.txt", "data.json"]

    def create_dir(self):
        # If the directory is not created, create it with the required files
        if not os.path.exists(self.dir_name):
            os.mkdir(self.dir_name)
            for file in self.files:
                with open(os.path.join(self.dir_name, file), "w", encoding="utf-8"):
                    pass
        # If the directory exists, check if each file is present, create if missing
        else:
            for file in self.files:
                file_path = os.path.join(self.dir_name, file)
                if not os.path.isfile(file_path):
                    with open(file_path, "w", encoding="utf-8"):
                        pass


class FetchData:
    def __init__(self):
        self.url = "https://raw.githubusercontent.com/arkadiyt/bounty-targets-data/refs/heads/main/data/bugcrowd_data.json"

    def extract_targets(self):
        response = requests.get(self.url)
        try:
            if response.status_code == 200:
                fetched_data_path = "BountyData/data.json"
                targets_path = "BountyData/all-targets.txt"

                # Save fetched data to data.json
                with open(fetched_data_path, "w", encoding="utf-8") as data_file:
                    json.dump(response.json(), data_file, indent=4)  # Save the raw data

                # Extract in-scope targets
                self.process_data(response.json(), targets_path)
            else:
                print(f"Failed to fetch data. Status code: {response.status_code}")
        except Exception as e:
            print(f"Error occurred: {e}")

    def process_data(self, data, targets_path):
        try:
            in_scope_targets = []

            # Assuming each entry in the JSON represents a target program
            for program in data:
                if 'targets' in program and 'in_scope' in program['targets']:
                    in_scope_list = program['targets']['in_scope']

                    # Add all in-scope targets to all-targets.txt
                    for target in in_scope_list:
                        in_scope_targets.append(target['target'])

            # Write all in-scope targets to all-targets.txt with UTF-8 encoding
            with open(targets_path, "w", encoding="utf-8") as targets_file:
                for target in in_scope_targets:
                    targets_file.write(target + "\n")

            print(f"All in-scope targets successfully saved to {targets_path}.")
        except Exception as e:
            print(f"Error processing data: {e}")


class ProcessTargets:
    def __init__(self):
        self.all_targets_path = "BountyData/all-targets.txt"
        self.wildscope_path = "BountyData/wildscope.txt"

    def extract_wildscope(self):
        try:
            # Check if all-targets.txt exists
            if not os.path.isfile(self.all_targets_path):
                print(f"{self.all_targets_path} does not exist.")
                return

            wildscope_targets = []

            # Read all-targets.txt and find targets containing "*."
            with open(self.all_targets_path, "r", encoding="utf-8") as all_targets_file:
                for line in all_targets_file:
                    if "*." in line:  # Check for wildcard
                        wildscope_targets.append(line.strip())

            # Write wildcard targets to wildscope.txt
            with open(self.wildscope_path, "w", encoding="utf-8") as wildscope_file:
                for target in wildscope_targets:
                    wildscope_file.write(target + "\n")

            print(f"Wildscope targets successfully extracted to {self.wildscope_path}.")
        except Exception as e:
            print(f"Error processing targets: {e}")


def main():
    # Step 1: Create directories and files
    make_dir = MakeDir()
    make_dir.create_dir()

    # Step 2: Fetch and extract in-scope targets
    fetch_data = FetchData()
    fetch_data.extract_targets()

    # Step 3: Extract wildscope targets from all-targets.txt
    process_targets = ProcessTargets()
    process_targets.extract_wildscope()


if __name__ == "__main__":
    main()
