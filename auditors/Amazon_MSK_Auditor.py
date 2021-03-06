# This file is part of ElectricEye.

# ElectricEye is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# ElectricEye is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with ElectricEye.  
# If not, see https://github.com/jonrau1/ElectricEye/blob/master/LICENSE.

import boto3
import os
import datetime
# import boto3 clients
sts = boto3.client('sts')
kafka = boto3.client('kafka')
securityhub = boto3.client('securityhub')
# create env vars for account and region
awsRegion = os.environ['AWS_REGION']
awsAccountId = sts.get_caller_identity()['Account']
# loop through managed kafka clusters
response = kafka.list_clusters()
myMskClusters = response['ClusterInfoList']

def inter_cluster_encryption_in_transit_check():
    for clusters in myMskClusters:
        clusterArn = str(clusters['ClusterArn'])
        clusterName = str(clusters['ClusterName'])
        interClusterEITCheck = str(clusters['EncryptionInfo']['EncryptionInTransit']['InCluster'])
        if interClusterEITCheck != 'True':
            try:
                # ISO Time
                iso8601Time = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
                # create Sec Hub finding
                response = securityhub.batch_import_findings(
                    Findings=[
                        {
                            'SchemaVersion': '2018-10-08',
                            'Id': clusterArn + '/intercluster-encryption-in-transit',
                            'ProductArn': 'arn:aws:securityhub:' + awsRegion + ':' + awsAccountId + ':product/' + awsAccountId + '/default',
                            'GeneratorId': clusterArn,
                            'AwsAccountId': awsAccountId,
                            'Types': [ 'Software and Configuration Checks/AWS Security Best Practices' ],
                            'FirstObservedAt': iso8601Time,
                            'CreatedAt': iso8601Time,
                            'UpdatedAt': iso8601Time,
                            'Severity': { 'Normalized': 80 },
                            'Confidence': 99,
                            'Title': '[MSK.1] Managed Kafka Stream clusters should have inter-cluster encryption in transit enabled',
                            'Description': 'MSK cluster ' + clusterName + ' does not have inter-cluster encryption in transit enabled. Refer to the remediation instructions if this configuration is not intended',
                            'Remediation': {
                                'Recommendation': {
                                    'Text': 'If your cluster should have inter-cluster encryption in transit enabled refer to the How Do I Get Started with Encryption? section of the Amazon Managed Streaming for Apache Kakfa Developer Guide',
                                    'Url': 'https://docs.aws.amazon.com/msk/latest/developerguide/msk-working-with-encryption.html'
                                }
                            },
                            'ProductFields': {
                                'Product Name': 'ElectricEye'
                            },
                            'Resources': [
                                {
                                    'Type': 'AwsManagedKafkaCluster',
                                    'Id': clusterArn,
                                    'Partition': 'aws',
                                    'Region': awsRegion,
                                    'Details': {
                                        'Other': { 'ClusterName': clusterName }
                                    }
                                }
                            ],
                            'Compliance': { 'Status': 'FAILED' },
                            'RecordState': 'ACTIVE'
                        }
                    ]
                )
                print(response)
            except Exception as e:
                print(e)
        else:
            try:
                # ISO Time
                iso8601Time = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
                # create Sec Hub finding
                response = securityhub.batch_import_findings(
                    Findings=[
                        {
                            'SchemaVersion': '2018-10-08',
                            'Id': clusterArn + '/intercluster-encryption-in-transit',
                            'ProductArn': 'arn:aws:securityhub:' + awsRegion + ':' + awsAccountId + ':product/' + awsAccountId + '/default',
                            'GeneratorId': clusterArn,
                            'AwsAccountId': awsAccountId,
                            'Types': [ 'Software and Configuration Checks/AWS Security Best Practices' ],
                            'FirstObservedAt': iso8601Time,
                            'CreatedAt': iso8601Time,
                            'UpdatedAt': iso8601Time,
                            'Severity': { 'Normalized': 0 },
                            'Confidence': 99,
                            'Title': '[MSK.1] Managed Kafka Stream clusters should have inter-cluster encryption in transit enabled',
                            'Description': 'MSK cluster ' + clusterName + ' has inter-cluster encryption in transit enabled.',
                            'Remediation': {
                                'Recommendation': {
                                    'Text': 'If your cluster should have inter-cluster encryption in transit enabled refer to the How Do I Get Started with Encryption? section of the Amazon Managed Streaming for Apache Kakfa Developer Guide',
                                    'Url': 'https://docs.aws.amazon.com/msk/latest/developerguide/msk-working-with-encryption.html'
                                }
                            },
                            'ProductFields': {
                                'Product Name': 'ElectricEye'
                            },
                            'Resources': [
                                {
                                    'Type': 'AwsManagedKafkaCluster',
                                    'Id': clusterArn,
                                    'Partition': 'aws',
                                    'Region': awsRegion,
                                    'Details': {
                                        'Other': { 'ClusterName': clusterName }
                                    }
                                }
                            ],
                            'Compliance': { 'Status': 'PASSED' },
                            'RecordState': 'ARCHIVED'
                        }
                    ]
                )
                print(response)
            except Exception as e:
                print(e)
        
