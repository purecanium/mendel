from itertools import product

def generate_gametes(s):
    if len(s) % 2 != 0:
        raise ValueError("Input must have an even number of characters.")

    for i in range(0, len(s), 2):
        if s[i].lower() != s[i + 1].lower():
            raise ValueError(f"Characters at positions {i} and {i+1} must be the same letter.")

    groups = {}
    for char in s:
        groups.setdefault(char.lower(), set()).add(char)
    choices = list(groups.values())
    combos = set(''.join(p) for p in product(*choices))
    return sorted(combos)

def generate_filial(parent1, parent2):
    def merge(h1, h2):
        return ''.join(
            ''.join(sorted([a, b], key=lambda c: (c.islower(), c)))
            for a, b in zip(h1, h2)
        )

    def simplify_ratios(counts):
        def gcd(a, b):
            while b:
                a, b = b, a % b
            return a
        d = counts[0]
        for c in counts[1:]:
            d = gcd(d, c)
        return [c // d for c in counts]

    def get_phenotype(geno):
        loci = [geno[i:i+2] for i in range(0, len(geno), 2)]
        phenotype = []
        for pair in loci:
            upper = any(c.isupper() for c in pair)
            if upper:
                phenotype.append(pair[0].upper() + '-')
            else:
                phenotype.append(pair[0].lower() * 2)
        return ''.join(phenotype)

    matrix = [[merge(h1, h2) for h1 in parent1] for h2 in parent2]
    flat = [geno for row in matrix for geno in row]

    seen = []
    for g in flat:
        if g not in seen:
            seen.append(g)
    unique = seen
    counts = [flat.count(u) for u in unique]
    ratios = simplify_ratios(counts)

    pheno_map = {}
    for g, r in zip(unique, ratios):
        pheno = get_phenotype(g)
        if pheno in pheno_map:
            pheno_map[pheno] += r
        else:
            pheno_map[pheno] = r

    filial_genotype = [unique, ratios]
    implicit_phenotypes_ratio = [list(pheno_map.keys()), list(pheno_map.values())]

    headered_matrix = [["♂/♀"] + parent1]
    for i, row in enumerate(matrix):
        headered_matrix.append([parent2[i]] + row)

    return headered_matrix, filial_genotype, implicit_phenotypes_ratio