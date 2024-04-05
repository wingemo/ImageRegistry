import subprocess
import yaml

def apply_kubernetes_resources(deployment_file, service_file, hpa_file):
    # Tillämpa deployment
    apply_deployments(deployment_file)

    # Tillämpa services
    apply_services(service_file)

    # Tillämpa HPAs
    apply_hpas(hpa_file)

def apply_deployments(deployment_file):
    # Läs in deployment-definitioner från YAML-filen
    with open(deployment_file, 'r') as file:
        deployments = yaml.safe_load_all(file)

        # Tillämpa varje deployment separat
        for deployment in deployments:
            kubectl_apply(deployment)

def apply_services(service_file):
    # Läs in service-definitioner från YAML-filen
    with open(service_file, 'r') as file:
        services = yaml.safe_load_all(file)

        # Tillämpa varje service separat
        for service in services:
            kubectl_apply(service)

def apply_hpas(hpa_file):
    # Läs in HPA-definitioner från YAML-filen
    with open(hpa_file, 'r') as file:
        hpas = yaml.safe_load_all(file)

        # Tillämpa varje HPA separat
        for hpa in hpas:
            kubectl_apply(hpa)

def kubectl_apply(resource):
    # Använd kubectl för att tillämpa resursen på Kubernetes-klustret
    kubectl_command = ['kubectl', 'apply', '-f', '-']
    subprocess.run(kubectl_command, input=yaml.dump(resource).encode('utf-8'))

if __name__ == "__main__":
    # Ange filnamn för deployments, services och HPAs
    deployment_file = 'deployments.yaml'
    service_file = 'services.yaml'
    hpa_file = 'hpa.yaml'

    # Tillämpa Kubernetes-resurser
    apply_kubernetes_resources(deployment_file, service_file, hpa_file)
