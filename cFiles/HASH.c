#include <stdio.h>
#include <wolfssl/options.h>
#include <wolfssl/wolfcrypt/sha256.h>

void print_hex(byte* buf, int len) {
    for (int i = 0; i < len; i++) {
        printf("%02x", buf[i]);
    }
    printf("\n");
}

int main() {
    int ret;
    byte buffer[] = "Hello, World!";
    byte hash[WC_SHA256_DIGEST_SIZE]; // Changed SHA256_DIGEST_SIZE to WC_SHA256_DIGEST_SIZE
    wc_Sha256 sha256;

    // Initialize SHA256 context
    ret = wc_InitSha256(&sha256);
    if (ret != 0) {
        fprintf(stderr, "Failed to initialize SHA256: %d\n", ret);
        return -1;
    }

    // Hash the data
    ret = wc_Sha256Update(&sha256, buffer, sizeof(buffer)-1); // -1 to exclude null terminator
    if (ret != 0) {
        fprintf(stderr, "Failed to update SHA256: %d\n", ret);
        return -1;
    }

    // Finalize the hash
    ret = wc_Sha256Final(&sha256, hash);
    if (ret != 0) {
        fprintf(stderr, "Failed to finalize SHA256: %d\n", ret);
        return -1;
    }

    // Print the resulting hash in hexadecimal
    printf("SHA-256 Hash: ");
    print_hex(hash, WC_SHA256_DIGEST_SIZE);

    return 0;
}