def client_broker_encryption_in_transit_check():
    for clusters in myMskClusters:
        clusterArn = str(clusters['ClusterArn'])
        clusterName = str(clusters['ClusterName'])
        clientBrokerTlsCheck = str(clusters['EncryptionInfo']['EncryptionInTransit']['ClientBroker'])
        if clientBrokerTlsCheck != 'TLS':
            try:
                # ISO Time
                iso8601Time = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
                # create Sec Hub finding
                response = securityhub.batch_import_findings(
                    Findings=[
                        {
                            'SchemaVersion': '2018-10-08',
                            'Id': clusterArn + '/client-broker-tls',
                            'ProductArn': 'arn:aws:securityhub:' + awsRegion + ':' + awsAccountId + ':product/' + awsAccountId + '/default',
                            'GeneratorId': clusterArn,
                            'AwsAccountId': awsAccountId,
                            'Types': [ 'Software and Configuration Checks/AWS Security Best Practices' ],
                            'FirstObservedAt': iso8601Time,
                            'CreatedAt': iso8601Time,
                            'UpdatedAt': iso8601Time,
                            'Severity': { 'Normalized': 80 },
                            'Confidence': 99,
                            'Title': '[MSK.2] Managed Kafka Stream clusters should enforce TLS-only communications between clients and brokers',
                            'Description': 'MSK cluster ' + clusterName + ' does not enforce TLS-only communications between clients and brokers. Refer to the remediation instructions if this configuration is not intended',
                            'Remediation': {
                                'Recommendation': {
                                    'Text': 'If your cluster should enforce TLS-only communications between clients and brokers refer to the How Do I Get Started with Encryption? section of the Amazon Managed Streaming for Apache Kakfa Developer Guide',
                                    'Url': 'https://docs.aws.amazon.com/msk/latest/developerguide/msk-working-with-encryption.html'
                                }
                            },
                            'ProductFields': {
                                'Product Name': 'ElectricEye'
                            },
                            'Resources': [
                                {
                                    'Type': 'AwsManagedKafkaCluster',
                                    'Id': clusterArn,
                                    'Partition': 'aws',
                                    'Region': awsRegion,
                                    'Details': {
                                        'Other': { 'ClusterName': clusterName }
                                    }
                                }
                            ],
                            'Compliance': { 'Status': 'FAILED' },
                            'RecordState': 'ACTIVE'
                        }
                    ]
                )
                print(response)
            except Exception as e:
                print(e)
        else:
            try:
                # ISO Time
                iso8601Time = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
                # create Sec Hub finding
                response = securityhub.batch_import_findings(
                    Findings=[
                        {
                            'SchemaVersion': '2018-10-08',
                            'Id': clusterArn + '/client-broker-tls',
                            'ProductArn': 'arn:aws:securityhub:' + awsRegion + ':' + awsAccountId + ':product/' + awsAccountId + '/default',
                            'GeneratorId': clusterArn,
                            'AwsAccountId': awsAccountId,
                            'Types': [ 'Software and Configuration Checks/AWS Security Best Practices' ],
                            'FirstObservedAt': iso8601Time,
                            'CreatedAt': iso8601Time,
                            'UpdatedAt': iso8601Time,
                            'Severity': { 'Normalized': 0 },
                            'Confidence': 99,
                            'Title': '[MSK.2] Managed Kafka Stream clusters should enforce TLS-only communications between clients and brokers',
                            'Description': 'MSK cluster ' + clusterName + ' enforces TLS-only communications between clients and brokers',
                            'Remediation': {
                                'Recommendation': {
                                    'Text': 'If your cluster should enforce TLS-only communications between clients and brokers refer to the How Do I Get Started with Encryption? section of the Amazon Managed Streaming for Apache Kakfa Developer Guide',
                                    'Url': 'https://docs.aws.amazon.com/msk/latest/developerguide/msk-working-with-encryption.html'
                                }
                            },
                            'ProductFields': {
                                'Product Name': 'ElectricEye'
                            },
                            'Resources': [
                                {
                                    'Type': 'AwsManagedKafkaCluster',
                                    'Id': clusterArn,
                                    'Partition': 'aws',
                                    'Region': awsRegion,
                                    'Details': {
                                        'Other': { 'ClusterName': clusterName }
                                    }
                                }
                            ],
                            'Compliance': { 'Status': 'PASSED' },
                            'RecordState': 'ARCHIVED'
                        }
                    ]
                )
                print(response)
            except Exception as e:
                print(e)
            
