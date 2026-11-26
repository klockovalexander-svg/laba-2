$ErrorActionPreference = 'Stop'
Push-Location (Join-Path $PSScriptRoot '..')
try {
    python -m unittest discover -s tests -k regression -v
    if ($LASTEXITCODE) { exit $LASTEXITCODE }

    python -m coverage run -m unittest discover -s tests -v
    if ($LASTEXITCODE) { exit $LASTEXITCODE }

    python -m coverage report
    if ($LASTEXITCODE) { exit $LASTEXITCODE }

    python -m flake8 src tests --count
    exit $LASTEXITCODE
} finally {
    Pop-Location
}
