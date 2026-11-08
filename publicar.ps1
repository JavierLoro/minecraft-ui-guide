[CmdletBinding()]
param(
    [ValidatePattern('^[A-Za-z0-9-]+$')][string]$Owner = 'JavierLoro',
    [ValidatePattern('^[A-Za-z0-9._-]+$')][string]$Repository = 'minecraft-ui-guide'
)
$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
foreach ($command in @('gh','git')) {
    if (-not (Get-Command $command -ErrorAction SilentlyContinue)) { throw "Falta instalar $command." }
}
if (-not (Test-Path -LiteralPath 'index.html')) { throw 'No se encuentra index.html junto al script.' }

& gh auth status --hostname github.com 2>$null
if ($LASTEXITCODE -ne 0) {
    & gh auth login --hostname github.com --git-protocol https --web
    if ($LASTEXITCODE -ne 0) { throw 'No se pudo completar el inicio de sesión en GitHub.' }
}
$profileJson = & gh api user
if ($LASTEXITCODE -ne 0) { throw 'No se pudo consultar la cuenta activa.' }
$profile = $profileJson | ConvertFrom-Json
if ($profile.login -ne $Owner) { throw "La cuenta activa es $($profile.login). Selecciona $Owner con gh auth switch o usa -Owner para elegir tu cuenta." }
$fullName = "$Owner/$Repository"
$remoteUrl = "https://github.com/$fullName.git"

& gh auth setup-git --hostname github.com
if ($LASTEXITCODE -ne 0) { throw 'No se pudo configurar Git para utilizar la sesión de GitHub CLI.' }
if (-not (Test-Path -LiteralPath '.git')) {
    & git init -b main
    if ($LASTEXITCODE -ne 0) { throw 'No se pudo inicializar el repositorio local.' }
}
$branch = & git branch --show-current
if ($branch -ne 'main') { throw "La rama local es $branch. El script publica únicamente main." }
$origin = & git config --get remote.origin.url
if ($origin -and $origin -ne $remoteUrl) { throw "El remoto origin no corresponde a $fullName. No se ha cambiado." }

& git add -- .gitignore .nojekyll index.html AGENTS.md GUIA-INTERFACES-MINECRAFT.md llms.txt llms-full.txt README.md requirements.txt source tools publicar.ps1
if ($LASTEXITCODE -ne 0) { throw 'No se pudieron preparar los archivos.' }
& git diff --cached --quiet
if ($LASTEXITCODE -eq 1) {
    $email = "$($profile.id)+$($profile.login)@users.noreply.github.com"
    & git -c "user.name=$Owner" -c "user.email=$email" commit -m 'Publica la guía de interfaces de Minecraft y documentación para agentes'
    if ($LASTEXITCODE -ne 0) { throw 'No se pudo crear el commit.' }
} elseif ($LASTEXITCODE -ne 0) { throw 'No se pudo comprobar el contenido preparado.' }

if (-not $origin) {
    & gh repo create $fullName --public --source . --remote origin --push --description 'Guía interactiva de interfaces y HUD en Minecraft Java, con documentación Markdown para agentes.'
    if ($LASTEXITCODE -ne 0) { throw 'No se pudo crear el repositorio. Si el nombre ya existe, elige otro con -Repository. No se sobrescribe ningún repositorio existente.' }
} else {
    & git push -u origin main
    if ($LASTEXITCODE -ne 0) { throw 'No se pudo subir main.' }
}

$pagesUrl = & gh api "repos/$fullName/pages" --jq .html_url 2>$null
if ($LASTEXITCODE -ne 0) {
    $requestFile = Join-Path $PSScriptRoot '.git/pages-request.json'
    @{ build_type='legacy'; source=@{ branch='main'; path='/' } } | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath $requestFile -Encoding utf8
    & gh api --method POST "repos/$fullName/pages" --input $requestFile
    if ($LASTEXITCODE -ne 0) { throw 'Los archivos están subidos, pero no se pudo activar Pages. Abre Settings > Pages y selecciona main / (root).' }
    $pagesUrl = & gh api "repos/$fullName/pages" --jq .html_url
    if ($LASTEXITCODE -ne 0) { throw 'Pages se ha solicitado, pero no se pudo obtener su URL.' }
}
Write-Host "Repositorio: https://github.com/$fullName"
Write-Host "GitHub Pages: $pagesUrl"
Write-Host "Lectura para agentes: $($pagesUrl.TrimEnd('/'))/AGENTS.md"
Write-Host 'La publicación puede tardar unos minutos. Comprueba el despliegue en la pestaña Actions.'
