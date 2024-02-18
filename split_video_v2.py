#!/usr/bin/env python
"""Generic video data processing script for Visual Inspection."""
import os
import argparse
import cv2


def extract_images(data_folder, path_out):
    curated_data_path = os.path.join('.', data_folder)
    for root, dirnames, filenames in os.walk(curated_data_path):
        for dirname in dirnames:
            component_folder_path = os.path.join(root, dirname)
            rel_path = os.path.relpath(component_folder_path, curated_data_path)
            component_folder_out = os.path.join(path_out, rel_path)
            print("component_folder_out", component_folder_out)
            os.makedirs(component_folder_out, exist_ok=True)

            component_filenames = os.listdir(component_folder_path)
            for filename in component_filenames:
                file_path = os.path.join(component_folder_path, filename)
                if os.path.isfile(file_path) and filename.endswith((".MOV", ".mp4")):
                    vidcap = cv2.VideoCapture(file_path)
                    fps = vidcap.get(cv2.CAP_PROP_FPS)
                    frame_interval = int(fps) # Split video into 1-second frames

                    frame_folder_out = os.path.join(component_folder_out, os.path.splitext(filename)[0])
                    os.makedirs(frame_folder_out, exist_ok=True)

                    frame_count = 0
                    success, image = vidcap.read()

                    while success:
                        if frame_count % frame_interval == 0:
                            frame_path = os.path.join(frame_folder_out, f"{filename}_frame_{frame_count // frame_interval}.jpg")
                            cv2.imwrite(frame_path, image)  # save frames

                        frame_count += 1
                        success, image = vidcap.read()


if __name__ == "__main__":
    arg = argparse.ArgumentParser()
    arg.add_argument("--data_folder", help="path to curated_data folder")
    arg.add_argument("--path_out", help="path to output images")
    args = arg.parse_args()
    extract_images(args.data_folder, args.path_out)
