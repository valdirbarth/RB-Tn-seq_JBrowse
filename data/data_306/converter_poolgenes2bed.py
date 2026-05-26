import pandas as pd

# Carregar os dados (ajuste o nome do arquivo se necessário)
# Se o seu arquivo for separado por tabulação, use sep='\t'
df = pd.read_csv('pool_genes.tsv', sep='\t')

# 1. Criar o BED para BedTabix (mostra cada inserção individual)
# Formato: scaffold, start, end, name (barcode), score (nTot), strand
bed_data = pd.DataFrame({
    'chrom': df['scaffold'],
    'start': df['pos'] - 1,
    'end': df['pos'],
    'name': df['barcode'],
    'score': df['nTot'],
    'strand': df['strand']
})

# Remover linhas onde a posição é inválida (NA)
bed_data = bed_data.dropna(subset=['start'])
bed_data['start'] = bed_data['start'].astype(int)
bed_data['end'] = bed_data['end'].astype(int)

bed_data.to_csv('insercoes.bed', sep='\t', index=False, header=False)

# 2. Criar BedGraph para o BigWig (agrupando por posição para ver densidade)
bg_data = bed_data.groupby(['chrom', 'start', 'end'])['score'].sum().reset_index()
bg_data.to_csv('insercoes.bedgraph', sep='\t', index=False, header=False)

print("Arquivos .bed e .bedgraph gerados com sucesso!")