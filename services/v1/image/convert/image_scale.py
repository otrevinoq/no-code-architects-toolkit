import os
import subprocess
import logging
from services.file_management import download_file
from PIL import Image
from config import LOCAL_STORAGE_PATH

logger = logging.getLogger(__name__)

def scale_image(image_url, width, height):
    try:
        # Download the image file
        image_path = download_file(image_url, LOCAL_STORAGE_PATH)
        logger.info(f"Downloaded image to {image_path}")

        # Prepare the output path
        output_path = os.path.join(LOCAL_STORAGE_PATH, f"scaled_{os.path.basename(image_path)}")

        # Prepare FFmpeg command for scaling
        cmd = [
            'ffmpeg', '-i', image_path,
            '-vf', f"scale={width}:{height}", output_path
           # '-c:v', 'libx264', '-pix_fmt', 'yuv420p', output_path
        ]

        logger.info(f"Running FFmpeg command: {' '.join(cmd)}")

        # Run FFmpeg command
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            logger.error(f"FFmpeg command failed. Error: {result.stderr}")
            raise subprocess.CalledProcessError(result.returncode, cmd, result.stdout, result.stderr)

        logger.info(f"Image scaled successfully: {output_path}")

        # Clean up input file
        os.remove(image_path)

        return output_path
    except Exception as e:
        logger.error(f"Error in scale_image: {str(e)}", exc_info=True)
        raise
