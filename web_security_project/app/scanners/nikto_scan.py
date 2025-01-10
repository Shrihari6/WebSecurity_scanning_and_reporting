import os
import subprocess
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_nikto(target):
    """
    Run Nikto scan on the given target and save the result to a file.
    """
    result_file = f"app/static/reports/nikto_{target.replace('.', '_')}.txt"
    try:
        command = ["nikto", "-h", target]
        logger.info(f"Running Nikto scan on target: {target}")
        result = subprocess.check_output(command, universal_newlines=True)
        
        # Save result to file
        with open(result_file, "w") as file:
            file.write(result)
        logger.info(f"Nikto scan completed. Result saved to {result_file}")
        return result_file
    except subprocess.CalledProcessError as e:
        error_message = f"Subprocess error: {str(e)}"
        logger.error(error_message)
        return error_message
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        logger.error(error_message)
        return error_message
