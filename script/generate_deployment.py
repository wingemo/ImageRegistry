import yaml
import subprocess

def generate_production_deployment(namespace_file, output_file):
    with open(namespace_file, 'r') as file:
        namespaces = yaml.safe_load(file)

    all_deployments = []
    all_services = []
    all_hpas = []

    for service, image in namespaces.items():
        deployment = {
            'apiVersion': 'apps/v1',
            'kind': 'Deployment',
            'metadata': {
                'name': service
            },
            'spec': {
                'replicas': 3,  # Tre replikor för produktion
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
                            'livenessProbe': {  # Liveness probe för att övervaka tjänstens hälsa
                                'httpGet': {
                                    'path': '/',
                                    'port': 8080
                                },
                                'initialDelaySeconds': 30,
                                'periodSeconds': 10
                            },
                            'readinessProbe': {  # Readiness probe för att avgöra om tjänsten är redo att ta emot trafik
                                'httpGet': {
                                    'path': '/',
                                    'port': 8080
                                },
                                'initialDelaySeconds': 30,
                                'periodSeconds': 10
                            },
                            'resources': {  # Resursbegränsningar för att säkerställa stabil drift
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

        # Skapa Kubernetes-service-definition
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

        # Skapa HPA-definition
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
    with open(output_file, 'w') as output:
        yaml.dump_all(all_deployments, output)

    # Skapa alla Kubernetes-services med kubectl
    for service_definition in all_services:
        kubectl_command = ['kubectl', 'apply', '-f', '-']
        subprocess.run(kubectl_command, input=yaml.dump(service_definition).encode('utf-8'))

    # Skapa alla HPAs med kubectl
    for hpa_definition in all_hpas:
        kubectl_command = ['kubectl', 'apply', '-f', '-']
        subprocess.run(kubectl_command, input=yaml.dump(hpa_definition).encode('utf-8'))

if __name__ == "__main__":
    generate_production_deployment('namespaces.yaml', 'deployments.yaml')
