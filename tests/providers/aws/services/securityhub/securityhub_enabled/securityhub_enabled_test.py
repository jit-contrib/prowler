from unittest import mock

from prowler.providers.aws.services.securityhub.securityhub_service import (
    SecurityHubHub,
)

AWS_REGION = "eu-west-1"
AWS_ACCOUNT_ID = "123456789012"
AWS_ACCOUNT_ARN = f"arn:aws:iam::{AWS_ACCOUNT_ID}:root"


class Test_securityhub_enabled:
    def test_securityhub_hub_inactive(self):
        securityhub_client = mock.MagicMock
        securityhub_client.securityhubs = [
            SecurityHubHub(
                arn=AWS_ACCOUNT_ARN,
                id="Security Hub",
                status="NOT_AVAILABLE",
                standards="",
                integrations="",
                region=AWS_REGION,
            )
        ]
        with mock.patch(
            "prowler.providers.aws.services.securityhub.securityhub_service.SecurityHub",
            new=securityhub_client,
        ):
            # Test Check
            from prowler.providers.aws.services.securityhub.securityhub_enabled.securityhub_enabled import (
                securityhub_enabled,
            )

            check = securityhub_enabled()
            result = check.execute()

            assert result[0].status == "FAIL"
            assert result[0].status_extended == "Security Hub is not enabled."
            assert result[0].resource_id == "Security Hub"
            assert result[0].resource_arn == AWS_ACCOUNT_ARN
            assert result[0].region == AWS_REGION

    def test_securityhub_hub_active_with_standards(self):
        securityhub_client = mock.MagicMock
        securityhub_client.securityhubs = [
            SecurityHubHub(
                arn="arn:aws:securityhub:us-east-1:0123456789012:hub/default",
                id="default",
                status="ACTIVE",
                standards="cis-aws-foundations-benchmark/v/1.2.0",
                integrations="",
                region="eu-west-1",
            )
        ]
        with mock.patch(
            "prowler.providers.aws.services.securityhub.securityhub_service.SecurityHub",
            new=securityhub_client,
        ):
            # Test Check
            from prowler.providers.aws.services.securityhub.securityhub_enabled.securityhub_enabled import (
                securityhub_enabled,
            )

            check = securityhub_enabled()
            result = check.execute()

            assert result[0].status == "PASS"
            assert (
                result[0].status_extended
                == "Security Hub is enabled with standards: cis-aws-foundations-benchmark/v/1.2.0."
            )
            assert result[0].resource_id == "default"
            assert (
                result[0].resource_arn
                == "arn:aws:securityhub:us-east-1:0123456789012:hub/default"
            )
            assert result[0].region == AWS_REGION

    def test_securityhub_hub_active_with_integrations(self):
        securityhub_client = mock.MagicMock
        securityhub_client.securityhubs = [
            SecurityHubHub(
                arn="arn:aws:securityhub:us-east-1:0123456789012:hub/default",
                id="default",
                status="ACTIVE",
                standards="",
                integrations="prowler",
                region="eu-west-1",
            )
        ]
        with mock.patch(
            "prowler.providers.aws.services.securityhub.securityhub_service.SecurityHub",
            new=securityhub_client,
        ):
            # Test Check
            from prowler.providers.aws.services.securityhub.securityhub_enabled.securityhub_enabled import (
                securityhub_enabled,
            )

            check = securityhub_enabled()
            result = check.execute()

            assert result[0].status == "PASS"
            assert (
                result[0].status_extended
                == "Security Hub is enabled without standards but with integrations: prowler."
            )
            assert result[0].resource_id == "default"
            assert (
                result[0].resource_arn
                == "arn:aws:securityhub:us-east-1:0123456789012:hub/default"
            )
            assert result[0].region == AWS_REGION

    def test_securityhub_hub_active_without_integrations_or_standards(self):
        securityhub_client = mock.MagicMock
        securityhub_client.securityhubs = [
            SecurityHubHub(
                arn="arn:aws:securityhub:us-east-1:0123456789012:hub/default",
                id="default",
                status="ACTIVE",
                standards="",
                integrations="",
                region="eu-west-1",
            )
        ]
        with mock.patch(
            "prowler.providers.aws.services.securityhub.securityhub_service.SecurityHub",
            new=securityhub_client,
        ):
            # Test Check
            from prowler.providers.aws.services.securityhub.securityhub_enabled.securityhub_enabled import (
                securityhub_enabled,
            )

            check = securityhub_enabled()
            result = check.execute()

            assert result[0].status == "FAIL"
            assert (
                result[0].status_extended
                == "Security Hub is enabled but without any standard or integration."
            )
            assert result[0].resource_id == "default"
            assert (
                result[0].resource_arn
                == "arn:aws:securityhub:us-east-1:0123456789012:hub/default"
            )
            assert result[0].region == AWS_REGION
