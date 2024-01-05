import argparse
import subprocess
import os
import time 

def run_job(job_name):
    subprocess.run(["python", os.path.join("app", f"{job_name}.py")])

def run_jobs(args):
    if args.job == 'main_job_scraper':
        if args.match:
            run_job(args.job)
            time.sleep(5)
            run_job(args.match)
        else:
            run_job(args.job)
    elif args.job == 'job_scraper_scheduler':
        if args.interval is None or args.interval >= 90:
            run_job(args.job)
    else:
        print("Use main_job_scraper or job_scraper_scheduler.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--job',
        choices=['main_job_scraper', 'job_scraper_scheduler'],
        default='main_job_scraper',
        help='Specify the job to run'
    )
    parser.add_argument(
        '--interval',
        type=int,
        help='Specify the interval for job_scraper_scheduler'
    )
    parser.add_argument(
        '--match',
        choices=['main_resume_matcher'],
        help='Specify the matching job to run after main_job_scraper'
    )

    args = parser.parse_args()
    run_jobs(args)
