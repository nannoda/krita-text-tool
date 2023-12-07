import os
import sys
import shutil


def build(
        output_folder: str = "build",
):
    # Build the project
    # zip the project using git
    zip_command = "git archive -o myplugin.zip HEAD"
    os.system(zip_command)
    # copy the zip file to the output folder
    os.makedirs(output_folder, exist_ok=True)
    shutil.move("myplugin.zip", os.path.join(output_folder, "myplugin.zip"))

    pass


if __name__ == "__main__":
    build()