def client_authentication_check():
    for clusters in myMskClusters:
        clusterArn = str(clusters['ClusterArn'])
        clusterName = str(clusters['ClusterName'])
        try:
            clientAuthCheck = str(clusters['ClientAuthentication']['Tls']['CertificateAuthorityArnList'])
            try:
                # ISO Time
                iso8601Time = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
                # create Sec Hub finding
                response = securityhub.batch_import_findings(
                    Findings=[
                        {
                            'SchemaVersion': '2018-10-08',
                            'Id': clusterArn + '/tls-client-auth',
                            'ProductArn': 'arn:aws:securityhub:' + awsRegion + ':' + awsAccountId + ':product/' + awsAccountId + '/default',
                            'GeneratorId': clusterArn,
                            'AwsAccountId': awsAccountId,
                            'Types': [ 'Software and Configuration Checks/AWS Security Best Practices' ],
                            'FirstObservedAt': iso8601Time,
                            'CreatedAt': iso8601Time,
                            'UpdatedAt': iso8601Time,
                            'Severity': { 'Normalized': 0 },
                            'Confidence': 99,
                            'Title': '[MSK.3] Managed Kafka Stream clusters should use TLS for client authentication',
                            'Description': 'MSK cluster ' + clusterName + ' uses TLS for client authentication.',
                            'Remediation': {
                                'Recommendation': {
                                    'Text': 'If your cluster should use TLS for client authentication refer to the Client Authentication section of the Amazon Managed Streaming for Apache Kakfa Developer Guide',
                                    'Url': 'https://docs.aws.amazon.com/msk/latest/developerguide/msk-authentication.html'
                                }
                            },
                            'ProductFields': {
                                'Product Name': 'ElectricEye'
                            },
                            'Resources': [
                                {
                                    'Type': 'AwsManagedKafkaCluster',
                                    'Id': clusterArn,
                                    'Partition': 'aws',
                                    'Region': awsRegion,
                                    'Details': {
                                        'Other': { 'ClusterName': clusterName }
                                    }
                                }
                            ],
                            'Compliance': { 'Status': 'PASSED' },
                            'RecordState': 'ARCHIVED'
                        }
                    ]
                )
                print(response)
            except Exception as e:
                print(e)
        except:
            try:
                # ISO Time
                iso8601Time = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
                # create Sec Hub finding
                response = securityhub.batch_import_findings(
                    Findings=[
                        {
                            'SchemaVersion': '2018-10-08',
                            'Id': clusterArn + '/tls-client-auth',
                            'ProductArn': 'arn:aws:securityhub:' + awsRegion + ':' + awsAccountId + ':product/' + awsAccountId + '/default',
                            'GeneratorId': clusterArn,
                            'AwsAccountId': awsAccountId,
                            'Types': [ 'Software and Configuration Checks/AWS Security Best Practices' ],
                            'FirstObservedAt': iso8601Time,
                            'CreatedAt': iso8601Time,
                            'UpdatedAt': iso8601Time,
                            'Severity': { 'Normalized': 40 },
                            'Confidence': 99,
                            'Title': '[MSK.3] Managed Kafka Stream clusters should use TLS for client authentication',
                            'Description': 'MSK cluster ' + clusterName + ' does not use TLS for client authentication. Refer to the remediation instructions if this configuration is not intended',
                            'Remediation': {
                                'Recommendation': {
                                    'Text': 'If your cluster should use TLS for client authentication refer to the Client Authentication section of the Amazon Managed Streaming for Apache Kakfa Developer Guide',
                                    'Url': 'https://docs.aws.amazon.com/msk/latest/developerguide/msk-authentication.html'
                                }
                            },
                            'ProductFields': {
                                'Product Name': 'ElectricEye'
                            },
                            'Resources': [
                                {
                                    'Type': 'AwsManagedKafkaCluster',
                                    'Id': clusterArn,
                                    'Partition': 'aws',
                                    'Region': awsRegion,
                                    'Details': {
                                        'Other': { 'ClusterName': clusterName }
                                    }
                                }
                            ],
                            'Compliance': { 'Status': 'FAILED' },
                            'RecordState': 'ACTIVE'
                        }
                    ]
                )
                print(response)
            except Exception as e:
                print(e)
            
