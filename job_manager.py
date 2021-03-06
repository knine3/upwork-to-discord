from job import Job
from datetime import datetime


class JobManager:
    def __init__(self, rss, state):
        self.rss = rss
        self.state = state

    def refresh_feed(self):
        self.rss.parse_feed()

    def new_jobs_available(self):
        self.refresh_feed()
        last_link = self.state.get_value('last_link')

        if last_link is False:
            return True

        current_last_link = self.rss.feed['entries'][0]['link']
        if current_last_link == last_link:
            return False
        else:
            return True

    def print_time(self):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print()
        print(" @ ", current_time)

    def get_new_jobs(self):
        self.print_time()
        if not self.new_jobs_available():
            print('[-] No new jobs available, waiting...')
            return []

        last_link = self.state.get_value('last_link')
        jobs = self.rss.feed['entries']

        #+------------------------------------------+
        #|      CASE I: if no last_link in states   |
        #+------------------------------------------+
        if not last_link:
            self.state.add_value('last_link', jobs[0].link)
            return Job.create_from_list(jobs)

        new_jobs = 0
        
        #+---------------------------------------------+
        #|CASE II: last_link not equal to current_last |
        #+---------------------------------------------+
        for job in jobs:
            if job['link'] != last_link:
                new_jobs += 1
            else:
                print(f'[+] Find new jobs: {new_jobs}')
                self.state.add_value('last_link', jobs[0].link)
                jobs = jobs[:new_jobs]
                return Job.create_from_list(jobs)