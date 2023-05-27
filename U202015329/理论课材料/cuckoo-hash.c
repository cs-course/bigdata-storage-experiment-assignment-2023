#include <stdlib.h>
#include <stdio.h>
#include <time.h>

// #define DEBUG
#define HASH_BITS 12
#define HASH_SIZE (1 << HASH_BITS)
#define HASH_CNT 2

#define BUCKET_SIZE 4
#define SPACE_OCCUPIED 0.95

#define MAX_LOOP_CNT 1000  

int bucket[HASH_CNT][HASH_SIZE][BUCKET_SIZE];

time_t insert_time, loop_time, get_time;

static inline int hash1(int key) { return key & (HASH_SIZE - 1); }
static inline int hash2(int key) { return (key >> HASH_BITS) & (HASH_SIZE - 1); }
int insert(int key);
int get(int key);
int delete(int key);
void cTest();
void pTest();

int main()
{
    srand(time(0));
    cTest();
}

int get(int key) {

#ifdef DEBUG
    printf("Get key: %d\n", key);
#endif

    int tag;
    clock_t start, end;
    start = clock();

    tag = hash1(key);
    for (int i = 0; i < BUCKET_SIZE; i++) 
        if (bucket[0][tag][i] == key) {
            end = clock();
            get_time += end - start;
            return 0;
        }
        
    tag = hash2(key);
    for (int i = 0; i < BUCKET_SIZE; i++) 
        if (bucket[1][tag][i] == key) {
            end = clock();
            get_time += end - start;
            return 0;
        }
        
    return 1;
}

int delete(int key) {
    int tag;
    
    tag = hash1(key);
    for (int i = 0; i < BUCKET_SIZE; i++) 
        if (bucket[0][tag][i] == key) {
            bucket[0][tag][i] = 0;
            return 0;
        }

    tag = hash2(key);
    for (int i = 0; i < BUCKET_SIZE; i++) 
        if (bucket[1][tag][i] == key) {
            bucket[1][tag][i] = 0;
            return 0;
        }

    return 1;
}

int insert(int key) {

#ifdef DEBUG
    printf("Insert key: %d\n", key);
#endif

    clock_t time_start, time_finish, time_loop_start;
    time_start = clock();
    int tag;
    tag = hash1(key);
    for (int i = 0; i < BUCKET_SIZE; i++)
        if (bucket[0][tag][i] == 0) {
            bucket[0][tag][i] = key;
            time_finish = clock();
            insert_time += time_finish - time_start;
            return 0;
        }

    tag = hash2(key);
    for (int i = 0; i < BUCKET_SIZE; i++)
        if (bucket[1][tag][i] == 0) {
            bucket[1][tag][i] = key;
            time_finish = clock();
            insert_time += time_finish - time_start;
            return 0;
        }
    
    // collide case
    // use cuckoo hash strategy
    int bucket_to_kick_out, pos_idx, loop_cnt;
    
    time_loop_start = clock();
    bucket_to_kick_out = rand() % HASH_CNT;
    loop_cnt = 0;
    while (loop_cnt < MAX_LOOP_CNT) {
        int tmp = key;
        if (bucket_to_kick_out == 0) 
            tag = hash1(key);
        else 
            tag = hash2(key);
        pos_idx = rand() % BUCKET_SIZE;
        key = bucket[bucket_to_kick_out][tag][pos_idx];
        bucket[bucket_to_kick_out][tag][pos_idx] = tmp;

        // update bucket_to_kick_out
        // find place to insert in new bucket
        bucket_to_kick_out = (bucket_to_kick_out + 1) % HASH_CNT;
        if (bucket_to_kick_out == 0) 
            tag = hash1(key);
        else 
            tag = hash2(key);
        for (int i = 0; i < BUCKET_SIZE; i++)
            if (bucket[bucket_to_kick_out][tag][i] == 0) {
                bucket[bucket_to_kick_out][tag][i] = key;
                time_finish = clock();
                insert_time += time_finish - time_start;
                loop_time += time_finish - time_loop_start;
                return 0;
            }
        
        loop_cnt++;
    }

    return 1;
}

// Correct Test
void cTest() {
    int cnt = 0;
    int test_size = SPACE_OCCUPIED * HASH_CNT * HASH_SIZE * BUCKET_SIZE;
    int arr[test_size];

    while (cnt < 10000) {
        printf("cTest %d: ", cnt);

        for (int i = 0; i < HASH_CNT; i++) 
            for (int j = 0; j < HASH_SIZE; j++)
                for (int k = 0; k < BUCKET_SIZE; k++)
                    bucket[i][j][k] = 0;

        for (int i = 0; i < test_size; i++) {
            arr[i] = rand();
            if (insert(arr[i]) != 0) {
                printf("ERROR: INSERT FAILED\n");
                return;
            }
        }

        for (int i = 0; i < test_size; i++) {
            if (get(arr[i]) != 0) {
                printf("ERROR: GET FAILED\n");
                break;
            }
        }

        printf("pass\n");
        cnt++;
    }

    printf("Correctness Test Successful.\n");
}

// Performance Test
void pTest() {
    int cnt = 0;
    int test_size = SPACE_OCCUPIED * HASH_CNT * HASH_SIZE * BUCKET_SIZE;
    int arr[test_size];

    for (int i = 0; i < test_size; i++) {
        arr[i] = rand();
        if (insert(arr[i]) != 0) {
            printf("ERROR: INSERT FAILED\n");
            return;
        }
    }

    for (int i = 0; i < test_size; i++) {
        if (get(arr[i]) != 0) {
            printf("ERROR: GET FAILED\n");
            break;
        }
    }
    

    printf("Performance\n");
    printf(" insert_time %ld, loop_time %ld\n", insert_time, loop_time);
    printf(" get_time %ld\n", get_time);

}