import yaml

def generate_production_deployment(namespace_file, deployment_file, service_file, hpa_file):
    with open(namespace_file, 'r') as file:
        namespaces = yaml.safe_load(file)

    all_deployments = []
    all_services = []
    all_hpas = []

    for service, image in namespaces.items():
        # Generera Deployment-definition
        deployment = {
            'apiVersion': 'apps/v1',
            'kind': 'Deployment',
            'metadata': {
                'name': service
            },
            'spec': {
                'replicas': 3,  
                'selector': {
                    'matchLabels': {
                        'app': service
                    }
                },
                'template': {
                    'metadata': {
                        'labels': {
                            'app': service
                        }
                    },
                    'spec': {
                        'containers': [{
                            'name': service,
                            'image': image,
                            'ports': [{
                                'containerPort': 8080
                            }],
                            'livenessProbe': {  
                                'httpGet': {
                                    'path': '/',
                                    'port': 8080
                                },
                                'initialDelaySeconds': 30,
                                'periodSeconds': 10
                            },
                            'readinessProbe': {  
                                'httpGet': {
                                    'path': '/',
                                    'port': 8080
                                },
                                'initialDelaySeconds': 30,
                                'periodSeconds': 10
                            },
                            'resources': {  
                                'limits': {
                                    'cpu': '0.5',
                                    'memory': '512Mi'
                                },
                                'requests': {
                                    'cpu': '0.1',
                                    'memory': '128Mi'
                                }
                            }
                        }]
                    }
                }
            }
        }
        all_deployments.append(deployment)

        # Generera Kubernetes-service-definition
        service_definition = {
            'apiVersion': 'v1',
            'kind': 'Service',
            'metadata': {
                'name': f'{service}-service'
            },
            'spec': {
                'selector': {
                    'app': service
                },
                'ports': [{
                    'protocol': 'TCP',
                    'port': 80,
                    'targetPort': 8080
                }]
            }
        }
        all_services.append(service_definition)

        # Generera HPA-definition
        hpa_definition = {
            'apiVersion': 'autoscaling/v2beta2',
            'kind': 'HorizontalPodAutoscaler',
            'metadata': {
                'name': f'{service}-hpa'
            },
            'spec': {
                'scaleTargetRef': {
                    'apiVersion': 'apps/v1',
                    'kind': 'Deployment',
                    'name': service
                },
                'minReplicas': 1,
                'maxReplicas': 10,
                'metrics': [{
                    'type': 'Resource',
                    'resource': {
                        'name': 'cpu',
                        'targetAverageUtilization': 50
                    }
                }]
            }
        }
        all_hpas.append(hpa_definition)

    # Skriv alla deployments till en YAML-fil
    with open(deployment_file, 'w') as output:
        yaml.dump_all(all_deployments, output)

    # Skriv alla Kubernetes-services till en YAML-fil
    with open(service_file, 'w') as output:
        yaml.dump_all(all_services, output)

    # Skriv alla HPAs till en YAML-fil
    with open(hpa_file, 'w') as output:
        yaml.dump_all(all_hpas, output)

if __name__ == "__main__":
    generate_production_deployment('namespaces.yaml', 'deployments.yaml', 'services.yaml', 'hpa.yaml')
