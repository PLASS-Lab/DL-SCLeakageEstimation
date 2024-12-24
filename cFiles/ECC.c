#include <stdio.h>
#include <wolfssl/options.h>
#include <wolfssl/ssl.h>
#include <wolfssl/wolfcrypt/ecc.h>
#include <wolfssl/wolfcrypt/asn_public.h>
#include <wolfssl/wolfcrypt/error-crypt.h>

void check_wolfssl_result(int ret, const char* func) {
    if (ret != 0) {
        printf("%s failed: %s\n", func, wc_GetErrorString(ret));
    }
}

int main() {
    int ret;
    ecc_key eccKey;
    WC_RNG rng;
    byte hash[WC_SHA256_DIGEST_SIZE];
    byte sig[128]; // Ensure this is large enough for the ECC curve being used
    word32 sigLen = sizeof(sig);
    word32 idx = 0;

    // Initialize the ECC key and RNG
    wc_InitRng(&rng);
    wc_ecc_init(&eccKey);

    // Generate a key pair
    ret = wc_ecc_make_key(&rng, 32, &eccKey); // 256-bit key
    check_wolfssl_result(ret, "wc_ecc_make_key");

    // Create a fake "hash" to sign
    wc_Sha256Hash((byte*)"Hello, World!", 13, hash);

    // Sign the hash
    ret = wc_ecc_sign_hash(hash, sizeof(hash), sig, &sigLen, &rng, &eccKey);
    check_wolfssl_result(ret, "wc_ecc_sign_hash");

    // Verify the signature
    int stat = 0;
    ret = wc_ecc_verify_hash(sig, sigLen, hash, sizeof(hash), &stat, &eccKey);
    check_wolfssl_result(ret, "wc_ecc_verify_hash");

    // if (stat == 1) {
    //     printf("Signature verified!\n");
    // } else {
    //     printf("Signature verification failed!\n");
    // }

    // Free resources
    wc_ecc_free(&eccKey);
    wc_FreeRng(&rng);

    return 0;
}
