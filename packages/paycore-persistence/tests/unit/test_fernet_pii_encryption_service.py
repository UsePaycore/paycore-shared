import pytest

from paycore_persistence import FernetPiiEncryptionService


class TestFernetPiiEncryptionService:
    def test_encrypt_returns_different_string(self):
        service = FernetPiiEncryptionService(encryption_key="my-secret-key")
        plaintext = "john@example.com"
        encrypted = service.encrypt(plaintext)
        assert encrypted != plaintext

    def test_decrypt_returns_original_value(self):
        service = FernetPiiEncryptionService(encryption_key="my-secret-key")
        plaintext = "john@example.com"
        encrypted = service.encrypt(plaintext)
        decrypted = service.decrypt(encrypted)
        assert decrypted == plaintext

    def test_round_trip_with_phone_number(self):
        service = FernetPiiEncryptionService(encryption_key="my-secret-key")
        plaintext = "+1-555-123-4567"
        encrypted = service.encrypt(plaintext)
        decrypted = service.decrypt(encrypted)
        assert decrypted == plaintext

    def test_round_trip_with_long_text(self):
        service = FernetPiiEncryptionService(encryption_key="my-secret-key")
        plaintext = "John Doe, 123 Main St, Springfield, IL 62701, SSN: 123-45-6789"
        encrypted = service.encrypt(plaintext)
        decrypted = service.decrypt(encrypted)
        assert decrypted == plaintext

    def test_same_key_can_decrypt(self):
        service1 = FernetPiiEncryptionService(encryption_key="shared-key")
        service2 = FernetPiiEncryptionService(encryption_key="shared-key")
        plaintext = "sensitive-data"
        encrypted = service1.encrypt(plaintext)
        decrypted = service2.decrypt(encrypted)
        assert decrypted == plaintext

    def test_different_key_cannot_decrypt(self):
        service1 = FernetPiiEncryptionService(encryption_key="key-one")
        service2 = FernetPiiEncryptionService(encryption_key="key-two")
        plaintext = "sensitive-data"
        encrypted = service1.encrypt(plaintext)
        with pytest.raises(Exception):
            service2.decrypt(encrypted)

    def test_encrypt_produces_different_ciphertexts(self):
        service = FernetPiiEncryptionService(encryption_key="my-secret-key")
        plaintext = "john@example.com"
        encrypted1 = service.encrypt(plaintext)
        encrypted2 = service.encrypt(plaintext)
        assert encrypted1 != encrypted2
