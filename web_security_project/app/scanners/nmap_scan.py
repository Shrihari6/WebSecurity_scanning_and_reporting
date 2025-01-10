import os
import subprocess
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_nmap(target):
    """
    Run an Nmap scan on the given target and save the result to a file.
    """
    # Replace invalid characters in the filename
    sanitized_target = target.replace('.', '_').replace(':', '_').replace('/', '_')
    report_name = f"nmap_{sanitized_target}.txt"
    report_path = os.path.join("app", "static", "reports", report_name)

    # Ensure the reports directory exists
    os.makedirs(os.path.dirname(report_path), exist_ok=True)

    try:
        # Run the Nmap command and save the output directly to the file
        logger.info(f"Running Nmap scan on {target} and saving results to {report_path}")
        subprocess.run(["nmap", "-A", target, "-oN", report_path], check=True)
        logger.info(f"Nmap scan completed successfully. Results saved to {report_path}")
        return report_path
    except subprocess.CalledProcessError as e:
        error_message = f"Nmap scan failed with error: {e}"
        logger.error(error_message)
        return error_message
    except FileNotFoundError as e:
        error_message = f"Error: Nmap command not found. Ensure Nmap is installed. {e}"
        logger.error(error_message)
        return error_message
    except Exception as e:
        error_message = f"Unexpected error during Nmap scan: {e}"
        logger.error(error_message)
        return error_message
