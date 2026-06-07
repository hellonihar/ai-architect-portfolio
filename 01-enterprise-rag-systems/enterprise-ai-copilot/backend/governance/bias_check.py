class BiasChecker:
    def check(self, text: str) -> list[str]:
        flags = []
        sensitive_terms = ["always", "never", "all", "none"]
        for term in sensitive_terms:
            if term in text.lower():
                flags.append(f"Contains absolute language: '{term}'")
        return flags
