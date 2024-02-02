Set-Location -Path ("full path do job scraper")
$scraper = Start-Process python -ArgumentList "scripts\main_nostreamlit.py --job main_job_scraper --match resume_data_processor" -NoNewWindow -PassThru
$scraper

Stop-Process -Id $scraper.Id