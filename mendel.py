from itertools import product

def generate_gametes(genotype):
    if len(genotype) % 2 != 0:
        raise ValueError("Input must have an even number of characters.")

    for i in range(0, len(genotype), 2):
        if genotype[i].lower() != genotype[i + 1].lower():
            raise ValueError(f"Characters at positions {i} and {i+1} must be the same letter.")

    groups = {}
    for char in genotype:
        groups.setdefault(char.lower(), set()).add(char)
    choices = list(groups.values())
    combos = set(''.join(p) for p in product(*choices))
    return sorted(combos)

def generate_filial(gametes1, gametes2):
    all_gametes = gametes1 + gametes2
    max_len = max(map(len, all_gametes), default=0)
    dominant, recessive = [], []
    for i in range(max_len):
        chars = [g[i] for g in all_gametes if len(g) > i]
        d = next((c for c in chars if c.isupper()), "")
        r = next((c for c in chars if c.islower()), "")
        dominant.append(d.upper() if d else "")
        recessive.append(r.lower() if r else "")
    loci = [ (d if d else r.upper()) for d, r in zip(dominant, recessive) ]

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

    def get_impl_phenotype(geno):
        loci = [geno[i:i+2] for i in range(0, len(geno), 2)]
        impl_phenotype = []
        for pair in loci:
            upper = any(c.isupper() for c in pair)
            if upper:
                impl_phenotype.append(pair[0].upper() + '-')
            else:
                impl_phenotype.append(pair[0].lower() * 2)
        return ''.join(impl_phenotype)

    punnet_matrix = [[merge(h1, h2) for h1 in gametes1] for h2 in gametes2]
    flat = [geno for row in punnet_matrix for geno in row]

    seen = []
    for g in flat:
        if g not in seen:
            seen.append(g)
    unique = seen
    counts = [flat.count(u) for u in unique]
    ratios = simplify_ratios(counts)

    pheno_map = {}
    for g, r in zip(unique, ratios):
        pheno = get_impl_phenotype(g)
        if pheno in pheno_map:
            pheno_map[pheno] += r
        else:
            pheno_map[pheno] = r

    genotypes = [unique, ratios]
    implicit_phenotypes = [list(pheno_map.keys()), list(pheno_map.values())]

    headered_punnet_square = [["♂/♀"] + gametes1]
    for i, row in enumerate(punnet_matrix):
        headered_punnet_square.append([gametes2[i]] + row)

    return headered_punnet_square, genotypes, implicit_phenotypes, loci

def generate_expl_phenotypes(loci, implicit_phenotypes, explicit_labels):
    implicit_patterns = implicit_phenotypes[0]
    phenotypes_ratio = implicit_phenotypes[1]
    phenotypes = []
    for pat in implicit_patterns:
        segs = [pat[i:i+2] for i in range(0, len(pat), 2)]
        names = []
        for seg, locus in zip(segs, loci):
            idx = loci.index(locus)
            dom_label = explicit_labels[idx*2]
            rec_label = explicit_labels[idx*2 + 1]
            names.append(dom_label if seg[0].isupper() else rec_label)
        phenotypes.append(" ".join(names))

    explicit_phenotypes = [phenotypes, phenotypes_ratio]
    return explicit_phenotypes