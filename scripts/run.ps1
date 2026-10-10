# Use the Codex document runtime when installed; pass all CLI arguments unchanged.
$studyRuntime = Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
if (-not (Test-Path -LiteralPath $studyRuntime)) {
    $studyRuntime = (Get-Command python -ErrorAction Stop).Source
}
& $studyRuntime -X utf8 (Join-Path $PSScriptRoot 'study.py') @args
exit $LASTEXITCODE
