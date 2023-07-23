import unittest


def run_tests():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover(start_dir='.', pattern='test_*.py')
    print(test_suite)
    test_runner = unittest.TextTestRunner(verbosity=2)
    test_result = test_runner.run(test_suite)

    if test_result.wasSuccessful():
        return 0
    return 1


if __name__ == "__main__":
    exit_code = run_tests()
    exit(exit_code)
