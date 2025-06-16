// modules/app-insights-avm.bicep
metadata name = 'AVM Application Insights and Log Analytics Workspace Module'
// AVM-compliant Application Insights and Log Analytics Workspace deployment
// param applicationInsightsName string
// param logAnalyticsWorkspaceName string
// param location string
// param dataRetention int = 30
// param skuName string = 'PerGB2018'
// param kind string = 'web'
// param disableIpMasking bool = false
// param flowType string = 'Bluefield'

@description('The name of the Application Insights resource')
param appInsightsName string

@description('The name of the Log Analytics Workspace resource')
param logAnalyticsWorkspaceName string

@description('Optional: Existing Log Analytics Workspace Resource ID')
param existingLogAnalyticsWorkspaceId string = '' 

@description('The location for the resources')
param location string

@description('SKU name for the Log Analytics Workspace resource')
param skuName string = 'PerGB2018'

@description('Retention period in days for the Application Insights resource')
param retentionInDays int = 30

@description('Kind of the Application Insights resource')
param kind string = 'web'

@description('Disable IP masking for the Application Insights resource')
param disableIpMasking bool = false

@description('Flow type for the Application Insights resource')
param flowType string = 'Bluefield'

@description('Application Type for the Application Insights resource')
param applicationType string = 'web'

@description('Disable local authentication for the Application Insights resource')
param disableLocalAuth bool = false

@description('Public network access for query in Application Insights resource')
param publicNetworkAccessForQuery string = 'Enabled'

@description('Request source for the Application Insights resource')
param requestSource string = 'rest'

@description('Tags to be applied to the resources')
param tags object = {}

var useExistingWorkspace = existingLogAnalyticsWorkspaceId != ''
var existingLawSubscription = useExistingWorkspace ? split(existingLogAnalyticsWorkspaceId, '/')[2] : ''
var existingLawResourceGroup = useExistingWorkspace ? split(existingLogAnalyticsWorkspaceId, '/')[4] : ''
var existingLawName = useExistingWorkspace ? split(existingLogAnalyticsWorkspaceId, '/')[8] : ''

module avmLogAnalyticsWorkspace 'br/public:avm/res/operational-insights/workspace:0.11.2' = if (!useExistingWorkspace) {
  name: 'deploy_log_analytics_workspace'
  params: {
    name: logAnalyticsWorkspaceName
    location: location
    skuName: skuName
    dataRetention: retentionInDays
    diagnosticSettings: [{ useThisWorkspace: true }]
    tags: tags
  }
}

resource existingLogAnalyticsWorkspace 'Microsoft.OperationalInsights/workspaces@2023-09-01' existing = if (useExistingWorkspace) {
  name: existingLawName
  scope: resourceGroup(existingLawSubscription ,existingLawResourceGroup)
}

module avmApplicationInsights 'br/public:avm/res/insights/component:0.6.0' = {
  name: 'deploy_application_insights'
  params: {
    name: appInsightsName
    location: location
    workspaceResourceId: useExistingWorkspace ? existingLogAnalyticsWorkspaceId : avmLogAnalyticsWorkspace.outputs.resourceId
    kind: kind
    applicationType: applicationType
    disableIpMasking: disableIpMasking
    disableLocalAuth: disableLocalAuth
    flowType: flowType
    publicNetworkAccessForQuery: publicNetworkAccessForQuery
    requestSource: requestSource
    tags: tags
  }
}

var lawKeys = useExistingWorkspace ? listKeys(existingLogAnalyticsWorkspace.id, '2020-08-01') : null

output applicationInsightsId string = avmApplicationInsights.outputs.resourceId
output logAnalyticsWorkspaceId string = avmLogAnalyticsWorkspace.outputs.logAnalyticsWorkspaceId
output logAnalyticsWorkspaceResourceId string = useExistingWorkspace ? existingLogAnalyticsWorkspaceId : avmLogAnalyticsWorkspace.outputs.resourceId
output logAnalyticsWorkspaceName string = useExistingWorkspace ? existingLogAnalyticsWorkspace.name : avmLogAnalyticsWorkspace.outputs.name
@secure()
output logAnalyticsWorkspacePrimaryKey string = useExistingWorkspace ? lawKeys.primarySharedKey : avmLogAnalyticsWorkspace.outputs.primarySharedKey
