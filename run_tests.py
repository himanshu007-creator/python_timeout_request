import logging
import subprocess

logging.basicConfig(filename='test_results.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def run_tests():
    try:
        result = subprocess.run(['pytest', '-v', 'tests'], capture_output=True, text=True)
        
        sync_passed = "test_sync_function_timeout PASSED" in result.stdout and "test_sync_function_success PASSED" in result.stdout
        async_passed = "test_async_function_timeout PASSED" in result.stdout and "test_async_function_success PASSED" in result.stdout
        
        if sync_passed:
            logging.info("✓ Sync decorator passed")
            print("✓ Sync decorator passed")
        else:
            logging.error("✗ Sync decorator failed")
            print("✗ Sync decorator failed")
        
        if async_passed:
            logging.info("✓ Async decorator passed")
            print("✓ Async decorator passed")
        else:
            logging.error("✗ Async decorator failed")
            print("✗ Async decorator failed")
        
        if sync_passed and async_passed:
            logging.info("✓ All checks passed")
            print("✓ All checks passed")
        else:
            logging.error("✗ Some checks failed")
            print("✗ Some checks failed")
        
        logging.info(f"Full test output:\n{result.stdout}")
        
        if result.returncode != 0:
            logging.error(f"Error output:\n{result.stderr}")
    except Exception as e:
        logging.error(f"An error occurred while running tests: {str(e)}")
        print(f"An error occurred while running tests: {str(e)}")

if __name__ == "__main__":
    run_tests()