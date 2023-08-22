# This is a sample Python script.
import sys

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import cv2
import os
import argparse
from os import listdir

import subprocess #for creating a new shell


segment_anything_command = "conda activate segmentor; cd ~/ki/segment-anything/segment-anything/; python scripts/amg.py --checkpoint ../segment-anything-ui/sam_vit_h_4b8939.pth --model-type vit_h --crop-n-layers 1 --input __REPLACE_INPUT_FOLDER__ --output __REPLACE_OUTPUT_FOLDER__"

def invert_image(filename,outputfolder):
    # Use a breakpoint in the code line below to debug your script.
    img = cv2.imread(filename)
    v_image = ~img

    filename_without_path = os.path.basename(filename)

    if(outputfolder[-1] != '/'):
        outputfolder = outputfolder + "/"

    inverted_filename = "inverted_"+filename_without_path

    cv2.imwrite(outputfolder+inverted_filename,v_image)
    return inverted_filename

def createSegmentAnythingCommand(input,output):
    global  segment_anything_command
    segment_anything_command = segment_anything_command.replace("__REPLACE_INPUT_FOLDER__", input).replace("__REPLACE_OUTPUT_FOLDER__", output)
    return segment_anything_command

def createClassifierCommand(command, input,output,fileid):
    command = command.replace("__REPLACE_INPUT_FOLDER__", input).replace("__REPLACE_OUTPUT_FOLDER__", output).replace("__ID__", fileid)
    return command



# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Controll Segment Anything.')

    parser.add_argument('--image_folder', help='folder of the images', required=True)
    parser.add_argument('--output_folder', help='folder for the result (crack length)', required=True)
    args = parser.parse_args()

    image_folder = args.image_folder
    output_folder = args.output_folder

    image_folder = os.path.abspath(image_folder)
    output_folder = os.path.abspath(args.output_folder)
    inverted_image_folder = os.path.abspath("inverted")

    segment_anything_command = createSegmentAnythingCommand(inverted_image_folder,output_folder)

    for file in listdir(image_folder):
        print("invert_image("+image_folder+"/"+file+", "+output_folder+")")
        imgname = invert_image(image_folder+"/"+file, inverted_image_folder)

    print(segment_anything_command)

    with open("run.sh", "w") as file:
        file.write(segment_anything_command)
        file.close()

    #os.system(segment_anything_command)

    os.system("bash -i run.sh")
    #p = subprocess.Popen(segment_anything_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    #out = p.communicate()[0]
    #print (out)

    #call segment anything with outputfolder/imgname
    #call csvreader

    counter = 0
    classifier_command = "conda activate csvreader; cd ~/PycharmProjects/csvreader/; python main.py  --image_folder __REPLACE_INPUT_FOLDER__ --output_folder __REPLACE_OUTPUT_FOLDER__ --id __ID__"
    classifier_output_folder = "results"
    classifier_output_folder = os.path.abspath(classifier_output_folder)

    for folder in listdir(output_folder):
        if(os.path.isdir(output_folder+"/"+folder)):
            print("classifier: main.py " + output_folder+"/"+folder+"/metadata.csv")
            fileid = str(counter)
            counter = counter+1
            command = createClassifierCommand(classifier_command,output_folder+"/"+folder, classifier_output_folder, fileid)

            with open("list.txt", "a") as file:
                file.write(folder + ";" + fileid+"\n")
                file.close()

            with open("classifier.sh", "w") as file:
                file.write(command)
                file.close()

            os.system("bash -i classifier.sh")

    #convert the output into the textfile for julian

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
