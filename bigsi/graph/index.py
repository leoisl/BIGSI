import logging

from bigsi.bloom import generate_hashes
from bigsi.bloom import BloomFilter
from bigsi.matrix import transpose
from bigsi.matrix import BitMatrix
from bigsi.utils import convert_query_kmer
from bigsi.utils import bitwise_and

BLOOMFILTER_SIZE_KEY = "ksi:bloomfilter_size"
NUM_HASH_FUNCTS_KEY = "ksi:num_hashes"
logger = logging.getLogger(__name__)


class KmerSignatureIndex:

    """
    Methods for managing kmer signature indexes
    """

    def __init__(self, storage):
        self.storage = storage
        self.bitmatrix = BitMatrix(storage)
        self.bloomfilter_size = storage.get_integer(BLOOMFILTER_SIZE_KEY)
        self.num_hashes = storage.get_integer(NUM_HASH_FUNCTS_KEY)

    @classmethod
    def create(cls, storage, bloomfilters, bloomfilter_size, num_hashes, lowmem=False):
        bloomfilters = [
            bf.bitarray if isinstance(bf, BloomFilter) else bf for bf in bloomfilters
        ]
        storage.set_integer(BLOOMFILTER_SIZE_KEY, bloomfilter_size)
        storage.set_integer(NUM_HASH_FUNCTS_KEY, num_hashes)
        logger.debug("Transpose bitarrays")
        rows = transpose(bloomfilters, lowmem=lowmem)
        logger.debug("Insert rows")
        bitmatrix = BitMatrix.create(
            storage, rows, num_rows=bloomfilter_size, num_cols=len(bloomfilters)
        )
        return cls(storage)

    def lookup(self, kmers, remove_trailing_zeros=True):
        if isinstance(kmers, str):
            kmers = [kmers]
        kmers=set(kmers)
        kmer_to_hashes = self.__kmers_to_hashes(kmers)
        hashes = {h for sublist in kmer_to_hashes.values() for h in sublist}
        rows = self.__batch_get_rows(hashes, remove_trailing_zeros)
        return self.__bitwise_and_kmers(kmer_to_hashes, rows)

    def insert_bloom(self, bloomfilter, column_index):
        self.bitmatrix.insert_column(bloomfilter, column_index)

    def merge_indexes(self, ksi, batch_size=10000):
        for i in range(0, self.bloomfilter_size, batch_size):
            lower_bound = i
            upper_bound = min(lower_bound+batch_size, self.bloomfilter_size)
            indexes = range(lower_bound, upper_bound)
            rows_from_first_index = list(self.bitmatrix.get_rows(indexes)) # here we need to explicitly convert the generator to list as it is used later
            rows_from_second_index = ksi.bitmatrix.get_rows(indexes)
            for r1, r2 in zip(rows_from_first_index, rows_from_second_index):
                r1.extend(r2)
            self.bitmatrix.set_rows(indexes, rows_from_first_index)
        self.bitmatrix.set_num_cols(self.bitmatrix.num_cols + ksi.bitmatrix.num_cols)

    def __kmers_to_hashes(self, kmers):
        d = {}
        for k in set(kmers):
            d[k] = set(
                generate_hashes(
                    convert_query_kmer(k), self.num_hashes, self.bloomfilter_size
                )
            )  ## use canonical kmer to generate lookup, but report query kmer
        return d

    def __batch_get_rows(self, row_indexes, remove_trailing_zeros=False):
        return dict(zip(row_indexes, self.bitmatrix.get_rows(row_indexes, remove_trailing_zeros=remove_trailing_zeros)))

    def __bitwise_and_kmers(self, kmer_to_hashes, rows):
        d = {}
        for k, hashes in kmer_to_hashes.items():
            subset_rows = [rows[h] for h in hashes]
            d[k] = bitwise_and(subset_rows)
        return d
