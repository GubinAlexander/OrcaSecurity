from rest_framework import status
from rest_framework.test import APITestCase
from attack_surface_service.api.v1.services import get_attacked_vm, get_machines_can_potentially_attack


class ClientAttackAPIViewTestCase(APITestCase):
    def test_attacked_vm_not_exists(self):
        data = {
            "vms": [
                {
                    "vm_id": "vm-a211de",
                    "name": "jira_server",
                    "tags": [
                        "ci",
                        "dev"
                    ]
                },
                {
                    "vm_id": "vm-c7bac01a07",
                    "name": "bastion",
                    "tags": [
                        "ssh",
                        "dev"
                    ]
                }
            ],
            "fw_rules": [
                {
                    "fw_id": "fw-82af742",
                    "source_tag": "ssh",
                    "dest_tag": "dev"
                }
            ]
        }
        vm_id = data['vms'][0]['vm_id']
        response = self.client.post(f'api/v1/attack?vm_id={vm_id}', data=data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_attacked_vm(self):
        data = {
            "vms": [
                {
                    "vm_id": "vm-a211de",
                    "name": "jira_server",
                    "tags": [
                        "ci",
                        "dev"
                    ]
                },
                {
                    "vm_id": "vm-c7bac01a07",
                    "name": "bastion",
                    "tags": [
                        "ssh",
                        "dev"
                    ]
                }
            ],
            "fw_rules": [
                {
                    "fw_id": "fw-82af742",
                    "source_tag": "ssh",
                    "dest_tag": "dev"
                }
            ]
        }
        vm_id = data['vms'][0]['vm_id']
        name = data['vms'][0]['name']
        vm = get_attacked_vm(data['vms'], vm_id)
        self.assertEqual(vm['name'], name)

    def test_machine_cannot_attack_itself(self):
        data = {
            "vms": [
                {
                    "vm_id": "vm-a211de",
                    "name": "jira_server",
                    "tags": [
                        "ssh",
                        "dev"
                    ]
                },
                {
                    "vm_id": "vm-c7bac01a07",
                    "name": "bastion",
                    "tags": [
                        "ssh",
                        "dev"
                    ]
                }
            ],
            "fw_rules": [
                {
                    "fw_id": "fw-82af742",
                    "source_tag": "ssh",
                    "dest_tag": "dev"
                }
            ]
        }
        vm_id = data['vms'][0]['vm_id']
        vms = get_machines_can_potentially_attack(data['fw_rules'], data['vms'], vm_id)
        self.assertTrue(len(vms) == 1)
        self.assertTrue(vms[0]['vm_id'] != vm_id)
