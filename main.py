import argparse
import subprocess
import os
import sys
import time

def run_job(job_name):
    subprocess.run(["python", os.path.join("app", f"{job_name}.py")])

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--job',
        choices=['main_job_scraper', 'job_scraper_scheduler'],
        default='main_job_scraper',
    )
    parser.add_argument(
        '--interval',
        type=int,
    )
    
    if 'main_job_scraper' in sys.argv:
        parser.add_argument(
            '--match',
            choices=['main_resume_matcher']
        )

    args = parser.parse_args()

    if args.job == 'job_scraper_scheduler':
        if (args.interval is None or args.interval >= 90):
            run_job(args.job)
    elif args.job == 'main_job_scraper':
        if hasattr(args, 'match') and args.match == 'main_resume_matcher':
            run_job(args.job)
            time.sleep(60)
            run_job(args.match)

        run_job(args.job)
    else:
        print("Use main_job_scraper or job_scraper_scheduler.")
