from mendel import generate_gametes, generate_filial

Genotype1 = input("Input 1st Parental's Genotype: ")
Genotype2 = input("Input 2nd Parental's Genotype: ")

Gametes1 = generate_gametes(Genotype1)
Gametes2 = generate_gametes(Genotype2)

print(generate_filial(Gametes1, Gametes2))