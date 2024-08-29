from app import processMap
import sys
import contextlib
from io import StringIO

def compare_results_with_file(processed_results, file_path, output_path):
    try:
        with open(file_path, "r") as file:
            file_lines = file.readlines()
            
            # Ensure the number of lines in the file matches the number of lists in the processed_results
            if len(file_lines) != len(processed_results):
                with open(output_path, "w") as output_file:
                    output_file.write(f"Mismatch: {file_path} has {len(file_lines)} lines but processed results have {len(processed_results)} lists.\n")
                return
            
            total_elements = 0
            matching_elements = 0
            
            # Open the output file for writing
            with open(output_path, "w") as output_file:
                
                # Compare each line in the file with the corresponding list from processed_results
                for i, (line, result_list) in enumerate(zip(file_lines, processed_results)):
                    # Split the line into strings and compare with the result list
                    file_strings = line.strip().split()
                    
                    # Count total elements and matching elements
                    total_elements += len(file_strings)
                    matching_elements += sum(1 for file_string, result_string in zip(file_strings, result_list) if file_string == result_string)
                    
                    if file_strings != result_list:
                        output_file.write(f"Mismatch in line {i + 1}:\n")
                        output_file.write(f"  File:   {file_strings}\n")
                        output_file.write(f"  Result: {result_list}\n")
                    else:
                        output_file.write(f"Line {i + 1}: Match\n")
                
                # Calculate and write the percentage of matches
                if total_elements > 0:
                    match_percentage = (matching_elements / total_elements) * 100
                    output_file.write(f"Total Elements: {total_elements}\n")
                    output_file.write(f"Matching Elements: {matching_elements}\n")
                    output_file.write(f"Match Percentage: {match_percentage:.2f}%\n")
                else:
                    output_file.write("No elements to compare.\n")
    
    except FileNotFoundError:
        with open(output_path, "w") as output_file:
            output_file.write(f"File {file_path} not found.\n")
    except Exception as e:
        with open(output_path, "w") as output_file:
            output_file.write(f"An error occurred: {str(e)}\n")



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

                    """
                    [MSE, PSNR, SSIM, ORB, PHash, Template Matching, Contour Matching, ChiSquare, Bhattacharyya Distance, 
                    majority, intersection, ranking, confidence, weighted, combined]
                    """
                    output_folder = r"tests\test_results"
                    algorythm = ["MSE", "PSNR", "SSIM", "ORB", "PHash", "Template_Matching", "Contour_Matching", "ChiSquare", "Bhattacharyya_Distance", "Majority", "Intersection", "Ranking", "Confidence", "Weighted", "Combined"]
                    i = 0
                    for result in processed_results:
                        output_path =f"{output_folder}\\{title}\\{algorythm[i]}_result.txt"
                        compare_results_with_file(result, absolute_truth_path, output_path)
                        i += 1
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
