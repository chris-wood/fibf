/* -*- Mode: C++; c-basic-offset: 4; indent-tabs-mode: nil -*- */
#include "cuckoofilter.h"

#include <cassert>
#include <cmath>
#include <iostream>
#include <vector>

using cuckoofilter::CuckooFilter;
using namespace std;

int main(int argc, char** argv) {
    size_t total_items  = 1000000;

    if (argc < 7) {
        cerr << "usage: test timeSteps filterSize filterHashes decayRate ..." << endl;
        return -1;
    }

    int timeSteps = atoi(argv[1]);  // * minimumTimeUnit # epochs (input is seconds and then multiplied by the MTU)
    int filterSize = atoi(argv[2]);
    int filterHashes = atoi(argv[2]);
    float decayRate = atof(argv[3]); // / minimumTimeUnit    # per second
    float arrivalRate = atof(argv[4]); // / minimumTimeUnit  # per second
    float deleteRate = atof(argv[5]); // / minimumTimeUnit # per second
    int randomSampleSize = atoi(argv[6]);

    // Create a cuckoo filter where each item is of type size_t and
    // use 12 bits for each item:
    //    CuckooFilter<size_t, 12> filter(total_items);
    // To enable semi-sorting, define the storage of cuckoo filter to be
    // PackedTable, accepting keys of size_t type and making 13 bits
    // for each key:
    //   CuckooFilter<size_t, 13, cuckoofilter::PackedTable> filter(total_items);

    // TODO: make 12 a parameter
    CuckooFilter<size_t, 12> filter(total_items);

    // // Insert items to this cuckoo filter
    // size_t num_inserted = 0;
    // for (size_t i = 0; i < total_items; i++, num_inserted++) {
    //     if (filter.Add(i) != cuckoofilter::Ok) {
    //         break;
    //     }
    // }

    // // Check if previously inserted items are in the filter, expected
    // // true for all items
    // for (size_t i = 0; i < num_inserted; i++) {
    //     assert(filter.Contain(i) == cuckoofilter::Ok);
    // }

    // // Check non-existing items, a few false positives expected
    // size_t total_queries = 0;
    // size_t false_queries = 0;
    // for (size_t i = total_items; i < 2 * total_items; i++) {
    //     if (filter.Contain(i) == cuckoofilter::Ok) {
    //         false_queries++;
    //     }
    //     total_queries++;
    // }

    // // Output the measured false positive rate
    // std::cout << "false positive rate is "
    //           << 100.0 * false_queries / total_queries
    //           << "%\n";

    return 0;
 }