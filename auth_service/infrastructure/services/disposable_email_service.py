import os


class DisposableEmailService:
    def __init__(self):
        self.disposable_domains = self._load_domains()

    def _load_domains(self):
        """Load disposable email domains from file"""
        domains = set()
        file_path = os.path.join(os.path.dirname(__file__), "../../application/data/disposable_email_domains.txt")

        try:
            with open(file_path, "r") as f:
                for line in f:
                    domain = line.strip().lower()
                    if domain:
                        domains.add(domain)
        except FileNotFoundError:
            pass

        return domains

    def is_disposable(self, email):
        """Check if email is from a disposable domain"""
        if not email or "@" not in email:
            return False

        domain = email.split("@")[-1].lower()
        return domain in self.disposable_domains
