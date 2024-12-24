#include <stdio.h>
#include <wolfssl/options.h>
#include <wolfssl/wolfcrypt/des3.h>

#define DES_BLOCK_SIZE 9

void check_wolfssl_result(int ret, const char* func) {
    if (ret != 0) {
        fprintf(stderr, "%s failed: error code %d\n", func, ret);
    }
}


int main() {
    Des3 des3;
    byte key[24];  // DES key (triple DES used here)
    byte iv[DES_BLOCK_SIZE] = {0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08};
    byte plaintext[DES_BLOCK_SIZE] = {'H', 'e', 'l', 'l', 'o', 'D', 'E', 'S', 'r'}; 
    byte ciphertext[DES_BLOCK_SIZE];
    byte decryptedtext[DES_BLOCK_SIZE] = {0};  // Initialize to zero
    int ret;

    // Example key
    for (int i = 0; i < sizeof(key); ++i) {
        key[i] = (byte)(i + 1);
    }

    // Initialize and set up the DES3 context for encryption
    ret = wc_Des3_SetKey(&des3, key, iv, DES_ENCRYPTION);
    check_wolfssl_result(ret, "wc_Des3_SetKey (encryption)");
    if (ret != 0) return ret;

    // Perform DES3 CBC encryption
    ret = wc_Des3_CbcEncrypt(&des3, ciphertext, plaintext, sizeof(plaintext));
    check_wolfssl_result(ret, "wc_Des3_CbcEncrypt");
    if (ret != 0) return ret;

    // Initialize and set up the DES3 context for decryption
    ret = wc_Des3_SetKey(&des3, key, iv, DES_DECRYPTION);
    check_wolfssl_result(ret, "wc_Des3_SetKey (decryption)");
    if (ret != 0) return ret;

    // Perform DES3 CBC decryption
    ret = wc_Des3_CbcDecrypt(&des3, decryptedtext, ciphertext, sizeof(ciphertext));
    check_wolfssl_result(ret, "wc_Des3_CbcDecrypt");
    if (ret != 0) return ret;

    // Output results
    printf("Ciphertext: ");
    for (int i = 0; i < sizeof(ciphertext); i++)
        printf("%02x ", ciphertext[i]);
    printf("\n");

    printf("Decrypted text: ");
    for (int i = 0; i < sizeof(decryptedtext); i++)
        printf("%c", decryptedtext[i]);
    printf("\n");

    return 0;
}

