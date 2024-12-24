#include <stdio.h>
#include <wolfssl/options.h>
#include <wolfssl/ssl.h>
#include <wolfssl/wolfcrypt/rsa.h>
#include <wolfssl/wolfcrypt/error-crypt.h>

#define RSA_KEY_SIZE 2048
#define EXPONENT 65537

void check_wolfssl_result(int ret, char* func) {
    if (ret != 0) {
        printf("%s failed: %s\n", func, wc_GetErrorString(ret));
    }
}

int main() {
    int ret;
    byte plainText[] = "Hello, World!";
    byte cipher[256]; // Adjust the size according to the key size
    byte decrypted[256]; // Adjust the size according to the key size
    word32 idx = 0;
    RsaKey rsaKey;
    WC_RNG rng;

    wc_InitRsaKey(&rsaKey, NULL);
    wc_InitRng(&rng);

    // Generate a new RSA Key
    ret = wc_MakeRsaKey(&rsaKey, RSA_KEY_SIZE, EXPONENT, &rng);
    check_wolfssl_result(ret, "wc_MakeRsaKey");

    // Encrypt the plaintext
    ret = wc_RsaPublicEncrypt(plainText, sizeof(plainText), cipher, sizeof(cipher), &rsaKey, &rng);
    check_wolfssl_result(ret, "wc_RsaPublicEncrypt");

    // Decrypt the ciphertext
    ret = wc_RsaPrivateDecrypt(cipher, ret, decrypted, sizeof(decrypted), &rsaKey);
    check_wolfssl_result(ret, "wc_RsaPrivateDecrypt");

    printf("Decrypted Text: %s\n", decrypted);

    // Free resources
    wc_FreeRsaKey(&rsaKey);
    wc_FreeRng(&rng);

    return 0;
}
