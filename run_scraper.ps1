Set-Location -Path ("Full path")
$scraper = Start-Process python -ArgumentList "scripts\main_nostreamlit.py --job main_job_scraper --match resume_data_processor" -NoNewWindow -PassThru -Wait
$scraper

Stop-Process -Id $scraper.Id
