from app import processMap
import sys
import contextlib
from io import StringIO

def compare_results_with_file(processed_results, file_path):
    
    try:
        with open(file_path, "r") as file:
            file_lines = file.readlines()
            
            # Ensure the number of lines in the file matches the number of lists in the processed results
            if len(file_lines) != len(processed_results):
                print(f"Mismatch: {file_path} has {len(file_lines)} lines but processed results have {len(processed_results)} lists.")
                return
            
            total_elements = 0
            matching_elements = 0
            
            # Compare each line in the file with the corresponding list from processed_results
            for i, (line, result_list) in enumerate(zip(file_lines, processed_results)):
                # Split the line into strings and compare with the result list
                file_strings = line.strip().split()
                
                # Count total elements and matching elements
                total_elements += len(file_strings)
                matching_elements += sum(1 for file_string, result_string in zip(file_strings, result_list) if file_string == result_string)
                
                if file_strings != result_list:
                    print(f"Mismatch in line {i + 1}:")
                    print(f"  File:   {file_strings}")
                    print(f"  Result: {result_list}")
                else:
                    print(f"Line {i + 1}: Match")
            
            # Calculate and print the percentage of matches
            if total_elements > 0:
                match_percentage = (matching_elements / total_elements) * 100
                print(f"Total Elements: {total_elements}")
                print(f"Matching Elements: {matching_elements}")
                print(f"Match Percentage: {match_percentage:.2f}%")
            else:
                print("No elements to compare.")
    
    except FileNotFoundError:
        print(f"File {file_path} not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


def test_requests_from_file(file_path=r"C:\Users\acvcl\Documents\GitHub\AtlasOfMystara\Backend\tests\request_history.txt"):
    try:
        with open(file_path, "r") as file:
            for line in file:
                # Strip newline characters and split the line into arguments
                args = line.strip().split()
                
                # Unpack the arguments and call processMap
                if len(args) == 6:  # Ensure there are exactly 6 arguments
                    title, author, image_data, hex_mask_type, selected_color, combined_image = args
                    with contextlib.redirect_stdout(StringIO()):
                        processed_results = processMap(title, author, image_data, hex_mask_type, selected_color, combined_image, True)
                    
                    print("results have been processed")
                    # Compare the results with the corresponding title.txt file
                    base_path = r"C:\Users\acvcl\Documents\GitHub\AtlasOfMystara\Backend\tests\absolute_truth"
                    absolute_truth_path = f"{base_path}\\{title}.txt"
                    compare_results_with_file(processed_results, absolute_truth_path)
                else:
                    print(f"Skipping invalid line")
                    for i in range(len(args)):
                        print("Argument " + str(i))
                        print(args[i][:20])
                        print("\n")
    except FileNotFoundError:
        print(f"File {file_path} not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    test_requests_from_file()
