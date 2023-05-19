from re import search
from unittest import mock

from prowler.providers.gcp.lib.audit_info.models import GCP_Audit_Info

GCP_PROJECT_ID = "123456789012"


class Test_compute_shielded_vm_enabled:
    def set_mocked_audit_info(self):
        audit_info = GCP_Audit_Info(
            credentials=None,
            project_id=GCP_PROJECT_ID,
            audit_resources=None,
            audit_metadata=None,
        )

        return audit_info

    def test_compute_no_instances(self):
        from prowler.providers.gcp.services.compute.compute_service import Compute

        gcp_audit_info = self.set_mocked_audit_info()

        with mock.patch(
            "prowler.providers.gcp.lib.audit_info.audit_info.gcp_audit_info",
            new=gcp_audit_info,
        ), mock.patch(
            "prowler.providers.gcp.services.compute.compute_service.generate_client",
            new=lambda *args, **kwargs: None,
        ), mock.patch(
            "prowler.providers.gcp.services.compute.compute_service.Compute.__get_zones__",
            new=lambda *args, **kwargs: None,
        ), mock.patch(
            "prowler.providers.gcp.services.compute.compute_service.Compute.__get_instances__",
            new=lambda *args, **kwargs: None,
        ), mock.patch(
            "prowler.providers.gcp.services.compute.compute_service.Compute.__get_networks__",
            new=lambda *args, **kwargs: None,
        ), mock.patch(
            "prowler.providers.gcp.services.compute.compute_shielded_vm_enabled.compute_shielded_vm_enabled.compute_client",
            new=Compute(gcp_audit_info),
        ), mock.patch(
            "prowler.providers.gcp.services.compute.compute_shielded_vm_enabled.compute_shielded_vm_enabled.compute_client.instances",
            new=[],
        ):
            from prowler.providers.gcp.services.compute.compute_shielded_vm_enabled.compute_shielded_vm_enabled import (
                compute_shielded_vm_enabled,
            )

            check = compute_shielded_vm_enabled()
            result = check.execute()
            assert len(result) == 0

    def test_one_compliant_instance(self):
        from prowler.providers.gcp.services.compute.compute_service import (
            Compute,
            Instance,
        )

        gcp_audit_info = self.set_mocked_audit_info()

        instance = Instance(
            name="test",
            id="1234567890",
            zone="us-central1-a",
            public_ip=True,
            metadata={},
            shielded_enabled_vtpm=True,
            shielded_enabled_integrity_monitoring=True,
            service_accounts=[],
        )

        with mock.patch(
            "prowler.providers.gcp.lib.audit_info.audit_info.gcp_audit_info",
            new=gcp_audit_info,
        ), mock.patch(
            "prowler.providers.gcp.services.compute.compute_service.generate_client",
            new=lambda *args, **kwargs: None,
        ), mock.patch(
            "prowler.providers.gcp.services.compute.compute_service.Compute.__get_zones__",
            new=lambda *args, **kwargs: None,
        ), mock.patch(
            "prowler.providers.gcp.services.compute.compute_service.Compute.__get_instances__",
            new=lambda *args, **kwargs: None,
        ), mock.patch(
            "prowler.providers.gcp.services.compute.compute_service.Compute.__get_networks__",
            new=lambda *args, **kwargs: None,
        ), mock.patch(
            "prowler.providers.gcp.services.compute.compute_shielded_vm_enabled.compute_shielded_vm_enabled.compute_client",
            new=Compute(gcp_audit_info),
        ), mock.patch(
            "prowler.providers.gcp.services.compute.compute_shielded_vm_enabled.compute_shielded_vm_enabled.compute_client.instances",
            new=[instance],
        ):
            from prowler.providers.gcp.services.compute.compute_shielded_vm_enabled.compute_shielded_vm_enabled import (
                compute_shielded_vm_enabled,
            )

            check = compute_shielded_vm_enabled()
            result = check.execute()

            assert len(result) == 1
            assert result[0].status == "PASS"
            assert search(
                f"VM Instance {instance.name} have vTPM or Integrity Monitoring set to on",
                result[0].status_extended,
            )
            assert result[0].resource_id == instance.id

    def test_one_instance_with_shielded_vtpm_disabled(self):
        from prowler.providers.gcp.services.compute.compute_service import (
            Compute,
            Instance,
        )

        gcp_audit_info = self.set_mocked_audit_info()

        instance = Instance(
            name="test",
            id="1234567890",
            zone="us-central1-a",
            public_ip=True,
            metadata={},
            shielded_enabled_vtpm=False,
            shielded_enabled_integrity_monitoring=True,
            service_accounts=[],
        )

        with mock.patch(
            "prowler.providers.gcp.lib.audit_info.audit_info.gcp_audit_info",
            new=gcp_audit_info,
        ), mock.patch(
            "prowler.providers.gcp.services.compute.compute_service.generate_client",
            new=lambda *args, **kwargs: None,
        ), mock.patch(
            "prowler.providers.gcp.services.compute.compute_service.Compute.__get_zones__",
            new=lambda *args, **kwargs: None,
        ), mock.patch(
            "prowler.providers.gcp.services.compute.compute_service.Compute.__get_instances__",
            new=lambda *args, **kwargs: None,
        ), mock.patch(
            "prowler.providers.gcp.services.compute.compute_service.Compute.__get_networks__",
            new=lambda *args, **kwargs: None,
        ), mock.patch(
            "prowler.providers.gcp.services.compute.compute_shielded_vm_enabled.compute_shielded_vm_enabled.compute_client",
            new=Compute(gcp_audit_info),
        ), mock.patch(
            "prowler.providers.gcp.services.compute.compute_shielded_vm_enabled.compute_shielded_vm_enabled.compute_client.instances",
            new=[instance],
        ):
            from prowler.providers.gcp.services.compute.compute_shielded_vm_enabled.compute_shielded_vm_enabled import (
                compute_shielded_vm_enabled,
            )

            check = compute_shielded_vm_enabled()
            result = check.execute()

            assert len(result) == 1
            assert result[0].status == "FAIL"
            assert search(
                f"VM Instance {instance.name} don't have vTPM and Integrity Monitoring set to on",
                result[0].status_extended,
            )
            assert result[0].resource_id == instance.id

    def test_one_instance_with_shielded_integrity_monitoring_disabled(self):
        from prowler.providers.gcp.services.compute.compute_service import (
            Compute,
            Instance,
        )

        gcp_audit_info = self.set_mocked_audit_info()

        instance = Instance(
            name="test",
            id="1234567890",
            zone="us-central1-a",
            public_ip=True,
            metadata={},
            shielded_enabled_vtpm=True,
            shielded_enabled_integrity_monitoring=False,
            service_accounts=[],
        )

        with mock.patch(
            "prowler.providers.gcp.lib.audit_info.audit_info.gcp_audit_info",
            new=gcp_audit_info,
        ), mock.patch(
            "prowler.providers.gcp.services.compute.compute_service.generate_client",
            new=lambda *args, **kwargs: None,
        ), mock.patch(
            "prowler.providers.gcp.services.compute.compute_service.Compute.__get_zones__",
            new=lambda *args, **kwargs: None,
        ), mock.patch(
            "prowler.providers.gcp.services.compute.compute_service.Compute.__get_instances__",
            new=lambda *args, **kwargs: None,
        ), mock.patch(
            "prowler.providers.gcp.services.compute.compute_service.Compute.__get_networks__",
            new=lambda *args, **kwargs: None,
        ), mock.patch(
            "prowler.providers.gcp.services.compute.compute_shielded_vm_enabled.compute_shielded_vm_enabled.compute_client",
            new=Compute(gcp_audit_info),
        ), mock.patch(
            "prowler.providers.gcp.services.compute.compute_shielded_vm_enabled.compute_shielded_vm_enabled.compute_client.instances",
            new=[instance],
        ):
            from prowler.providers.gcp.services.compute.compute_shielded_vm_enabled.compute_shielded_vm_enabled import (
                compute_shielded_vm_enabled,
            )

            check = compute_shielded_vm_enabled()
            result = check.execute()

            assert len(result) == 1
            assert result[0].status == "FAIL"
            assert search(
                f"VM Instance {instance.name} don't have vTPM and Integrity Monitoring set to on",
                result[0].status_extended,
            )
            assert result[0].resource_id == instance.id
