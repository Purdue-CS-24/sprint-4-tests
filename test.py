import os
import subprocess
import sys

test_failed = False
memory_test_enabled = False


def test_run(test_file_name):
    if memory_test_enabled:
        return memtest_run(test_file_name=test_file_name)

    command = "./html_parser test_cases/{}.html output_test.txt".format(test_file_name)
    print("Run: {}".format(command))
    os.system(command)

    global test_failed
    try:
        output = subprocess.check_output("diff -bwuBE output_test.txt test_cases/{}.txt".format(test_file_name),
                                         shell=True)
    except subprocess.CalledProcessError as e:
        # We got a non-zero exit code, a test failed
        test_failed = True
        print(str(e.output, 'utf-8'))
    else:
        if output:
            test_failed = True


def memtest_run(test_file_name):
    command = "valgrind --leak-check=full ./html_parser test_cases/{}.html output_test.txt".format(test_file_name)
    print("Run: {}".format(command))
    os.system(command)


def test_suite_run(test_suite_name):
    # Go over directory and find all test cases that belong in a given suite
    i = 1
    while True:
        if os.path.exists("test_cases/{}_{}.html".format(test_suite_name, i)):
            test_run("{}_{}".format(test_suite_name, i))
            i += 1
        else:
            break


def special_test_run(test_file_name, word_count_enabled=False, frequency_count_enabled=False, frequency_word="",
                     word_count=0, frequency_count=0):
    global test_failed

    if memory_test_enabled:
        return special_memtest_run(test_file_name, word_count_enabled=word_count_enabled,
                                   frequency_count_enabled=frequency_count_enabled, frequency_word=frequency_word)

    command = "./html_parser "
    if word_count_enabled:
        command += "-c "
    if frequency_count_enabled:
        command += "-f {} ".format(frequency_word)
    command += "test_cases/{}.html output_test.txt".format(test_file_name)

    print("Run: {}".format(command))

    try:
        output = subprocess.check_output(command, shell=True)
    except subprocess.CalledProcessError as e:
        # We got a non-zero exit code, a test failed
        test_failed = True
        print(str(e.output, 'utf-8'))
    else:
        if output:
            # Parse output
            output = str(output, 'utf-8')
            if word_count_enabled and frequency_count_enabled:
                import parse
                result = parse.parse('Word Count: {}. {} Frequency: {}.\n', output)
                values = list(result)
                if int(values[0]) != word_count:
                    print("{}: Warning, word count does not match! Expected: {}, Actual: {}."
                          .format(test_file_name, word_count, int(values[0])))
                    test_failed = True
                if int(values[2]) != frequency_count:
                    print("{}: Warning, frequency count does not match! Expected: {}, Actual: {}."
                          .format(test_file_name, frequency_count, int(values[2])))
                    test_failed = True
            elif word_count_enabled:
                import parse
                result = parse.parse('Word Count: {}.\n', output)
                values = list(result)
                if int(values[0]) != word_count:
                    print("{}: Warning, word count does not match! Expected: {}, Actual: {}."
                          .format(test_file_name, word_count, int(values[0])))
                    test_failed = True
            elif frequency_count_enabled:
                import parse
                result = parse.parse('{} Frequency: {}.\n', output)
                values = list(result)
                if int(values[1]) != frequency_count:
                    print("{}: Warning, frequency count does not match! Expected: {}, Actual: {}."
                          .format(test_file_name, frequency_count, int(values[1])))
                    test_failed = True

    try:
        output = subprocess.check_output("diff -bwuBE output_test.txt test_cases/{}.txt".format(test_file_name),
                                         shell=True)
    except subprocess.CalledProcessError as e:
        # We got a non-zero exit code, a test failed
        test_failed = True
        print(str(e.output, 'utf-8'))
    else:
        if output:
            test_failed = True


def special_memtest_run(test_file_name, word_count_enabled=False, frequency_count_enabled=False, frequency_word=""):
    command = "valgrind --leak-check=full ./html_parser "
    if word_count_enabled:
        command += "-c "
    if frequency_count_enabled:
        command += "-f {} ".format(frequency_word)
    command += "test_cases/{}.html output_test.txt".format(test_file_name)

    print("Run: {}".format(command))
    os.system(command)


def memtest_prerequisites_check():
    if sys.platform != "linux":
        print("Warning: this script will only run on Linux distributions.")
        sys.exit(0)
    import distutils.spawn
    if distutils.spawn.find_executable("valgrind") is None:
        print("Warning: cannot find valgrind. This script needs valgrind to run properly.")
        sys.exit(0)


def main():
    global memory_test_enabled

    import argparse
    parser = argparse.ArgumentParser(description='Runs tests for Sprint 4')
    parser.add_argument('-m', '--memory', action='store_true', help='enables memtest mode (with valgrind)')
    args = parser.parse_args()

    if args.memory:
        memtest_prerequisites_check()
        memory_test_enabled = True

    # Define all test cases here \/
    test_suite_run("discord_test")
    test_suite_run("handout_test")
    test_suite_run("self_test")
    test_suite_run("cw_test")
    test_suite_run("cs24_test")

    # Define special tests here \/
    special_test_run("discord_test_1", word_count_enabled=True, word_count=32)
    special_test_run("discord_test_1", word_count_enabled=True, word_count=32, frequency_count_enabled=True,
                     frequency_word="document", frequency_count=3)
    special_test_run("handout_test_4", word_count_enabled=True, word_count=7)
    special_test_run("handout_test_4", word_count_enabled=True, word_count=7, frequency_count_enabled=True,
                     frequency_word="Heading", frequency_count=1)
    special_test_run("cw_test_1", word_count_enabled=True, word_count=3)
    special_test_run("cw_test_2", word_count_enabled=True, word_count=13)

    if memory_test_enabled:
        print("Finished running all valgrind tests. Please manually review the valgrind output for any memory leaks.")
    else:
        if test_failed:
            print("Some tests failed, see the differences above.")
        else:
            print("All the tests passed!")

    # Clean up output file
    os.remove("output_test.txt")


if __name__ == "__main__":
    main()
