import json
from typing import List, Dict


# Class for the ports inside status
class Port:
    def __init__(self, name: str, port: int):
        self.name = name
        self.port = port

    @classmethod
    def from_dict(cls, data: Dict):
        return cls(name=data['name'], port=data['port'])


# Class for the status field
class Status:
    def __init__(self, state: str, address: str, ports: List[Port]):
        self.state = state
        self.address = address
        self.ports = ports

    @classmethod
    def from_dict(cls, data: Dict):
        ports = [Port.from_dict(p) for p in data['ports']]
        return cls(state=data['state'], address=data['address'], ports=ports)


# Class for annotations and labels inside object_meta
class ObjectMeta:
    def __init__(self, name: str, namespace: str, uid: str, resource_version: str,
                 generation: str, creation_timestamp: str, annotations: Dict[str, str],
                 labels: Dict[str, str]):
        self.name = name
        self.namespace = namespace
        self.uid = uid
        self.resource_version = resource_version
        self.generation = generation
        self.creation_timestamp = creation_timestamp
        self.annotations = annotations
        self.labels = labels

    @classmethod
    def from_dict(cls, data: Dict):
        return cls(
            name=data['name'],
            namespace=data['namespace'],
            uid=data['uid'],
            resource_version=data['resource_version'],
            generation=data['generation'],
            creation_timestamp=data['creation_timestamp'],
            annotations=data['annotations'],
            labels=data['labels']
        )


# Class for the main object that combines object_meta and status
class AgonesInfoResponse:
    def __init__(self, object_meta: ObjectMeta, status: Status):
        self.object_meta = object_meta
        self.status = status

    @classmethod
    def from_dict(cls, data: Dict):
        object_meta = ObjectMeta.from_dict(data['object_meta'])
        status = Status.from_dict(data['status'])
        return cls(object_meta=object_meta, status=status)

    def to_dict(self):
        return {
            "object_meta": {
                "name": self.object_meta.name,
                "namespace": self.object_meta.namespace,
                "uid": self.object_meta.uid,
                "resource_version": self.object_meta.resource_version,
                "generation": self.object_meta.generation,
                "creation_timestamp": self.object_meta.creation_timestamp,
                "annotations": self.object_meta.annotations,
                "labels": self.object_meta.labels,
            },
            "status": {
                "state": self.status.state,
                "address": self.status.address,
                "ports": [{"name": port.name, "port": port.port} for port in self.status.ports]
            }
        }