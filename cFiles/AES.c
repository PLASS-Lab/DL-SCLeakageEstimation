#include <stdio.h>
#include <wolfssl/options.h>
#include <wolfssl/wolfcrypt/aes.h>
#include <wolfssl/wolfcrypt/types.h>
#include <wolfssl/wolfcrypt/error-crypt.h>


#define AES_BLOCK_SIZE 16
#define KEY_SIZE 32  // Using AES-256

void check_wolfssl_result(int ret, const char* func) {
    if (ret != 0) {
        printf("%s failed: %s\n", func, wc_GetErrorString(ret));
    }
}

int main() {
    Aes aes;
    byte key[KEY_SIZE] = {0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07,
                          0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f,
                          0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17,
                          0x18, 0x19, 0x1a, 0x1b, 0x1c, 0x1d, 0x1e, 0x1f};
    byte iv[AES_BLOCK_SIZE] = {0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07,
                               0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f};
    byte plaintext[AES_BLOCK_SIZE] = "a;sdlkjfei4344@#";
    byte ciphertext[AES_BLOCK_SIZE];
    byte decryptedtext[AES_BLOCK_SIZE];
    int ret;

    // Initialize and set up the AES context for encryption
    wc_AesInit(&aes, NULL, INVALID_DEVID);
    ret = wc_AesSetKey(&aes, key, sizeof(key), iv, AES_ENCRYPTION);
    check_wolfssl_result(ret, "wc_AesSetKey (encrypt)");

    // Perform AES CBC encryption
    ret = wc_AesCbcEncrypt(&aes, ciphertext, plaintext, sizeof(plaintext));
    check_wolfssl_result(ret, "wc_AesCbcEncrypt");

    // Initialize and set up the AES context for decryption
    wc_AesInit(&aes, NULL, INVALID_DEVID);
    ret = wc_AesSetKey(&aes, key, sizeof(key), iv, AES_DECRYPTION);
    check_wolfssl_result(ret, "wc_AesSetKey (decrypt)");

    // Perform AES CBC decryption
    ret = wc_AesCbcDecrypt(&aes, decryptedtext, ciphertext, sizeof(ciphertext));
    check_wolfssl_result(ret, "wc_AesCbcDecrypt");

    // Output results
    //printf("Plaintext: %s\n", plaintext);
    //printf("Ciphertext: ");
    for (int i = 0; i < sizeof(ciphertext); i++)
        printf("%02x ", ciphertext[i]);
    //printf("\nDecrypted text: %s\n", decryptedtext);

    return 0;
}
