# Use the caller's Python (including an activated virtual environment).
$studyRuntime = (Get-Command python -ErrorAction Stop).Source
& $studyRuntime -X utf8 (Join-Path $PSScriptRoot 'study.py') @args
exit $LASTEXITCODE
