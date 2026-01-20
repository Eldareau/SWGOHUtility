import unittest
import sys
import os

def run_all_tests():
    # Ensure current directory is in sys.path
    project_root = os.path.abspath(os.path.dirname(__file__))
    if project_root not in sys.path:
        sys.path.append(project_root)
    
    # Define test directory
    test_dir = os.path.join(project_root)
    
    # Discover all tests
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=test_dir, pattern='test_*.py')
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Exit with code 1 if failed, 0 if success
    if not result.wasSuccessful():
        sys.exit(1)
        
if __name__ == "__main__":
    run_all_tests()
