import os
import unittest


class PollReader():
    """
    A class for reading and analyzing polling data.
    """
    def __init__(self, filename):
        """
        The constructor. Opens up the specified file, reads in the data,
        closes the file handler, and sets up the data dictionary that will be
        populated with build_data_dict().

        We have implemented this for you. You should not need to modify it.
        """

        # this is used to get the base path that this Python file is in in an
        # OS agnostic way since Windows and Mac/Linux use different formats
        # for file paths, the os library allows us to write code that works
        # well on any operating system
        self.base_path = os.path.abspath(os.path.dirname(__file__))

        # join the base path with the passed filename
        self.full_path = os.path.join(self.base_path, filename)

        # open up the file handler
        self.file_obj = open(self.full_path, 'r')

        # read in each line of the file to a list
        self.raw_data = self.file_obj.readlines()

        # close the file handler
        self.file_obj.close()

        # set up the data dict that we will fill in later
        self.data_dict = {
            'month': [],
            'date': [],
            'sample': [],
            'sample type': [],
            'Harris result': [],
            'Trump result': []
        }

    def build_data_dict(self):
        """
        Reads all of the raw data from the CSV and builds a dictionary where
        each key is the name of a column in the CSV, and each value is a list
        containing the data for each row under that column heading.

        There may be a couple bugs in this that you will need to fix.
        Remember that the first row of a CSV contains all of the column names,
        and each value in a CSV is seperated by a comma.
        """

        # iterate through each row of the data
        for i in self.raw_data[1:]:
            # split up the row by column
            parts = i.strip().split(',')  

            month = parts[0]
            date = int(parts[1])

            sample_with_type = parts[2].strip()   
            sample_num_str, sample_type = sample_with_type.split()
            sample = int(sample_num_str)

            harris = float(parts[3])
            trump = float(parts[4])

            # map each part of the row to the correct column
            self.data_dict['month'].append(month)
            self.data_dict['date'].append(date)
            self.data_dict['sample'].append(sample)
            self.data_dict['sample type'].append(sample_type)
            self.data_dict['Harris result'].append(harris)
            self.data_dict['Trump result'].append(trump)


    def highest_polling_candidate(self):
        """
        This method should iterate through the result columns and return
        the name of the candidate with the highest single polling percentage
        alongside the highest single polling percentage.
        If equal, return the highest single polling percentage and "EVEN".

        Returns:
            str: A string indicating the candidate with the highest polling percentage or EVEN,
             and the highest polling percentage.
        """
        max_h = max(self.data_dict['Harris result'])
        max_t = max(self.data_dict['Trump result'])

        if abs(max_h - max_t) < 1e-12:
            return f"EVEN {max_h*100:.1f}%"
        elif max_h > max_t:
            return f"Harris {max_h*100:.1f}%"
        else:
            return f"Trump {max_t*100:.1f}%"


    def likely_voter_polling_average(self):
        """
        Calculate the average polling percentage for each candidate among likely voters.

        Returns:
            tuple: A tuple containing the average polling percentages for Harris and Trump
                   among likely voters, in that order.
        """
        h_vals, t_vals = [], []
        for st, h, t in zip(self.data_dict['sample type'],
                        self.data_dict['Harris result'],
                        self.data_dict['Trump result']):
            if st == 'LV':
                h_vals.append(h)
                t_vals.append(t)

        h_avg = sum(h_vals) / len(h_vals) if h_vals else 0.0
        t_avg = sum(t_vals) / len(t_vals) if t_vals else 0.0
        return h_avg, t_avg


    def polling_history_change(self):
        """
        Calculate the change in polling averages between the earliest and latest polls.

        This method calculates the average result for each candidate in the earliest 30 polls
        and the latest 30 polls, then returns the net change.

        Returns:
            tuple: A tuple containing the net change for Harris and Trump, in that order.
                   Positive values indicate an increase, negative values indicate a decrease.
        """
        h = self.data_dict['Harris result']
        t = self.data_dict['Trump result']

        latest_h = h[:30]
        latest_t = t[:30]
        earliest_h = h[-30:]
        earliest_t = t[-30:]

        latest_h_avg = sum(latest_h) / len(latest_h) if latest_h else 0.0
        earliest_h_avg = sum(earliest_h) / len(earliest_h) if earliest_h else 0.0

        latest_t_avg = sum(latest_t) / len(latest_t) if latest_t else 0.0
        earliest_t_avg = sum(earliest_t) / len(earliest_t) if earliest_t else 0.0

        return (latest_h_avg - earliest_h_avg, latest_t_avg - earliest_t_avg)


class TestPollReader(unittest.TestCase):
    """
    Test cases for the PollReader class.
    """
    def setUp(self):
        self.poll_reader = PollReader('polling_data.csv')
        self.poll_reader.build_data_dict()

    def test_build_data_dict(self):
        self.assertEqual(len(self.poll_reader.data_dict['date']), len(self.poll_reader.data_dict['sample']))
        self.assertTrue(all(isinstance(x, int) for x in self.poll_reader.data_dict['date']))
        self.assertTrue(all(isinstance(x, int) for x in self.poll_reader.data_dict['sample']))
        self.assertTrue(all(isinstance(x, str) for x in self.poll_reader.data_dict['sample type']))
        self.assertTrue(all(isinstance(x, float) for x in self.poll_reader.data_dict['Harris result']))
        self.assertTrue(all(isinstance(x, float) for x in self.poll_reader.data_dict['Trump result']))

    def test_highest_polling_candidate(self):
        result = self.poll_reader.highest_polling_candidate()
        self.assertTrue(isinstance(result, str))
        self.assertTrue("Harris" in result)
        self.assertTrue("57.0%" in result)

    def test_likely_voter_polling_average(self):
        harris_avg, trump_avg = self.poll_reader.likely_voter_polling_average()
        self.assertTrue(isinstance(harris_avg, float))
        self.assertTrue(isinstance(trump_avg, float))
        self.assertTrue(f"{harris_avg:.2%}" == "49.34%")
        self.assertTrue(f"{trump_avg:.2%}" == "46.04%")

    def test_polling_history_change(self):
        harris_change, trump_change = self.poll_reader.polling_history_change()
        self.assertTrue(isinstance(harris_change, float))
        self.assertTrue(isinstance(trump_change, float))
        self.assertTrue(f"{harris_change:+.2%}" == "+1.53%")
        self.assertTrue(f"{trump_change:+.2%}" == "+2.07%")


def main():
    poll_reader = PollReader('polling_data.csv')
    poll_reader.build_data_dict()

    highest_polling = poll_reader.highest_polling_candidate()
    print(f"Highest Polling Candidate: {highest_polling}")
    
    harris_avg, trump_avg = poll_reader.likely_voter_polling_average()
    print(f"Likely Voter Polling Average:")
    print(f"  Harris: {harris_avg:.2%}")
    print(f"  Trump: {trump_avg:.2%}")
    
    harris_change, trump_change = poll_reader.polling_history_change()
    print(f"Polling History Change:")
    print(f"  Harris: {harris_change:+.2%}")
    print(f"  Trump: {trump_change:+.2%}")



if __name__ == '__main__':
    main()
    unittest.main(verbosity=2)