def cluster_enhanced_monitoring_check():
    for clusters in myMskClusters:
        clusterArn = str(clusters['ClusterArn'])
        clusterName = str(clusters['ClusterName'])
        enhancedMonitoringCheck = str(clusters['EnhancedMonitoring'])
        if enhancedMonitoringCheck == 'DEFAULT':
            try:
                # ISO Time
                iso8601Time = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
                # create Sec Hub finding
                response = securityhub.batch_import_findings(
                    Findings=[
                        {
                            'SchemaVersion': '2018-10-08',
                            'Id': clusterArn + '/detailed-monitoring',
                            'ProductArn': 'arn:aws:securityhub:' + awsRegion + ':' + awsAccountId + ':product/' + awsAccountId + '/default',
                            'GeneratorId': clusterArn,
                            'AwsAccountId': awsAccountId,
                            'Types': [ 'Software and Configuration Checks/AWS Security Best Practices' ],
                            'FirstObservedAt': iso8601Time,
                            'CreatedAt': iso8601Time,
                            'UpdatedAt': iso8601Time,
                            'Severity': { 'Normalized': 20 },
                            'Confidence': 99,
                            'Title': '[MSK.4] Managed Kafka Stream clusters should use enhanced monitoring',
                            'Description': 'MSK cluster ' + clusterName + ' does not use enhanced monitoring. Refer to the remediation instructions if this configuration is not intended',
                            'Remediation': {
                                'Recommendation': {
                                    'Text': 'If your cluster should use enhanced monitoring refer to the Monitoring an Amazon MSK Cluster section of the Amazon Managed Streaming for Apache Kakfa Developer Guide',
                                    'Url': 'https://docs.aws.amazon.com/msk/latest/developerguide/monitoring.html'
                                }
                            },
                            'ProductFields': {
                                'Product Name': 'ElectricEye'
                            },
                            'Resources': [
                                {
                                    'Type': 'AwsManagedKafkaCluster',
                                    'Id': clusterArn,
                                    'Partition': 'aws',
                                    'Region': awsRegion,
                                    'Details': {
                                        'Other': { 'ClusterName': clusterName }
                                    }
                                }
                            ],
                            'Compliance': { 'Status': 'FAILED' },
                            'RecordState': 'ACTIVE'
                        }
                    ]
                )
                print(response)
            except Exception as e:
                print(e)
        else:
            try:
                # ISO Time
                iso8601Time = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
                # create Sec Hub finding
                response = securityhub.batch_import_findings(
                    Findings=[
                        {
                            'SchemaVersion': '2018-10-08',
                            'Id': clusterArn + '/detailed-monitoring',
                            'ProductArn': 'arn:aws:securityhub:' + awsRegion + ':' + awsAccountId + ':product/' + awsAccountId + '/default',
                            'GeneratorId': clusterArn,
                            'AwsAccountId': awsAccountId,
                            'Types': [ 'Software and Configuration Checks/AWS Security Best Practices' ],
                            'FirstObservedAt': iso8601Time,
                            'CreatedAt': iso8601Time,
                            'UpdatedAt': iso8601Time,
                            'Severity': { 'Normalized': 0 },
                            'Confidence': 99,
                            'Title': '[MSK.4] Managed Kafka Stream clusters should use enhanced monitoring',
                            'Description': 'MSK cluster ' + clusterName + ' uses enhanced monitoring.',
                            'Remediation': {
                                'Recommendation': {
                                    'Text': 'If your cluster should use enhanced monitoring refer to the Monitoring an Amazon MSK Cluster section of the Amazon Managed Streaming for Apache Kakfa Developer Guide',
                                    'Url': 'https://docs.aws.amazon.com/msk/latest/developerguide/monitoring.html'
                                }
                            },
                            'ProductFields': {
                                'Product Name': 'ElectricEye'
                            },
                            'Resources': [
                                {
                                    'Type': 'AwsManagedKafkaCluster',
                                    'Id': clusterArn,
                                    'Partition': 'aws',
                                    'Region': awsRegion,
                                    'Details': {
                                        'Other': { 'ClusterName': clusterName }
                                    }
                                }
                            ],
                            'Compliance': { 'Status': 'PASSED' },
                            'RecordState': 'ARCHIVED'
                        }
                    ]
                )
                print(response)
            except Exception as e:
                print(e)
        
def msk_auditor():
    inter_cluster_encryption_in_transit_check()
    client_broker_encryption_in_transit_check()
    cluster_enhanced_monitoring_check()
    client_authentication_check()
    
msk_auditor()