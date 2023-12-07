import os
import sys
import shutil


def build(
        output_folder: str = "build",
        output_file: str = "krita_text_tool.zip",
):
    # Build the project
    # zip the project using git
    zip_command = f"git archive -o {output_file} HEAD"
    os.system(zip_command)
    # copy the zip file to the output folder
    os.makedirs(output_folder, exist_ok=True)
    shutil.move(output_file, os.path.join(output_folder, output_file))

    pass


if __name__ == "__main__":
    build()
