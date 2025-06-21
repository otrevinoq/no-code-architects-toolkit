# Copyright (c) 2025 Stephen G. Pope
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import os
import shutil
import logging
from pathlib import Path

# Configure logging
logger = logging.getLogger(__name__)

def copy_to_storage(file_path: str) -> str:
    """Copy file to local storage and return its URL.
    
    Args:
        file_path: Path to the file to be copied
        
    Returns:
        str: Public URL of the copied file
    """
    try:
        storage_path = os.getenv('LOCAL_RESULT_STORAGE_PATH')
        base_url = os.getenv('LOCAL_RESULT_STORAGE_URL')
        
        # Ensure storage directory exists
        Path(storage_path).mkdir(parents=True, exist_ok=True)
        
        # Extract filename without extension
        filename = os.path.basename(file_path)
        file_stem = Path(filename).stem
        
        # Create a directory named after the file (without extension)
        file_dir_path = os.path.join(storage_path, file_stem)
        Path(file_dir_path).mkdir(parents=True, exist_ok=True)
        
        # Copy file to the new directory
        dest_path = os.path.join(file_dir_path, filename)
        shutil.copy2(file_path, dest_path)
        
        # Build and return URL
        return f"{base_url}/{file_stem}/{filename}"
        
    except Exception as e:
        logger.error(f"Error copying file to local storage: {e}")
        raise
