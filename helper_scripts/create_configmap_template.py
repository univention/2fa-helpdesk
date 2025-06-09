# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

import yaml
import argparse

def load_env_file(env_path):
    env_vars = {}
    with open(env_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            key, sep, value = line.partition('=')
            if sep:
                env_vars[key.strip()] = value.strip()
    return env_vars

def create_configmap(env_vars, name, namespace="default"):

    configmap = {
        "apiVersion": "v1",
        "kind": "ConfigMap",
        "metadata": {
            "name": name,
            "namespace": namespace,
        },
        "data": env_vars,
    }

    return configmap

def main():
    parser = argparse.ArgumentParser(description="Create a Kubernetes ConfigMap from a .env file.")
    parser.add_argument("env_path", help="Path to the .env file")
    parser.add_argument("configmap_name", help="Name of the ConfigMap")
    parser.add_argument("--namespace", default="default", help="Namespace for the ConfigMap (default: default)")
    args = parser.parse_args()

    env_vars = load_env_file(args.env_path)
    configmap = create_configmap(env_vars, args.configmap_name, args.namespace)

    output_filename = f"{args.configmap_name}.yaml"
    with open(output_filename, 'w') as f:
        yaml.dump(configmap, f, sort_keys=False)

    print(f"ConfigMap '{output_filename}' created in namespace '{args.namespace}'.")

if __name__ == "__main__":
    main()
