import os

def merge_txt_files(input_dir, output_file):

    output_dir = os.path.dirname(output_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(output_file, 'w', encoding='utf-8') as outfile:

        for filename in os.listdir(input_dir):
            if filename.endswith('.txt'):
                file_path = os.path.join(input_dir, filename)

                with open(file_path, 'r', encoding='utf-8') as infile:
                    outfile.write(infile.read())

                    outfile.write('\n' + '-'*40 + '\n')

input_directory = 'policy'
output_file = 'merge/merge.txt'

merge_txt_files(input_directory, output_file)