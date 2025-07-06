from flask import Blueprint, request, jsonify
from app_utils import *
import logging
from services.v1.image.convert.image_scale import scale_image
from services.authentication import authenticate
from services.cloud_storage import upload_file

image_scale_bp = Blueprint('v1_image_scale', __name__)
logger = logging.getLogger(__name__)

@image_scale_bp.route('/v1/image/convert/image-scale', methods=['POST'])
@authenticate
@validate_payload({
    "type": "object",
    "properties": {
        "image_url": {"type": "string", "format": "uri"},
        "width": {"type": "integer", "minimum": 1},
        "height": {"type": "integer", "minimum": 1}
    },
    "required": ["image_url", "width", "height"],
    "additionalProperties": False
})
def image_scale():
    data = request.get_json()
    image_url = data.get('image_url')
    width = data.get('width')
    height = data.get('height')

    logger.info(f"Received image scaling request for {image_url} with dimensions {width}x{height}")

    try:
        # Process image scaling
        output_filename = scale_image(image_url, width, height)

        # Log the successful scaling
        logger.info(f"Image scaled successfully: {output_filename}")

        # Return the path to the scaled image
        #return jsonify({"scaled_image_path": output_filename}), 200
        cloud_url = upload_file(output_filename)
        logger.info(
            f"Scaled image uploaded to cloud storage: {cloud_url}"
        )

        return jsonify({"local_path": output_filename, "cloud_url":cloud_url}), 200
        
    except Exception as e:
        logger.error(f"Error processing image scaling: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500


