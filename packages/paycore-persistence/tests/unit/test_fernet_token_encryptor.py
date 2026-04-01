import pytest
from cryptography.fernet import Fernet

from paycore_persistence import FernetTokenEncryptor


class TestFernetTokenEncryptor:
    def _generate_key(self) -> str:
        return Fernet.generate_key().decode()

    def test_encrypt_returns_different_string(self):
        key = self._generate_key()
        encryptor = FernetTokenEncryptor(encryption_key=key)
        plaintext = "my-secret-token"
        encrypted = encryptor.encrypt(plaintext)
        assert encrypted != plaintext

    def test_decrypt_returns_original_value(self):
        key = self._generate_key()
        encryptor = FernetTokenEncryptor(encryption_key=key)
        plaintext = "my-secret-token"
        encrypted = encryptor.encrypt(plaintext)
        decrypted = encryptor.decrypt(encrypted)
        assert decrypted == plaintext

    def test_round_trip_with_special_characters(self):
        key = self._generate_key()
        encryptor = FernetTokenEncryptor(encryption_key=key)
        plaintext = "token/with+special=chars&more!"
        encrypted = encryptor.encrypt(plaintext)
        decrypted = encryptor.decrypt(encrypted)
        assert decrypted == plaintext

    def test_round_trip_with_unicode(self):
        key = self._generate_key()
        encryptor = FernetTokenEncryptor(encryption_key=key)
        plaintext = "token-with-unicode-chars-cafe"
        encrypted = encryptor.encrypt(plaintext)
        decrypted = encryptor.decrypt(encrypted)
        assert decrypted == plaintext

    def test_encrypt_produces_different_ciphertexts(self):
        key = self._generate_key()
        encryptor = FernetTokenEncryptor(encryption_key=key)
        plaintext = "my-secret-token"
        encrypted1 = encryptor.encrypt(plaintext)
        encrypted2 = encryptor.encrypt(plaintext)
        assert encrypted1 != encrypted2

    def test_raises_without_key(self):
        with pytest.raises(ValueError, match="OAUTH_ENCRYPTION_KEY is required"):
            FernetTokenEncryptor(encryption_key=None)

    def test_different_keys_produce_different_ciphertexts(self):
        key1 = self._generate_key()
        key2 = self._generate_key()
        encryptor1 = FernetTokenEncryptor(encryption_key=key1)
        encryptor2 = FernetTokenEncryptor(encryption_key=key2)
        plaintext = "my-secret-token"
        encrypted1 = encryptor1.encrypt(plaintext)
        with pytest.raises(Exception):
            encryptor2.decrypt(encrypted1)
