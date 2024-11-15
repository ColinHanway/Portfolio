import requests
import json
from api_keys import SENTINEL_ACCESS_KEY

url = "https://usea1-ninjaone2.sentinelone.net/web/api/v2.1/sites"


def create_site(name):
    payload = json.dumps(
        {
            "data": {
                "name": name,
                "policy": {
                    "agentLoggingOn": True,
                    "agentNotification": True,
                    "agentUi": {
                        "agentUiOn": True,
                        "contactCompany": "",
                        "contactDirectMessage": "",
                        "contactEmail": "",
                        "contactFreeText": "Please contact the Alphamedia helpdesk if you have any question. \n\n(971) 420-0311",
                        "contactOther": "",
                        "contactPhoneNumber": "(971) 420-0311",
                        "contactSupportWebsite": "",
                        "devicePopUpNotifications": True,
                        "maxEventAgeDays": 30,
                        "showAgentWarnings": False,
                        "showDeviceTab": True,
                        "showQuarantineTab": True,
                        "showSupport": True,
                        "showSuspicious": True,
                        "threatPopUpNotifications": True,
                    },
                    "agentUiOn": True,
                    "allowRemoteShell": True,
                    "allowUnprotectByApprovedProcess": False,
                    "antiTamperingOn": True,
                    "autoDecommissionDays": 21,
                    "autoDecommissionOn": True,
                    "autoFileUpload": {
                        "enabled": True,
                        "includeBenignFiles": False,
                        "maxDailyFileUpload": 524288000,
                        "maxDailyFileUploadLimit": 524288000,
                        "maxFileSize": 262144000,
                        "maxFileSizeLimit": 262144000,
                        "maxLocalDiskUsage": 2147483648,
                        "maxLocalDiskUsageLimit": 2147483648,
                    },
                    "autoImmuneOn": True,
                    "autoMitigationAction": "mitigation.remediateThreat",
                    "cloudValidationOn": True,
                    "createdAt": "2024-09-13T14:08:53.309042Z",
                    "driverBlocking": True,
                    "dvAttributesPerEventType": {
                        "autoInstallBrowserExtensions": {
                            "autoInstallBrowserExtensions": False
                        },
                        "behavioralIndicators": {
                            "dvEventTypeBehavioralIndicators": True
                        },
                        "commandScripts": {"dvEventTypeCommandScripts": True},
                        "crossProcess": {
                            "dvEventTypeCrossProcessDuplicateProcess": True,
                            "dvEventTypeCrossProcessDuplicateThread": True,
                            "dvEventTypeCrossProcessOpenProcess": True,
                            "dvEventTypeCrossProcessRemoteThread": True,
                        },
                        "dataMasking": {"dataMasking": False},
                        "dllModuleLoad": {"dvEventTypeDllModuleLoad": False},
                        "dns": {"dvEventTypeDns": True},
                        "driver": {"dvEventTypeDriverLoad": True},
                        "file": {
                            "dvEventTypeFileCreation": True,
                            "dvEventTypeFileDeletion": True,
                            "dvEventTypeFileModification": True,
                            "dvEventTypeFileRename": True,
                            "fullDiskScan": False,
                        },
                        "ip": {
                            "dvEventTypeIpConnect": True,
                            "dvEventTypeIpListen": True,
                        },
                        "login": {
                            "dvEventTypeLoginLoggedIn": True,
                            "dvEventTypeLoginLoggedOut": True,
                        },
                        "namedPipe": {
                            "dvEventTypeNamedPipeConnection": False,
                            "dvEventTypeNamedPipeCreation": False,
                        },
                        "namedPipeExtended": {"namedPipeExtended": False},
                        "process": {"dvEventTypeProcessCreation": True},
                        "registry": {
                            "dvEventTypeRegistryKeyCreated": True,
                            "dvEventTypeRegistryKeyDelete": True,
                            "dvEventTypeRegistryKeyExport": True,
                            "dvEventTypeRegistryKeyImport": True,
                            "dvEventTypeRegistryKeyRename": True,
                            "dvEventTypeRegistryKeySecurityChanged": True,
                            "dvEventTypeRegistryValueCreated": True,
                            "dvEventTypeRegistryValueDeleted": True,
                            "dvEventTypeRegistryValueModified": True,
                        },
                        "scheduledTask": {
                            "dvEventTypeScheduledTaskDelete": True,
                            "dvEventTypeScheduledTaskRegister": True,
                            "dvEventTypeScheduledTaskStart": True,
                            "dvEventTypeScheduledTaskTrigger": True,
                            "dvEventTypeScheduledTaskUpdate": True,
                        },
                        "smartFileMonitoring": {"smartFileMonitoring": True},
                        "url": {"dvEventTypeUrl": True},
                        "windowsEventLogs": {
                            "dvEventTypeWindowsEventLogCreation": False
                        },
                        "windowsEventLogsExtended": {"windowsEventLogsExtended": False},
                    },
                    "engines": {
                        "applicationControl": "on",
                        "dataFiles": "on",
                        "executables": "on",
                        "exploits": "on",
                        "idr": "on",
                        "lateralMovement": "on",
                        "penetration": "on",
                        "preExecution": "on",
                        "preExecutionSuspicious": "on",
                        "pup": "on",
                        "remoteShell": "on",
                        "reputation": "on",
                    },
                    "forensicsAutoTriggering": {
                        "linuxEnabled": False,
                        "linuxProfileId": None,
                        "linuxProfileName": "",
                        "macosEnabled": False,
                        "macosProfileId": None,
                        "macosProfileName": "",
                        "windowsEnabled": False,
                        "windowsProfileId": None,
                        "windowsProfileName": "",
                    },
                    "fwForNetworkQuarantineEnabled": False,
                    "identityEndpointReporting": "moderate",
                    "identityOn": False,
                    "identityReportInterval": 5,
                    "identityThrottlingInterval": 2880,
                    "identityUpdateInterval": 60,
                    "inheritedFrom": None,
                    "ioc": True,
                    "iocAttributes": {
                        "autoInstallBrowserExtensions": False,
                        "behavioralIndicators": True,
                        "commandScripts": True,
                        "crossProcess": True,
                        "dataMasking": False,
                        "dllModuleLoad": False,
                        "dns": True,
                        "driver": True,
                        "fds": False,
                        "file": True,
                        "ip": True,
                        "login": True,
                        "namedPipe": False,
                        "namedPipeExtended": False,
                        "process": True,
                        "registry": True,
                        "scheduledTask": True,
                        "smartFileMonitoring": True,
                        "url": True,
                        "windowsEventLogs": False,
                        "windowsEventLogsExtended": False,
                    },
                    "isDefault": False,
                    "isDvPolicyPerEventType": True,
                    "mitigationMode": "protect",
                    "mitigationModeSuspicious": "protect",
                    "monitorOnExecute": True,
                    "monitorOnWrite": True,
                    "networkQuarantineOn": True,
                    "remoteScriptOrchestration": {
                        "alwaysUploadStreamToCloud": False,
                        "maxDailyFileDownload": 524288000,
                        "maxDailyFileDownloadLimit": 1610612736,
                        "maxDailyFileUpload": 524288000,
                        "maxDailyFileUploadLimit": 3221225472,
                        "maxFileSize": 262144000,
                        "maxFileSizeLimit": 1610612736,
                        "maxLocalPackageDiskUsage": 2147483648,
                        "maxLocalPackageDiskUsageLimit": 5368709120,
                    },
                    "removeMacros": True,
                    "researchOn": True,
                    "scanNewAgents": True,
                    "signedDriverBlockingOn": True,
                    "snapshotsOn": True,
                    "unsignedDriverBlockingOn": True,
                    "updatedAt": "2024-09-20T00:02:45.643273Z",
                },
                "licenses": {},
                "totalLicenses": 0,
                "unlimitedExpiration": True,
                "siteType": "Paid",
                "unlimitedLicenses": True,
                "description": "Test API creation of site based on columbia firewall rules",
                "expiration": None,
                "sku": "Complete",
                "externalId": None,
                "accountId": 2031452979633495986,
                "suite": "Core",
                "accountSfId": None,
                "inherits": False,
            }
        }
    )
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": SENTINEL_ACCESS_KEY,
    }

    try:
        response = requests.request("POST", url, headers=headers, data=payload)

        if response.status_code == 200:
            return f"{name} successfully created"
        raise ValueError(f"{name} could not be created. Error: {response.text}")
    except ValueError as e:
        return repr(e)
