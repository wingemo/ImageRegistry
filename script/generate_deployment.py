import yaml

def generate_deployment(namespace_file):
    with open(namespace_file, 'r') as file:
        namespaces = yaml.safe_load(file)

    for service, image in namespaces.items():
        deployment = {
            'apiVersion': 'apps/v1',
            'kind': 'Deployment',
            'metadata': {
                'name': service
            },
            'spec': {
                'replicas': 1,
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
                            }]
                        }]
                    }
                }
            }
        }
        
        with open(f'{service}_deployment.yaml', 'w') as deployment_file:
            yaml.dump(deployment, deployment_file)

if __name__ == "__main__":
    generate_deployment('namespaces.yaml')

