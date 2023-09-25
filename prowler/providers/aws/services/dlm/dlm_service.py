import threading

from prowler.lib.logger import logger
from prowler.providers.aws.aws_provider import generate_regional_clients


################## Data Lifecycle Manager
class Dlm:
    def __init__(self, audit_info):
        self.service = "dlm"
        self.session = audit_info.audit_session
        self.audited_account = audit_info.audited_account
        self.audited_partition = audit_info.audited_partition
        self.audited_account_arn = audit_info.audited_account_arn
        self.audit_resources = audit_info.audit_resources
        self.regional_clients = generate_regional_clients(self.service, audit_info)
        self.lifecycle_policies = []
        self.__threading_call__(self.__get_lifecycle_policies__)

    def __get_session__(self):
        return self.session

    def __threading_call__(self, call):
        threads = []
        for regional_client in self.regional_clients.values():
            threads.append(threading.Thread(target=call, args=(regional_client,)))
        for t in threads:
            t.start()
        for t in threads:
            t.join()

    def __get_lifecycle_policies__(self, regional_client):
        logger.info("DLM - Getting EBS Snapshots Lifecycle Policies...")
        try:
            lifecycle_policies = regional_client.get_lifecycle_policies()
            self.lifecycle_policies += lifecycle_policies["Policies"]
        except Exception as error:
            logger.error(
                f"{regional_client.region} -- {error.__class__.__name__}[{error.__traceback__.tb_lineno}]: {error}"
            )
