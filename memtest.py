import os


# Run each test case
def test_run(test_file_name):
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


def special_test_run(test_file_name, word_count_enabled=False, frequency_count_enabled=False, frequency_word=""):
    command = "valgrind --leak-check=full ./html_parser "
    if word_count_enabled:
        command += "-c "
    if frequency_count_enabled:
        command += "-f {} ".format(frequency_word)
    command += "test_cases/{}.html output_test.txt".format(test_file_name)

    print("Run: {}".format(command))
    os.system(command)


def main():
    test_suite_run("discord_test")
    test_suite_run("handout_test")
    test_suite_run("self_test")
    test_suite_run("cw_test")

    # Define special tests here
    special_test_run("discord_test_1", word_count_enabled=True)
    special_test_run("discord_test_1", word_count_enabled=True, frequency_count_enabled=True,
                     frequency_word="document")
    special_test_run("handout_test_4", word_count_enabled=True)
    special_test_run("handout_test_4", word_count_enabled=True, frequency_count_enabled=True,
                     frequency_word="Heading")
    special_test_run("cw_test_1", word_count_enabled=True)
    special_test_run("cw_test_2", word_count_enabled=True)

    print("Finished running all valgrind tests. Review the output for any memory leaks.")

    # Clean up output file
    os.remove("output_test.txt")


if __name__ == "__main__":
    main()
