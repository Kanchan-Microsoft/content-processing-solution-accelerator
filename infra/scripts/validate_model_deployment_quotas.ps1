param (
    [string]$SubscriptionId,
    [string]$Location,
    [string]$ModelsParameter
)

# Verify all required parameters are provided
$MissingParams = @()

if (-not $SubscriptionId) {
    $MissingParams += "subscription"
}

if (-not $Location) {
    $MissingParams += "location"
}

if (-not $ModelsParameter) {
    $MissingParams += "models-parameter"
}

if ($MissingParams.Count -gt 0) {
    Write-Error "❌ ERROR: Missing required parameters: $($MissingParams -join ', ')"
    Write-Host "Usage: .\validate_model_deployment_quotas.ps1 -SubscriptionId <SUBSCRIPTION_ID> -Location <LOCATION> -ModelsParameter <MODELS_PARAMETER>"
    exit 1
}

$JsonContent = Get-Content -Path "./infra/ai-resources.json" -Raw | ConvertFrom-Json

if (-not $JsonContent) {
    Write-Error "❌ ERROR: Failed to parse ai-resources.json. Ensure the JSON file is valid."
    exit 1
}

$aiModelDeployments = $JsonContent."aiModelDeployments"

if (-not $aiModelDeployments -or -not ($aiModelDeployments -is [System.Collections.IEnumerable])) {
    Write-Error "❌ ERROR: The specified property $ModelsParameter does not exist or is not an array."
    exit 1
}

az account set --subscription $SubscriptionId
Write-Host "🎯 Active Subscription: $(az account show --query '[name, id]' --output tsv)"

$QuotaAvailable = $true
# $previousErrorActionPreference = $ErrorActionPreference
# $ErrorActionPreference = 'silentlyContinue' # Ignore errors for the script execution
foreach ($deployment in $aiModelDeployments) {
    $name = $deployment.name
    $model = $deployment.model.name
    $type = $deployment.sku.name
    $capacity = $deployment.sku.capacity

    Write-Host "🔍 Validating model deployment: $name ..."
    # when executing the script, once we've got exception, ignore and continue without stopping the script
    & .\infra\scripts\validate_model_quota.ps1 -Location $Location -Model $model -Capacity $capacity -DeploymentType $type

    # Check if the script failed
    if ($LASTEXITCODE -ne 0) {
        Write-Error "❌ ERROR: Quota validation failed for model deployment: $name"
        $QuotaAvailable = $false
    }
}

# $ErrorActionPreference = $previousErrorActionPreference

if (-not $QuotaAvailable) {
    Write-Error "❌ ERROR: One or more model deployments failed validation."
    exit 1
}
else {
    Write-Host "✅ All model deployments passed quota validation successfully."
    exit 0
}