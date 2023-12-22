import argparse
import subprocess
import os


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

    args = parser.parse_args()

    if args.job == 'job_scraper_scheduler':
        if (args.interval is None or args.interval >= 90):
            run_job(args.job)
    elif args.job == 'main_job_scraper':
        run_job(args.job)
    else:
        print("Use main_job_scraper or job_scraper_scheduler.")