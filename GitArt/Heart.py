import os
import subprocess
import datetime
import time

from config import MARKED_DAYS, HEADER, HEART


class ErrorMessage(Exception):

    """
        Exceptions for GitHeart class
    """

    def __init__(self, msg):
        """
            Initializes exceptions class with a custom message
        """
        self.value = msg

    def __str__(self):
        """
            Returns a custom message
        """
        return repr(self.value)


class GitHeart(object):

    """
        Main Class to Make a Heart on Your GitHub Profiles' Contribution Summary
    """

    def get_end_date(self):
        """
            Returns the end_date on which the Heart's Right center boundary will be.
            i.e:
                                              **   **
                                            *    *    *
                                            *         * <------- This point
                                              *     *
                                                 *
        """
        try:
            today = datetime.date.today()
            end_date = today + \
                datetime.timedelta(
                    days=-1*today.weekday()+2, weeks=-self.weeks_from_now)
            return end_date
        except Exception as e:
            msg = "Please enter the 'weeks_from_now' as Int, Error: " + str(e)
            raise ErrorMessage(msg)

    def create_heart(self, git_repo_url, max_commits=10, weeks_from_now=1):
        """
            Creates heart on the Summary.
            Args:
                git_repo_url: The url (ssh or https) of the Repository, used for cloning
                max_commits: Maximum number of commits in a day
                weeks_from_now: The number of week from this week the Heart's Right center boundary will be. 
        """
        self.weeks_from_now = weeks_from_now
        self.end_date = self.get_end_date()
        try:
            self.repository_name = git_repo_url.split('/')[-1][:-4]
            self.git_repo_url = git_repo_url
            self.max_commits = max_commits
            self.do_commits()
            self.do_commit_amends()
        except IndexError as ie:
            raise ErrorMessage(
                "Please provide the correct URL for the Repository")
        except Exception as e:
            raise ErrorMessage(str(e))

    def append_onto_file(self, file_name, msg):
        """
            Appends msg onto the Given File
        """
        with open(file_name, "a") as heart_file:
            heart_file.write(msg)
            heart_file.close()

    def do_commits(self):
        """
            Perform len(MARKED_DAYS)*self.max_commits and Push to the Repository
        """
        git_clone_command = "git clone " + str(self.git_repo_url)
        subprocess.call(git_clone_command, shell=True)
        subprocess.check_call(
            ['touch', 'gitHeart.txt'], cwd=self.repository_name)
        self.append_onto_file(self.repository_name+"/gitHeart.txt", HEADER)
        subprocess.check_call(
            ['git', 'add', 'gitHeart.txt'], cwd=self.repository_name)
        subprocess.check_call(
            ['git', 'commit', '-m', '"Commit Number 0"'], cwd=self.repository_name)
        for commit_number in range(1, len(MARKED_DAYS)*self.max_commits+1):
            heart_msg = HEART.format(commit_number=str(commit_number))
            self.append_onto_file(
                self.repository_name+"/gitHeart.txt", heart_msg)
            subprocess.check_call(
                ['git', 'add', 'gitHeart.txt'], cwd=self.repository_name)
            subprocess.check_call(['git', 'commit', '-m', '"Commit Number {commit_number}"'.format(
                commit_number=commit_number)], cwd=self.repository_name)
        subprocess.check_call(
            ['git', 'push', 'origin', 'master'], cwd=self.repository_name)

    def do_commit_amends(self):
        """
            Amends the Commit to form the heart
        """
        commit_cumalative_count = 0
        for days in MARKED_DAYS:
            amend_date = (
                self.end_date - datetime.timedelta(days)).strftime("%Y-%m-%d %H:%M:%S")
            for commit_number_in_a_day in xrange(0, self.max_commits):
                commit_cumalative_count += 1
                subprocess.check_call(
                    ['git', 'commit', '--amend', "--date='<" + amend_date + " + 0530 >' ", '-C',
                     'HEAD~{commit_number}'.format(commit_number=commit_cumalative_count)], cwd=self.repository_name)
                subprocess.check_call(
                    ['git', 'pull', '--no-edit'], cwd=self.repository_name)
                subprocess.check_call(
                    ['git', 'push', 'origin', 'master'], cwd=self.repository_name)
