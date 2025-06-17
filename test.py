def test_imports():
    packages = [
        "qiskit",
        "matplotlib",
        "PIL",  # Pillow
        "Cryptodome",  # Pycryptodomex
        "cryptography"
    ]

    for pkg in packages:
        try:
            __import__(pkg)
            print(f"✅ {pkg} - OK")
        except ImportError:
            print(f"❌ {pkg} - MISSING")
            exit(1)

if __name__ == "__main__":
    test_imports()
