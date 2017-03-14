import hashlib
import struct 
import sys
COMPLEMENT = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A'}
BITS={'A':'00','G':'01','C':'10','T':'11'}
BASES={'00':'A','01':'G','10':'C','11':'T'}

def chunks(l, int n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

def decode_kmer(bytes binary_kmer, int kmer_size):
    """
    Returns a string representation of the specified kmer.
    """
    # G and C are the wrong way around because we reverse the sequence.
    # This really is a nasty way to do this!
    assert kmer_size <= 31
    binary_kmer_int = struct.unpack('Q', binary_kmer)[0]

    b = "{0:064b}".format(binary_kmer_int)[::-1]
    ret = []
    for j in range(kmer_size):
        nuc = BASES[b[j * 2: (j + 1) * 2]]
        ret.append(nuc)
    ret = "".join(ret)

    return ret[::-1]

cdef long encode_kmer(str kmer):
    """
    Returns the encoded integer representation of the specified string kmer.
    """
    ret = 0
    codes = {"A": 0, "C": 1, "G": 2, "T": 3}
    for j, nuc in enumerate(reversed(kmer)):
        v = codes[nuc]
        ret |= v << (2 * j)
    return ret#struct.pack('Q', ret)

def make_hash(str s):
    return hashlib.sha256(s.encode("ascii", errors="ignore")).hexdigest()

def hash_key(bytes k, int i=4):
    return hashlib.sha256(k).hexdigest()[:i]


def reverse_comp(str s):
    return "".join([COMPLEMENT.get(base, base) for base in reversed(s)])

def convert_query_kmers(kmers):
    for k in kmers:
        yield convert_query_kmer(k)

def convert_query_kmer(str kmer):
    return canonical(kmer)

cdef str canonical(str k):
    l = [k,reverse_comp(k)]
    l.sort()
    return l[0]

def min_lexo(str k):
    l = [k,reverse_comp(k)]
    l.sort()
    return l[0]
    
def seq_to_kmers(str seq, int kmer_size = 31):
    for i in range(len(seq)-kmer_size+1):
        yield seq[i:i+kmer_size]

cdef set seq_to_kmer_set(str seq, int kmer_size = 31):
    return {seq[i:i+kmer_size] for i in range(len(seq)-kmer_size+1)}



        

def bits(f):
    return [(s >> i) & 1 for s in f for i in xrange(7, -1, -1)]


def kmer_to_bits(str kmer):
    return "".join([BITS[k] for k in kmer])

def bits_to_kmer(str bitstring, int l):
    bases=[]
    for i in range(0,l*2,2):
         bases.append( BASES[bitstring[i:i+2]])
    return "".join(bases)


def kmer_to_bytes(str kmer,int bitpadding=0):
    bitstring = kmer_to_bits(kmer)
    if not bitpadding == 0:
        bitstring = "".join([bitstring, '0'*bitpadding])[::-1]
    list_of_bytes = [bitstring[i:i+8] for i in range(0, len(bitstring), 8)]
    _bytes = [int(byte, 2) for byte in list_of_bytes]
    return bytes(_bytes)